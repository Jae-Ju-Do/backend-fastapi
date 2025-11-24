import json as json_lib
from pathlib import Path
from .parser import parse_malware_report
from .renderer import generate_pdf_from_data


def pdf(json_data, filename, output_dir=None):
    try:
        print(f"json 타입 : {type(json_data)}")
        
        if isinstance(json_data, str):
            json_data = json_data.strip()
            if json_data.startswith("```"):
                json_data = "\n".join(
                    line for line in json_data.splitlines() if not line.strip().startswith("```")
                )
            json_data = json_lib.loads(json_data)

        # --- 경로 설정 수정 ---
        base_name = Path(filename).stem  # 확장자 제거 (.exe 등)
        pdf_name = f"{base_name}.pdf"
        output_path = Path(output_dir) / pdf_name

        report_data = parse_malware_report(json_data)
        result = generate_pdf_from_data(report_data["content"], str(output_path), filename)
        return {"status_code": 200, "content": result["content"]}
    except Exception as e:
        print(f"pdf 변환 실패 : {e}")
        return {"status_code": 400, "content": f"pdf 변환 실패 : {e}"}