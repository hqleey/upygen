import os
import sys
import openai
import tiktoken
from io import StringIO
from contextlib import redirect_stdout

def extract_python_code(text):
    output = ""
    grabbing = False
    for l in text.splitlines():
        if l.strip() == "```":
            break
        elif grabbing and l:
            output += l + "\n"
        elif l.strip() in ["```python", "```python3", "```py", "```py3", "```"]:
            grabbing = True

    # If we never saw ```python then assume all of it is code
    if not grabbing:
        output = text


    return output



def num_tokens_from_string(string: str, encoding_name="cl100k_base") -> int:
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def generate(query):
        
        fs_prompt = "Here is an example of a UCLID5 Module"
        fs_prompt += "\n module main {"
        fs_prompt += "\n// Part 1: System description."
        fs_prompt += "\nvar a, b : integer;"
        fs_prompt += "\ninit {"
        fs_prompt += "\na = 0;"
        fs_prompt += "\nb = 1;"
        fs_prompt += "\n}"
        fs_prompt += "\nnext {"
        fs_prompt += "\na\', b\' = b, a + b;"
        fs_prompt += "\n}"

        fs_prompt += "\n// Part 2: System specification."
        fs_prompt += "\ninvariant a_le_b: a <= b;"
        fs_prompt += "\n// Part 3: Proof script."
        fs_prompt += "\ncontrol {"
        fs_prompt += "\nbmc (3);"
        fs_prompt += "\ncheck;"
        fs_prompt += "\nprint_results;"
        fs_prompt += "\n}"
        fs_prompt += "\n Use this example to : " + query
        fs_prompt += "only produce UCLID5 code"
    
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": fs_prompt}
        ],
       max_tokens=num_tokens_from_string(fs_prompt) + num_tokens_from_string(query)

    )
        code = response["choices"][0]["message"]["content"]
        return code
        
uclidCode = generate("Represent a model of the fibonacci sequence using two integer values in UCLID5")
uclidCodeExtract = extract_python_code(uclidCode)
print(uclidCodeExtract)
