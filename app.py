from flask import Flask, jsonify, request
from database import db, init_app
from models import Episode, Color
from etl import run_etl

app = Flask(__name__)
init_app(app)

@app.route('/episodes')
def get_episodes():
    # Retrieve episodes based on filters
    month = request.args.get('month')
    subject_matter = request.args.get('subject_matter')
    colors = request.args.getlist('colors')
    
    episodes = Episode.query
    
    if month:
        episodes = episodes.filter(Episode.month == month)
    if subject_matter:
        episodes = episodes.filter(Episode.subject_matter.ilike(f'%{subject_matter}%'))
    if colors:
        episodes = episodes.join(Color).filter(Color.name.in_(colors))
    
    episodes = episodes.all()
    
    results = []
    for episode in episodes:
        episode_data = {
            'id': episode.id,
            'title': episode.title,
            'month': episode.month,
            'subject_matter': episode.subject_matter,
            'colors': [color.name for color in episode.colors]
        }
        results.append(episode_data)
    
    return jsonify(results)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        run_etl()
    app.run()