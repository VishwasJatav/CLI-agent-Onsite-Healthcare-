# Project Complete
AI-Native CLI Assistant
An AI-powered command-line and GUI assistant that lets users perform software development operations using natural language commands. This tool converts plain English into structured, actionable developer operations, from creating files to refactoring code and making git commits.

Screenshot
Features
Natural Language Understanding: Interprets plain English commands to perform complex tasks.

Code Generation: Creates new files with boilerplate or functional code based on a concept (e.g., "a prime number script").

Code Refactoring: Reads, analyzes, and refactors existing code files using AI to improve structure and readability.

File System Operations: Seamlessly creates files and directories.

Git Integration: Performs git commits with natural language messages.

Dual Interface: Can be used as both a traditional Command-Line Interface (CLI) and a user-friendly Graphical User Interface (GUI).

Tech Stack
Backend: Python 3

AI: Google Gemini API

GUI: Tkinter

CLI: Click

Setup and Installation
Follow these steps to get the project running on your local machine.

Clone the Repository
Replace YourUsername/YourRepoName.git with your actual repository URL.

Bash

git clone https://github.com/YourUsername/YourRepoName.git
cd ai-native-cli
Create and Activate a Virtual Environment

Create the environment:

Bash

python -m venv venv
Activate it:

On Windows (PowerShell):

PowerShell

.\venv\Scripts\activate
On macOS/Linux:

Bash

source venv/bin/activate
Install Dependencies

Bash

pip install -r requirements.txt
Set Up Your API Key

Create a new file in the root directory named .env.

Add your Google Gemini API key to the file like this:

GEMINI_API_KEY='your-secret-api-key-here'
Usage
You can run the application in two ways:

1. Running the GUI (Recommended)
To launch the graphical user interface, run:

Bash

python gui.py
2. Running the CLI
To use the command-line interface, pass your prompt as an argument:

Bash

python cli.py "your command in quotes"
Example Prompts
Here are a few examples of what you can ask the assistant to do:

list all files in detail

create a python script in app.py that runs a simple flask server

make a new folder called 'assets'

refactor the code in the file utils.py

commit my changes with the message 'feat: implement user authentication'
