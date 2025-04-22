from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def read_index():
    try:
        html_content = Path("source/index.html").read_text(encoding="utf-8")
        return HTMLResponse(content=html_content, media_type="text/html; charset=utf-8")
    except FileNotFoundError:
        return HTMLResponse(content="File not found.", status_code=404)


@app.get("/transition/", response_class=HTMLResponse)
async def read_transition_page():
    try:
        html_content = Path("source/transition_page.html").read_text(encoding="utf-8")
        return HTMLResponse(content=html_content, media_type="text/html; charset=utf-8")
    except FileNotFoundError:
        return HTMLResponse(content="File not found.", status_code=404)


if __name__ == "__main__":
    import uvicorn
    import sys

    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    uvicorn.run(app, host="127.0.0.1", port=port)
