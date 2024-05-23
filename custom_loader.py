import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle

def load_data_csv(sub, root_folder, train_size = 0.8,n_samples=500,classes_labels = ['all']):
    # classes_labels = ['break','foot','left_hand','right_hand','tongue']
    train_data, test_data = [], []
    train_labels, test_labels = [], []
    data, labels = [], []
    for sub_folder in os.listdir(root_folder):
        if str(sub_folder).startswith('__'):
            continue
        elif not str(sub_folder).startswith(f"{sub+1}_"):
            continue
        # print(str(sub_folder))
        folder_path = os.path.join(root_folder, sub_folder)
        for class_folder in os.listdir(folder_path):
            if class_folder not in classes_labels:
                continue
            class_folder_path = os.path.join(folder_path, class_folder)
            if os.path.isdir(class_folder_path):

                for i, filename in enumerate(os.listdir(class_folder_path)):
                    if filename.endswith('.csv'):
                        df = pd.read_csv(os.path.join(class_folder_path, filename), skiprows=2)
                        df = df.iloc[:, 4:18]  # Load data from column 5 to column 19
                        if len(df) < n_samples:
                            mode_values = df.mode().iloc[0]  # Get the mode values of each column
                            mode_df = pd.DataFrame([mode_values]*(n_samples-len(df)), columns=df.columns)
                            while len(df) < n_samples:
                                df = pd.concat([df, mode_df], ignore_index=True)
                        else:
                            df = df.iloc[:n_samples]
                        data.append(df.values.T)
                        labels.append(classes_labels.index(class_folder))  # Create an array of class names
                    
    data = np.array(data)
    labels = np.array(labels)
    data, labels = shuffle(data, labels, random_state=42)
    return train_test_split(data, labels, train_size=train_size , random_state=42, stratify=labels)  # 80% training, 20% testing
if  __name__ == '__main__':
    # Usage
    root_folder = './records/'  # Replace with your root folder path
    classes_labels = ['break','left_hand','right_hand','tongue']
    train_data, test_data, train_labels, test_labels = load_data_csv(0, root_folder,train_size=0.6,n_samples=1125,classes_labels = classes_labels)
    print(test_labels)
    for i in range(5):
        print(np.sum(test_labels[:]==i))
    print(train_data.shape, train_labels.shape, test_data.shape, test_labels.shape)
    # print(train_data)
