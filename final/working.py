from dotenv import load_dotenv
import os
import traceback
import base64
import math
import random
import requests
from urllib.parse import urlencode
from database import get_db
from sqlalchemy.orm import Session
from models import User,Playlist
from dataaccess import store_spotify_user_data, store_user_playlists_data,store_tracks_for_playlist
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Response, Request, HTTPException, Depends
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from recommend import get_book_recommendations  # Add this import at the top

app = FastAPI() #instantiation of FastAPI
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="./templates") # To render the html template, instantiation

#dependency
db = get_db()

STATE_KEY = "spotify_auth_state"
CLIENT_ID =  "72daf50002ac4c54a83c6a59dda0e359"
CLIENT_SECRET = "b5807038ba4040b6a2591dbcf2c733ac"
URI = "http://127.0.0.1:8000"
REDIRECT_URI = "http://127.0.0.1:8000/callback"


def generate_random_string(string_length):
    possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    text = "".join(
        [
            possible[math.floor(random.random() * len(possible))]
            for i in range(string_length)
        ]
    )

    return text


@app.get("/login")
def read_root(response: Response):
    state = generate_random_string(20)

    scope = "user-read-private user-read-email user-read-recently-played user-top-read playlist-read-private playlist-read-collaborative"

    params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "scope": scope,
        "redirect_uri": REDIRECT_URI,
        "state": state,
    }
    response = RedirectResponse(
        url="https://accounts.spotify.com/authorize?" + urlencode(params)
    )
    response.set_cookie(key=STATE_KEY, value=state)
    return response


@app.get("/callback")
def callback(request: Request, response: Response, db:Session = Depends(get_db)):
    try:
        code = request.query_params.get("code")
        state = request.query_params.get("state")
        stored_state = request.cookies.get(STATE_KEY)

        if not state or state != stored_state:
            raise HTTPException(status_code=400, detail="State mismatch")

        response.delete_cookie(STATE_KEY)

        # Exchange code for access token
        token_url = "https://accounts.spotify.com/api/token"
        credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        headers = {"Authorization": f"Basic {encoded_credentials}"}
        
        form_data = {"code": code, "redirect_uri": REDIRECT_URI, "grant_type": "authorization_code"}
        token_response = requests.post(token_url, data=form_data, headers=headers)

        if token_response.status_code == 200:
            token_data = token_response.json()
            access_token = token_data["access_token"]
            print(token_data)
            #user data
            user_data = get_spotify_user_data(access_token)
            user = store_spotify_user_data(user_data, db)
            if not user:
                raise HTTPException(status_code=400, detail="User not found")
            
            user_playlists = get_user_playlists(access_token)
            store_user_playlists_data(user_playlists, db, user.id)

            all_playlists = db.query(Playlist).all()
            for x in all_playlists:
                spotify_playlist_id = x.playlist_id
                track_data=get_playlist_tracks(access_token,spotify_playlist_id)
                store_tracks_for_playlist(track_data,db,spotify_playlist_id)


            categories = get_categories(access_token)

            response = RedirectResponse(url="/recommend")
            response.set_cookie(key="accessToken", value=access_token)


        return response
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/", response_class=HTMLResponse)
def main(request: Request):

    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/refresh_token")
def refresh_token(request: Request):

    refresh_token = request.query_params["refresh_token"]
    request_string = CLIENT_ID + ":" + CLIENT_SECRET
    encoded_bytes = base64.b64encode(request_string.encode("utf-8"))
    encoded_string = str(encoded_bytes, "utf-8")
    header = {"Authorization": "Basic " + encoded_string}

    form_data = {"grant_type": "refresh_token", "refresh_token": refresh_token}

    url = "https://accounts.spotify.com/api/token"

    response = requests.post(url, data=form_data, headers=header)
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Error with refresh token")
    else:
        data = response.json()
        access_token = data["access_token"]

        return {"access_token": access_token}
    

@app.get("/blank", response_class=HTMLResponse)
def blank(request: Request):
    return templates.TemplateResponse("blank.html", {"request": request})

@app.get("/recommend", response_class=HTMLResponse)
def recommend(request: Request):
    recommendations = get_book_recommendations()
    return templates.TemplateResponse("blank.html", {"request": request, "recommendations": recommendations})

def get_spotify_user_data(access_token: str):
    """Fetches Spotify user profile data."""
    
    url = "https://api.spotify.com/v1/me"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        user_data = response.json()
        return {
            "name": user_data.get("display_name"),
            "email": user_data.get("email")
        }

    else:
        raise HTTPException(status_code=400, detail="Failed to fetch Spotify user data")
    
def get_user_playlists(access_token: str):
    url = "https://api.spotify.com/v1/me/playlists"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json() # List of playlists
    else:
        raise HTTPException(status_code=400, detail="Failed to fetch playlists from Spotify")

def get_playlist_tracks(access_token: str, playlist_id: str):

    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=400, detail="Failed to fetch playlist tracks")



def get_user_playlist(access_token: str,playlist_id:str):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=400, detail="Failed to fetch Spotify user playlist")



def get_categories(access_token: str):
    url = "https://api.spotify.com/v1/browse/categories"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers = headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=400, detail="Failed to fetch categories")

