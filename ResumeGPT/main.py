from fastapi import FastAPI, File, UploadFile
import shutil
import os
import pandas as pd
from OCR_Reader import CVsReader
from ChatGPT_Pipeline import CVsInfoExtractor

app = FastAPI()

UPLOAD_FOLDER = "uploaded_CVs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.post("/upload_cvs/")
async def upload_cvs(files: list[UploadFile] = File(...)):
    saved_files = []
    
    for file in files:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        saved_files.append(file_path)
    
    return {"message": f"Uploaded {len(saved_files)} CVs successfully", "files": saved_files}


@app.get("/process_cvs/")
def process_cvs(openai_api_key: str):
    # Read uploaded CVs
    cvs_reader = CVsReader(cvs_directory_path=UPLOAD_FOLDER)
    cvs_content_df = cvs_reader.read_cv()

    # Extract CV information
    cvs_info_extractor = CVsInfoExtractor(cvs_df=cvs_content_df, openai_api_key=openai_api_key)
    extracted_results = cvs_info_extractor.extract_cv_info()

    return {"results": extracted_results}


# python main.py "../CVs" "AIzaSyDzbCa6zdR2Im-bhQadx1zF7KBigEZiew4"
