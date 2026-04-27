from fastapi import APIRouter
from app.schemas.tour import TourRequest, TourResponse
from app.services.landmark_service import get_nearby_landmarks
from app.services.story_service import generate_story
from app.services.tts_service import text_to_speech_background

from app.graphs.tour_graph import TOUR_GRAPH
from app.debug_store import save_last_run
from app.debug_store import get_last_run
from fastapi import HTTPException
""" 
router = APIRouter(prefix="/tour", tags=["Tour"])

@router.post("/nearby", response_model=TourResponse)
async def tour_nearby(payload: TourRequest):
    landmarks = get_nearby_landmarks(
        payload.latitude,
        payload.longitude,
        payload.radius
    )

    # Run LangGraph pipeline
    state_in = {
        "latitude": payload.latitude,
        "longitude": payload.longitude,
        "radius": payload.radius,
        "landmarks": landmarks,
        "rewrite_count": 0,
    }

    state_out = TOUR_GRAPH.invoke(state_in)
    save_last_run(state_out)

    primary = state_out.get("primary_place")
    narration = state_out.get("narration_final") or "You are driving through a beautiful area. There are no major landmarks nearby."

    audio = await text_to_speech_background(narration)

    if not primary:
        return TourResponse(
            landmark="None",
            narration=narration,
            audio_file=audio
        )

    return TourResponse(
        landmark=primary.get("name", "Unknown place"),
        narration=narration,
        audio_file=audio
    )

@router.get("/last-run")
def last_run():
    state = get_last_run()
    if not state:
        raise HTTPException(status_code=404, detail="No LangGraph run recorded yet.")
    return state """


#below i am mocking whil i sort out the app part 

from fastapi import APIRouter
from app.schemas.tour import TourRequest, TourResponse

router = APIRouter(prefix="/tour", tags=["Tour"])


MOCK_LANDMARKS = [
    {
        "name": "Christuskirche",
        "lat": -22.5609,
        "lon": 17.0658,
        "narration": "On your right is Christuskirche, one of Windhoek’s most iconic landmarks. Its sandstone walls and Gothic Revival style tell a story of Namibia’s colonial past and the city’s evolving identity.",
        "audio_file": "audio/mock-christuskirche.mp3",
    },
    {
        "name": "Independence Memorial Museum",
        "lat": -22.5614,
        "lon": 17.0667,
        "narration": "Nearby is the Independence Memorial Museum, a striking modern building dedicated to Namibia’s liberation struggle and national identity.",
        "audio_file": "audio/mock-independence-museum.mp3",
    },
    {
        "name": "Swakopmund Jetty",
        "lat": -22.6795,
        "lon": 14.5270,
        "narration": "You are near the Swakopmund Jetty, where the Atlantic Ocean meets Namibia’s coastal history. This is one of the town’s most recognizable seaside landmarks.",
        "audio_file": "audio/mock-swakopmund-jetty.mp3",
    },
    {
        "name": "Dune 45",
        "lat": -24.7293,
        "lon": 15.3028,
        "narration": "Ahead is Dune 45, one of the most photographed dunes in the Namib Desert. Its red sand glows beautifully at sunrise and sunset.",
        "audio_file": "audio/mock-dune-45.mp3",
    },
]


def find_mock_landmark(latitude: float, longitude: float):
    # Simple mock matching: close enough to known test coordinates
    for landmark in MOCK_LANDMARKS:
        if abs(latitude - landmark["lat"]) < 0.01 and abs(longitude - landmark["lon"]) < 0.01:
            return landmark

    return None


@router.post("/nearby", response_model=TourResponse)
async def tour_nearby(payload: TourRequest):
    landmark = find_mock_landmark(payload.latitude, payload.longitude)

    if not landmark:
        return TourResponse(
            landmark="None",
            narration="You are driving through a beautiful area. There are no major landmarks nearby, but OryxGo is still listening for points of interest along your route.",
            audio_file="audio/mock-default.mp3",
        )

    return TourResponse(
        landmark=landmark["name"],
        narration=landmark["narration"],
        audio_file=landmark["audio_file"],
    )


@router.get("/last-run")
def last_run():
    return {
        "mock": True,
        "message": "Mock mode is active. LangGraph and live landmark lookup are currently bypassed.",
    }