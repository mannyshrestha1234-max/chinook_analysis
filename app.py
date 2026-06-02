import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = f"postgresql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

engine = create_engine(DATABASE_URL)

query = """
SELECT
	t."name" ,
	t.album_id ,
	a.title AS album_title,
	a2."name" AS artist_name,
	g."name" AS genre_name,
	mt."name" AS media_name,
	t.bytes ,
	t.composer ,
	t.genre_id ,
	t.media_type_id ,
	t.milliseconds ,
	t.track_id ,
	t.unit_price
	
FROM track t 
JOIN album a 
	ON t.album_id = a.album_id 
JOIN artist a2 
	ON a2.artist_id = a.artist_id 
JOIN genre g 
	ON g.genre_id = t.genre_id 
JOIN media_type mt 
	ON mt.media_type_id = t.media_type_id"""

df = pd.read_sql_query(query, engine)

artist = st.selectbox('Select an artist', df['artist_name'].unique())
st.dataframe(df[df['artist_name'] == artist][['name', 'album_title', 'artist_name', 'genre_name']])

track_count_by_genre = df.groupby("artist_name").agg(num_tracks=("track_id", "count")).reset_index()

fig, ax = plt.subplots()
sns.barplot(x="num_tracks", y="artist_name", data=track_count_by_genre.sort_values("num_tracks", ascending=False).head(15), ax=ax)
st.title("Top 15 Artists by Number of Tracks")
st.pyplot(fig)

df['duration_minutes'] = df['milliseconds'] / 60000

fig1, ax1 = plt.subplots()
sns.histplot(df['duration_minutes'],bins=40, ax=ax1)
st.title("Distribution of Track Durations in minutes")
ax1.set_title('Distribution of Track Durations')	
st.pyplot(fig1)
