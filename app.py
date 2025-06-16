from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from typing import List
import requests, os

from processor import process_instagram_data

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (optional on localhost)
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the frontend directory
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

@app.get("/")
async def serve_frontend():
    return FileResponse("frontend/index.html")

@app.post("/process/")
async def process_links(links: List[str] = Form(...)):
    result = [link.strip() for link in links]
    await process_instagram_data(result)

    cloud_function_url = "https://asia-south1-closer-influencer.cloudfunctions.net/getEmailsFromInstagram"

    try:
        response = requests.post(cloud_function_url, json={"links": result})
        if response.status_code == 200:
            cloud_output = response.json()

            # Save CSV if available
            if "csv_content" in cloud_output:
                os.makedirs("csv_outputs", exist_ok=True)
                file_path = os.path.join("csv_outputs", "latest.csv")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(cloud_output["csv_content"])
                cloud_output["csv_path"] = "/download/latest.csv"
        else:
            cloud_output = {"error": f"Status: {response.status_code}", "raw": response.text}

    except Exception as e:
        cloud_output = {"error": str(e)}

    return JSONResponse({
        "status": "success",
        "data": result,
        "cloud_response": cloud_output
    })

@app.get("/download/latest.csv")
async def download_csv():
    path = "csv_outputs/latest.csv"
    if os.path.exists(path):
        return FileResponse(path, media_type="text/csv", filename="instagram_data.csv")
    return JSONResponse(status_code=404, content={"error": "CSV not found"})
