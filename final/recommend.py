from sqlalchemy import create_engine, MetaData, Table, select, text
import ollama
from fastapi.responses import RedirectResponse
from models import Playlist

def get_book_recommendations(playlist_id, db):
    # fetching selected playlist
    playlist = db.query(Playlist).filter(Playlist.playlist_id == playlist_id).first()
    if not playlist or not playlist.tracks:
        return "No tracks found for this playlist.", None

    # track list for the prompt
    track_list = "\n".join(
        [f"{i+1}. {track.track_name} from album '{track.album_name}'" for i, track in enumerate(playlist.tracks)]
    )

    prompt = f"""Here are the music tracks and their album names from the selected playlist:

{track_list}

Suggest 5 book recommendations on the basis of these tracks."""

    response = ollama.chat(
        model="llama2",
        messages=[{"role": "user", "content": prompt}]
    )

    return response['message']['content'], playlist.playlist_name
