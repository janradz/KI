import torch
import torchvision
from torchvision import datasets, transforms


fashion_data = torchvision.datasets.FashionMNIST(root='./data', train=True, download=True, transform=transforms.ToTensor())

fashion_data_loader = torch.utils.data.DataLoader(fashion_data, batch_size=4, shuffle=True, num_workers=2)

len_data = len(fashion_data_loader)
print(len_data)

fashion_len = fashion_data.__len__()
print(fashion_len)
