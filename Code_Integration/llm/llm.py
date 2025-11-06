import openai
import os
from dotenv import load_dotenv
from openai import OpenAI
import tiktoken
from .get_prompt import get_prompt
from .code_optimizer import code_optimizer


load_dotenv()

model_name = "gpt-4o-mini-2024-07-18"
client = OpenAI(api_key=os.getenv("GPT_API_KEY"))
encoding = tiktoken.encoding_for_model(model_name)


def read_code(code_path):
    try:
        with open(code_path, 'r', encoding='utf-8') as file:
            malware_code = file.read()  # 파일의 내용을 읽어 반환
        return malware_code
    except Exception as e:
        print(f"Error reading the file: {e}")
        return None  # 오류 발생 시 None을 반환


def get_response(malware_code, level, sha256):
    # malware_type = [
    #     "Trojan", "Ransomware", "Worm", "Rootkit", "Adware",
    #     "Spyware", "Botnet", "Keylogger", "Backdoor", "Virus",
    #     "Phishing", "Fileless Malware", "Dropper", "DDoS"
    # ]

    prompt = get_prompt(malware_code, level, sha256)
    gpt_response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": "You are a professional malware analyst."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=4000,
        temperature=0.0,
        top_p=0.0
    )

    return gpt_response.choices[0].message.content.strip()


def get_prompt_token(code, level, sha256):
    prompt = get_prompt(code, level, sha256)
    return len(encoding.encode(prompt))


def llm(c_path, level_flag, sha256):
    code = code_optimizer(read_code(c_path))
    level = ["Beginner", "Intermediate", "Advanced"]

    try:
        print(f"Level: {level[level_flag]}")
        print(f"Input Token Count: {get_prompt_token(code, level[level_flag], sha256)}")
        response = get_response(code, level[level_flag], sha256)
        print("---------------------")
        print(response)
        print("---------------------")
        print(f"Output Token Count: {len(encoding.encode(response))}")
        return {"status_code": 200, "content": response}
    except Exception as e:
        return {"status_code": 400, "content": f"virus_check 오류 : {e}"}
