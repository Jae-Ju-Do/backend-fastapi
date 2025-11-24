import os

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("VIRUSTOTOAL_API_KEY")

def check_file_reputation(hash_name):
    """주어진 SHA256 해시 값에 대한 VirusTotal 보고서를 조회"""
    url = f"https://www.virustotal.com/api/v3/files/{hash_name}"
    headers = {"x-apikey": API_KEY}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # HTTP 오류 발생 시 예외를 발생시킴.

        report = response.json()
        analysis_results = report["data"]["attributes"].get("last_analysis_stats", {})
        malicious = analysis_results.get("malicious", 0)
        suspicious = analysis_results.get("suspicious", 0)
        harmless = analysis_results.get("harmless", 0)
        undetected = analysis_results.get("undetected", 0)
                
        total = sum(analysis_results.values())

        check_percent_mal = 1
        if total > 0:
            if (malicious / total) * 100 >= check_percent_mal:
                return 1 # 악성    
            return 0 # 정상
        return 2 # 오류
    except requests.exceptions.RequestException as e:
        print(f"API 요청 실패: {e}")
        return 2 # 오류


def virstotal(hash_name):
    result = check_file_reputation(hash_name)
    return result
