from flask import Flask, request, jsonify
import sqlite3
import joblib
import numpy as np
import pandas as pd

app = Flask(__name__)

# Load model and scaler
kmeans = joblib.load("spotify_predictor.pkl")
scaler = joblib.load("scaler.pkl")

features = ["danceability", "energy", "valence", "tempo", "duration_ms", "popularity"]

def get_db_connection():
    conn = sqlite3.connect("spotify_clusters.db")
    conn.row_factory = sqlite3.Row
    return conn

# --- NEW: Initialize DB ---
def init_db(csv_file="spotify_tracks_with_metadata_10000.csv"):
    """Initialize the SQLite database with clustered tracks."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create table if not exists
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tracks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        track_name TEXT,
        artist_name TEXT,
        cluster INTEGER
    )
    """)

    # Load data
    df = pd.read_csv(csv_file)

    # Extract features and predict clusters
    X = df[features]
    X_scaled = scaler.transform(X)
    df["cluster"] = kmeans.predict(X_scaled)

    # Insert into DB
    for _, row in df.iterrows():
        cursor.execute(
            "INSERT INTO tracks (track_name, artist_name, cluster) VALUES (?, ?, ?)",
            (row["track_name"], row.get("artist_name", "Unknown"), int(row["cluster"]))
        )

    conn.commit()
    conn.close()
    print("Database initialized with clustered tracks.")

# --- Existing routes ---
@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    try:
        X = np.array([data[f] for f in features]).reshape(1, -1)
        X_scaled = scaler.transform(X)
        cluster = int(kmeans.predict(X_scaled)[0])

        conn = get_db_connection()
        rows = conn.execute("SELECT * FROM tracks WHERE cluster=?", (cluster,)).fetchall()
        conn.close()

        return jsonify({
            "predicted_cluster": cluster,
            "tracks": [dict(r) for r in rows]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/update/<int:track_id>", methods=["POST"])
def update(track_id):
    data = request.json
    conn = get_db_connection()
    conn.execute("UPDATE tracks SET track_name=?, artist_name=?, cluster=? WHERE id=?",
                 (data["track_name"], data["artist_name"], data["cluster"], track_id))
    conn.commit()
    conn.close()
    return jsonify({"status": "updated"})

@app.route("/analysis")
def analysis():
    conn = get_db_connection()
    rows = conn.execute("SELECT cluster, COUNT(*) as count FROM tracks GROUP BY cluster").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

if __name__ == "__main__":
    # Run init once before starting server
    init_db()
    app.run(debug=True)
