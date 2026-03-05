# scripts/render_tour_graph.py
import sys
from pathlib import Path

# Add project root to PYTHONPATH dynamically
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from app.graphs.tour_graph import TOUR_GRAPH


if __name__ == "__main__":
    compiled = TOUR_GRAPH
    drawable = compiled.get_graph()

    # Save Mermaid file
    mermaid = drawable.draw_mermaid()
    (ROOT_DIR / "tour_pipeline_graph.mmd").write_text(mermaid, encoding="utf-8")
    print("Mermaid diagram saved as tour_pipeline_graph.mmd")

    # Save PNG
    img_bytes = drawable.draw_mermaid_png()
    (ROOT_DIR / "tour_pipeline_graph.png").write_bytes(img_bytes)
    print("Graph PNG saved as tour_pipeline_graph.png")