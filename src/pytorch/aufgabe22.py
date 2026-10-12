import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms




class FashionNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.flatten = nn.Flatten()
        self.model = nn.Linear(28*28, 10)

    def forward(self, x):
        x = self.flatten(x)
        logits = self.model(x)
        return logits


class FashionNet2(nn.Module):
    def __init__(self):
        super().__init__()
        self.flatten = nn.Flatten()
        self.model = nn.Sequential(
            nn.Linear(28*28, 128),
            nn.ReLU(),

            nn.Linear(128,32),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(32,10)
        )

    def forward(self, x):
        x = self.flatten(x)
        logits = self.model(x)
        return logits


class FashionNet3(nn.Module):
    def __init__(self):
        super().__init__()
        self.flatten = nn.Flatten()
        self.model = nn.Sequential(
            nn.Linear(28 * 28, 64), nn.ReLU(),
            nn.Linear(64, 32), nn.ReLU(),
            nn.Linear(32, 16), nn.ReLU(),
            nn.Linear(16, 8), nn.ReLU(),

            # bottleneck
            nn.Linear(8, 4), nn.ReLU(),

            nn.Linear(4, 8), nn.ReLU(),
            nn.Linear(8, 16), nn.ReLU(),
            nn.Linear(16, 32), nn.ReLU(),


            nn.Linear(32, 10)
        )

    def forward(self, x):
        x = self.flatten(x)
        logits = self.model(x)
        return logits
# 1. Bild in Tensor umwandeln
transform = transforms.Compose([
    transforms.ToTensor(),
])

# 2. Datensätze herunterladen (Trainings- und Testmenge)
train_dataset = datasets.FashionMNIST(root="data", train=True, download=True, transform=transform)
test_dataset = datasets.FashionMNIST(root="data", train=False, download=True, transform=transform)

# 3. DataLoader verpacken die Daten in kleine Stapel (Batches)
batch_size = 64
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

# Instanzieren Sie Ihr Modell, eine Verlustfunktion und einen Optimierer
model = FashionNet2()  # Hier wird Ihre Klasse von oben zum Leben erweckt
loss_fn = nn.CrossEntropyLoss()  # Berechnet den Fehler (Quadratischer Verlust aus Folie 205, aber für Wahrscheinlichkeiten optimiert)
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)  # Der "Lehrer", der die Gewichte anpasst

def train(dataloader, model, loss_fn, optimizer):
    model.train()  # Setzt das Modell in den Trainingsmodus
    for batch, (X, y) in enumerate(dataloader):

        # LÜCKE 1: Forward-Pass und Loss berechnen
        pred = model(X)
        loss = loss_fn(pred, y)

        # LÜCKE 2: Back-Propagation (Rückwärts-Pass)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if batch % 100 == 0:
            print(f"Loss: {loss.item():>7f}")


def compute_accuracy(dataloader, model):
    model.eval()

    correct = 0
    total = 0

    with torch.no_grad():
        for X, y in dataloader:
            outputs = model(X)
            _, predicted = torch.max(outputs, 1)

            total += y.size(0)
            correct += (predicted == y).sum().item()

    return correct / total


# Wir trainieren das Modell für 5 Epochen
epochs = 5

for t in range(epochs):
    print(f"Epoche {t + 1}\n-------------------------------")

    # 1. Trainiere für eine Epoche
    train(train_loader, model, loss_fn, optimizer)

    # 2. Prüfe, wie gut das Modell jetzt ist (Accuracy auf den Trainingsdaten berechnen)
    acc = compute_accuracy(train_loader, model)

    print(f"-> Accuracy nach Epoche {t + 1}: {acc * 100:.2f}%\n")

print("Training fertig!")