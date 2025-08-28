import tkinter as tk
from tkinter import scrolledtext, Entry, Button, Frame, END
import threading
import queue

# Import the logic from your core file
from ai_native_cli.core_logic import get_command_from_ai, run_command

# --- UI Styling ---
BG_COLOR = "#2c3e50"
TEXT_COLOR = "#ecf0f1"
INPUT_BG_COLOR = "#34495e"
BUTTON_COLOR = "#3498db"
BUTTON_TEXT_COLOR = "#ffffff"
FONT_MAIN = ("Helvetica", 12)
FONT_OUTPUT = ("Consolas", 11)


class AIAssistantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI-Native Assistant")
        self.root.geometry("750x550")
        self.root.configure(bg=BG_COLOR)

        # Queue for thread communication
        self.result_queue = queue.Queue()

        self.setup_ui()
        self.check_queue()

    def setup_ui(self):
        # --- Input Frame ---
        input_frame = Frame(self.root, bg=BG_COLOR, pady=10)
        input_frame.pack(fill='x', padx=10)

        self.prompt_input = Entry(input_frame, font=FONT_MAIN, bg=INPUT_BG_COLOR, fg=TEXT_COLOR, insertbackground=TEXT_COLOR, relief='flat')
        self.prompt_input.pack(fill='x', side='left', expand=True, ipady=5)
        self.prompt_input.bind("<Return>", lambda event: self.start_task())

        self.run_button = Button(input_frame, text="Run", command=self.start_task, font=FONT_MAIN, bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR, relief='flat', padx=10)
        self.run_button.pack(padx=(5, 0), side='left')

        self.clear_button = Button(input_frame, text="Clear", command=self.clear_output, font=FONT_MAIN, bg="#95a5a6", fg=BUTTON_TEXT_COLOR, relief='flat', padx=10)
        self.clear_button.pack(padx=(5, 0), side='left')

        # --- Output Text Box ---
        self.output_box = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, font=FONT_OUTPUT, state=tk.DISABLED, bg="#1e272e", fg=TEXT_COLOR, relief='flat')
        self.output_box.pack(expand=True, fill='both', padx=10, pady=(0, 10))
    
    def clear_output(self):
        self.output_box.config(state=tk.NORMAL)
        self.output_box.delete('1.0', END)
        self.output_box.config(state=tk.DISABLED)

    def start_task(self):
        """Starts the AI processing in a separate thread to keep the GUI responsive."""
        prompt = self.prompt_input.get()
        if not prompt:
            return

        self.run_button.config(state=tk.DISABLED, text="Processing...")
        self.output_box.config(state=tk.NORMAL)
        self.output_box.delete('1.0', END)
        self.output_box.insert(END, f"🤖 Processing: '{prompt}'\n\n")
        self.output_box.config(state=tk.DISABLED)

        # Run the blocking task in a new thread
        threading.Thread(target=self.process_task, args=(prompt,), daemon=True).start()

    def process_task(self, prompt):
        """This function runs in a separate thread."""
        parsed_command = get_command_from_ai(prompt)
        result_output = run_command(parsed_command)
        # Put the result in the queue to be picked up by the main thread
        self.result_queue.put(result_output)

    def check_queue(self):
        """Periodically checks the queue for results from the worker thread."""
        try:
            result = self.result_queue.get_nowait()
            self.update_output(result)
        except queue.Empty:
            pass
        finally:
            # Schedule this function to run again after 100ms
            self.root.after(100, self.check_queue)
    
    def update_output(self, result):
        """Updates the GUI with the result from the thread."""
        self.output_box.config(state=tk.NORMAL)
        self.output_box.insert(END, result)
        self.output_box.config(state=tk.DISABLED)
        self.prompt_input.delete(0, END)
        self.run_button.config(state=tk.NORMAL, text="Run")


if __name__ == "__main__":
    root = tk.Tk()
    app = AIAssistantApp(root)
    root.mainloop()