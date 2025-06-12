import os
import subprocess

def run_python_file(working_directory, file_path):
  abs_path = os.path.abspath(os.path.join(working_directory, file_path))
  abs_working = os.path.abspath(working_directory)

  try:
    if not abs_path.startswith(abs_working):
      return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(abs_path):
      return f'Error: File "{file_path}" not found.'
    
    filename, extension = os.path.splitext(abs_path)
    if extension != ".py":
      return f'Error: "{file_path}" is not a Python file.'
    
    execution = subprocess.run(
      ["python3", abs_path],
      timeout=30,
      capture_output=True,
      text=True,
      cwd=abs_working
    )
    if not execution.stdout and not execution.stderr:
      return "No output produced."

    result_list = []
    if execution.stdout:
      result_list.append("STDOUT: " + execution.stdout.strip())
    if execution.stderr:
      result_list.append("STDERR: " + execution.stderr.strip())
    if execution.returncode != 0:
      result_list.append("Process exited with code " +  str(execution.returncode))


    return "\n".join(result_list)
    
  except Exception as e:
    return f"Error: executing Python file: {e}"