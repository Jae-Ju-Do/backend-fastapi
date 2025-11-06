import subprocess
import pathlib, shutil
from fastapi.responses import JSONResponse

GHIDRA_HEADLESS = r"C:\Users\USER\Desktop\ghidra_11.3.1_PUBLIC\support\analyzeHeadless.bat"
GHIDRA_SCRIPT_PATH = r"./ghidra/decompile_script.py"
OUTPUT_DIR = r"./filedata/c_file"

def ghidra_analysis(file_path: str):
    """Ghidra를 실행해 디컴파일 및 디어셈블리 코드 추출"""
    project_name = pathlib.Path(file_path).stem
    project_path = pathlib.Path(OUTPUT_DIR) / f"{project_name}.rep"
    if not project_path.exists():
        print(f"Creating project directory: {project_path}")
        project_path.mkdir(parents=True)

    command = [
        str(GHIDRA_HEADLESS), str(project_path), project_name, 
        "-import", str(file_path),
        "-postScript", str(GHIDRA_SCRIPT_PATH),
        "-analysisMode", "deep",
        "-overwrite"
    ]
    
    try:
        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8'
        )

        for stdout_line in process.stdout:
            print(stdout_line, end="")  
        for stderr_line in process.stderr:
            print(stderr_line, end="") 

        process.wait()

        shutil.rmtree(project_path)
        
        if process.returncode != 0:
            return {"status_code": 400, "content": f"Ghidra 실행 실패: {process.returncode}"}
        
        return {"status_code": 200, "content": rf"./filedata/c_file/{project_name}.c"}

    except Exception as e:
        return {"status_code": 400, "content": f"Ghidra 실행 실패: {e}"}
