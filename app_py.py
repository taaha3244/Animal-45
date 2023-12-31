# -*- coding: utf-8 -*-
"""app.py

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1LxQIoWzdJ0XgjBsg9JsNOCtpXkYuTm3Z
"""

!pip install gradio

import torch
import gradio as gr
from torchvision import models  # Assuming you're using a torchvision model
from torch import nn
from collections import OrderedDict

# Initialize the model
newmodel = models.densenet121(pretrained=False)

# Freeze parameters
for param in newmodel.parameters():
    param.requires_grad = False

# Redefine the classifier
classifier = nn.Sequential(OrderedDict([
    ('fc1', nn.Linear(1024, 500)),  # Adjust the input features to match DenseNet121
    ('relu', nn.ReLU()),
    ('fc2', nn.Linear(500, 45)),
    ('output', nn.LogSoftmax(dim=1))
]))

newmodel.classifier = classifier

newmodel.load_state_dict(torch.load('/content/drive/MyDrive/densenet121_state_dict.pth'))
newmodel.eval()

from torchvision import datasets, transforms
# Define the preprocessing steps
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# Define the prediction function
def predict(image):
    input_tensor = preprocess(image)
    input_batch = input_tensor.unsqueeze(0)

    with torch.no_grad():
        output = newmodel(input_batch)  # Use newmodel instead of model

    probabilities = torch.nn.functional.softmax(output[0], dim=0)
    top_prob, top_catid = torch.topk(probabilities, 1)

    # Replace the following line with your class names
    class_names = ['african_elephant', 'alpaca', 'american_bison', 'anteater', 'arctic_fox', 'armadillo', 'baboon', 'badger', 'blue_whale', 'brown_bear', 'camel', 'dolphin', 'giraffe', 'groundhog', 'highland_cattle', 'horse', 'jackal', 'kangaroo', 'koala', 'manatee', 'mongoose', 'mountain_goat', 'opossum', 'orangutan', 'otter', 'polar_bear', 'porcupine', 'red_panda', 'rhinoceros', 'sea_lion', 'seal', 'snow_leopard', 'squirrel', 'sugar_glider', 'tapir', 'vampire_bat', 'vicuna', 'walrus', 'warthog', 'water_buffalo', 'weasel', 'wildebeest', 'wombat', 'yak', 'zebra']
    return class_names[top_catid[0]]

gr.Interface(fn=predict, inputs=gr.Image(type="pil"), outputs="text").launch()

