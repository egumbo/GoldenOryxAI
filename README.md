# AI Tourism Multi-Agent Demo

This project demonstrates a simple multi-agent AI system built using:

- FastAPI
- LangGraph
- Azure OpenAI
- Edge TTS
- OpenStreetMap Overpass API

The system simulates an AI tour guide that detects nearby landmarks and generates narration.

## Agents in the System

1. Context Agent – selects the main landmark
2. Retrieval Agent – enriches location information
3. Narration Agent – generates the story
4. Safety Agent – checks narration quality