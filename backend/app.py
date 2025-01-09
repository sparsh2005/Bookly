from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
from fuzzywuzzy import process
import requests

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# ---------------------------
# Load Saved Models
# ---------------------------
try:
    pt = pickle.load(open('pivot_table.pkl', 'rb'))
    similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))
    filtered_ratings = pickle.load(open('filtered_ratings.pkl', 'rb'))
    print("Models loaded successfully.")
except Exception as e:
    print(f"Error loading models: {e}")

# ---------------------------
# Helper Functions
# ---------------------------

def find_closest_match(book_name):
    """Find the closest matching title in the pivot table."""
    matches = process.extractOne(book_name, pt.index)
    return matches[0] if matches else None


def recommend(book_name):
    """Recommend books based on collaborative filtering."""
    closest_match = find_closest_match(book_name)
    if closest_match is None:
        return []  # Return an empty list instead of an error

    try:
        # Fetch index of the matched book
        index = np.where(pt.index == closest_match)[0][0]

        # Get similarity scores
        scores = list(enumerate(similarity_scores[index]))
        scores = sorted(scores, key=lambda x: x[1], reverse=True)[1:6]
        recommendations = [pt.index[i[0]] for i in scores]
        return recommendations
    except Exception as e:
        print(f"Error generating recommendations: {e}")
        return []

# ---------------------------
# Google Books API
# ---------------------------
def fetch_google_books(title):
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
        print(f"Error fetching Google Books data for {title}: {e}")
    return None

# ---------------------------
# Open Library API
# ---------------------------
def fetch_open_library(title):
    """Fetch book details from Open Library API."""
    try:
        query = title.replace(" ", "+")
        url = f"https://openlibrary.org/search.json?title={query}"
        response = requests.get(url)
        data = response.json()

        if 'docs' in data and len(data['docs']) > 0:
            book = data['docs'][0]
            return {
                'title': book.get('title', 'N/A'),
                'author': ', '.join(book.get('author_name', ['Unknown'])),
                'thumbnail': f"http://covers.openlibrary.org/b/id/{book['cover_i']}-M.jpg" if 'cover_i' in book else '',
                'description': 'No description available.'
            }
    except Exception as e:
        print(f"Error fetching Open Library data for {title}: {e}")
    return None

# ---------------------------
# Combined API
# ---------------------------
def fetch_combined_data(title):
    """Fetch book data from both APIs and merge."""
    # Try Google Books first
    book_details = fetch_google_books(title)

    # If Google Books fails, use Open Library
    if not book_details or not book_details['description']:
        fallback_details = fetch_open_library(title)
        if fallback_details:
            # Merge missing fields
            book_details = book_details or {}
            book_details['title'] = book_details.get('title', fallback_details['title'])
            book_details['author'] = book_details.get('author', fallback_details['author'])
            book_details['thumbnail'] = book_details.get('thumbnail', fallback_details['thumbnail'])
            book_details['description'] = book_details.get('description', fallback_details['description'])

    return book_details

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
    try:
        # Parse input data
        data = request.json
        book_name = data.get('book_name', '')

        # Validate input
        if not book_name:
            return jsonify({"error": "Book name is required!"}), 400

        # Generate Recommendations
        recommendations = recommend(book_name)

        # Deduplicate recommendations
        unique_recommendations = []
        seen_titles = set()
        for title in recommendations:
            normalized_title = title.strip().lower()
            if normalized_title not in seen_titles:
                seen_titles.add(normalized_title)
                unique_recommendations.append(title)

        # Fetch additional details for each unique recommendation
        results = []
        for original_title in unique_recommendations:
            details = fetch_combined_data(original_title)
            if details:
                normalized_details_title = details['title'].strip().lower()
                if normalized_details_title not in seen_titles:
                    seen_titles.add(normalized_details_title)
                    results.append(details)

        # Handle case where no results are found
        if not results:
            return jsonify({"error": "No book recommendations found."})

        return jsonify({'books': results})
    except Exception as e:
        print(f"Error processing request: {e}")
        return jsonify({"error": "Internal server error"}), 500


# ---------------------------
# Run Flask App
# ---------------------------
if __name__ == '__main__':
    app.run(debug=True)