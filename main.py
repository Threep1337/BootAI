import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.call_function import call_function
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python import run_python_file
from functions.write_file import write_file

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Gets the text contents of a file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file, relative to the working directory. Must be a file, if the path is a directory an error will be returned.",
            ),
        },
    ),
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Used to run a file. Use this if the user asks to run a file. Constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to run, relative to the working directory. Must be a file with a .py extension, otherwise an error will be returned.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional arguments to pass to the Python file.",
                ),
                description="Optional arguments to pass to the Python file.",
            ),
        },
        required=["file_path"],
    ),
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes text to a file, constrained to the working directory.  If the file already exists, its content will be overwritten.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
    ),
)

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,schema_get_file_content,schema_run_python_file,schema_write_file
    ]
    )


    if len(sys.argv) == 1:
        raise Exception("Error, you need to provide a prompt!")
    question = sys.argv[1]
    verbose = False
    if len(sys.argv) == 3 and sys.argv[2] == "--verbose":
        verbose = True
        print (f"User prompt: {question}")

    

    messages = [
    types.Content(role="user", parts=[types.Part(text=question)]),
    ]


    client = genai.Client(api_key=api_key)
    config = types.GenerateContentConfig(system_instruction=system_prompt, tools=[available_functions])
    response = client.models.generate_content(model="gemini-2.0-flash-001",contents=messages,config=config)

    
    
    if len(response.function_calls) > 0:
        for function_call in response.function_calls:
            #print(f"Calling function: {function_call.name}({function_call.args})")
            if verbose:
                function_call_result = call_function(function_call,True)
            else:
                function_call_result = call_function(function_call)

            function_call_result_text = function_call_result.parts[0].function_response.response
            if not function_call_result_text:
                raise Exception("No function call results")
            
            if verbose:
                print (print(f"-> {function_call_result.parts[0].function_response.response}"))
    else:
        print (response.text)

    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()