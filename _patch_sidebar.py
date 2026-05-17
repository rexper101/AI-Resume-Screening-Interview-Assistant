from pathlib import Path

p = Path(__file__).parent / "app.py"
text = p.read_text(encoding="utf-8")
start = text.index("def render_sidebar():")
end = text.index("\n\n# ── Helper: Run Analysis")

TAG = "div"
o, c = f"<{TAG}", f"</{TAG}>"
