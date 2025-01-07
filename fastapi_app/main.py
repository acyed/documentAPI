from fastapi import FastAPI
from fastapi.responses import FileResponse
import os

app = FastAPI()

UPLOAD_DIR = "./shared"  # Directory for uploaded files (shared volume)

def list_files_recursively(directory):
    """Recursively list all files and folders in a directory."""
    result = []
    for root, dirs, files in os.walk(directory):
        relative_root = os.path.relpath(root, directory)
        if relative_root == ".":
            relative_root = ""  # Adjust root for clean output
        # Add directories
        for d in dirs:
            result.append({"type": "folder", "name": d, "path": os.path.join(relative_root, d)})
        # Add files
        for f in files:
            result.append({"type": "file", "name": f, "path": os.path.join(relative_root, f)})
    return result

@app.get("/files")
def list_files():
    """List all files and folders in the upload directory recursively."""
    files_and_folders = list_files_recursively(UPLOAD_DIR)
    return {"items": files_and_folders}

@app.get("/files/{file_path:path}")
def get_file_or_folder(file_path: str):
    """Retrieve a specific file or list contents of a folder."""
    file_path_full = os.path.join(UPLOAD_DIR, file_path)

    if not os.path.exists(file_path_full):
        return {"error": "Path not found"}

    if os.path.isdir(file_path_full):
        # If the path is a folder, list its contents
        items = []
        for item in os.listdir(file_path_full):
            item_full_path = os.path.join(file_path_full, item)
            item_type = "folder" if os.path.isdir(item_full_path) else "file"
            items.append({"type": item_type, "name": item, "path": os.path.join(file_path, item)})
        return {"items": items}

    # If the path is a file, return the file
    return FileResponse(file_path_full)
