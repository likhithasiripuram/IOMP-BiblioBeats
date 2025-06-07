from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True

class PlaylistCreate(BaseModel):
    playlist_id: str
    playlist_name: str
    description: str
    snapshot_id: str
    user_id: int

class PlaylistResponse(BaseModel):
    playlist_id: str
    playlist_name: str
    description: str
    snapshot_id: str
    user_id: int

    class Config:
        orm_mode = True

class TrackCreate(BaseModel):
    track_id : str
    track_name : str
    album_name : str
    artist : str
    track_url : str
    playlist_id: str

class TrackResponse(BaseModel):
    track_id : str
    track_name : str
    album_name : str
    artist : str
    track_url : str
    playlist_id: str

    class Config:
        orm_mode = True

class ImagesCreate(BaseModel):
    playlist_id: str
    url: str
    height: int
    width: int
    
class ImagesResponse(BaseModel):
    playlist_id: str
    url: str
    height: int
    width: int

    class Config:
        orm_mode = True

class OwnerCreate(BaseModel):
    owner_id: str
    playlist_id: str
    url: str
    name: str

class OwnerResponse(BaseModel):
    owner_id: str
    playlist_id: str
    url: str
    name: str

    class Config:
        orm_mode = True