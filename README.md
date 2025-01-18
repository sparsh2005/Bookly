# 📚 Bookly - Your Personal Literary Guide

Welcome to **Bookly**, your go-to book recommendation system designed to simplify and enhance your literary journey. With Bookly, discovering your next favorite book is as easy as typing a title you loved. Dive in and let Bookly curate the perfect reading list for you!

---

## 🚀 Features

1. **Intuitive User Interface**: 
   - A clean and modern UI designed for seamless navigation.
   - Light/Dark mode toggle for user comfort. (Dark mode coming soon)

2. **Book Recommendations**:
   - Input the title of a book, and Bookly will suggest recommendations based on it.
   - Recommendations are displayed in visually appealing cards, with:
     - Book cover image
     - Title
     - Author(s)

3. **Interactive Experience**:
   - User input appears as green chat bubbles.
   - Recommendations are grouped into rows and separate cards for clarity.
   - Cards expand to show book descriptions with a 3D popup effect. (coming soon)

4. **Hybrid Recommendation System**:
   - Uses **Google Books API**, **Open Library API**, and other sources for highly accurate and diverse suggestions.
   - Filters out duplicate recommendations for a cleaner experience.

---

## 🔧 How It Works

### Recommendation Modal:
1. **User Input**: Enter the title of a book you loved in the text box at the bottom of the page.
2. **API Integration**: 
   - Bookly fetches data from multiple APIs to provide diverse recommendations.
3. **Display**: 
   - Recommendations are shown in rows of cards, with each card containing:
     - Cover Image
     - Title
     - Author
     - On click: Expandable card with a detailed description. (coming soon)

---

## 📸 Screenshots

### 1. Homepage
<img width="1400" alt="image" src="https://github.com/user-attachments/assets/78ab4464-a587-4790-bf42-214979b65dfb" />


### 2. User Input & Recommendations
<img width="936" alt="image" src="https://github.com/user-attachments/assets/c7b17842-938c-478b-8633-1c2e885dafbd" />
<img width="660" alt="image" src="https://github.com/user-attachments/assets/3dda8e03-ce92-47c5-a29f-201a9cd4a5b2" />

---

## 🛠 Upcoming Features

1. **Expanded Cards with more details**:
   - Bigger cards of each book will appear when recommendation card is clicked. This will contain more information about the book.

2. **Search by Genre/Author**:
   - Allow users to filter recommendations by genre or author names.

3. **Download/Buy Links**:
   - Add links for downloading or purchasing the recommended books.

4. **Dark Mode**:
   - User preference for dark mode.

5. **Additional APIs**:
   - Integration with Goodreads API for enhanced recommendations.

---

## 🌟 Getting Started

To run this project locally:
1. Clone the repository:
   ```bash
   git clone https://github.com/<username>/Bookly.git

2. Install requirements:
   ```bash
    pip install -r requirements.txt

4. Run the app.
   Navigate to the backend
   ```bash
   python app.py
