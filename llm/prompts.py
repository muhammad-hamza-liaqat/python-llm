import re

def reword_task_prompt(task: str, language: str = "python") -> str:
    task = task.strip().rstrip(".")
    
    base_prompt = f"Below is a programming task. OUTPUT ONLY THE CODE. Do NOT repeat the task or add explanations.\nTask: {task}"
    
    return f"Write only Python code. {base_prompt}"


def extract_code(content: str) -> str:
    code_keywords = ["def", "class", "import", "from"]
    code_chars = [";", "{", "}", "=", "(", ")", "[", "]"]

    lines = content.splitlines()
    code_lines = []
    code_started = False

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        if not code_started:
            if any(stripped.startswith(kw) for kw in code_keywords) or any(c in stripped for c in code_chars):
                code_started = True

        if code_started:
            code_lines.append(line)

    return "\n".join(code_lines).strip()
