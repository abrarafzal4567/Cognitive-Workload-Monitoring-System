import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest, f_classif
from keras.models import Sequential
from keras.layers import LSTM, GRU, Dense
from keras.optimizers import Adam
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import tensorflow as tf




from keras.models import load_model

class HybridModelCode:
    def __init__(self) -> None:
        # self.runModel(dataArray)
        self.model = ""
        pass

    def predictFreqValues(self, dataArray):
        # Extract the values from the first 14 columns and all rows

        # data = pd.read_csv('tsv.csv').dropna()
        data = dataArray
        # print("Read Data From File is :: ", data)
        # loaded_model = load_model('m.h5')
        print("Read Data From CoAP is :: ", data["dataArrayFreq"])
        data = pd.DataFrame(data["dataArrayFreq"])
        # Read the CSV file containing 19200 rows and 15 columns
        # Extract the values from the first 14 columns and all rows
        # input_values = data.iloc[:, :14].values
        input_values = data.iloc[:, 1:-1].values
        # input_values = data.iloc[:, :14].values
        # Define and fit the scaler
        scaler_high = StandardScaler()
        input_values_scaled = scaler_high.fit_transform(input_values)

        # Reshape the input values
        input_values_reshaped = np.reshape(input_values_scaled, (input_values_scaled.shape[0], input_values_scaled.shape[1], 1))

        # Load the saved model
       
        model = tf.keras.models.load_model('My_New_model.h5')

        # Classify the cognitive workload using the preprocessed input values
        predicted_probabilities = model.predict(input_values_reshaped)
        predicted_labels = np.argmax(predicted_probabilities, axis=1)

        # Define the label mapping dictionary
        label_mapping = {0: 'low', 1: 'Average', 2: 'High'}

        predicted_categories = [label_mapping[label] for label in predicted_labels]

        # Print the predicted categories
        print('Predicted Categories:', predicted_categories)
        return self.countFreq(predicted_categories)
    
    def countFreq(self, predicted_categories):


        data = [predicted_categories.count("low"), predicted_categories.count("Average"), predicted_categories.count("High")]
        val = max(data)
        index = data.index(val)
        if index == 0:
            return "Low"
        elif index == 1:
            return "Average"
        elif index == 2:
            return "High"
        else:
            return "Invalid"
        
if __name__ == '__main__':
    obj = HybridModelCode()
