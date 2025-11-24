import pathlib
import shutil
import subprocess
import os

GHIDRA_HEADLESS = "/home/work/ISP_LAB/moon/hcy/backend-fastapi/ghidra_11.3.1_PUBLIC/support/analyzeHeadless"
GHIDRA_SCRIPT_PATH = r"./ghidra/decompile_script.py"

def ghidra_analysis(file_path: str, output_dir: str):
    """Ghidra를 실행해 디컴파일 및 디어셈블리 코드 추출"""

    file_path_obj = pathlib.Path(file_path)
    output_dir_obj = pathlib.Path(output_dir)
    project_name = pathlib.Path(file_path).stem

    # Ghidra 프로젝트(.rep)와 C파일 경로를 임시 디렉토리 기준으로 설정
    project_path = output_dir_obj / f"{project_name}.rep"
    c_output_path = output_dir_obj / f"{project_name}.c"
    if not project_path.exists():
        print(f"Creating project directory: {project_path}")
        project_path.mkdir(parents=True)

    command = [
        str(GHIDRA_HEADLESS), str(project_path), project_name, 
        "-import", str(file_path_obj),
        "-postScript", str(GHIDRA_SCRIPT_PATH),
        "-analysisMode", "deep",
        "-overwrite"
    ]

    # --- 환경 변수 설정 (가장 중요) ---
    # 현재 환경 변수를 복사한 뒤, C_OUTPUT_PATH를 추가하여 subprocess에 전달
    env = os.environ.copy()
    env['C_OUTPUT_PATH'] = str(c_output_path)
    
    try:
        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', env=env
        )

        for stdout_line in process.stdout:
            print(stdout_line, end="")  
        for stderr_line in process.stderr:
            print(stderr_line, end="") 

        process.wait()

        # Ghidra 임시 프로젝트 파일(.rep) 삭제
        if project_path.exists():
            shutil.rmtree(project_path)

        shutil.rmtree(project_path)
        
        if process.returncode != 0:
            return {"status_code": 400, "content": f"Ghidra 실행 실패: {process.returncode}"}

        # 8. C파일이 실제로 생성되었는지 확인
        if not c_output_path.exists():
            return {"status_code": 400, "content": "Ghidra 스크립트 실행은 성공했으나 C파일이 생성되지 않음"}

        return {"status_code": 200, "content": str(c_output_path)}

    except Exception as e:
        return {"status_code": 400, "content": f"Ghidra 실행 실패: {e}"}
