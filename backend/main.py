from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from typing import List
import requests
import os

from processor import process_instagram_data

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static route for frontend
app.mount("/frontend", StaticFiles(directory="../frontend"), name="frontend")

@app.get("/")
async def serve_frontend():
    return FileResponse("../frontend/index.html")

@app.post("/process/")
async def process_links(links: List[str] = Form(...)):
    result = []
    for link in links:
        cleaned_link = link.strip()
        result.append(cleaned_link)
        print("📎 Link received:", cleaned_link)

    await process_instagram_data(result)

    cloud_function_url = "https://asia-south1-closer-influencer.cloudfunctions.net/getEmailsFromInstagram"

    try:
        response = requests.post(cloud_function_url, json={"links": result})

        if response.status_code == 200:
            cloud_output = response.json()

            # Save CSV to local file
            if "csv_content" in cloud_output:
                output_dir = "csv_outputs"
                os.makedirs(output_dir, exist_ok=True)
                filename = "latest.csv"
                file_path = os.path.join(output_dir, filename)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(cloud_output["csv_content"])
                cloud_output["csv_path"] = f"/download/{filename}"

        else:
            cloud_output = {"error": f"Failed with status {response.status_code}", "raw": response.text}

    except Exception as e:
        print("❌ Exception sending to Cloud Function:", str(e))
        cloud_output = {"error": str(e)}

    return JSONResponse(content={
        "status": "success",
        "data": result,
        "cloud_response": cloud_output
    })

@app.get("/download/latest.csv")
async def download_latest_csv():
    path = "csv_outputs/latest.csv"
    if os.path.exists(path):
        return FileResponse(path, media_type="text/csv", filename="instagram_data.csv")
    return JSONResponse(status_code=404, content={"error": "CSV not found"})
