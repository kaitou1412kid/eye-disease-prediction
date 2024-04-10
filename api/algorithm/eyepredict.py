import torch
from torchvision import transforms
from PIL import Image
import sys
import os
import torch.nn as nn

#         return x
class CNN6(nn.Module):
    def __init__(self, NUMBER_OF_CLASSES):
        super(CNN6, self).__init__()
        self.conv_layers = nn.Sequential(
            nn.Conv2d(in_channels=3, out_channels=32, kernel_size=3, stride=2),
            nn.BatchNorm2d(32),
            nn.LeakyReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(in_channels=32, out_channels=64,
                      kernel_size=3, stride=2),
            nn.BatchNorm2d(64),
            nn.LeakyReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(in_channels=64, out_channels=128,
                      kernel_size=3, stride=2),
            nn.BatchNorm2d(128),
            nn.LeakyReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
        )

        self.dense_layers = nn.Sequential(
            nn.Dropout(0.2),
            nn.Linear(128 * 3 * 3, 128),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(128, NUMBER_OF_CLASSES),
        )

    def forward(self, x):
        x = self.conv_layers(x)
        x = x.view(x.size(0), -1)
        x = self.dense_layers(x)

        return x

def predict(image_path):
    disease = {0 : "Cataract", 1 : "Glaucoma", 2 : "Normal"}
    predictions = None
    # relative_path = os.path.join("api","alogrithm")
    # model_path = os.path.join(os.getcwd(), relative_path, "cnn6.pt")
    # print(model_path)
    model = torch.load("cnn6.pt")
    model.eval()
    transform = transforms.Compose([
        transforms.Resize((256,256)),
        transforms.ToTensor()
    ])

    # image_path = path
    # normalized_path = os.path.normpath(image_path)
    # img_obj = Disease.objects.get(pk=id)
    # image_path = img_obj.image
    image = Image.open(image_path)
    image = transform(image)
    image_tensor = image.unsqueeze(0)
    with torch.no_grad():
        outputs = model(image_tensor)
        _, predicted = torch.max(outputs, 1)
        # print(outputs)
        predictions = predicted.item()
    return disease[predictions]
    
    
