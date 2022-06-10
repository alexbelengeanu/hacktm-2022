# ML
from sklearn.metrics import accuracy_score

import cv2
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
from torchsummary import summary

# Plots
import matplotlib.pyplot as plt

# Utils
from collections import OrderedDict
from tqdm import tqdm, trange
from PIL import Image
import numpy as np
import os

MODEL_PATH = r'D:/Lucru/github-folder/hacktm-2022/my_resnet18.pth'

if __name__ == '__main__':
    resnet18 = torchvision.models.resnet18(pretrained=False)

    fc = nn.Sequential(OrderedDict([
        ('fc1', nn.Linear(512, 128)),
        ('dropout', nn.Dropout(p = .5)),
        ('relu', nn.ReLU()),
        ('fc2', nn.Linear(128, 2)),
        ('output', nn.LogSoftmax(dim=1))
    ]))
    resnet18.fc = fc

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    resnet18 = resnet18.to(device)

    resnet18.load_state_dict(torch.load(MODEL_PATH))
    resnet18.eval()

    # Camera
    cap = cv2.VideoCapture(0)

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        frame = frame[:, ::-1]
        sample = frame
        cv2.imshow('frame', sample)
        # Preprocessing

        sample = cv2.resize(sample, dsize=(256, 256),
                            interpolation=cv2.INTER_AREA)
        sample = sample / sample.max()
        sample = sample.transpose(2, 0, 1)
        sample = torch.Tensor(sample)
        sample = sample.unsqueeze(0)

        prediction = resnet18(sample.to(device))
        print(torch.argmax(prediction.cpu(), axis=1))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    cap.release()
    cv2.destroyAllWindows()