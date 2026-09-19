from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
import zipfile
import io
import os
import shutil
import tempfile

app = FastAPI()

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

PLATFORMS = {
    "linux": "linux",
    "mac": "mac",
    "win": "win",
}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "platforms": PLATFORMS})


@app.post("/package")
async def package_project(
    file: UploadFile = File(...),
    platform: str = Form(...)
):
    if platform not in PLATFORMS:
        return {"error": "Invalid platform"}

    template_dir = os.path.join(BASE_DIR, PLATFORMS[platform])

    # Create a temporary directory for working
    with tempfile.TemporaryDirectory() as temp_dir:
        # Extract uploaded zip
        extract_dir = os.path.join(temp_dir, "project")
        os.makedirs(extract_dir)

        zip_content = await file.read()
        with zipfile.ZipFile(io.BytesIO(zip_content), 'r') as zip_ref:
            zip_ref.extractall(extract_dir)

        # Check for runcode.py
        runcode_py_path = os.path.join(extract_dir, "runcode.py")
        if not os.path.exists(runcode_py_path):
            return {"error": "runcode.py not found in uploaded project"}

        # Copy template to output directory
        output_dir = os.path.join(temp_dir, "output")
        shutil.copytree(template_dir, output_dir, dirs_exist_ok=True)

        # Copy all project files to _internal directory
        for item in os.listdir(extract_dir):
            src = os.path.join(extract_dir, item)
            dst = os.path.join(output_dir, "_internal", item)
            if os.path.isdir(src):
                if os.path.exists(dst):
                    shutil.rmtree(dst)
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)

        # Create output zip
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(output_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, output_dir)
                    zipf.write(file_path, arcname)

        zip_buffer.seek(0)

        # Generate filename
        filename = f"project_{platform}.zip"

        return StreamingResponse(
            iter([zip_buffer.getvalue()]),
            media_type="application/zip",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
