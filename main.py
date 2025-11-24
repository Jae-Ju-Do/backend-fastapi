import logging
import os
import shutil
from pathlib import Path

import boto3
import requests
from botocore.exceptions import ClientError
from dotenv import load_dotenv
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware

# 기존 모듈 임포트 (경로에 맞게 수정 필요)
from Code_Integration.Ghidra.ghidra_analysis import ghidra_analysis
from Code_Integration.change_sha256.change_sha256 import change_sha256
from Code_Integration.llm.llm import llm
from Code_Integration.pdf.pdf import pdf
from Code_Integration.vir_check import vir_check

load_dotenv()

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # 또는 ["*"] (모두 허용)
    allow_credentials=True,
    allow_methods=["*"],         # GET, POST, OPTIONS 등 모두 허용
    allow_headers=["*"],         # 모든 헤더 허용
    expose_headers=["*"],
)

# 환경 변수 로드
load_dotenv()
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "ap-northeast-2")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
SPRING_BOOT_CALLBACK_URL = os.getenv("SPRING_BOOT_URL", "http://localhost:8080") + "/api/analysis/callback"

# S3 클라이언트 초기화
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)


class WorkflowRequest(BaseModel):
    jobId: str
    s3FileKey: str


def download_from_s3(s3_key: str, local_path: str):
    """S3에서 파일 다운로드"""
    try:
        s3_client.download_file(S3_BUCKET_NAME, s3_key, local_path)
        logger.info(f"Downloaded {s3_key} to {local_path}")
        return True
    except ClientError as e:
        logger.error(f"S3 Download Error: {e}")
        return False


def upload_to_s3(local_path: str, s3_key: str):
    """S3로 파일 업로드"""
    try:
        s3_client.upload_file(local_path, S3_BUCKET_NAME, s3_key)
        logger.info(f"Uploaded {local_path} to {s3_key}")
        return True
    except ClientError as e:
        logger.error(f"S3 Upload Error: {e}")
        return False


def send_callback(payload: dict):
    """Spring Boot로 완료/실패 알림 전송"""
    try:
        response = requests.post(SPRING_BOOT_CALLBACK_URL, json=payload, timeout=10)
        response.raise_for_status()
        logger.info(f"Callback sent successfully for job {payload.get('jobId')}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Callback failed for job {payload.get('jobId')}: {e}")


def process_workflow(job_id: str, s3_file_key: str):
    """전체 분석 워크플로우 실행 (백그라운드 작업)"""
    # 작업별 임시 디렉토리 생성
    work_dir = Path(f"/tmp/analysis_{job_id}")
    work_dir.mkdir(parents=True, exist_ok=True)

    try:
        logger.info(f"Starting workflow for job {job_id}")

        # 1. S3에서 EXE 다운로드
        local_exe_path = work_dir / Path(s3_file_key).name
        if not download_from_s3(s3_file_key, str(local_exe_path)):
            raise Exception("Failed to download EXE from S3")

        # 2. SHA256 변환 (기존 함수 활용)
        # 주의: 기존 함수들이 내부적으로 절대경로를 쓰는지 확인하고, work_dir 기반으로 수정 필요할 수 있음
        sha256_res = change_sha256(str(local_exe_path))
        if sha256_res["status_code"] != 200:
            raise Exception(f"SHA256 Error: {sha256_res['content']}")
        target_path = sha256_res["content"]  # 변환된 파일 경로

        # 3. 바이러스 체크 (선택사항, 생략 가능)
        vir_check_res = vir_check(str(work_dir), Path(target_path).name)
        if vir_check_res["status_code"] != 200:
            # 바이러스 체크 실패를 에러로 처리할지, 경고만 남기고 진행할지 결정 필요
            logger.warning(f"Virus check failed: {vir_check_res['content']}")
            # raise Exception(...) # 필요시 에러 발생

        # 4. Ghidra 디컴파일
        ghidra_res = ghidra_analysis(target_path, str(work_dir))
        if ghidra_res["status_code"] != 200:
            raise Exception(f"Ghidra Error: {ghidra_res['content']}")
        c_code_path = ghidra_res["content"]

        # 5. LLM 분석
        llm_res = llm(c_code_path, 1, Path(target_path).stem)  # level=1(Intermediate) 가정
        if llm_res["status_code"] != 200:
            raise Exception(f"LLM Error: {llm_res['content']}")
        analysis_json = llm_res["content"]

        # 6. PDF 생성
        pdf_res = pdf(analysis_json, Path(target_path).name, output_dir=str(work_dir))
        if pdf_res["status_code"] != 200:
            raise Exception(f"PDF Error: {pdf_res['content']}")
        local_pdf_path = pdf_res["content"]

        # 7. 결과 PDF S3 업로드
        s3_pdf_key = f"pdf/{job_id}/{Path(local_pdf_path).name}"
        if not upload_to_s3(local_pdf_path, s3_pdf_key):
            raise Exception("Failed to upload PDF to S3")

        # 8. 성공 콜백
        send_callback({
            "jobId": job_id,
            "s3PdfKey": s3_pdf_key,
            "success": True,
            "errorMessage": None
        })

    except Exception as e:
        logger.exception(f"Workflow failed for job {job_id}")
        # 실패 콜백
        send_callback({
            "jobId": job_id,
            "s3PdfKey": None,
            "success": False,
            "errorMessage": str(e)
        })

    finally:
        # 9. 임시 디렉토리 정리
        if work_dir.exists():
            shutil.rmtree(work_dir, ignore_errors=True)
            logger.info(f"Cleaned up work directory {work_dir}")


@app.post("/api/v1/workflow/start")
async def start_workflow_endpoint(request: WorkflowRequest, background_tasks: BackgroundTasks):
    """Spring Boot로부터 분석 요청 수신"""
    # 백그라운드 작업으로 등록하고 즉시 응답
    background_tasks.add_task(process_workflow, request.jobId, request.s3FileKey)
    return {"status": "accepted", "jobId": request.jobId}