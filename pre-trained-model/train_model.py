import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib
import json
import time

def train_and_save_model():
    print("🚀 N.O.V.A AI Training Sequence Initiated...")
    start_time = time.time()
    
    # 1. Load the full dataset
    print("📊 Loading dataset: Receptor_western_NAmerica_ozone_obs_1994_2021_from900to300.csv")
    df = pd.read_csv("Receptor_western_NAmerica_ozone_obs_1994_2021_from900to300.csv")
    
    # 2. Calculate Dashboard Statistics
    print("🧮 Calculating global statistics...")
    stats = {
        'total': len(df),
        'avg_ozone': round(df['Ozone_ppbv'].mean(), 2),
        'max_ozone': round(df['Ozone_ppbv'].max(), 2)
    }

    # 3. Prepare Data
    print("✂️ Splitting training and testing data...")
    X = df[['Pressure', 'Year', 'Month', 'Latitude', 'Longitude']]
    y = df['Ozone_ppbv']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 4. Train the Model (OPTIMIZED FOR FILE SIZE & ACCURACY)
    print("🧠 Training Optimized Random Forest Regressor...")
    model = RandomForestRegressor(
        n_estimators=100,      # Lowered slightly to save space, still highly accurate
        max_depth=16,          # Capped depth to prevent exponential memory usage
        min_samples_leaf=10,   # CRITICAL FOR SIZE: Stops trees from memorizing single rows
        n_jobs=-1,             
        random_state=42
    )
    model.fit(X_train, y_train)

    # 5. Evaluate
    accuracy = round(model.score(X_test, y_test) * 100, 2)
    stats['accuracy'] = accuracy
    print(f"✅ Model successfully trained! Accuracy (R² Score): {accuracy}%")

    # 6. Export Model with COMPRESSION
    print("🗜️ Compressing and saving model to 'nova_ozone_model.pkl'...")
    # 'compress=3' applies high-efficiency zlib compression to shrink the file drastically
    joblib.dump(model, "nova_ozone_model.pkl", compress=3) 
    
    print("💾 Saving stats to 'nova_stats.json'...")
    with open("nova_stats.json", "w") as f:
        json.dump(stats, f)

    elapsed = round(time.time() - start_time, 2)
    print(f"🏁 Training complete in {elapsed} seconds. File size should be drastically smaller!")

if __name__ == "__main__":
    train_and_save_model()