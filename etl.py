import pandas as pd
from models import Episode, Color
from database import db

def extract_data():
    # Extract data from "The Joy of Painting - Colors Used.csv"
    episodes_df = pd.read_csv('ColorsUsed.csv')
    
    # Extract data from "The Joy of Painting - Subject Matter.csv"
    colors_df = pd.read_csv('SubjectMatter.csv')
    
    # Extract data from "The Joy of Painting - Episode Dates.csv"
    guests_df = pd.read_csv('EpisodeDates.csv', on_bad_lines='skip')
    
    return episodes_df, colors_df, guests_df

def transform_data(episodes_df, colors_df, guests_df):
    # Perform data transformations and cleaning
    # Example: Rename columns, handle missing values, convert data types, etc.
    transformed_episodes = episodes_df.rename(columns={'EPISODE': 'title'})
    transformed_colors = colors_df.dropna()
    transformed_guests = guests_df.copy()
    
    return transformed_episodes, transformed_colors, transformed_guests

def load_data(episodes, colors, guests):
    # Load data into the database
    for _, episode_data in episodes.iterrows():
        episode = Episode(title=episode_data['painting_title'])
        db.session.add(episode)
        db.session.commit()  # Commit the episode to get the generated ID
        
        for _, color_data in colors[colors['EPISODE'] == episode_data['painting_title']].iterrows():
            color = Color(name=color_data['COLOR'], episode_id=episode.id)
            db.session.add(color)
    
    # Load guest data
    # ...
    
    db.session.commit()

def run_etl():
    episodes_df, colors_df, guests_df = extract_data()
    transformed_episodes, transformed_colors, transformed_guests = transform_data(episodes_df, colors_df, guests_df)
    load_data(transformed_episodes, transformed_colors, transformed_guests)
