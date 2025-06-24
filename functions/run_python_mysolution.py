import os
import subprocess

def run_python_file(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join (abs_working_dir,file_path))

    #print (f"abs working dir {abs_working_dir}")
    #print (f"abs file path {abs_file_path}")

    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    
    if not abs_file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    return_string =""
    try:
        process = subprocess.run(["python3",abs_file_path],timeout=30,capture_output=True,cwd=abs_working_dir,text=True)
        if process.stdout != "":
            return_string +=f"STDOUT: {process.stdout}"
        
        if process.stderr != "":
            return_string += f"STDERR: {process.stderr}"
        
        if return_string == "":
            return_string+="No output produced."

        if process.returncode != 0:
            return_string += f"Process exited with code {process.returncode}"
    except Exception as e:
        return_string += f"Error: executing Python file: {e}"

    return return_string

def main():
    print(run_python_file("/home/threep/bootdev/AIAgent","mytest.py"))

if __name__ == "__main__":
    main()