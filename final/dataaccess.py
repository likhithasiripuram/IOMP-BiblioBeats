from models import User,Playlist,Track
import schemas
import requests

def store_spotify_user_data(user_data,db):
    # store the user data into db using models.py
    email = user_data["email"]
    existing_user = db.query(User).filter(User.email == email).first()
    if not existing_user:
        new_user = User(name = user_data["name"],email=email)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    return existing_user
    
def store_user_playlists_data(user_playlists, db, user_id: int, access_token: str):
    for playlist in user_playlists.get("items", []):
        playlist_id = playlist["id"]
        # trying fetching tracks to verify accessibility
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Skipping inaccessible playlist: {playlist['name']} ({playlist_id})")
            continue 

        existing_playlist = db.query(Playlist).filter(Playlist.playlist_id == playlist_id).first()
        if not existing_playlist:
            new_playlist = Playlist(
                playlist_id=playlist_id,
                playlist_name=playlist["name"],
                description=playlist.get("description", ""),
                snapshot_id=playlist["snapshot_id"],
                user_id = user_id
            )
            db.add(new_playlist)
    db.commit()


def store_tracks_for_playlist(tracks_data, db, playlist_id: str):
    playlist = db.query(Playlist).filter(Playlist.playlist_id == playlist_id).first()
    if not playlist:
        return

    for item in tracks_data.get("items", []):
        track_info = item.get("track")
        if not track_info:
            continue

        track_id = track_info["id"]
        existing_track = db.query(Track).filter(Track.track_id == track_id).first()
        if not existing_track:
            new_track = Track(
                track_id=track_id,
                track_name=track_info["name"],
                album_name=track_info.get("album", {}).get("name", ""),
                artist=", ".join([
                a.get("name") for a in track_info.get("artists", []) if a.get("name")
                ]),
                track_url=track_info["external_urls"]["spotify"]
            )
            db.add(new_track)
            db.commit()
            track = new_track
        else:
            track = existing_track

        if track and track not in playlist.tracks:
            playlist.tracks.append(track)
            db.commit()

