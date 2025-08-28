# cli.py

import click
from ai_native_cli.core_logic import get_command_from_ai, run_command

@click.command()
@click.argument('prompt', nargs=-1)
def main(prompt):
    """
    AI-Native CLI: Your assistant for software development.
    Takes natural language prompts and executes them as commands.
    Example: python cli.py "list all files"
    """
    if not prompt:
        click.echo("Please provide a prompt. For example: python cli.py \"create a new file named test.txt\"")
        return

    user_prompt = " ".join(prompt)
    click.echo(f"🤖 Processing: '{user_prompt}'")

    # 1. Get structured command from the AI
    parsed_command = get_command_from_ai(user_prompt)
    
    # 2. Run the command and get the output string
    result_output = run_command(parsed_command)

    # 3. Print the results to the console
    click.echo("---")
    click.echo(result_output)

if __name__ == "__main__":
    main()