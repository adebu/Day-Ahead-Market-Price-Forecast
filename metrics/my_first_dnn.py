import torch
from torch import nn, optim
from torch.utils.data import Dataset, DataLoader
import pandas as pd
import numpy as np
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
models_data_dir = os.path.abspath(os.path.join(parent_dir, 'metrics'))
sys.path.insert(1, models_data_dir)
sys.path.insert(1, parent_dir)


from metrics import calculate_metrics

# Load data
X_train = pd.read_csv('X_train.csv')
X_test = pd.read_csv('X_test.csv')
y_train = pd.read_csv('y_train.csv')
y_test = pd.read_csv('y_test.csv')

# Custom dataset
class CustomDataset(Dataset):
    def __init__(self, features, labels, transform=None):
        self.features = features
        self.labels = labels
        self.transform = transform

    def __len__(self):
        return len(self.features)

    def __getitem__(self, idx):
        feature = self.features.iloc[idx].values if isinstance(self.features, pd.DataFrame) else self.features[idx]
        label = self.labels.iloc[idx].values if isinstance(self.labels, pd.DataFrame) else self.labels[idx]

        if self.transform:
            feature = self.transform(feature)

        return feature, label

# Model definition
class SimpleNN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(SimpleNN, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        out = self.fc1(x)
        out = self.relu(out)
        out = self.fc2(out)
        return out

def main():
    # Define the model
    input_size = X_train.shape[1]  
    hidden_size = 20
    output_size = 1  # For regression tasks
    model = SimpleNN(input_size, hidden_size, output_size)

    # Define the loss function (Mean Absolute Error)
    criterion = nn.L1Loss()

    # Define the optimizer
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    # Print model summary (optional)
    print(model)

    # Create custom datasets
    train_dataset = CustomDataset(X_train, y_train, transform=None)
    test_dataset = CustomDataset(X_test, y_test, transform=None)

    # Create data loaders
    train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True, num_workers=2)
    test_loader = DataLoader(test_dataset, batch_size=64, shuffle=False, num_workers=2)

    # Move model to the appropriate device
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)

    # Training loop
    print('Starting training....')
    for epoch in range(5):
        running_loss = 0.0
        for i, (data, target) in enumerate(train_loader):
            data, target = torch.tensor(data).float().to(device), torch.tensor(target).float().to(device).view(-1, 1)
            optimizer.zero_grad()
            output = model(data)
            loss = criterion(output, target)
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item()
            if i % 5 == 0:  # Print every 5 batches
                print('[%d, %5d] loss: %.3f' % (epoch + 1, i + 1, running_loss / 5))
                running_loss = 0.0

    # Save final model
    torch.save(model.state_dict(), 'final_model.pth')

    # Forecasting function
    def forecast(model, data_loader):
        model.eval()
        predictions, actuals = [], []
        with torch.no_grad():
            for data, target in data_loader:
                data, target = torch.tensor(data).float().to(device), torch.tensor(target).float().to(device).view(-1, 1)
                output = model(data)
                predictions.extend(output.cpu().numpy())
                actuals.extend(target.cpu().numpy())
        return np.array(predictions), np.array(actuals)

    # Make predictions on test data
    print('Making predictions on test data...')
    predictions, actuals = forecast(model, test_loader)
    
    # Evaluate predictions
    metrics = calculate_metrics(predictions, actuals, 'DNN')
    print(metrics)

if __name__ == "__main__":
    main()
