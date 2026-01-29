from flask import Flask, request, jsonify
import joblib
import sqlite3
import pandas as pd

app = Flask(__name__)

# Load trained models
linreg_model = joblib.load("price_predicter.pkl")
logreg_model = joblib.load("sales_predicter.pkl")

# Initialize DB with correct schema
def init_db():
    conn = sqlite3.connect("housing.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Square_Footage REAL,
            Bedrooms INTEGER,
            Bathrooms REAL,
            Age INTEGER,
            Garage_Spaces REAL,
            Lot_Size REAL,
            Floors INTEGER,
            Neighborhood_Rating INTEGER,
            Condition INTEGER,
            School_Rating REAL,
            Has_Pool INTEGER,
            Renovated INTEGER,
            Location_Type TEXT,
            Distance_To_Center_KM REAL,
            Days_On_Market REAL,
            Predicted_Price REAL,
            Sold_Within_Week INTEGER
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    df = pd.DataFrame([data])  # Convert input to DataFrame
    
    # Predictions
    price_pred = linreg_model.predict(df)[0]
    sold_pred = logreg_model.predict(df)[0]
    
    # Save to DB with explicit casting
    conn = sqlite3.connect("housing.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO predictions (
            Square_Footage, Bedrooms, Bathrooms, Age, Garage_Spaces, Lot_Size, Floors,
            Neighborhood_Rating, Condition, School_Rating, Has_Pool, Renovated,
            Location_Type, Distance_To_Center_KM, Days_On_Market, Predicted_Price, Sold_Within_Week
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        float(data["Square_Footage"]), int(data["Bedrooms"]), float(data["Bathrooms"]), int(data["Age"]),
        float(data["Garage_Spaces"]), float(data["Lot_Size"]), int(data["Floors"]),
        int(data["Neighborhood_Rating"]), int(data["Condition"]), float(data["School_Rating"]),
        int(data["Has_Pool"]), int(data["Renovated"]), str(data["Location_Type"]),
        float(data["Distance_To_Center_KM"]), float(data["Days_On_Market"]),
        float(price_pred), int(sold_pred)
    ))
    conn.commit()
    conn.close()
    
    return jsonify({"Predicted_Price": price_pred, "Sold_Within_Week": int(sold_pred)})

@app.route("/update/<int:record_id>", methods=["PUT"])
def update(record_id):
    data = request.json
    conn = sqlite3.connect("housing.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE predictions SET
            Square_Footage=?, Bedrooms=?, Bathrooms=?, Age=?, Garage_Spaces=?, Lot_Size=?, Floors=?,
            Neighborhood_Rating=?, Condition=?, School_Rating=?, Has_Pool=?, Renovated=?, Location_Type=?,
            Distance_To_Center_KM=?, Days_On_Market=?
        WHERE id=?
    """, (
        float(data["Square_Footage"]), int(data["Bedrooms"]), float(data["Bathrooms"]), int(data["Age"]),
        float(data["Garage_Spaces"]), float(data["Lot_Size"]), int(data["Floors"]),
        int(data["Neighborhood_Rating"]), int(data["Condition"]), float(data["School_Rating"]),
        int(data["Has_Pool"]), int(data["Renovated"]), str(data["Location_Type"]),
        float(data["Distance_To_Center_KM"]), float(data["Days_On_Market"]), record_id
    ))
    conn.commit()
    conn.close()
    return jsonify({"message": "Record updated successfully!"})

@app.route("/delete/<int:record_id>", methods=["DELETE"])
def delete(record_id):
    conn = sqlite3.connect("housing.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM predictions WHERE id=?", (record_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Record deleted successfully!"})

if __name__ == "__main__":
    app.run(debug=True)