from flask import Flask, render_template, request
from recommender import recommend, movie
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def get_recommendations():
    movie_name = request.form['movie']
    recommendations = recommend(movie_name)

    return render_template(
        'index.html',
        recommendations=recommendations
    )
from flask import jsonify

@app.route('/suggest')
def suggest():
    query = request.args.get('q', '').lower()

    suggestions = movie[
        movie['title'].str.lower().str.contains(query, na=False)
    ]['title'].head(10).tolist()

    return jsonify(suggestions)

if __name__ == '__main__':
    app.run(debug=True)