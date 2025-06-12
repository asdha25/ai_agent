import os

def get_files_info(working_directory, directory=None):
  if directory is None or directory == ".":
    directory = working_directory
  try:
    abs_working = os.path.abspath(working_directory)
    abs_directory = os.path.abspath(directory)
    if not abs_directory.startswith(abs_working):
      return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(abs_directory):
      return f'Error: "{directory}" is not a directory'
    
    list_path = []

    for path in sorted(os.listdir(abs_directory)):
      full_path = os.path.join(abs_directory, path)
      if os.path.isfile(full_path):
        size = os.path.getsize(full_path)
      elif os.path.isdir(full_path):
        size = 128
      else:
        continue
      
      list_path.append(f"- {path}: file_size={size} bytes, is_dir={os.path.isdir(full_path)}")
    
    return "\n".join(list_path)
  
  except Exception as e:
    return f"Error: {e}"