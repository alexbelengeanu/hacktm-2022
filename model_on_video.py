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

    # Load video
    video = r'D:/Lucru/github-folder/hacktm-2022/input-video/cropped_input.mp4'
    cap = cv2.VideoCapture(video)
    cap_no = 0
    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        cap_no = cap_no + 1
        if not ret and frame is None:
                break
        if cap_no % 3 == 0:
            sample = frame

            sample = cv2.resize(sample, dsize=(256, 256),
                                interpolation=cv2.INTER_AREA)
            sample = sample / sample.max()
            sample = sample.transpose(2, 0, 1)
            sample = torch.Tensor(sample)
            sample = sample.unsqueeze(0)

            prediction = resnet18(sample.to(device))
            probability = F.softmax(prediction, dim=1)
            top_probability, top_class = probability.topk(1, dim = 1)

            if str(torch.argmax(prediction.cpu(), axis=1)) == 'tensor([0])':
                prediction = "organic"
            elif str(torch.argmax(prediction.cpu(), axis=1)) == 'tensor([1])':
                prediction = "recyclable"


            frame = cv2.resize(frame, dsize=(256, 256),
                                interpolation=cv2.INTER_AREA)
            cv2.putText(frame, f"class: {prediction}", (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)
            cv2.putText(frame, f"proba: {torch.round(top_probability[0][0],decimals=2)}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)

            cv2.imshow('result', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
    cap.release()
    cv2.destroyAllWindows()