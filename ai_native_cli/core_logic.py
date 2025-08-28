import os
import json
import subprocess
import platform
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables and configure the Gemini API
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)
else:
    print("Error: GEMINI_API_KEY not found. Please check your .env file.")

# NEW: A dedicated model for the refactoring task
refactor_model = genai.GenerativeModel('gemini-1.5-flash')

def get_command_from_ai(user_prompt):
    """Sends the prompt to the Gemini API and gets a structured command back."""
    # MODIFIED: Added a rule for the new "refactor_code" intent.
    system_prompt = """
    You are an expert command-line assistant and a skilled code generator. Your task is to convert a user's natural language prompt 
    into a structured JSON command. You must adhere to the following rules:

    1.  For file/directory listing, return: {"intent": "list_files", "detail": true/false}
    2.  For directory creation, return: {"intent": "create_directory", "dirname": "the_dir_name"}
    3.  For 'git' commands, return: {"command": "git", "args": ["..."]}
    
    4.  For file creation (if the user asks for code based on a CONCEPT), generate the code and return:
        {"intent": "create_file", "filename": "file.ext", "content": "code to write"}

    5.  NEW: For refactoring existing code, return:
        {"intent": "refactor_code", "filename": "file_to_refactor.py"}

    6.  If a command is not supported or unsafe, return: {"error": "Command not supported."}

    Examples:
    - User: "list all files" -> {"intent": "list_files", "detail": false}
    - User: "create a prime number checker in prime.py" -> {"intent": "create_file", "filename": "prime.py", "content": "def is_prime(n): ..."}
    - User: "refactor the script named utils.py" -> {"intent": "refactor_code", "filename": "utils.py"}
    - User: "commit my changes" -> {"command": "git", "args": ["commit", "-m", "AI generated commit"]}

    Now, convert the following user prompt. ONLY return the JSON object.
    """
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content([system_prompt, user_prompt])
        cleaned_response = response.text.strip().replace('```json', '').replace('```', '').strip()
        return json.loads(cleaned_response)
    except Exception as e:
        return {"error": f"AI Error or JSON Parsing Failed: {e}"}

def run_command(parsed_command):
    """Executes a command from parsed JSON and returns the output as a string."""
    output_lines = []
    
    if "error" in parsed_command:
        output_lines.append(f"❌ Error: {parsed_command['error']}")
        return "\n".join(output_lines)

    intent = parsed_command.get("intent")
    
    if intent == "list_files":
        # ... (this part is unchanged)
        is_detailed = parsed_command.get("detail", False)
        if platform.system() == "Windows":
            command = ["dir"]
        else:
            command = ["ls", "-l" if is_detailed else "-a"]
        full_command_str = " ".join(command)

    elif intent == "create_file":
        # ... (this part is unchanged)
        filename = parsed_command.get("filename")
        content = parsed_command.get("content", "")
        if not filename: return "❌ Error: Filename not provided."
        try:
            with open(filename, 'w') as f: f.write(content)
            msg = "with content" if content else "empty"
            output_lines.append(f"✅ Executed: Created {msg} file '{filename}'")
            return "\n".join(output_lines)
        except Exception as e: return f"❌ Error creating file: {e}"

    elif intent == "create_directory":
        # ... (this part is unchanged)
        dirname = parsed_command.get("dirname")
        if not dirname: return "❌ Error: Directory name not provided."
        try:
            os.makedirs(dirname, exist_ok=True)
            output_lines.append(f"✅ Executed: Created directory '{dirname}'")
            return "\n".join(output_lines)
        except Exception as e: return f"❌ Error creating directory: {e}"

    # NEW: The logic to handle the refactoring intent.
    elif intent == "refactor_code":
        filename = parsed_command.get("filename")
        if not filename: return "❌ Error: Filename not provided for refactoring."
        
        try:
            output_lines.append(f"Attempting to refactor '{filename}'...")
            # 1. Read the existing code
            with open(filename, 'r') as f:
                original_code = f.read()
            
            output_lines.append("Original code read successfully.")
            
            # 2. Analyze and get refactored code from the AI
            refactor_prompt = f"Please refactor the following Python code to improve its readability, structure, and efficiency. Only return the complete, refactored code inside a single code block. Do not add any explanations before or after the code.\n\n```python\n{original_code}\n```"
            response = refactor_model.generate_content(refactor_prompt)
            refactored_code = response.text.strip().replace("```python", "").replace("```", "").strip()

            output_lines.append("AI has generated the refactored code.")
            
            # 3. Rewrite the file with the new code
            with open(filename, 'w') as f:
                f.write(refactored_code)
            
            output_lines.append(f"✅ Executed: Successfully refactored and overwrote '{filename}'.")
            return "\n".join(output_lines)

        except FileNotFoundError:
            return f"❌ Error: The file '{filename}' was not found."
        except Exception as e:
            return f"❌ An error occurred during refactoring: {e}"

    elif "command" in parsed_command:
        # ... (this part is unchanged)
        command_name = parsed_command.get("command")
        args = parsed_command.get("args", [])
        ALLOWED_COMMANDS = ['git']
        if command_name not in ALLOWED_COMMANDS: return f"❌ Error: The command '{command_name}' is not allowed."
        
        command = [command_name] + args
        full_command_str = " ".join(command)
    
    else:
        return "❌ Error: Could not understand the parsed command format."

    # Execute file listing or git commands
    try:
        output_lines.append(f"✅ Executing: `{full_command_str}`\n")
        result = subprocess.run(full_command_str, capture_output=True, text=True, shell=True, check=False)

        if result.stdout: output_lines.append("---\n" + result.stdout)
        if result.stderr: output_lines.append("--- ERRORS ---\n" + result.stderr)
        output_lines.append("\n✅ Task completed.")
    except Exception as e:
        output_lines.append(f"❌ An unexpected error occurred during execution: {e}")

    return "\n".join(output_lines)