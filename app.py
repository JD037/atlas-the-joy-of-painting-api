from flask import Flask, jsonify, request
from database import db, init_app
from models import Episode, Color
from etl import run_etl

app = Flask(__name__)
init_app(app)

@app.route('/api/episodes', methods=['GET'])
def get_episodes():
    # Retrieve query parameters
    month = request.args.get('month')
    subject_matter = request.args.get('subject_matter')
    colors = request.args.getlist('colors')
    filter_logic = request.args.get('filter_logic', default='AND')  # Default to 'AND'

    print(f"Month: {month}")
    print(f"Subject Matter: {subject_matter}")
    print(f"Colors: {colors}")
    print(f"Filter Logic: {filter_logic}")

    # Build the query based on the provided filters and filter logic
    query = Episode.query

    if month:
        if filter_logic == 'AND':
            query = query.filter(Episode.month == month)
        else:
            query = query.filter(Episode.month.in_(month.split(',')))

    if subject_matter:
        if filter_logic == 'AND':
            query = query.filter(Episode.subject_matter.contains(subject_matter))
        else:
            query = query.filter(Episode.subject_matter.in_(subject_matter.split(',')))

    if colors:
        if filter_logic == 'AND':
            query = query.join(Color).filter(Color.name.in_(colors))
        else:
            query = query.join(Color).filter(Color.name.in_(colors)).group_by(Episode.id)

    # Execute the query and retrieve the episodes
    episodes = query.all()

    # Serialize the episodes to JSON format
    episode_data = []
    for episode in episodes:
        episode_dict = {
            'id': episode.id,
            'title': episode.title,
            'month': episode.month,
            'subject_matter': episode.subject_matter,
            'colors': [color.name for color in episode.colors]
        }
        episode_data.append(episode_dict)

    return jsonify(episode_data)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        run_etl()
    app.run()