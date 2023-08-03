# Practice Code Hub

A collection of coding interview questions and solutions for practice. 
This repository aims to improve problem-solving skills and prepare for technical interviews. 
Questions are categorized by topics like Arrays, Linked Lists, Trees, Sorting, etc. Solutions are provided in Python, Golang. Contributions are welcome!

Utility classes like tree_util.py for handling tree-related operations efficiently are available. 
Contribute your own solutions or add new coding questions to expand the repository and make it a valuable resource for the programming community. 
Happy coding and good luck with technical interviews! Let's practice together and excel in our coding journey! 🚀👩‍💻👨‍💻

Coding questions are organized into categories, each containing individual question folders. 
Within each folder, find a detailed question description, sample input, and output. Solution files in different programming languages, including Python, Golang, and more, are provided.


```
PracticeCodeHub/
|-- Questions/                           # Directory for all the questions
|   |-- Category1/                       # Category 1 questions
|   |   |-- question_1.md               # Description of Question 1 with sample input/output
|   |   |-- Question1/                  # Solutions for Question 1
|   |   |   |-- Python/                 # Python solutions
|   |   |   |   |-- solution.py         # Python solution for Question 1
|   |   |   |   |-- solution_test.py    # Test cases for Python solution
|   |   |   |-- Golang/                 # Golang solutions
|   |   |   |   |-- solution.go         # Golang solution for Question 1
|   |   |   |   |-- solution_test.go    # Test cases for Golang solution
|   |   |-- Question2/                  # Folder for Question 2 (similar structure as Question 1)
|   |   |   |-- ...
|   |-- Category2/                       # Category 2 questions (similar structure as Category 1)
|   |   |-- ...
|-- CommonResources/                     # Common resources for programming languages
|   |-- Python/                          # Python related resources
|   |   |-- requirements.txt             # Python dependencies
|   |   |-- tree_util.py                 # Utility class for tree-related operations (Python)
|   |   |-- pytest.ini                   # Configuration file for pytest (Python)
|   |-- Golang/                          # Golang related resources
|   |   |-- go.mod                       # Golang dependencies
|-- README.md                            # Repository's main README file

```

# Instructions for Generating Python Solution Templates

To maintain a consistent template structure for Python solutions in this repository, there is a script called "gen_python_solution_template.py". This script automates the creation of Python solution and test files for new questions that don't have a Python solution folder yet.

## Usage:

1. Ensure that you have Python installed on your system.

2. Navigate to the root directory of the repository.

3. Add a new question `.md` file for the question you want to add a Python solution to. Ensure the filename of the `.md` file represents the question in some way and follows the suggested format: `{appropriate_filename}.md`. The appropriate filename can be an alphanumeric string with a maximum of 32 characters. For example, "two_sum_problem.md", "maximum_subarray.md", "find_common_elements.md", etc.

4. Before running the gen_python_solution_template.py script, carefully read the MD format guidelines to ensure that your .md file adheres to the provided format. The input and output sections should be clearly marked with ## Sample Input and ## Expected Output, respectively. The input section should end with --- to separate it from the output section.

5. Run the `gen_python_solution_template.py` script by executing the following command in the terminal:

    ```
    python gen_python_solution_template.py
    ```

6. The script will search for `.md` question files that don't have a corresponding Python solution folder. It will create two Python solution files for each question that meets the criteria:

    - `solution.py`: This file contains the Python function to solve the question.
    - `solution_test.py`: This file contains test cases to validate the correctness of the solution.

7. If the `-f` flag is explicitly provided with the filepath of an existing `.md` file (e.g., `python gen_python_solution_template.py -f Questions/Category1/question_1.md`), and the `solution.py` file already exists in the corresponding Python solution folder, the script will create an additional solution file named `solution_1.py` for that question. This allows having multiple solution files for a single question.

8. Once the script completes, the newly generated Python solution folders will be found inside the respective question directories under the `Solutions/Python` folder.

Please use this script whenever you add a new question or want to create additional Python solution templates. It ensures consistency and saves time in setting up the initial structure for each question.


# Markdown File Format Guidelines:

1. Use ## Sample Input to denote the beginning of the input section.
2. Use ## Expected Output to denote the beginning of the output section.
3. The input and output sections should contain the sample input and output, respectively.
4. The input section should end with --- to separate it from the output section.
5. Follow the provided format to ensure consistency and readability of the .md files.


## Example:

Suppose you have a question file named `two_sum_problem.md` 
as 
```
question description .....
....
....

## sample input  
array = [1,2,4,5]
targetSum = 10

---

## expected output
[-1 , 10] // can be in reverse order as well 

---
```
in the `Questions/Category1/` directory. After running the script, the folder structure will look like this:


```
PracticeCodeHub/
|-- Questions/
| |-- Category1/
| | |-- two_sum_problem.md
| | |-- two_sum_problem/
| | | |-- Python/
| | | | |-- solution.py
| | | | |-- solution_test.py

```
where solution.py looks like
```
def solution_func(array: list, target_sum: int) -> list:
    return []

```
and solution_test.py looks like
```
from solution import solution_func

test_cases = [
    ({'array': [1,2,4,5], 'target_sum': 10}, [-1, 10]),  # input, output
]


def test_solution_func():
    for input_kwargs, output in test_cases:
        assert solution_func(**input_kwargs) == output

```
note: in test_case file you can add further cases with input and expected output in test_cases list 

With this example, it can be observed that the script creates a new folder named two_sum_problem inside the Questions/Category1/ directory. Within this folder, the script generates the solution.py and solution_test.py files in the Python subfolder for the question. Similarly, the script maintains the structure for Golang solutions as well.