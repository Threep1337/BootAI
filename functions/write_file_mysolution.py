import os

def write_file(working_directory, file_path, content):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join (abs_working_dir,file_path))

    #print (f"abs working dir {abs_working_dir}")
    #print (f"abs file path {abs_file_path}")

    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    try:
        #print(f"abs file path is {abs_file_path}")

        #print(f"dirname is {os.path.dirname(abs_file_path)}")

        if not os.path.exists(os.path.dirname(abs_file_path)):
            #print(f"Creating dir {os.path.dirname(abs_file_path)}")
            #Create the parent dir
            os.makedirs(os.path.dirname(abs_file_path))
        
        #print("right before with with block")
        with open(abs_file_path,"w") as f:
            #print(f"writing to the file {abs_file_path}")
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
    except Exception as e:
        return f"Error listing files: {e}"


def main():
    write_file("/home/threep/bootdev/AIAgent","test/testfile.txt","this is a test")


if __name__ == "__main__":
    main()