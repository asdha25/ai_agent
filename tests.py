import os
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

#print(get_files_info(".", "."))
#print(get_files_info(".", "pkg"))
#print(get_files_info(".", "/bin"))
#print(get_files_info(".", "../"))

#print(get_file_content(".", "lorem.txt"))

#print(get_file_content(".", "main.py"))
#print(get_file_content(".", "pkg/calculator.py"))
#print(get_file_content(".", "/bin/cat"))

#print(write_file(".", "lorem.txt", "wait, this isn't lorem ipsum"))
#print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
#print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))

print(run_python_file("calculator", "main.py"))
print(run_python_file("calculator", "tests.py"))
print(run_python_file("calculator", "../main.py"))
print(run_python_file("calculator", "nonexistent.py"))