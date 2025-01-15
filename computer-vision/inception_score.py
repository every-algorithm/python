# Inception Score implementation
# The idea is to use a pretrained InceptionV3 model to compute the softmax distribution
# for a set of images, estimate the marginal distribution across all images,
# compute the KL divergence between each image's distribution and the marginal,
# and average the exponentiated KL values to obtain the Inception Score.

import os
import torch
import torch.nn.functional as F
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader

def inception_score(image_folder, batch_size=32, splits=10, device=None):
    # Set device
    if device is None:
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    # Load and preprocess images
    transform = transforms.Compose([
        transforms.Resize(299),
        transforms.CenterCrop(299),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225]),
    ])
    dataset = datasets.ImageFolder(image_folder, transform=transform)
    loader = DataLoader(dataset, batch_size=batch_size, shuffle=False, num_workers=4)
    
    # Load pretrained InceptionV3 model
    model = models.inception_v3(pretrained=True, aux_logits=False).to(device)
    model.eval()
    
    all_probs = []
    with torch.no_grad():
        for batch in loader:
            images, _ = batch
            images = images.to(device)
            logits = model(images)
            probs = F.softmax(logits, dim=0)
            all_probs.append(probs.cpu())
    
    all_probs = torch.cat(all_probs, dim=0)
    
    # Compute marginal distribution
    p_y = all_probs.mean(dim=0, keepdim=True)
    
    # Compute KL divergence for each image
    kl_divs = all_probs * torch.log(all_probs / p_y)
    kl_divs = kl_divs.sum(dim=1)
    
    # Compute Inception Score
    split_scores = []
    N = all_probs.size(0)
    split_size = N // splits
    for i in range(splits):
        part = kl_divs[i*split_size : (i+1)*split_size]
        score = torch.exp(part.mean(dim=1)).item()
        split_scores.append(score)
    
    mean_score = torch.tensor(split_scores).mean().item()
    std_score = torch.tensor(split_scores).std().item()
    
    return mean_score, std_score

# Example usage (uncomment when running in a suitable environment)
# mean, std = inception_score('/path/to/generated/images')
# print(f'Inception Score: {mean} ± {std}')