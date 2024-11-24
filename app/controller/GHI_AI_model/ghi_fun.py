
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
from numpy import split, array

def process_solar_data(dataset_path):
    """
    Load and preprocess the solar radiation dataset
    """
    # Read the JSON file
    df = pd.read_json(dataset_path)

    # Drop unnecessary columns
    columns_to_drop = ["DHI", "DNI", "Clearsky DHI", "Clearsky DNI",
                      "Clearsky GHI", "Fill Flag", "Cloud Type"]
    df = df.drop(columns_to_drop, axis=1)

    # Create datetime index
    datetime_cols = ["Year", "Month", "Day", "Hour", "Minute"]
    df["date_time"] = df[datetime_cols].apply(
        lambda row: "-".join(row.values.astype(str)), axis=1)
    df['date_time'] = pd.to_datetime(df['date_time'], format='%Y-%m-%d-%H-%M')

    # Drop the individual date/time columns and set datetime as index
    df = df.drop(datetime_cols, axis=1)
    df = df.set_index('date_time')

    # Ensure GHI is the last column
    ghi = df.pop('GHI')
    df['GHI'] = ghi

    return df

def forecast(model, history, n_input):
    """
    Make a single forecast using the given model and history
    """
    data = array(history)
    data = data.reshape((data.shape[0]*data.shape[1], data.shape[2]))
    input_x = data[-n_input:, :]
    input_x = input_x.reshape((1, input_x.shape[0], input_x.shape[1]))
    yhat = model.predict(input_x, verbose=0)
    yhat = yhat[0]
    return yhat

def predict_model(model, test, n_input, n_predict=1):
    """
    Make predictions for multiple time steps
    """
    history = [x for x in test]
    predictions = list()
    for i in range(n_predict):
        yhat_sequence = forecast(model, history, n_input+110)
        predictions.append(yhat_sequence)
    predictions = array(predictions)
    return predictions

def predict_solar_radiation(model_path, dataset_path):
    """
    Main function to load data and model, and make predictions for multiple days

    Parameters:
    model_path (str): Path to the saved Keras model (.h5 file)
    dataset_path (str): Path to the dataset JSON file

    Returns:
    dict: Dictionary containing predictions for each day
    """
    try:
        # Load and process data
        df = process_solar_data(dataset_path)
        
        # Load model
        model = load_model(model_path)
        print("model loded")
        
        # Prepare test data
        test = array(split(df, len(df)/4))

        # Make predictions for 7 days
        predictions = {}
        for i in range(1, 8):
            prediction = predict_model(model, test, i)
            predictions[f"Day {i}"] = float(prediction.mean())  # Convert to float for JSON serialization

        return {
            "status": "success",
            "predictions": predictions
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

def main():        
    model_path = r"C:\Users\saif\OneDrive - SUPCOM\SupCom1\Projects\challenge CAS\Back end\app\controller\GHI_AI_model\my_model.h5"
    dataset_path = r"C:\Users\saif\OneDrive - SUPCOM\SupCom1\Projects\challenge CAS\Back end\app\controller\GHI_AI_model\2019_TUN.json"
    return(predict_solar_radiation(model_path, dataset_path))