# Time Series Analysis Homework Assignment

## Context: Time Series as a Regression Problem

Time series analysis is traditionally approached with specific techniques designed for sequential data, such as ARIMA, exponential smoothing, or state space models. However, an alternative approach is to transform time series forecasting into a supervised learning regression problem.

In this framework, we use historical values from previous time steps as input features to predict future values. This technique is often called the "sliding window" or "lag feature" approach and offers several advantages:

1. **Flexibility**: Allows the use of any regression algorithm for forecasting
2. **Feature Engineering**: Enables incorporation of additional predictive variables beyond just the time series itself
3. **Interpretability**: Makes it easier to understand which historical time points influence predictions the most
4. **Complex Patterns**: Can capture non-linear relationships and complex temporal dependencies

For example, instead of using a specialized time series model to predict next month's sales, we could:

- Use the previous 6 months of sales as features
- Train a regression model that maps these 6 values to the next month's sales
- Apply this model to new data to make predictions

This reformulation preserves the temporal structure while opening up the entire world of regression algorithms to time series problems.

## Assignment Tasks

### 1. Data Preparation and Feature Engineering

For this assignment, you will use the Air Passengers dataset, which contains monthly totals of international airline passengers from 1949 to 1960:

```
https://raw.githubusercontent.com/AileenNielsen/TimeSeriesAnalysisWithPython/master/data/AirPassengers.csv
```

Here is the code to transform the time series data into a supervised learning problem using a sliding window approach:

```python
import pandas as pd
import numpy as np

# Load the data
url = "https://raw.githubusercontent.com/AileenNielsen/TimeSeriesAnalysisWithPython/master/data/AirPassengers.csv"
df = pd.read_csv(url)

# Convert the 'Month' column to datetime
df['Month'] = pd.to_datetime(df['Month'])
df.set_index('Month', inplace=True)

# Create a function to transform time series to supervised learning problem
def create_features(data, window_size=6):
    """
    Transform time series to supervised learning with a sliding window.

    Parameters:
    -----------
    data : pandas Series
        The time series data
    window_size : int
        Number of previous time steps to use as features

    Returns:
    --------
    X : pandas DataFrame
        Feature matrix with window_size columns
    y : pandas Series
        Target variable (next value in the time series)
    """
    X = pd.DataFrame()

    # Create window_size lag features
    for i in range(window_size, 0, -1):
        X[f'lag_{i}'] = data.shift(i)

    # Align the target with the features
    y = data.copy()

    # Drop rows with NaN values resulting from the lag
    X = X.dropna()
    y = y.loc[X.index]

    return X, y

# Apply the transformation
X, y = create_features(df['#Passengers'])

# Create a DataFrame with both features and target for inspection
result_df = X.copy()
result_df['target'] = y

# Save the prepared data for modeling
result_df.to_csv('air_passengers_supervised.csv')

# Split the data into training and testing sets (80% train, 20% test)
train_size = int(len(X) * 0.8)
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

print(f"Training set size: {X_train.shape}")
print(f"Testing set size: {X_test.shape}")
```

### 2. Combined EDA and Model Training

Create a comprehensive Jupyter notebook (`air_passengers_analysis.ipynb`) that includes both exploratory data analysis and model training. Your notebook should include the following sections:

#### 2.1 Data Loading and Preparation

- Load the original Air Passengers dataset
- Apply the time series to regression transformation (using the code provided above)
- Examine the structure of the transformed data

#### 2.2 Exploratory Data Analysis

- Provide statistical summary of the original time series
- Visualize the original time series data
- Analyze the distribution of the target variable
- Analyze the distributions of feature variables
- Compute and visualize correlations between features and target
- Create pairplots to visualize relationships
- Perform seasonal decomposition of the original time series
- Identify any trends, seasonality, or other patterns in the data

#### 2.3 Model Training with TabPFNRegressor

- Prepare the data for modeling (scaling if necessary)
- Train a TabPFNRegressor model on the transformed data
- Evaluate the model using appropriate metrics:
  - Mean Squared Error (MSE)
  - Mean Absolute Error (MAE)
  - R² Score
- Visualize the actual vs. predicted values
- Analyze model residuals
- Save the trained model with an appropriate name (e.g., `tabpfn_air_passengers_model.pkl`)

#### 2.4 Model Interpretation

- Discuss the model's performance
- Analyze which lag features are most important for prediction
- Compare the model's results with the patterns observed in the EDA
- Consider the limitations of the approach

### 3. REST API Service

Develop a Flask application that:

- Loads the trained model
- Provides an endpoint that accepts 6 months of passenger data as input
- Returns a prediction for the next month's passenger count
- Includes appropriate error handling and input validation

## Evaluation Criteria

Your submission will be evaluated based on:

1. Correct implementation of the time series to regression transformation
2. Quality and depth of exploratory data analysis
3. Model performance and appropriate evaluation techniques
4. Functionality and robustness of the REST API
5. Code quality, documentation, and clarity of explanation

## Submission Requirements

Submit the following files:

1. Combined EDA and model training Jupyter notebook (`air_passengers_analysis.ipynb`)
2. Flask API application code (`app.py`)
3. Trained model file (`tabpfn_air_passengers_model.pkl` or similar)
4. A brief report discussing your approach and findings

Good luck!
