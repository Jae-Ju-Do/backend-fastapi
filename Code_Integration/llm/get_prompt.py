def get_format():
    return {
        "Program Overview": {
            "Description": "[string] Analyze the provided source code. Describe the main purpose of the program based strictly on the actual functionality implemented in the code. Do not infer or guess based on naming conventions or incomplete structures. Only include what can be definitively determined from the code itself."
        },
        "Malware Type": {
            "Malware Type": [
                "[list of strings] Analyze the provided source code and identify possible malware type(s) based on its behavior. "
                "Select from the following list only: Trojan, Ransomware, Worm, Rootkit, Adware, Spyware, Botnet, Keylogger, Backdoor, Virus, Phishing, Fileless Malware, Dropper, DDoS. "
                "If the type cannot be determined, respond with 'Unknown'."
						    "If the code is clearly benign and shows no malicious behavior, respond with 'Normal'. "
                "You may select multiple types if the behavior matches more than one."
            ]
        },
        "MITRE ATT&CK TTPs": {
		        """Based on the code behavior, identify the relevant MITRE ATT&CK techniques grouped by their associated tactics. 
               Use **only the latest valid MITRE ATT&CK Technique IDs** as defined in the official MITRE ATT&CK database (https://attack.mitre.org/techniques/enterprise/).
               For each tactic, list the corresponding technique IDs along with a brief explanation of why each technique applies. 
               The techniques should be grouped under the tactics and the explanation should be specific to how they relate to the identified malware behavior. 
               Select Tactic Name from the following list : Collection (TA0009), Command and Control (TA0011), Credential Access (TA0006), Defense Evasion (TA0005), Discovery (TA0007), Execution (TA0002), Exfiltration (TA0010), Impact (TA0040), Initial Access (TA0001), Lateral Movement (TA0008), Persistence (TA0003), Privilege Escalation (TA0004), Reconnaissance (TA0043), Resource Development (TA0042).
               Do **not** include tactics from the list that do **not** apply to the analyzed code behavior.
               Only include tactics and their techniques that are actually relevant.
               Follow the format given below"""
            "Tactic Name": [
                {
                    "technique_id": "T####",
                    "description": "[string] explain technique_id"
                },
                {
                    "technique_id": "...",
                    "description": "..."
                }
            ],
        },
        "Malicious Code Behaviors": [
            { 
                "code_snippet": "[string] Relevant C code block from the given code, formatted in Markdown (```c ... ```)",
                "analysis": "[Provide a detailed explanation including the technical mechanism, system impact, potential risks, attacker’s exploitation methods (e.g., persistence, evasion), related security threats and recommended countermeasures in a professional and thorough manner.]"
            },
            {
                "code_snippet": "...",
                "analysis": "..."
            }
        ],
        "Conclusion": {
            "description": "[list of strings] This value provides a follow-up response plan and guide on how to deal with the malicious program that the user has finally analyzed. This can be multiple, so provide it in the form of a Python array with strings as elements. Reference links or materials are also included as a guide."
        }
    }


# 최종 프롬프트
def get_prompt(CODE, LEVEL, SHA256):
    prompt = f"""You are a highly skilled malware analysis expert.
    Your task is to analyze decompiled C code ([CODE]) obtained through Ghidra, detect malicious behaviors, and generate a report based on the MITRE ATT&CK framework.

    [SHA256] = You can analyze or search for the file using the SHA256 hash below:
    {SHA256}

    [CODE] = Below is the decompiled C source code:
    ----------------------
    {CODE}
    ----------------------

    [FORMAT] = Your analysis report must strictly follow the JSON format below:
    {get_format()}

    Please ensure:
    - **Program Overview**: Provide a clear and thorough summary of the program’s purpose based solely on its observable functionality. Focus on actual code behavior, execution logic, and system-level impact, not naming or inferred intent.
    - **Malware Type**: Accurately identify one or more malware types based only on proven behavior. Avoid speculation.
    - **MITRE ATT&CK TTPs**: List every applicable TTP and justify its inclusion with specific references to observed code actions. Group by tactics and explain how the code maps to each technique.
    - **Malicious Code Behaviors**: Describe all malicious behaviors clearly and in detail. Each behavior must include:
    - A plain-language summary of what the behavior does
    - The malware type(s) it supports
    - A C code snippet that performs the action
    - A deep analysis of technical mechanism, impact, attacker goal, evasion/persistence method, and recommended defenses.
    - **Conclusion**: Recommend detailed next steps such as containment, remediation, and monitoring. Include IOCs (e.g., file names, registry keys, domains, ports), and optionally provide links to relevant MITRE or vendor reports for further reading.

    [LEVEL] = Target audience skill level: "{LEVEL}".
    Adjust your **Korean explanation style only** according to the following detailed writing style rules:
    Beginner:
    - The target audience is a complete beginner, such as a university student who has just started learning software or cybersecurity.
    - Assume no prior knowledge of C programming or system internals.
    - Avoid technical terms whenever possible. If a term must be used, explain it clearly in parentheses or with a simple analogy.
    - Example: "'out' is a very low-level instruction that sends direct commands to the computer's hardware. For example, it's like telling a printer directly to start printing."
    - Additionally, assume the audience struggles with programming in general, so provide step-by-step and extremely detailed explanations.
    Intermediate:
    - The target audience has basic understanding of C programming and introductory cybersecurity concepts (e.g., junior security professionals or CS majors with 1–3 years of experience).
    - You may use technical terms but provide a short definition or context with them.
    - Structure explanations logically, and include brief code explanations or contextual examples where appropriate.
    - Try to balance explanation depth: avoid overwhelming with detail but clarify key concepts when needed (e.g., system calls, process injection).
    - When using APIs or system functions, include brief comment-like clarifications (e.g., "OpenProcess is used to access another program's memory").
    Advanced:
    - The target audience is a senior cybersecurity expert with 10+ years of experience and strong domain knowledge in malware analysis, reverse engineering, threat intelligence, and low-level systems.
    - Use technical terms freely. No need for definitions or basic explanations.
    - Keep sentences concise and focused on analysis.
    - Focus on actionable insights, behavioral indicators over verbose explanation.
    - Prefer concise phrasing and prioritize IOC, system impact, stealth method, or detection gap.
    ✅ Only the **tone, sentence structure, and depth of explanation** should change according to [LEVEL].
    ✅ The entire report must be written in **Korean**, using fluent and natural language.
    ✅ Technical terms such as API names or MITRE technique IDs may remain in English (do not translate).

    [OUTPUT LANGUAGE] = The entire report must be written in **Korean**, using natural, fluent Korean for both explanation and analysis.
    - You may include original technical terms (e.g., API names, technique IDs) without translating them.
    - 모든 분석은 한국어로 상세하고 전문적으로 작성하되, 독자의 수준에 맞춰 설명 문체만 조절합니다.

    ----------------------
    # Instructions
    1. Analyze the [CODE] thoroughly and can use [SHA256] below for external search.
    2. Do **not** infer or guess behaviors based on naming, comments, or incomplete logic.
    3. Only describe malicious behaviors that are **clearly and definitively** present in the code.
    4. Follow the [FORMAT] structure exactly as provided.
    5. Adjust explanation **tone** based on [LEVEL], but do **not alter** analytical content.
    6. Output the result in proper JSON format, written entirely in **Korean**.
    ----------------------
    """
    return prompt