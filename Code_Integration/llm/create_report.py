import json as json_lib
import os
import re

import tiktoken
from dotenv import load_dotenv
from fpdf import FPDF
from fpdf.enums import XPos, YPos
from openai import OpenAI

from get_prompt import get_prompt

load_dotenv()

model_name = "gpt-4o-mini-2024-07-18"
client = OpenAI(api_key=os.getenv("GPT_API_KEY"))
encoding = tiktoken.encoding_for_model(model_name)

class PDF(FPDF):
    def __init__(self):
        super().__init__()

        # fonts 폴더에 해당 ttf 파일들이 있어야 함
        font_dir = r"../../fonts/"
        self.set_auto_page_break(auto=True, margin=15)
        self.add_font("Malgun", style="", fname=str(font_dir + "malgun.ttf"))
        self.add_font("Malgun", style="B", fname=str(font_dir + "malgunbd.ttf"))

        emoji_font_path = font_dir + "/seguiemj.ttf"
        self.add_font("Emoji", style="", fname=str(emoji_font_path))
        self.add_page()
        self.set_font("Malgun", size=12)

    def section_title(self, title):
        self.ln(10)
        icon = ''
        if '🛡️' in title: icon = '🛡️'
        elif '🔍' in title: icon = '🔍'
        elif '🚨' in title: icon = '🚨'
        elif '🛠️' in title: icon = '🛠️'
        elif '🦠' in title: icon = '🦠'

        title_text = title.replace(icon, '').strip()
        self.set_font("Emoji", size=15)
        self.cell(12, 10, icon, new_x=XPos.RIGHT, new_y=YPos.TOP)
        self.set_font("Malgun", style="B", size=14)
        self.cell(0, 10, title_text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.set_font("Malgun", size=12)
        self.ln(3)

    def multi_line(self, text):
        max_width = self.w - self.l_margin - self.r_margin
        lines = []
        current_line = ""
        for char in text:
            if self.get_string_width(current_line + char) > max_width:
                lines.append(current_line)
                current_line = char
            else:
                current_line += char
        lines.append(current_line)
        for line in lines:
            self.cell(0, 8, line, ln=True)

    def code_block(self, code):
        self.set_font("Malgun", size=10)
        self.set_fill_color(245, 245, 245)
        self.set_draw_color(200)
        max_width = self.epw - 2

        code = code.replace("```c", "").replace("```C", "").replace("```", "").strip()
        code = code.replace("\\r", "").replace("\\n", "\n")
        code = re.sub(r'(?<!\\)\\n', '\n', code)

        processed_lines = []
        for line in code.splitlines():
            segment = ""
            for char in line:
                if self.get_string_width(segment + char) > max_width:
                    processed_lines.append(segment)
                    segment = char
                else:
                    segment += char
            processed_lines.append(segment)

        final_code = "\n".join(processed_lines)
        # final_code에 lstrip()을 한 번 더 적용
        final_code = final_code.lstrip()
        self.multi_cell(0, 6, final_code, border=1, fill=True)
        self.ln(2)
        self.set_font("Malgun", size=12)


def generate_pdf_from_data(data, output_path):
    try:
        pdf = PDF()

        pdf.set_font("Malgun", "B", 13) 
        pdf.multi_line(f"{output_path} 보고서")
        pdf.ln(5)  

        pdf.section_title("🔍 Program Overview")
        overview = data.get("overview", {})
        if isinstance(overview, dict):
            for k, v in overview.items():
                pdf.multi_line(f"{k}: {v}")
        else:
            pdf.multi_line(str(overview))

        pdf.section_title("🦠 Malware Type")
        types = data.get("malware_type", [])
        pdf.multi_line(", ".join(types) if isinstance(types, list) else str(types))

        pdf.section_title("🛠️ MITRE ATT&CK TTPs")
        ttp = data.get("ttp", {})
        for tactic, techniques in ttp.items():
            pdf.multi_line(f"[{tactic}]")
            for t in techniques:
                tid = t.get("technique_id", "N/A")
                desc = t.get("description", "N/A")
                pdf.multi_line(f"- {tid}: {desc}")

        pdf.section_title("🚨 Malicious Code Behaviors")
        behaviors = data.get("behaviors", [])
        if isinstance(behaviors, dict):
            # 혹시 dict일 경우 (안 쓰는 게 좋음)
            for key, behavior in behaviors.items():
                pdf.multi_line("코드 스니펫:")
                pdf.code_block(behavior.get("code_snippet", ""))
                pdf.multi_line(f"분석: {behavior.get('analysis', 'N/A')}")
                pdf.ln(5)
        elif isinstance(behaviors, list):
            for behavior in behaviors:
                pdf.multi_line("코드 스니펫:")
                pdf.code_block(behavior.get("code_snippet", ""))
                pdf.multi_line(f"분석: {behavior.get('analysis', 'N/A')}")
                pdf.ln(5)
        else:
            pdf.multi_line("No malicious behaviors found.")

        pdf.section_title("🛡️ Conclusion")
        conclusion = data.get("conclusion", [])
        if isinstance(conclusion, list):
            for item in conclusion:
                pdf.multi_line(f"- {item}")
        else:
            pdf.multi_line(conclusion if conclusion else "결론 없음.")

        pdf.output(output_path)
    except Exception as e:
        print(f"pdf 생성 실패 : {e}")


def parse_malware_report(json):
    try:
        data = {
            "overview": json.get("Program Overview", "").get("Description", []),
            "malware_type": json.get("Malware Type", {}).get("Malware Type", []),
            "ttp": json.get("MITRE ATT&CK TTPs", {}),
            "behaviors": json.get("Malicious Code Behaviors", {}),
            "conclusion": json.get("Conclusion", {}).get("description", [])
        } 
        return data
    except Exception as e:
        print(f"파싱 실패 : {e}")


def pdf(json_data, output_path):
    try:
        print(f"json 타입 : {type(json_data)}")
        
        if isinstance(json_data, str):
            json_data = json_data.strip()
            if json_data.startswith("```"):
                json_data = "\n".join(
                    line for line in json_data.splitlines() if not line.strip().startswith("```")
                )
            json_data = json_lib.loads(json_data)
        
        report_data = parse_malware_report(json_data)

        generate_pdf_from_data(report_data, output_path)
    except Exception as e:
        print(f"pdf 변환 실패 : {e}")

def read_code(code_path):
    try:
        with open(code_path, 'r', encoding='utf-8') as file:
            malware_code = file.read()  # 파일의 내용을 읽어 반환
        return malware_code
    except Exception as e:
        print(f"Error reading the file: {e}")
        return None  # 오류 발생 시 None을 반환


def get_response(malware_code, level, sha256, top_p_value, temperature_value):
    prompt = get_prompt(malware_code, level, sha256)
    gpt_response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": "You are a professional malware analyst."},
            {"role": "user", "content": prompt}
        ],
        max_completion_tokens=4000,
        # temperature=temperature_value,
        # top_p=top_p_value
    )

    print(gpt_response)

    return gpt_response.choices[0].message.content.strip()

