import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, AdamW
from torch.utils.data import DataLoader, TensorDataset
import torch.nn as nn

# Function to preprocess text data
def preprocess_data(data, tokenizer, max_len):
    tokens = tokenizer(data, padding="max_length", truncation=True, max_length=max_len, return_tensors="pt")
    return tokens

# Define training function (simplified for brevity)
def train_model(model, train_loader, optimizer, criterion, epochs):
    for epoch in range(epochs):
        for batch in train_loader:
            # Forward pass, calculate loss
            outputs = model(**batch)
            loss = criterion(outputs.logits, batch["labels"])

            # Backward pass, update weights
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            # Print training progress (omitted for brevity)

# Function to generate medication predictions
def predict_medication(model, tokenizer, condition, max_len):
    condition_tokens = tokenizer(condition, padding="max_length", truncation=True, max_length=max_len, return_tensors="pt")
    generated_ids = model.generate(**condition_tokens)
    predicted_medication = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
    return predicted_medication

# Load data from Kaggle (replace with your download path)
data = pd.read_csv("/Users/rishabpaul/Desktop/Minor 2/drugs_for_common_treatments.csv")

# Separate features and targets
medical_conditions = data["medical_condition"]
medications = data["drug_name"]

# Hyperparameters (adjust based on resources)
learning_rate = 2e-5
batch_size = 8
epochs = 3  # Increase epochs for better results (requires more compute)
max_len = 512  # Adjust based on model and data

# Define tokenizer and model (e.g., Bart)
tokenizer = AutoTokenizer.from_pretrained("facebook/bart-base")
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-base")

# Preprocess data
condition_tokens = preprocess_data(medical_conditions, tokenizer, max_len)
medication_tokens = preprocess_data(medications, tokenizer, max_len)

# Prepare data for training (DataLoader)
train_dataset = TensorDataset(condition_tokens.input_ids, medication_tokens.input_ids) 
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

# Define optimizer and loss function
optimizer = AdamW(model.parameters(), lr=learning_rate)
criterion = nn.CrossEntropyLoss(ignore_index=tokenizer.pad_token_id)

# Train the model (complex process, replace with actual training loop)
train_model(model, train_loader, optimizer, criterion, epochs)

# Define a new medical condition for prediction
new_condition = "Stomach Ache"

# Generate medication suggestion
predicted_medication = predict_medication(model, tokenizer, new_condition, max_len)

print(f"Predicted medication for {new_condition}: {predicted_medication}")
