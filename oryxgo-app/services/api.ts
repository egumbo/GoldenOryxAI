const API_BASE_URL = 'http://192.168.1.157:8000';

export async function getNearbyTour(latitude: number, longitude: number) {
  const res = await fetch(`${API_BASE_URL}/tour/nearby`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ latitude, longitude, radius: 1000 }),
  });

  if (!res.ok) {
    throw new Error('Failed to fetch tour');
  }

  return res.json();
}
