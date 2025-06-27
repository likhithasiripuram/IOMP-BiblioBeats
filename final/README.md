# BiblioBeats

BiblioBeats is a web application that recommends books based on your Spotify playlists. It connects to your Spotify account, fetches your playlists and tracks, and uses AI to suggest books inspired by your music taste.

## Features

- **Spotify Login:** Authenticate securely with your Spotify account.
- **Playlist Selection:** View and select your Spotify playlists.
- **Book Recommendations:** Get AI-generated book recommendations based on the tracks in your selected playlist.
- **Modern UI:** Clean, responsive interface built with FastAPI and Jinja2 templates.

## Tech Stack

- **Backend:** FastAPI, SQLAlchemy, SQLite
- **Frontend:** Jinja2, HTML, CSS
- **AI Model:** [Ollama](https://ollama.com/) (Llama2)
- **Spotify API** for user data and playlists

## Setup Instructions

### 1. Clone the Repository

```sh
git clone https://github.com/yourusername/BiblioBeats.git
cd BiblioBeats/final
```

### 2. Create a Virtual Environment

```sh
python -m venv venv
venv\Scripts\activate   # On Windows
# or
source venv/bin/activate  # On Linux/Mac
```

### 3. Install Dependencies

```sh
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the `final` directory with the following content:

```
CLIENT_ID=your_spotify_client_id
CLIENT_SECRET=your_spotify_client_secret
REDIRECT_URI=http://127.0.0.1:8000/callback
```

Replace the values with your Spotify app credentials.

### 5. Run the Application

```sh
uvicorn working:app --reload
```

Visit [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

### 6. (Optional) Ollama Model

Make sure you have [Ollama](https://ollama.com/) installed and running with the `llama2` model:

```sh
ollama run llama2
```

## Project Structure

```
final/
│
├── static/                # CSS, images, etc.
├── templates/             # HTML templates
├── database.py            # Database setup
├── dataaccess.py          # Data access logic
├── models.py              # SQLAlchemy models
├── recommend.py           # AI recommendation logic
├── schemas.py             # Pydantic schemas
├── working.py             # Main FastAPI app
├── requirements.txt
└── README.md
```

## Usage

1. Go to the home page and click **Login**.
2. Authorize the app with your Spotify account.
3. Select a playlist from your Spotify account.
4. View book recommendations based on your playlist's tracks.

## License

This project is for educational purposes.

---

**Note:** You need valid Spotify API credentials and Ollama running locally for full functionality.