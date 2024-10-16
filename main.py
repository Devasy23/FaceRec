from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor

import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import models

# Import FastAPI and Flask functions
from API import run_fastapi_app
from FaceRec.app.main import run_flask


# Function to load different CNN backbones
def get_backbone(backbone_name: str):
    if backbone_name == "resnet50":
        backbone = models.resnet50(pretrained=True)
        backbone = nn.Sequential(
            *list(backbone.children())[:-2]
        )  # Remove the fully connected layers
    elif backbone_name == "vgg16":
        backbone = models.vgg16(pretrained=True)
        backbone = backbone.features  # Use VGG16 features as backbone
    elif backbone_name == "efficientnet_b0":
        backbone = models.efficientnet_b0(pretrained=True)
        backbone = nn.Sequential(
            *list(backbone.children())[:-2]
        )  # EfficientNet backbone
    else:
        raise ValueError(f"Backbone {backbone_name} not supported.")

    return backbone


# Custom model definition that uses the selected backbone
class CustomModel(nn.Module):
    def __init__(self, backbone, num_classes):
        super(CustomModel, self).__init__()
        self.backbone = backbone
        self.avgpool = nn.AdaptiveAvgPool2d((1, 1))  # Global Average Pooling
        if isinstance(backbone, models.VGG):
            # VGG output feature size is 512
            self.fc = nn.Linear(512, num_classes)
        else:
            self.fc = nn.Linear(
                2048, num_classes
            )  # ResNet50 and EfficientNet output feature size is 2048

    def forward(self, x):
        x = self.backbone(x)
        x = self.avgpool(x)
        x = torch.flatten(x, 1)
        x = self.fc(x)
        return x


# Function to freeze layers in the model
def freeze_layers(model, layers_to_freeze=10):
    layers = list(model.children())
    for layer in layers[:layers_to_freeze]:
        for param in layer.parameters():
            param.requires_grad = False


# Dummy training loop (to be implemented based on your training dataset)
def train_model(model, criterion, optimizer, num_epochs=10):
    for epoch in range(num_epochs):
        # This is where you'd load your training data and perform forward/backward passes.
        # Example forward pass:
        inputs = torch.randn(8, 3, 224, 224)  # Random batch of images
        labels = torch.randint(0, 10, (8,))  # Random labels for 10 classes

        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        print(f"Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item()}")


# Loop through different backbones and train the model
def run_experiments():
    backbones = ["resnet50", "vgg16", "efficientnet_b0"]
    # Define number of output classes (e.g., for classification)
    num_classes = 10

    for backbone_name in backbones:
        print(f"\nTraining with {backbone_name} backbone...")

        # Get the backbone and create the model
        backbone = get_backbone(backbone_name)
        model = CustomModel(backbone, num_classes=num_classes)

        # Optional: Freeze some layers if fine-tuning
        # Freeze first 5 layers, for example
        freeze_layers(model, layers_to_freeze=5)

        # Define the loss function and optimizer
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(model.parameters(), lr=0.001)

        # Train the model
        train_model(model, criterion, optimizer, num_epochs=10)


# Multithreading used to start both FastAPI and Flask apps along with running experiments.
if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=3) as executor:
        # Run Flask and FastAPI applications
        executor.submit(run_flask)
        executor.submit(run_fastapi_app)

        # Run the CNN backbone experiments concurrently
        executor.submit(run_experiments)
