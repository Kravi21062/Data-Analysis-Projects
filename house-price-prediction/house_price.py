import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib

# LOAD DATA ---
print("Loading data...")
# We use the built-in California Housing dataset from Scikit-Learn
data = fetch_california_housing(as_frame=True)
df = data.frame

# View the first 5 rows to understand the data
print(f"Dataset shape: {df.shape}")
print(df.head())

# DATA PREPROCESSING ---
print("\nPreprocessing data...")

# Check for missing values (Real-world step)
if df.isnull().sum().sum() > 0:
    df = df.dropna()

# Define Features (X) and Target (y)
# Target: MedHouseVal (Median House Value)
X = df.drop("MedHouseVal", axis=1)
y = df["MedHouseVal"]

# Split data into Training (80%) and Testing (20%) sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale the features (Important for many algorithms)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# MODEL TRAINING ---
print("\nTraining the model (Random Forest)...")
# We use Random Forest because it handles complex relationships better than simple Linear Regression
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)
print("Training complete.")

# EVALUATION ---
print("\nEvaluating model performance...")
y_pred = model.predict(X_test_scaled)

# Calculate metrics
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print(f"Root Mean Squared Error (RMSE): {rmse:.4f}")
print(f"R^2 Score (Accuracy): {r2:.4f}")
# Note: An R^2 score of 1.0 is perfect. A score around 0.8 is usually considered very good for this dataset.

# VISUALIZATION ---
plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred, alpha=0.5)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
plt.xlabel("Actual")
plt.ylabel("Predicted")
plt.title("Actual vs Predicted House Prices")
plt.show()

# SAVE THE MODEL ---
print("\nSaving model and scaler...")
joblib.dump(model, 'house_price.pkl')
joblib.dump(scaler, 'scaler.pkl')
print("Model saved as 'house_price.pkl'. You can now use this for deployment!")