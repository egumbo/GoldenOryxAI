import requests

OVERPASS_URL = "https://overpass-api.de/api/interpreter"

def get_nearby_landmarks(lat: float, lon: float, radius=1000):
    query = f"""
    [out:json];
    (
      node["tourism"](around:{radius},{lat},{lon});
      node["historic"](around:{radius},{lat},{lon});
      node["amenity"="place_of_worship"](around:{radius},{lat},{lon});
    );
    out body;
    """

    try:
        response = requests.post(OVERPASS_URL, data=query, timeout=60)

        # If Overpass returns an error page or rate-limit HTML, this prevents JSONDecodeError
        if response.status_code != 200:
            return []

        content_type = response.headers.get("Content-Type", "")
        if "application/json" not in content_type:
            return []

        data = response.json()

    except (requests.RequestException, ValueError):
        # Request failed or JSON decode failed → treat as "no landmarks"
        return []

    landmarks = []
    for el in data.get("elements", []):
        landmarks.append({
            "name": el.get("tags", {}).get("name", "Unknown place"),
            "type": el.get("tags", {}).get("tourism") or el.get("tags", {}).get("historic"),
            "lat": el.get("lat"),
            "lon": el.get("lon"),
        })

    return landmarks