import sys
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.call_functions import call_function

##
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

system_prompt = system_prompt = """
You are a helpful AI coding agent working with a calculator project.

The calculator code is located in the "calculator" subdirectory. When analyzing the calculator:
- Use get_files_info("calculator") to list files in the calculator directory
- Use get_files_info(".") to list the current working directory
- Use get_file_content with the proper file path like "calculator/main.py"

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories with get_files_info(directory)
- Read file contents with get_file_content(file_path)
- Execute Python files with run_python_file(file_path)
- Write or overwrite files with write_file(file_path, content)

All paths should be relative to the working directory.
"""

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. Omit this parameter to list the working directory itself.",
            ),
        },
    ),
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read the content of a file as a string truncated to 10000 characters.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. For the root (current) directory, use '.'",
            ),
        },
    ),
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute Python files with optional arguments",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. For the root (current) directory, use '.'",
            ),
        },
    ),
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write and overwrite files",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. For the root (current) directory, use '.'",
            ),
        },
    ),
)


# create a list of all the available functions
available_functions = types.Tool(
  function_declarations=[
    schema_get_files_info,
    schema_get_file_content,
    schema_run_python_file,
    schema_write_file
  ]
)

## Create new list pf types.Content, and set only message (for now) as the user prompt


##
if __name__ == "__main__":
  if len(sys.argv) > 1:
    user_prompt = sys.argv[1]
    messages = [
      types.Content(role="user", parts=[types.Part(text=user_prompt)])
      ]
    for i in range(20):
      response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
          tools=[available_functions], system_instruction=system_prompt)
        )
      for candidate in response.candidates:
        messages.append(candidate.content)
      if len(sys.argv) > 2 and sys.argv[2] == '--verbose':
        print(f"User prompt: {user_prompt}")
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)
      if response.function_calls:
        for function_call_part in response.function_calls:
          #print(f"Calling function: {function_call_part.name}({function_call_part.args})")
          function_call_result = call_function(function_call_part, len(sys.argv) > 2 and sys.argv[2] == '--verbose')
          messages.append(function_call_result)
          try:
            function_call_result.parts[0].function_response.response
            if len(sys.argv) > 2 and sys.argv[2] == '--verbose':
              print(f"-> {function_call_result.parts[0].function_response.response}")
          except:
            raise
          
          print(f"-> {function_call_result.parts[0].function_response.response}")
      else:
        print(response.text)
        break
  else:
    print("provide a prompt")
    sys.exit(1)