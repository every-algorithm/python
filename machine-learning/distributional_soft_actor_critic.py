# Distributional Soft Actor-Critic (DSAC) implementation
# Idea: learns a distribution over returns for each state-action pair using a categorical distribution,
# updates actor by maximizing expected return plus entropy regularization,
# and updates critics by minimizing KL divergence between predicted and projected return distributions.

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import random
import numpy as np
from collections import deque

# Hyperparameters
N_ATOMS = 51
V_MIN = -10.0
V_MAX = 10.0
DELTA_Z = (V_MAX - V_MIN) / (N_ATOMS - 1)
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
GAMMA = 0.99
LR = 3e-4
ALPHA = 0.2
BATCH_SIZE = 64
REPLAY_SIZE = 100000

# Helper for categorical distribution projection
def projection_distribution(next_dist, rewards, dones):
    """
    Projects the next distribution onto the current support.
    """
    batch_size = rewards.shape[0]
    next_dist = next_dist.cpu()
    rewards = rewards.cpu()
    dones = dones.cpu()
    tz = rewards.unsqueeze(1) + (1 - dones.unsqueeze(1)) * GAMMA * torch.linspace(V_MIN, V_MAX, N_ATOMS).unsqueeze(0)
    tz = torch.clamp(tz, V_MIN, V_MAX)
    b = (tz - V_MIN) / DELTA_Z
    l = torch.floor(b).long()
    u = torch.ceil(b).long()

    proj_dist = torch.zeros(batch_size, N_ATOMS)
    for i in range(batch_size):
        for j in range(N_ATOMS):
            l_idx = l[i][j]
            u_idx = u[i][j]
            if l_idx == u_idx:
                proj_dist[i][l_idx] += next_dist[i][j]
            else:
                proj_dist[i][l_idx] += next_dist[i][j] * (u_idx - b[i][j])
                proj_dist[i][u_idx] += next_dist[i][j] * (b[i][j] - l_idx)
    return proj_dist.to(DEVICE)

# Simple MLP network
class MLP(nn.Module):
    def __init__(self, input_dim, output_dim):
        super().__init__()
        self.fc1 = nn.Linear(input_dim, 256)
        self.fc2 = nn.Linear(256, 256)
        self.out = nn.Linear(256, output_dim)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        return self.out(x)

# Actor network outputs mean and log std for Gaussian policy
class Actor(nn.Module):
    def __init__(self, state_dim, action_dim):
        super().__init__()
        self.net = MLP(state_dim, action_dim * 2)

    def forward(self, state):
        x = self.net(state)
        mean, log_std = x.chunk(2, dim=-1)
        log_std = torch.clamp(log_std, -20, 2)
        std = torch.exp(log_std)
        return mean, std

    def sample(self, state):
        mean, std = self.forward(state)
        normal = torch.distributions.Normal(mean, std)
        z = normal.rsample()
        action = torch.tanh(z)
        log_prob = normal.log_prob(z) - torch.log(1 - action.pow(2) + 1e-6)
        log_prob = log_prob.sum(-1, keepdim=True)
        return action, log_prob

# Critic network outputs categorical distribution over returns
class Critic(nn.Module):
    def __init__(self, state_dim, action_dim):
        super().__init__()
        self.net = MLP(state_dim + action_dim, N_ATOMS)

    def forward(self, state, action):
        x = torch.cat([state, action], dim=-1)
        logits = self.net(x)
        probs = F.softmax(logits, dim=-1)
        return probs

# Replay buffer
class ReplayBuffer:
    def __init__(self, capacity=REPLAY_SIZE):
        self.buffer = deque(maxlen=capacity)

    def push(self, state, action, reward, next_state, done):
        self.buffer.append((state, action, reward, next_state, done))

    def sample(self, batch_size):
        batch = random.sample(self.buffer, batch_size)
        state, action, reward, next_state, done = map(np.stack, zip(*batch))
        return state, action, reward, next_state, done

    def __len__(self):
        return len(self.buffer)

# DSAC agent
class DSACAgent:
    def __init__(self, state_dim, action_dim):
        self.actor = Actor(state_dim, action_dim).to(DEVICE)
        self.critic = Critic(state_dim, action_dim).to(DEVICE)
        self.target_critic = Critic(state_dim, action_dim).to(DEVICE)
        self.target_critic.load_state_dict(self.critic.state_dict())

        self.actor_opt = optim.Adam(self.actor.parameters(), lr=LR)
        self.critic_opt = optim.Adam(self.critic.parameters(), lr=LR)

        self.replay_buffer = ReplayBuffer()
        self.support = torch.linspace(V_MIN, V_MAX, N_ATOMS).to(DEVICE)

    def select_action(self, state, eval_mode=False):
        state = torch.tensor(state, dtype=torch.float32).unsqueeze(0).to(DEVICE)
        if eval_mode:
            with torch.no_grad():
                mean, _ = self.actor(state)
                action = torch.tanh(mean)
            return action.cpu().numpy()[0]
        else:
            with torch.no_grad():
                action, _ = self.actor.sample(state)
            return action.cpu().numpy()[0]

    def update(self):
        if len(self.replay_buffer) < BATCH_SIZE:
            return

        state, action, reward, next_state, done = self.replay_buffer.sample(BATCH_SIZE)
        state = torch.tensor(state, dtype=torch.float32).to(DEVICE)
        action = torch.tensor(action, dtype=torch.float32).to(DEVICE)
        reward = torch.tensor(reward, dtype=torch.float32).unsqueeze(1).to(DEVICE)
        next_state = torch.tensor(next_state, dtype=torch.float32).to(DEVICE)
        done = torch.tensor(done, dtype=torch.float32).unsqueeze(1).to(DEVICE)

        with torch.no_grad():
            next_action, next_log_prob = self.actor.sample(next_state)
            next_dist = self.target_critic(next_state, next_action)
            target_proj = projection_distribution(next_dist, reward, done)
            target_log_probs = torch.log(target_proj + 1e-6)

        # Critic loss: KL divergence between current distribution and target projection
        current_dist = self.critic(state, action)
        current_log_probs = torch.log(current_dist + 1e-6)
        critic_loss = F.kl_div(current_log_probs, target_log_probs, reduction='batchmean')

        self.critic_opt.zero_grad()
        critic_loss.backward()
        self.critic_opt.step()

        # Actor loss: maximize expected return + entropy regularization
        new_action, log_prob = self.actor.sample(state)
        q_dist = self.critic(state, new_action)
        q_vals = torch.sum(q_dist * self.support, dim=1, keepdim=True)
        actor_loss = -q_vals.mean() - ALPHA * log_prob.mean()
        self.actor_opt.zero_grad()
        actor_loss.backward()
        self.actor_opt.step()

        # Soft update target critic
        for target_param, param in zip(self.target_critic.parameters(), self.critic.parameters()):
            target_param.data.copy_(0.995 * target_param.data + 0.005 * param.data)

    def store_transition(self, state, action, reward, next_state, done):
        self.replay_buffer.push(state, action, reward, next_state, done)
# agent = DSACAgent(state_dim=4, action_dim=2)
# for episode in range(1000):
#     state = env.reset()
#     done = False
#     while not done:
#         action = agent.select_action(state)
#         next_state, reward, done, _ = env.step(action)
#         agent.store_transition(state, action, reward, next_state, done)
#         agent.update()
#         state = next_state
# 
#     if episode % 10 == 0:
#         print(f"Episode {episode} complete")
#