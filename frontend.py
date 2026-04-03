import gradio as gr
import time
import random
import numpy as np

import joblib
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score, confusion_matrix
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv1D, Flatten, LSTM, SimpleRNN, Dropout
from tensorflow.keras.utils import to_categorical
from sklearn.preprocessing import MinMaxScaler

# Load the meta-learner
meta_learner = joblib.load("stacking_meta_learner.pkl")

# Load the individual models
ann_model = load_model("ann_model.h5")
cnn_model = load_model("cnn_model.h5")
lstm_model = load_model("lstm_model.h5")
rnn_model = load_model("rnn_model.h5")

# Load the scaler (assuming it was saved previously)
scaler = joblib.load("scaler.pkl") # You need to save the scaler in the previous code

import pandas as pd
from sklearn.preprocessing import MinMaxScaler

import pandas as pd

# Load the dataset
# dataset_path = "Dataset/UNSW_NB15_training-set.parquet"
dataset_path = 'UNSW_NB15_training-set.parquet'
data = pd.read_parquet(dataset_path)
feature_names = ['dur', 'spkts', 'dpkts', 'sbytes', 'dbytes', 'rate', 'sttl', 'dttl', 'sload', 'dload', 'sloss', 'dloss', 'sinpkt', 'dinpkt', 'sjit', 'djit', 'swin', 'stcpb', 'dtcpb', 'dwin', 'tcprtt', 'synack', 'ackdat', 'smean', 'dmean', 'trans_depth', 'response_body_len', 'ct_srv_src', 'ct_state_ttl', 'ct_dst_ltm', 'ct_src_dport_ltm', 'ct_dst_sport_ltm', 'ct_dst_src_ltm', 'is_ftp_login', 'ct_ftp_cmd', 'ct_flw_http_mthd', 'ct_src_ltm', 'ct_srv_dst', 'is_sm_ips_ports','proto', 'service', 'state','sport','dport','pctsdroped','ackdroppd','protocol']

# Display the first few rows
print("Dataset Shape:", data.shape)
print(data.head())

# Drop rows with missing values (if applicable)
data.dropna(inplace=True)
print("Dataset Shape After Dropping Missing Values:", data.shape)

# Identify categorical columns
categorical_columns = data.select_dtypes(include=['object']).columns
print("Categorical Columns:", categorical_columns)

# One-hot encode categorical columns
data = pd.get_dummies(data, columns=categorical_columns, drop_first=True)
print("Dataset Shape After Encoding:", data.shape)

# Separate features and target
X = data.drop(['label', 'attack_cat'], axis=1)  # 'attack_cat' is often excluded if it's not part of the model
y = data['attack_cat']

# Handle categorical columns
categorical_cols = ['proto', 'service', 'state']  # Excluding 'attack_cat' as it's a secondary target or description
X_encoded = pd.get_dummies(X, columns=categorical_cols)

# Normalize numeric features
X = data.drop(['label', 'attack_cat'], axis=1)  # 'attack_cat' is often excluded if it's not part of the model
y = data['attack_cat']

# Handle categorical columns
categorical_cols = ['proto', 'service', 'state']  # Excluding 'attack_cat' as it's a secondary target or description
X_encoded = pd.get_dummies(X, columns=categorical_cols)

# Normalize numeric features
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X_encoded)

# Check the resulting shape
print("Scaled Feature Shape:", X_scaled.shape)

# Check the resulting shape
print("Scaled Feature Shape:", X_scaled.shape)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42, stratify=y)

# Print shapes of training and testing sets
print("Training Set Shape:", X_train.shape)
print("Testing Set Shape:", X_test.shape)

from tensorflow.keras.utils import to_categorical


# Import LabelEncoder
from sklearn.preprocessing import LabelEncoder

# Create a LabelEncoder object
label_encoder = LabelEncoder()

# Fit the encoder to your target variable and transform
y_train_encoded = label_encoder.fit_transform(y_train)
y_test_encoded = label_encoder.transform(y_test)

# Now use the encoded target variables with to_categorical
y_train_cat = to_categorical(y_train_encoded)
y_test_cat = to_categorical(y_test_encoded)
print("One-Hot Encoded Target Shape:", y_train_cat.shape)


# # Convert target labels to categorical format
# y_train_cat = to_categorical(y_train)
# y_test_cat = to_categorical(y_test)
print("One-Hot Encoded Target Shape:", y_train_cat.shape)

attack_labels = label_encoder.classes_


def simulate_network_traffic(X_train, feature_names, meta_learner, ann_model, cnn_model, lstm_model, rnn_model):
    def generator():
        while True:
            row_index = random.randint(0, len(X_train) - 1)
            selected_row = X_train[row_index]
            selected_row_reshaped = selected_row.reshape(1, -1)

            ann_pred = ann_model.predict(selected_row_reshaped)
            cnn_pred = cnn_model.predict(selected_row_reshaped.reshape(1, selected_row_reshaped.shape[1], 1))
            lstm_pred = lstm_model.predict(selected_row_reshaped.reshape(1, selected_row_reshaped.shape[1], 1))
            rnn_pred = rnn_model.predict(selected_row_reshaped.reshape(1, selected_row_reshaped.shape[1], 1))

            stacked_input = np.hstack((ann_pred, cnn_pred, lstm_pred, rnn_pred))
            prediction = meta_learner.predict(stacked_input)[0]

            non_zero_indices = np.where(selected_row != 0)[0]
            non_zero_values = selected_row[non_zero_indices]
            field_value_pairs = "<br>".join(
                [f"<b>{feature_names[i] if i < len(feature_names) else '-'}:</b> {non_zero_values[j]}" 
                for j, i in enumerate(non_zero_indices)]
            )
            
            attack_label = attack_labels[prediction]
            color = "green" if "Normal" in attack_label else "red"

            formatted_output = (
                f"<b>Row Number:</b> {row_index}<br>"
                f"<b>Selected Row (Non-Zero Values):</b><br>{field_value_pairs}<br>"
                f"<b>Prediction:</b> <span style='color:{color}'>{attack_label}</span>"
            )
            yield formatted_output
            time.sleep(5)

    return generator

def start_simulation():
    return gr.update(visible=True)

def stop_simulation():
    return gr.update(visible=False)

with gr.Blocks() as demo:
    gr.Markdown("# Network Traffic Simulation")
    start_btn = gr.Button("Start Simulation")
    stop_btn = gr.Button("Stop Simulation")
    output = gr.HTML(visible=False, label="Simulation Output")
    
    start_btn.click(start_simulation, None, output)
    stop_btn.click(stop_simulation, None, output)
    
    gr.Interface(fn=simulate_network_traffic(X_train, feature_names, meta_learner, ann_model, cnn_model, lstm_model, rnn_model),
                 inputs=[], outputs=[output], live=True)

demo.launch(debug=True)