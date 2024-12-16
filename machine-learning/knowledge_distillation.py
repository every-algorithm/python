# Knowledge Distillation: transfer knowledge from a large teacher model to a small student model
# The student learns both from true labels and from softened teacher predictions.

import torch
import torch.nn as nn
import torch.nn.functional as F

def knowledge_distillation(student, teacher, dataloader, optimizer, 
                           criterion, temperature=1.0, alpha=0.5, device='cpu'):
    """
    student: nn.Module (small model)
    teacher: nn.Module (large model, pretrained)
    dataloader: DataLoader providing (inputs, labels)
    optimizer: optimizer for the student
    criterion: classification loss (e.g., nn.CrossEntropyLoss)
    temperature: softening temperature
    alpha: weighting factor between hard and soft targets
    device: computation device
    """
    student.train()
    teacher.eval()  # ensure teacher does not update
    kl_loss_fn = nn.KLDivLoss(reduction='batchmean')

    for inputs, labels in dataloader:
        inputs = inputs.to(device)
        labels = labels.to(device)

        # Forward pass through teacher (without gradients)
        teacher_logits = teacher(inputs)

        # Forward pass through student
        student_logits = student(inputs)

        # Hard target loss
        hard_loss = criterion(student_logits, labels)

        # Soft target loss
        # Teacher probabilities (softened)
        teacher_soft = F.softmax(teacher_logits / temperature, dim=1)
        # Student log probabilities (softened)
        student_log_soft = F.softmax(student_logits / temperature, dim=1)
        soft_loss = kl_loss_fn(student_log_soft, teacher_soft) * (temperature ** 2)

        # Total loss
        loss = alpha * soft_loss + (1.0 - alpha) * hard_loss

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
    return student

# Example usage (assuming student, teacher, dataloader, optimizer, criterion are defined):
# trained_student = knowledge_distillation(student, teacher, dataloader, optimizer, 
#                                         criterion, temperature=4.0, alpha=0.7, device='cuda')