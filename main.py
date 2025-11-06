import os
import pefile
import shutil

from fastapi import FastAPI, UploadFile, File, Body, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse

from Code_Integration.Ghidra.ghidra_analysis import ghidra_analysis
from Code_Integration.change_sha256.change_sha256 import change_sha256
from Code_Integration.llm.llm import llm
from Code_Integration.pdf.pdf import pdf
from Code_Integration.vir_check import vir_check

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # 또는 ["*"] (모두 허용)
    allow_credentials=True,
    allow_methods=["*"],         # GET, POST, OPTIONS 등 모두 허용
    allow_headers=["*"],         # 모든 헤더 허용
    expose_headers=["*"],
)

def sha256(file_path):
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file_path.file, buffer)
    change_sha256_result = change_sha256(file_path)
    return change_sha256_result


@app.post("/sha256")
def sha256(file: UploadFile = File(...)):
    original_name = file.filename
    orignal_path = f"./filedata/original/{original_name}"
    with open(orignal_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    change_sha256_result = change_sha256(orignal_path)

    if change_sha256_result["status_code"] != 200:
        return JSONResponse(
            status_code = 400,
            content = f"sha256 변환 오류 : {change_sha256_result['content']}"
        )
    return JSONResponse(
        status_code = 200,
        content = change_sha256_result["content"]
    )

@app.post("Code_Integration/Ghidra")
def ghidra_post(sha256_path: str = Body(...)):
    ghidra_result = ghidra_analysis(sha256_path)
    print(ghidra_result)
    if ghidra_result["status_code"] != 200:
        return JSONResponse(
            status_code = 400,
            content = f"ghidra 오류 : {ghidra_result['content']}"
        )
    return JSONResponse(
        status_code = 200,
        content = ghidra_result["content"]
    )

def is_pe_file(file_path: str) -> bool:
    try:
        pe = pefile.PE(file_path)
        return True
    except Exception as e:
        return False

@app.post("/virus_analysis")
def virs_analysis_post(sha256_path: str = Body(...)):
    dir, filename = os.path.split(sha256_path)
    vir_check_result = vir_check(dir, filename)

    if not is_pe_file(sha256_path):
        return JSONResponse(
            status_code=200,
            content = 2    
        )
    
    if vir_check_result["status_code"] != 200:
        return JSONResponse(
            status_code = 400,
            content = f"virus_analysis 오류 : {vir_check_result['content']}"
        )
    return JSONResponse(
        status_code = 200,
        content = vir_check_result["content"]
    )

@app.post("Code_Integration/llm")
def llm_post(c_path: str = Form(...), level: int = Form(...)):
    dir, filename = os.path.split(c_path)
    llm_result = llm(c_path, level, filename[:-2])
    if llm_result["status_code"] != 200:
        return JSONResponse(
            status_code = 400,
            content = f"llm 오류 : {llm_result['content']}"
        )
    return JSONResponse(
        status_code = 200,
        content = llm_result["content"]
    )

@app.post("Code_Integration/pdf")
def pdf_post(sha256_name: str = Form(...), json_data: str = Form(...)):
    dir, filename = os.path.split(sha256_name)
    print(filename)
    pdf_result = pdf(json_data, filename)
    if pdf_result["status_code"] != 200:
        print(f"pdf 오류 : {pdf_result['content']}")
        return JSONResponse(
            status_code = 400,
            content = f"pdf 오류 : {pdf_result['content']}"
        )
    return FileResponse(
        path=pdf_result["content"],
        filename=f"{filename}.pdf",
        media_type="application/pdf"
    )