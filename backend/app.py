from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
from fuzzywuzzy import process
import requests

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Load saved models
pt = pickle.load(open('pivot_table.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))
filtered_ratings = pickle.load(open('filtered_ratings.pkl', 'rb'))

# ---------------------------
# Helper Function for Recommendations
# ---------------------------

def find_closest_match(book_name):
    """Find the closest matching title in the pivot table."""
    matches = process.extractOne(book_name, pt.index)
    return matches[0] if matches else None


def recommend(book_name):
    """Recommend books based on collaborative filtering."""
    closest_match = find_closest_match(book_name)
    if closest_match is None:
        return ["Book not found in dataset."]

    # Fetch index of the matched book
    index = np.where(pt.index == closest_match)[0][0]

    # Get similarity scores
    scores = list(enumerate(similarity_scores[index]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)[1:6]
    recommendations = [pt.index[i[0]] for i in scores]

    return recommendations


def fetch_book_details(title):
    """Fetch book details from Google Books API."""
    try:
        url = f"https://www.googleapis.com/books/v1/volumes?q={title}"
        response = requests.get(url)
        data = response.json()

        if 'items' in data:
            book = data['items'][0]['volumeInfo']
            return {
                'title': book.get('title', 'N/A'),
                'author': ', '.join(book.get('authors', ['Unknown'])),
                'thumbnail': book['imageLinks']['thumbnail'] if 'imageLinks' in book else '',
                'description': book.get('description', 'No description available.')
            }
    except Exception as e:
        print(f"Error fetching details for {title}: {e}")
    return None

# ---------------------------
# Flask Routes
# ---------------------------

@app.route('/')
def home():
    """Render homepage."""
    return render_template('index.html')


@app.route('/recommend', methods=['POST'])
def recommend_books():
    """Handle recommendation requests."""
    data = request.json
    book_name = data.get('book_name', '')

    # Validate input
    if not book_name:
        return jsonify({"error": "Book name is required!"}), 400

    # Generate Recommendations
    recommendations = recommend(book_name)

    # Fetch additional details for each recommendation
    results = []
    for title in recommendations:
        details = fetch_book_details(title)
        if details:
            results.append(details)

    # Handle case where no results are found
    if not results:
        return jsonify({"error": "No book recommendations found."})

    return jsonify({'books': results})


# ---------------------------
# Run Flask App
# ---------------------------
if __name__ == '__main__':
    app.run(debug=True)