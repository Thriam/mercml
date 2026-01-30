import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

st.title("Spotify Cluster Explorer")

# Input form for prediction
st.subheader("Predict Cluster")
danceability = st.slider("Danceability", 0.0, 1.0, 0.5)
energy = st.slider("Energy", 0.0, 1.0, 0.5)
valence = st.slider("Valence", 0.0, 1.0, 0.5)
tempo = st.number_input("Tempo", 50, 250, 120)
duration_ms = st.number_input("Duration (ms)", 100000, 600000, 200000)
popularity = st.slider("Popularity", 0, 100, 50)

if st.button("Predict"):
    payload = {
        "danceability": danceability,
        "energy": energy,
        "valence": valence,
        "tempo": tempo,
        "duration_ms": duration_ms,
        "popularity": popularity
    }
    response = requests.post("http://127.0.0.1:5000/predict", json=payload)
    if response.status_code == 200:
        result = response.json()
        st.write("Predicted Cluster:", result.get("predicted_cluster"))
        st.write("Tracks in this cluster:")
        st.table(pd.DataFrame(result.get("tracks", [])))
    else:
        st.error(f"Error: {response.text}")

# Update entry
st.subheader("Update Track")
track_id = st.number_input("Track ID", min_value=1)
new_name = st.text_input("New Track Name")
new_artist = st.text_input("New Artist Name")
new_cluster = st.number_input("New Cluster", min_value=0, max_value=4)

if st.button("Update Track"):
    payload = {"track_name": new_name, "artist_name": new_artist, "cluster": new_cluster}
    response = requests.put(f"http://127.0.0.1:5000/update/{track_id}", json=payload)
    st.write(response.json())

# Analysis chart
st.subheader("Cluster Analysis")
response = requests.get("http://127.0.0.1:5000/analysis")

if response.status_code == 200:
    try:
        data = pd.DataFrame(response.json())
        fig, ax = plt.subplots()
        ax.bar(data["cluster"], data["count"])
        ax.set_xlabel("Cluster")
        ax.set_ylabel("Number of Tracks")
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Failed to parse JSON: {e}")
        st.text(response.text)
else:
    st.error(f"Request failed: {response.status_code}")