def get_prompt_token(code, level, sha256):
    prompt = get_prompt(code, level, sha256)

    return len(encoding.encode(prompt))

def create_report(directory_path, filename):
    code = read_code(os.path.join(directory_path, filename))
    level = ["Beginner", "Intermediate", "Advanced"]

    print(code)
    print(f"filename: {filename}")
    print(f"Level: {level[1]}")
    
    # print(f"Input Token Count: {get_prompt_token(code, level[1], None)}")
    print(f"Input Token Count: {len(encoding.encode(code))}")

    top_p_values = [0.0]
    temperature_values = [1]
    for top_p in top_p_values:
        for temperature in temperature_values:
            response_beginner = get_response(code, level[0], None, top_p, temperature)
            print(response_beginner)
            response_intermediate = get_response(code, level[1], None, top_p, temperature)
            print(response_intermediate)
            # response_advanced = get_response(code, level[2], None, top_p, temperature)
            # print(response_advanced)

            pdf(response_beginner, rf"./결과/{filename}-beginner.pdf")
            pdf(response_intermediate, rf"./결과/{filename}-intermediate.pdf")
            # pdf(response_advanced, rf"./결과/{filename}-advanced.pdf")
            

def run_reports_on_c_files(directory_path):
    for filename in os.listdir(directory_path):
        if filename.endswith(".c"):
            create_report(directory_path, filename)

target_dir = r"./C파일"
run_reports_on_c_files(target_dir)
