import os


def get_files_info(working_directory, directory=None,verbose=False):
    working_directory_contents = os.listdir(working_directory)

    if directory == ".":
        directory = None

    if (verbose):
        print(f"Working directory contents is:{working_directory_contents}")

    if directory and not directory in working_directory_contents:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    elif directory and not os.path.isdir(os.path.join(working_directory,directory)):
        return f'Error: "{directory}" is not a directory'

    if directory:
        full_directory_path = os.path.join(working_directory,directory)
    else:
        full_directory_path = working_directory


    directory_contents = os.listdir(full_directory_path)
    file_strings=[]
    for item in directory_contents:
        item_path = os.path.join(full_directory_path,item)
        item_is_dir = os.path.isdir(item_path)
        item_size = os.path.getsize(item_path)
        file_strings.append(f"- {item}: file_size={item_size}, is_dir={item_is_dir}")

    return_string = "\n".join(file_strings)
    return return_string
    if (verbose):
        print(return_string)
        #- README.md: file_size=1032 bytes, is_dir=False

def main():
    print(get_files_info('/home/threep/bootdev/AIAgent'))

if __name__=="__main__":
    main()