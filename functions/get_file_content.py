import os


def get_file_content(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join (abs_working_dir,file_path))

    #print (f"abs working dir {abs_working_dir}")
    #print (f"abs file path {abs_file_path}")

    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(abs_file_path) or not os.path.isfile(abs_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(abs_file_path) as file:
            content = file.read()
        return content
    except Exception as e:
        return f"Error: {e}"


def main():
    pass


if __name__=="__main__":
    main()