from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import subprocess
import asyncio
import time

# Load environment variables
load_dotenv()

# OpenRouter Client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

# ---------------- TOOLS ---------------- #

async def create_folder(folder_data):

    try:

        # Handle object input
        if isinstance(folder_data, dict):
            folder_name = folder_data.get("folder_name")

        # Handle string input
        else:
            folder_name = folder_data

        os.makedirs(folder_name, exist_ok=True)

        return f"Folder '{folder_name}' created successfully"

    except Exception as e:
        return str(e)


async def write_file(data):

    try:

        filename = data["filename"]
        content = data["content"]

        # Create parent directory automatically
        directory = os.path.dirname(filename)

        if directory:
            os.makedirs(directory, exist_ok=True)

        with open(filename, "w", encoding="utf-8") as file:
            file.write(content)

        return f"File '{filename}' written successfully"

    except Exception as e:
        return str(e)


async def read_file(filename=""):

    try:

        with open(filename, "r", encoding="utf-8") as file:
            return file.read()

    except Exception as e:
        return str(e)


async def open_browser(filename=""):

    try:

        subprocess.run(["open", filename])

        return "Browser opened successfully"

    except Exception as e:
        return str(e)


# ---------------- TOOL MAP ---------------- #

tool_map = {
    "create_folder": create_folder,
    "write_file": write_file,
    "read_file": read_file,
    "open_browser": open_browser
}

# ---------------- MAIN ---------------- #

async def main():

    system_prompt = """
You are an AI Website Cloning Agent.

You work in START, THINK, TOOL, OBSERVE and OUTPUT steps.

Your task is to create responsive websites step by step.

Available tools:

1. create_folder(folder_name)
2. write_file({filename, content})
3. read_file(filename)
4. open_browser(filename)

Rules:

1. Always return ONLY valid JSON
2. Never return markdown
3. Never use ```json
4. Perform one step at a time
5. Always think before using tools
6. Generate HTML, CSS and JS separately
7. Do not generate everything in one step
8. After every TOOL step wait for OBSERVE
9. Keep responses concise
10. Keep HTML/CSS/JS compact

Output Format:

{
  "step": "START | THINK | TOOL | OBSERVE | OUTPUT",
  "content": "string",
  "tool_name": "string",
  "tool_args": "string or object"
}
"""

    user_input = input(">>> ")

    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": user_input
        }
    ]

    while True:

        try:

            # Small delay
            time.sleep(2)

            response = client.chat.completions.create(

                model="openai/gpt-4o-mini",

                messages=messages,

                temperature=0.7
            )

            content = response.choices[0].message.content

            # Cleanup markdown if model sends it
            content = content.replace("```json", "")
            content = content.replace("```", "")
            content = content.strip()

            try:

                parsed_content = json.loads(content)

            except Exception as e:

                print("\nJSON Parse Error:\n")
                print(e)
                print(content)

                break

            # Store assistant response
            messages.append({
                "role": "assistant",
                "content": json.dumps(parsed_content)
            })

            step = parsed_content.get("step")

            # ---------------- START ---------------- #

            if step == "START":

                print("\nSTART\n")
                print(parsed_content.get("content"))

                # Execute tool if included
                if parsed_content.get("tool_name"):

                    tool_name = parsed_content.get("tool_name")
                    tool_args = parsed_content.get("tool_args")

                    print(f"\nExecuting Tool: {tool_name}")

                    if tool_name not in tool_map:

                        observe_message = {
                            "step": "OBSERVE",
                            "content": "Tool not found"
                        }

                    else:

                        result = await tool_map[tool_name](tool_args)

                        observe_message = {
                            "step": "OBSERVE",
                            "content": result
                        }

                    print(observe_message["content"])

                    messages.append({
                        "role": "user",
                        "content": json.dumps(observe_message)
                    })

                messages.append({
                    "role": "user",
                    "content": "Proceed to next step"
                })

            # ---------------- THINK ---------------- #

            elif step == "THINK":

                print("\nTHINK\n")
                print(parsed_content.get("content"))

                # Execute tool if model included it
                if parsed_content.get("tool_name"):

                    tool_name = parsed_content.get("tool_name")
                    tool_args = parsed_content.get("tool_args")

                    print(f"\nExecuting Tool: {tool_name}")

                    if tool_name not in tool_map:

                        observe_message = {
                            "step": "OBSERVE",
                            "content": "Tool not found"
                        }

                    else:

                        result = await tool_map[tool_name](tool_args)

                        observe_message = {
                            "step": "OBSERVE",
                            "content": result
                        }

                    print(observe_message["content"])

                    messages.append({
                        "role": "user",
                        "content": json.dumps(observe_message)
                    })

                messages.append({
                    "role": "user",
                    "content": "Proceed to next step"
                })

            # ---------------- TOOL ---------------- #

            elif step == "TOOL":

                print("\nTOOL\n")

                tool_name = parsed_content.get("tool_name")
                tool_args = parsed_content.get("tool_args")

                print(f"Executing Tool: {tool_name}")

                if tool_name not in tool_map:

                    observe_message = {
                        "step": "OBSERVE",
                        "content": "Tool not found"
                    }

                else:

                    result = await tool_map[tool_name](tool_args)

                    observe_message = {
                        "step": "OBSERVE",
                        "content": result
                    }

                print(observe_message["content"])

                messages.append({
                    "role": "user",
                    "content": json.dumps(observe_message)
                })

                messages.append({
                    "role": "user",
                    "content": "Proceed to next step"
                })

            # ---------------- OUTPUT ---------------- #

            elif step == "OUTPUT":

                print("\nFINAL OUTPUT\n")
                print(parsed_content.get("content"))

                break

            # ---------------- OBSERVE ---------------- #

            elif step == "OBSERVE":

                print("\nOBSERVE\n")
                print(parsed_content.get("content"))

                messages.append({
                    "role": "user",
                    "content": "Proceed to next step"
                })

            # ---------------- UNKNOWN ---------------- #

            else:

                print("\nUNKNOWN STEP\n")
                print(parsed_content)

                break

        except Exception as e:

            print("\nERROR OCCURRED:\n")
            print(e)

            break


# Run App
asyncio.run(main())