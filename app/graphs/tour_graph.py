from __future__ import annotations

from typing import Any, Dict, List, Optional, TypedDict

from langgraph.graph import StateGraph, END

from app.services.location_service import haversine_distance
from app.services.story_service import generate_story


# ---------- State ----------
class TourState(TypedDict, total=False):
    latitude: float
    longitude: float
    radius: int

    landmarks: List[Dict[str, Any]]

    # context agent outputs
    primary_place: Optional[Dict[str, Any]]
    candidate_places: List[Dict[str, Any]]  # top N

    # retrieval agent outputs
    enriched: Dict[str, Any]  # distances + recommendations

    # narration agent outputs
    narration_draft: str
    narration_final: str

    # safety agent outputs
    needs_rewrite: bool
    rewrite_count: int


# ---------- Agent 1: Context Agent ----------
def context_agent(state: TourState) -> TourState:
    landmarks = state.get("landmarks") or []
    if not landmarks:
        state["primary_place"] = None
        state["candidate_places"] = []
        return state

    # Keep minimal, but more “agentic”: prefer named places, not "Unknown place"
    def score(lm: Dict[str, Any]) -> int:
        name = (lm.get("name") or "").strip()
        t = (lm.get("type") or "").strip()
        s = 0
        if name and name.lower() != "unknown place":
            s += 10
        if t:
            s += 2
        return s

    ranked = sorted(landmarks, key=score, reverse=True)

    # choose primary + keep next 2 as candidates (for recommendations later)
    candidates = ranked[:3]
    state["primary_place"] = candidates[0] if candidates else None
    state["candidate_places"] = candidates
    return state


# ---------- Agent 2: Retrieval / Enrichment Agent ----------
def retrieval_agent(state: TourState) -> TourState:
    lat = state["latitude"]
    lon = state["longitude"]

    candidates = state.get("candidate_places") or []
    enriched: Dict[str, Any] = {"recommendations": []}

    # compute distances for candidates (including primary)
    for lm in candidates:
        lm_lat = lm.get("lat")
        lm_lon = lm.get("lon")
        if lm_lat is None or lm_lon is None:
            dist = None
        else:
            dist = haversine_distance(lat, lon, lm_lat, lm_lon)
        enriched["recommendations"].append(
            {
                "name": lm.get("name", "Unknown place"),
                "type": lm.get("type"),
                "distance_m": dist,
            }
        )

    # Ensure we recommend “2–3 places”: include primary + two nearby if available
    state["enriched"] = enriched
    return state


# ---------- Agent 3: Narration Agent ----------
def narration_agent(state: TourState) -> TourState:
    primary = state.get("primary_place")

    # fallback narration if nothing found
    if not primary:
        draft = "You are driving through a beautiful area. There are no major landmarks nearby."
        state["narration_draft"] = draft
        state["narration_final"] = draft
        return state

    place_name = primary.get("name", "Unknown place")
    place_type = primary.get("type") or "place"

    # Build a small “discussion/recommendation” section from 2nd/3rd candidates
    recs = state.get("enriched", {}).get("recommendations", [])
    # recs[0] is usually the primary; recommend the next 2 if available
    nearby_recs = []
    for r in recs[1:3]:
        nm = r.get("name")
        tp = r.get("type") or "place"
        if nm and nm.lower() != "unknown place":
            nearby_recs.append(f"{nm} ({tp})")

    # Minimal change: pass optional “nearby suggestions” to the prompt
    draft = generate_story(
        place_name=place_name,
        place_type=place_type,
        country="Namibia",
        nearby_suggestions=nearby_recs,
    )

    state["narration_draft"] = draft
    # set default final (safety agent may change it)
    state["narration_final"] = draft
    return state


# ---------- Agent 4: Safety & Quality Agent ----------
def safety_quality_agent(state: TourState) -> TourState:
    text = (state.get("narration_draft") or "").strip()
    rewrite_count = int(state.get("rewrite_count") or 0)

    # Not too strict: only catch obvious issues for the demo
    issues = []

    # Too long for spoken demo (keep it short-ish)
    if len(text.split()) > 90:
        issues.append("too_long")

    # Avoid leaking exact coordinates (we don’t even include them, but just in case)
    if "latitude" in text.lower() or "longitude" in text.lower():
        issues.append("coords")

    # Very basic PII heuristic (overkill, but safe)
    if "@" in text:
        issues.append("email_like")

    needs_rewrite = len(issues) > 0 and rewrite_count < 1  # only 1 rewrite max

    state["needs_rewrite"] = needs_rewrite
    state["rewrite_count"] = rewrite_count

    # If needs rewrite, ask narration agent again with tighter constraints by setting a hint
    # (We keep it minimal: just append an instruction and re-run narration node once)
    if needs_rewrite:
        # Store a small hint the narration agent can react to via nearby_suggestions logic
        # We'll implement the hint inside generate_story prompt in story_service.
        state["rewrite_count"] = rewrite_count + 1

    return state


# ---------- Conditional routing ----------
def after_safety_router(state: TourState) -> str:
    # If safety says rewrite, go back to narration agent once.
    return "narration" if state.get("needs_rewrite") else "end"


# ---------- Build graph ----------
def build_tour_graph():
    g = StateGraph(TourState)

    g.add_node("context", context_agent)
    g.add_node("retrieval", retrieval_agent)
    g.add_node("narration", narration_agent)
    g.add_node("safety", safety_quality_agent)

    g.set_entry_point("context")
    g.add_edge("context", "retrieval")
    g.add_edge("retrieval", "narration")
    g.add_edge("narration", "safety")

    g.add_conditional_edges(
        "safety",
        after_safety_router,
        {
            "narration": "narration",
            "end": END,
        },
    )

    return g.compile()


# Create a single compiled graph instance to reuse
TOUR_GRAPH = build_tour_graph()