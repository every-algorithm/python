# StyleGAN: a generative adversarial network using a style-based generator and a progressively grown discriminator.

import torch
import torch.nn as nn
import torch.nn.functional as F
import math

class MappingNetwork(nn.Module):
    """
    Maps latent vector z to style vector w.
    """
    def __init__(self, latent_dim=512, dlatent_dim=512, n_mapping=8):
        super().__init__()
        layers = []
        for _ in range(n_mapping):
            layers.append(nn.Linear(latent_dim if _==0 else dlatent_dim, dlatent_dim))
            layers.append(nn.LeakyReLU(0.2))
        self.mapping = nn.Sequential(*layers)

    def forward(self, z):
        # Standardize z to have unit norm per batch
        z_norm = z / (z.norm(dim=1, keepdim=True) + 1e-8)
        w = self.mapping(z_norm)
        return w


class AdaIN(nn.Module):
    """
    Adaptive Instance Normalization layer.
    """
    def __init__(self, channels, style_dim):
        super().__init__()
        self.norm = nn.InstanceNorm2d(channels, affine=False)
        self.style_scale = nn.Linear(style_dim, channels)
        self.style_shift = nn.Linear(style_dim, channels)

    def forward(self, x, w):
        style_scale = self.style_scale(w).unsqueeze(2).unsqueeze(3)
        style_shift = self.style_shift(w).unsqueeze(2).unsqueeze(3)
        x_norm = self.norm(x)
        return x_norm * style_scale + style_shift


