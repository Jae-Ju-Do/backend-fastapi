def parse_malware_report(json):
    try:
        data = {
            "overview": json.get("Program Overview", "").get("Description", []),
            "malware_type": json.get("Malware Type", {}).get("Malware Type", []),
            "ttp": json.get("MITRE ATT&CK TTPs", {}),
            "behaviors": json.get("Malicious Code Behaviors", {}),
            "conclusion": json.get("Conclusion", {}).get("description", [])
        } 
        return {"status_code":200, "content": data}
    except Exception as e:
        return {"status_code": 400, "content": f"json 파싱 오류 : {e}"}   