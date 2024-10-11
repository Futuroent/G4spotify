# Spotify Recommender

This application is a song recommender using Spotify music data. The user is asked the title of a song, and the application suggest other songs to listen to based on shared characteristics.

## Features
- Input request from user for a song title.
- API connection to Spotify to obtain data about song features.
- Prediction model (Kmeans) to classify the song based on Spotify Data.
- Recommend another song from a model databased of song clusters.

## Tools used:
- Python: programming language used for writing the prediction model and functions.
- Libraies: Pandas, Pickle, sklearn.
- Streamlit: creation of the recommender application.
- Spotify: API connection and Spotipy library.