import os

def write_file(working_directory, file_path, content):
  abs_path = os.path.abspath(os.path.join(working_directory, file_path))
  abs_working = os.path.abspath(working_directory)

  try:
    if not abs_path.startswith(abs_working):
      return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
 
    directory, file = os.path.split(abs_path)
    os.makedirs(directory, exist_ok=True)

    with open(abs_path, "w") as f:
      f.write(content)

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

  except Exception as e:
    return f"Error: {e}"