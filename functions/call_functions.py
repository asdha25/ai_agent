from .get_file_content import get_file_content
from .get_files_info import get_files_info
from .run_python_file import run_python_file
from .write_file import write_file
from google import genai
from google.genai import types

def call_function(function_call_part, verbose=False):

  if verbose:
    print(f"Calling function: {function_call_part.name}({function_call_part.args})")
  else:
    print(f" - Calling function: {function_call_part.name}")

  function_list = {
    "get_file_content": get_file_content,
    "get_files_info": get_files_info,
    "write_file": write_file,
    "run_python_file": run_python_file
  }

  if function_call_part.name not in function_list:
    return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_call_part.name,
            response={"error": f"Unknown function: {function_call_part.name}"},
        )
    ],
)

  function_to_call = function_list[function_call_part.name]

  function_call_part.args["working_directory"] = "./calculator"

  if function_call_part.name == "get_file_content":
    filtered_args = {
      "working_directory": "./calculator",
      "file_path": function_call_part.args.get("directory", "")
    }
    result = function_to_call(**filtered_args)
  elif function_call_part.name == "get_files_info":
    filtered_args = {
      "working_directory": "./calculator",
      "directory": function_call_part.args.get("directory", "")
    }
    result = function_to_call(**filtered_args)
  elif function_call_part.name == "write_file":
    filtered_args = {
      "working_directory": "./calculator",
      "file_path": function_call_part.args.get("directory", ""),
      "content": function_call_part.args.get("content", "")
    }
    result = function_to_call(**filtered_args)

  elif function_call_part.name == "run_python_file":
    filtered_args = {
      "working_directory": "./calculator",
      "file_path": function_call_part.args.get("directory", "")
    }
    result = function_to_call(**filtered_args)

  

  return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_call_part.name,
            response={"result": result},
        )
    ],
)