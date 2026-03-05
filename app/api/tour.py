from fastapi import APIRouter
from app.schemas.tour import TourRequest, TourResponse
from app.services.landmark_service import get_nearby_landmarks
from app.services.story_service import generate_story
from app.services.tts_service import text_to_speech_background

from app.graphs.tour_graph import TOUR_GRAPH
from app.debug_store import save_last_run
from app.debug_store import get_last_run
from fastapi import HTTPException

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
    return state