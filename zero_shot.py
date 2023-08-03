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
        
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": query}
        ],
       max_tokens=1000

    )
        code = response["choices"][0]["message"]["content"]
        return code
        
uclidCode = generate("Represent a model of the fibonacci sequence using two integer values in UCLID5")
uclidCodeExtract = extract_python_code(uclidCode)
print(uclidCodeExtract)