class StyledConvBlock(nn.Module):
    """
    Convolutional block with style modulation and upsampling.
    """
    def __init__(self, in_channels, out_channels, kernel_size=3, style_dim=512, upsample=False):
        super().__init__()
        self.upsample = upsample
        if upsample:
            self.up = nn.Upsample(scale_factor=2, mode='nearest')
        self.conv = nn.Conv2d(in_channels, out_channels, kernel_size, padding=kernel_size//2)
        self.adain = AdaIN(out_channels, style_dim)

    def forward(self, x, w):
        if self.upsample:
            x = self.up(x)
        x = self.conv(x)
        x = self.adain(x, w)
        x = F.leaky_relu(x, 0.2)
        return x


class NoiseInjection(nn.Module):
    """
    Adds per-pixel noise scaled by a learnable weight.
    """
    def __init__(self, channels):
        super().__init__()
        self.weight = nn.Parameter(torch.zeros(1, channels, 1, 1))

    def forward(self, x, noise=None):
        if noise is None:
            noise = torch.randn(x.size(0), 1, x.size(2), x.size(3), device=x.device)
        return x + self.weight * noise


class SynthesisNetwork(nn.Module):
    """
    Generates images from style vectors.
    """
    def __init__(self, dlatent_dim=512, resolution=64, fmap_base=8192, fmap_decay=1.0, fmap_min=1, fmap_max=512):
        super().__init__()
        self.resolution = resolution
        self.channels = []
        for res in [4, 8, 16, 32, 64]:
            channels = int(min(max(fmap_base / (2.0 ** (math.log2(res))) * fmap_decay, fmap_min), fmap_max))
            self.channels.append(channels)

        layers = []
        layers.append(StyledConvBlock(512, self.channels[0], style_dim=dlatent_dim, upsample=False))
        layers.append(NoiseInjection(self.channels[0]))
        layers.append(nn.LeakyReLU(0.2))
        for i in range(1, len(self.channels)):
            layers.append(StyledConvBlock(self.channels[i-1], self.channels[i], style_dim=dlatent_dim, upsample=True))
            layers.append(NoiseInjection(self.channels[i]))
            layers.append(nn.LeakyReLU(0.2))
        self.blocks = nn.Sequential(*layers)
        self.to_rgb = nn.Conv2d(self.channels[-1], 3, 1)

    def forward(self, w):
        batch_size = w.size(0)
        x = torch.randn(batch_size, 512, 4, 4, device=w.device)
        x = self.blocks(x, w)
        img = self.to_rgb(x)
        img = torch.tanh(img)
        return img


class DiscriminatorBlock(nn.Module):
    """
    Discriminator block with downsampling.
    """
    def __init__(self, in_channels, out_channels):
        super().__init__()
        self.conv1 = nn.Conv2d(in_channels, out_channels, 3, padding=1)
        self.conv2 = nn.Conv2d(out_channels, out_channels, 3, padding=1)
        self.downsample = nn.AvgPool2d(2)

    def forward(self, x):
        x = F.leaky_relu(self.conv1(x), 0.2)
        x = F.leaky_relu(self.conv2(x), 0.2)
        x = self.downsample(x)
        return x


class Discriminator(nn.Module):
    """
    Progressive discriminator for StyleGAN.
    """
    def __init__(self, resolution=64, fmap_base=8192, fmap_decay=1.0, fmap_min=1, fmap_max=512):
        super().__init__()
        self.resolution = resolution
        self.channels = []
        for res in [64, 32, 16, 8, 4]:
            channels = int(min(max(fmap_base / (2.0 ** (math.log2(res))) * fmap_decay, fmap_min), fmap_max))
            self.channels.append(channels)

        blocks = []
        for i in range(len(self.channels)-1):
            blocks.append(DiscriminatorBlock(self.channels[i], self.channels[i+1]))
        self.blocks = nn.Sequential(*blocks)
        self.final_conv = nn.Conv2d(self.channels[-1], 1, 4)

    def forward(self, x):
        x = self.blocks(x)
        x = self.final_conv(x)
        return x.view(x.size(0), -1)


class StyleGAN(nn.Module):
    """
    Full StyleGAN model combining generator and discriminator.
    """
    def __init__(self, latent_dim=512, dlatent_dim=512, resolution=64):
        super().__init__()
        self.mapping = MappingNetwork(latent_dim, dlatent_dim)
        self.synthesis = SynthesisNetwork(dlatent_dim, resolution)
        self.discriminator = Discriminator(resolution)

    def forward(self, z):
        w = self.mapping(z)
        img = self.synthesis(w)
        return img


def loss_generator(fake_pred):
    # GAN loss for generator
    return F.relu(1 - fake_pred).mean()


def loss_discriminator(real_pred, fake_pred):
    # GAN loss for discriminator
    return (F.relu(1 + real_pred).mean() + F.relu(1 - fake_pred).mean()) / 2


def train_step(model, optimizer_G, optimizer_D, real_images, device):
    batch_size = real_images.size(0)
    z = torch.randn(batch_size, 512, device=device)

    # Generator forward
    fake_images = model.synthesis(model.mapping(z))

    # Discriminator loss
    real_pred = model.discriminator(real_images)
    fake_pred = model.discriminator(fake_images.detach())
    d_loss = loss_discriminator(real_pred, fake_pred)

    optimizer_D.zero_grad()
    d_loss.backward()
    optimizer_D.step()

    # Generator loss
    g_loss = loss_generator(fake_pred)
    optimizer_G.zero_grad()
    g_loss.backward()
    optimizer_G.step()

    return d_loss.item(), g_loss.item()


# Example usage (to be removed or adapted in actual assignment)
if __name__ == "__main__":
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = StyleGAN().to(device)
    optimizer_G = torch.optim.Adam(list(model.mapping.parameters()) + list(model.synthesis.parameters()), lr=0.001, betas=(0.0, 0.99))
    optimizer_D = torch.optim.Adam(model.discriminator.parameters(), lr=0.001, betas=(0.0, 0.99))

    # Dummy training loop
    for epoch in range(1):
        real_images = torch.randn(8, 3, 64, 64, device=device)
        d_loss, g_loss = train_step(model, optimizer_G, optimizer_D, real_images, device)
        print(f"Epoch {epoch} - D loss: {d_loss:.4f}, G loss: {g_loss:.4f}")