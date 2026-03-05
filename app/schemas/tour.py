from pydantic import BaseModel

class TourRequest(BaseModel):
    latitude: float
    longitude: float
    radius: int = 1000

class TourResponse(BaseModel):
    landmark: str
    narration: str
    audio_file: str
