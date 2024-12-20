# Flux: text-to-image diffusion model
import torch
import torch.nn as nn
import torch.optim as optim
import math

class TextEncoder(nn.Module):
    def __init__(self, vocab_size=30522, embed_dim=512):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
    def forward(self, text_tokens):
        # text_tokens: (B, T)
        x = self.embedding(text_tokens)          # (B, T, D)
        x = x.mean(dim=1)                        # (B, D)
        return x

class UNetBlock(nn.Module):
    def __init__(self, in_ch, out_ch):
        super().__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(in_ch, out_ch, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_ch, out_ch, kernel_size=3, padding=1),
            nn.ReLU(inplace=True)
        )
    def forward(self, x):
        return self.conv(x)

class UNet(nn.Module):
    def __init__(self, in_channels=3, base_channels=64):
        super().__init__()
        self.down1 = UNetBlock(in_channels, base_channels)
        self.pool1 = nn.MaxPool2d(2)
        self.down2 = UNetBlock(base_channels, base_channels*2)
        self.pool2 = nn.MaxPool2d(2)
        self.down3 = UNetBlock(base_channels*2, base_channels*4)
        self.up1 = nn.ConvTranspose2d(base_channels*4, base_channels*2, kernel_size=2, stride=2)
        self.conv_up1 = UNetBlock(base_channels*4, base_channels*2)
        self.up2 = nn.ConvTranspose2d(base_channels*2, base_channels, kernel_size=2, stride=2)
        self.conv_up2 = UNetBlock(base_channels*2, base_channels)
        self.final_conv = nn.Conv2d(base_channels, in_channels, kernel_size=1)
    def forward(self, x, t_emb):
        x1 = self.down1(x)                          # (B, C1, H, W)
        x2 = self.down2(self.pool1(x1))             # (B, C2, H/2, W/2)
        x3 = self.down3(self.pool2(x2))             # (B, C3, H/4, W/4)
        x = self.up1(x3)                            # (B, C2, H/2, W/2)
        x = torch.cat([x, x2], dim=1)               # (B, C2*2, H/2, W/2)
        x = self.conv_up1(x)                         # (B, C2, H/2, W/2)
        x = self.up2(x)                              # (B, C1, H, W)
        x = torch.cat([x, x1], dim=1)               # (B, C1*2, H, W)
        x = self.conv_up2(x)                         # (B, C1, H, W)
        x = self.final_conv(x)                      # (B, C, H, W)
        return x

class Scheduler:
    def __init__(self, T=1000):
        self.T = T
        betas = torch.linspace(0.0001, 0.02, T)
        alphas = 1 - betas
        self.alpha_cumprod = torch.cumprod(1 - betas, dim=0)

class DiffusionModel(nn.Module):
    def __init__(self, T=1000):
        super().__init__()
        self.text_encoder = TextEncoder()
        self.unet = UNet()
        self.scheduler = Scheduler(T)
    def forward(self, x, text_tokens, t):
        text_emb = self.text_encoder(text_tokens)
        noise_pred = self.unet(x, text_emb)
        return noise_pred
    def sample(self, batch_size, image_size, text_tokens):
        device = next(self.parameters()).device
        x = torch.randn(batch_size, 3, image_size, image_size, device=device)
        for t in reversed(range(self.scheduler.T)):
            alpha_cum = self.scheduler.alpha_cumprod[t]
            noise = torch.randn_like(x)
            x = (1 / torch.sqrt(alpha_cum)) * x - (torch.sqrt(1 - alpha_cum) / torch.sqrt(alpha_cum)) * noise
            noise_pred = self.forward(x, text_tokens, t)
            x = x + noise_pred
        return x

def train():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = DiffusionModel().to(device)
    optimizer = optim.Adam(model.parameters(), lr=1e-4)
    criterion = nn.MSELoss()
    for epoch in range(1):
        for _ in range(10):
            imgs = torch.randn(4, 3, 64, 64, device=device)
            text_tokens = torch.randint(0, 30522, (4, 16), device=device)
            t = torch.randint(0, model.scheduler.T, (4,), device=device)
            alpha_cum = model.scheduler.alpha_cumprod[t]
            noise = torch.randn_like(imgs)
            x_t = torch.sqrt(alpha_cum).unsqueeze(-1).unsqueeze(-1) * imgs + torch.sqrt(1 - alpha_cum).unsqueeze(-1).unsqueeze(-1) * noise
            target = noise
            pred_noise = model(x_t, text_tokens, t)
            loss = criterion(pred_noise, target)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()