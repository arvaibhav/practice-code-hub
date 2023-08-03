import argparse
import ast
import re
import os
from CommonResources.Python.graph_util import Graph
from CommonResources.Python.tree_util import Tree


def extract_content_inside_parentheses(text):
    match = re.search(r'\((.*?)\)', text)
    return match.group(1) if match else None


def remove_comments(text):
    return re.sub(r"\/\/.*", "", text)


def evaluate_value(value: str):
    if "tree" in value.lower():
        value = Tree(evaluate_value(extract_content_inside_parentheses(value.replace("tree", ""))))
    elif 'graph' in value.lower():
        value = Graph(evaluate_value(extract_content_inside_parentheses(value.replace("graph", ""))))

    try:
        return ast.literal_eval(value)
    except (ValueError, SyntaxError):
        return value


def extract_samples_from_string(input_str):
    content = remove_comments(input_str)

    input_matches = re.findall(r'(?i)##\s*sample\s*input\s+(.*?)\s*---', content, re.DOTALL)
    output_matches = re.findall(r'(?i)##\s*expected\s*output\s+(.*?)\s*---', content, re.DOTALL)

    if not (input_matches and output_matches):
        raise ValueError("Sample input or output not found in the input text.")

    input_dict = {}
    for inp in input_matches:
        lines = inp.split('\n')
        for line in lines:
            if line.strip():
                key, value = line.split("=")
                input_dict[key.strip()] = evaluate_value(value.strip())

    if len(output_matches) > 1:
        raise Exception("More than 1 output")

    output = evaluate_value(output_matches[0].strip())
    return input_dict, output


def convert_to_snake_case(input_string):
    # Remove special characters and replace spaces and hyphens with underscores
    cleaned_string = re.sub(r'[^a-zA-Z0-9]', ' ', input_string)
    words = cleaned_string.split()

    # Split on uppercase letters in camel case
    words = [re.sub('([a-z0-9])([A-Z])', r'\1 \2', word).split() for word in words]
    words = [item for sublist in words for item in sublist]

    # Join the words with underscores and convert to lowercase
    snake_case_string = '_'.join(words).lower()
    return snake_case_string


def generate_function_definition(input_kwargs, output_arg):
    other_import_str = ""
    type_mapping = {
        dict: "dict",
        list: "list",
        set: "set",
        tuple: "tuple",
        None: "None",
    }
    type_import_mapping = {
        'tree': "from CommonResources.Python.tree_util import Tree",
        "graph": "from CommonResources.Python.graph_util import Graph"
    }
    snake_case_input_kwargs = {convert_to_snake_case(key): value for key, value in
                               input_kwargs.items()}

    input_strs = []
    for key, value in snake_case_input_kwargs.items():
        if value.__class__ in type_mapping:
            value = type_mapping[value.__class__]
        else:
            value = value.__class__.__name__
            import_str = f"{type_import_mapping.get(value.lower(), '')}"
            if import_str:
                if other_import_str:
                    other_import_str = other_import_str.strip()
                other_import_str += f"{import_str}\n\n"

        input_strs.append(f"{key}: {value}")

    input_args_str = ', '.join(input_strs)

    if output_arg.__class__ in type_mapping:
        return_type = type_mapping[output_arg.__class__]
    else:
        return_type = output_arg.__class__.__name__
        import_str = f"{type_import_mapping.get(return_type.lower(), '')}"
        if import_str:
            if other_import_str:
                other_import_str = other_import_str.strip()
            other_import_str += f"{import_str}\n\n\n"
    if return_type in ['int', 'None']:
        return_default_value = "None"
    elif return_type == 'list':
        return_default_value = "[]"
    else:
        return_default_value = f"{return_type}()"

    function_name = "solution_func"
    function_def = f"{other_import_str}def {function_name}({input_args_str}) -> {return_type}:\n    return {return_default_value}"

    test_case_function = f"""{other_import_str}from solution import {function_name}

test_cases = [
    ({snake_case_input_kwargs}, {output_arg}),  # input, output
]


def test_{function_name}():
    for input_kwargs, output in test_cases:
        assert {function_name}(**input_kwargs) == output
"""

    return function_def, test_case_function


def find_md_file(md_filename):
    for root, _, files in os.walk("Questions"):
        for file in files:
            if file.lower() == md_filename.lower():
                return os.path.join(root, file)
    return None


def create_folder_structure(md_filepath):
    folder_name = os.path.splitext(os.path.basename(md_filepath))[0]
    folder_path = os.path.join(os.path.dirname(md_filepath), folder_name)
    python_folder_path = os.path.join(folder_path, "Python")

    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
    if not os.path.exists(python_folder_path):
        os.mkdir(python_folder_path)

    return folder_path, python_folder_path


def create_solution_files(python_folder_path, function_definition, create_new_sol):
    if not create_new_sol:
        file_name = os.path.join(python_folder_path, "solution.py")
    else:
        suffix = 1
        while True:
            file_name = os.path.join(python_folder_path, f"solution_{suffix}.py")
            if os.path.exists(file_name):
                suffix += 1
            else:
                break

    with open(file_name, "w") as file:
        file.write(function_definition)
    return file_name


def create_solution_test_files(solution_file_path, function_definition):
    solution_file_name = os.path.splitext(os.path.basename(solution_file_path))[0]
    with open(solution_file_path.replace(".py", "_test.py"), "w") as file:
        file.write(function_definition.replace("from solution import ", f"from {solution_file_name} import "))


def main(md_filepath=None):
    if md_filepath and not os.path.exists(md_filepath):
        print(f"Error: File '{md_filepath}' not found ")
        return

    if not md_filepath:
        md_filepath = None
        for root, _, files in os.walk("Questions"):
            for file in files:
                if ".md" in file:
                    folder_name = os.path.splitext(file)[0]
                    if not os.path.exists(os.path.join(root, folder_name)):
                        md_filepath = os.path.join(root, file)
                        break
            if md_filepath:
                break

    if md_filepath:
        folder_name = os.path.splitext(os.path.basename(md_filepath))[0]
        python_folder_path = os.path.join(os.path.dirname(md_filepath), folder_name, "Python")
        solution_file_path = os.path.join(python_folder_path, "solution.py")
        create_new_sol = os.path.exists(python_folder_path) and os.path.exists(solution_file_path)

        with open(md_filepath, "r") as md_file:
            input_str = md_file.read()
        input_kwargs, output_arg = extract_samples_from_string(input_str)

        if not (input_kwargs and output_arg):
            print(f"Error: Unable to extract input or output from {md_filepath}.")
            return

        function_definition, function_test_def = generate_function_definition(input_kwargs, output_arg)
        folder_path, python_folder_path = create_folder_structure(md_filepath)
        solution_file_name = create_solution_files(python_folder_path, function_definition, create_new_sol)
        create_solution_test_files(solution_file_name, function_test_def)

        print(f"Created files for '{folder_name}' in '{python_folder_path}'.")
    else:
        print("No unprocessed .md file found in the 'Questions' folder.")


if __name__ == "__main__":
    # Create the argparse parser
    parser = argparse.ArgumentParser(description="Script to process .md files")

    # Add an argument for the -f option
    parser.add_argument("-f", "--file_path", help="Specify the .md filename")

    # Parse the command-line arguments
    args = parser.parse_args()

    # Call the main function with the filename argument
    main(args.file_path)
