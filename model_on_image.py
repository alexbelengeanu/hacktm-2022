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
    # Load model
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

    size = 0
    while size**2 < len(os.listdir("./input")):
        size = size + 1
    size = size**2

    if len(os.listdir("./input")) > 9:
        print("Due to the fact that the number of samples is >9, the display may look uglier. We suggest using <= 9 samples as input.")

    files = list([pth for pth in os.listdir(r'D:/Lucru/github-folder/hacktm-2022/input/')])
    files.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))

    fig = plt.figure(figsize=(12, 10))
    plt.subplots_adjust(top = .9, bottom=.05, hspace=.9, wspace=.05)

    for idx, filename in enumerate(files):
        sample = Image.open(os.path.join(r'D:/Lucru/github-folder/hacktm-2022/input/',filename))
        sample = sample.resize((256, 256))

        sample_ = sample.copy()
        sample_ = np.array(sample_)

        sample_ = sample_ / sample_.max()
        sample_ = sample_.transpose(2, 0, 1)
        sample_ = torch.Tensor(sample_)
        sample_ = sample_.unsqueeze(0)

        predict = resnet18(sample_.to(device))
        probability = F.softmax(predict, dim=1)
        top_probability, top_class = probability.topk(1, dim = 1)

        print(f'sample {filename} got a predict score of {top_probability[0][0]}')
        if str(torch.argmax(predict.cpu(), axis=1)) == 'tensor([0])':
            predict = "organic"
        elif str(torch.argmax(predict.cpu(), axis=1)) == 'tensor([1])':
            predict = "recyclable"

        fig.add_subplot(int(np.sqrt(size)), int(np.sqrt(size)), idx+1)
        plt.imshow(sample)
        plt.title(f"predict: {predict}")
    
    plt.show()

    