import streamlit as st
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pickle

st.image("spotify6.png", width=100) 
# Title of the app
st.title(":green[_Spotify_] Song Recommender")
st.subheader("_Music for Everyone_ :sunglasses:", divider=True)

# Spotify API Authentication
client_id = 'a6db8fab957a42bea4da6fc433c87a93'  
client_secret = '0b8e4df683934d28ac8e978ffdc7df40'  

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Load the pre-trained KMeans model
with open('spotify_kmeans_model.pkl', 'rb') as model_file:
    kmeans = pickle.load(model_file)

df_songs = pd.read_csv('df5k2.csv')

# Function to fetch song features from Spotify
def bring_song(song_name):
    result = sp.search(q=song_name, limit=1, market="ES")  # Search for the result
    if result["tracks"]["items"]:
        id = result["tracks"]["items"][0]["id"]  # Bring the ID
        return id
    else:
        return None

# Function to classify song into clusters
def classify_song(id):
    features = sp.audio_features(id)  # Fetch all features
    if features:
        X = pd.DataFrame(features)
        X = X[["danceability", "energy", "loudness", "speechiness", "acousticness",
               "instrumentalness", "liveness", "valence", "tempo", "duration_ms"]]  # Select required features
        cluster = kmeans.predict(X)  # Run prediction
        return cluster[0]  # Return the predicted cluster
    else:
        return None

# Function to recommend songs from the same cluster
def song_recommender(cluster):
    same_cluster_songs = df_songs.loc[df_songs['cluster'] == cluster]
    random_sample = same_cluster_songs.sample(n=4)  # Select 4 random songs
    return random_sample[['names', 'id']]  # Return song names and IDs

# Input form for song name
song_name = st.text_input("Enter the song name:", '')

if song_name:
    song_id = bring_song(song_name)
    
    if song_id:
        predicted_cluster = classify_song(song_id)
        
        if predicted_cluster is not None:
            st.write(f"Predicted cluster: {predicted_cluster}")

            # Recommend and show songs from the same cluster
            st.write("### Recommended Songs:")
            recommended_songs = song_recommender(predicted_cluster)

            # Display the recommended songs with embedded players in a single column
            for index, row in recommended_songs.iterrows():
                track_id = row['id']
                st.markdown(f"""
                    <div style="margin: 10px; display: flex; flex-direction: column; align-items: center;">
                        <iframe src="https://open.spotify.com/embed/track/{track_id}"
                                width="300" height="80" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>
                        <p style="text-align: center;">{row['names']}</p>
                    </div>
                """, unsafe_allow_html=True)

        else:
            st.write("Could not retrieve features for the song.")
    else:
        st.write("Song not found.")
