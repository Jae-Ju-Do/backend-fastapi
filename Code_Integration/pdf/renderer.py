from fpdf import FPDF
from fpdf.enums import XPos, YPos
import re

class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        self.add_font("Malgun", style="", fname="C:\\Windows\\Fonts\\malgun.ttf")
        self.add_font("Malgun", style="B", fname="C:\\Windows\\Fonts\\malgunbd.ttf")
        self.add_font("Emoji", style="", fname="C:\\Windows\\Fonts\\seguiemj.ttf")
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


# def generate_pdf_from_data(data, pdf_path):
#     try:
#         pdf = PDF()
#         pdf.section_title("🔍 Program Overview")
#         overview = data["overview"]
#         if isinstance(overview, dict):
#             for k, v in overview.items():
#                 pdf.multi_line(f"{k}: {v}")
#         else:
#             pdf.multi_line(str(overview))

#         pdf.section_title("🦠 Malware Type")
#         types = data["malware_type"]
#         pdf.multi_line(", ".join(types) if isinstance(types, list) else str(types))

#         pdf.section_title("🛠️ MITRE ATT&CK TTPs")
#         for tactic, techniques in data["ttp"].items():
#             pdf.multi_line(f"[{tactic}]")
#             for t in techniques:
#                 tid = t.get("technique_id", "N/A")
#                 desc = t.get("description", "N/A")
#                 pdf.multi_line(f"- {tid}: {desc}")

#         pdf.section_title("🚨 Malicious Code Behaviors")
#         for key, behavior in data["behaviors"].items():
#             pdf.multi_line(f"{key}: {behavior.get('summary', 'N/A')}")
#             pdf.multi_line(f"관련성: {behavior.get('malware_type_relation', 'N/A')}")
#             pdf.multi_line("코드 스니펫:")
#             pdf.code_block(behavior.get("code_snippet", ""))
#             pdf.multi_line(f"분석: {behavior.get('analysis', 'N/A')}")
#             pdf.ln(2)

#         pdf.section_title("🛡️ Conclusion")
#         conclusion = data["conclusion"]
#         if isinstance(conclusion, list):
#             for item in conclusion:
#                 pdf.multi_line(f"- {item}")
#         else:
#             pdf.multi_line(conclusion if conclusion else "결론 없음.")

#         pdf.output(pdf_path)
#         return {"status_code":200, "content": pdf_path}
#     except Exception as e:
#         return {"status_code": 400, "content": f"pdf 생성 오류 : {e}"}   


def generate_pdf_from_data(data, pdf_path, file_name):
    try:
        pdf = PDF()

        pdf.set_font("Malgun", "B", 13) 
        pdf.multi_line(f"{file_name} 보고서")
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
                # pdf.multi_line(f"{key}: {behavior.get('summary', 'N/A')}")
                # pdf.multi_line(f"관련성: {behavior.get('malware_type_relation', 'N/A')}")
                pdf.multi_line("코드 스니펫:")
                pdf.code_block(behavior.get("code_snippet", ""))
                pdf.multi_line(f"분석: {behavior.get('analysis', 'N/A')}")
                pdf.ln(5)
        elif isinstance(behaviors, list):
            for behavior in behaviors:
                # pdf.multi_line(f"Summary: {behavior.get('summary', 'N/A')}")
                # pdf.multi_line(f"관련성: {behavior.get('malware_type_relation', 'N/A')}")
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

        pdf.output(pdf_path)
        return {"status_code": 200, "content": pdf_path}
    except Exception as e:
        return {"status_code": 400, "content": f"pdf 생성 오류 : {e}"}
