# main.py
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
import os
import uuid
from caption import generate_caption
from stylizer import stylize_caption
import shutil

app = FastAPI()
UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/caption")
async def get_caption(
    image: UploadFile = File(...),
    style: str = Form("cool and Gen Z")
):
    # Save uploaded image
    temp_filename = f"temp_{uuid.uuid4().hex}.jpg"
    with open(temp_filename, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    try:
        base_caption = generate_caption(temp_filename)
        styled_captions = stylize_caption(base_caption, style)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
    finally:
        os.remove(temp_filename)

    return {
        "base_caption": base_caption,
        "styled_captions": styled_captions
    }
