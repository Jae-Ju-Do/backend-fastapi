import os
from static_analysis import static_analysis 
from virustotal.virustotal import virstotal

def vir_check(dir, file_name):
    """# 0:정상 1:악성 2:not pe"""
    file_path = os.path.join(dir, file_name)
    try:
        if virstotal(os.path.splitext(file_name)[0]) == 2:
            return {"status_code": 200, "content": 2}
        elif virstotal(os.path.splitext(file_name)[0]) == 0:
            if static_analysis(dir, file_name) == 1:
                return {"status_code": 200, "content": 1}
            else:
                return {"status_code": 200, "content": 0}
        return {"status_code": 200, "content": 1}
    except Exception as e:
        return {"status_code": 400, "content": f"vir_check 오류 : {e}"}
