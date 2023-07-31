#!/usr/bin/python3

import os
import sys
import openai
import tiktoken
from io import StringIO
from contextlib import redirect_stdout

openai.api_key = os.environ["OPENAI_API_KEY"]


def num_tokens_from_string(string: str, encoding_name="cl100k_base") -> int:
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


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

    if "print(m)" not in output:
        output += "\nprint(m)"

    return output


def execute_python_code(text):
    f = StringIO()
    with redirect_stdout(f):
        exec(text)
    s = f.getvalue()
    return s


def classify(query):
    examples = {
        "full": ["write a UCLID5 program that represents an ATM", "give me a model a of a simple processor in uclid5", "Generate a UCLID5 module that describes an infinite sequence"],
        "init": ["write the inititalization block for a UCLID5 module that represents an ATM", "give me the init block for a UCLID5 module that models a simple processor", "Generate the init block for a UCLID5 module that describes an infinite sequence"],
        "next": ["write the next block for a UCLID5 module that represents an ATM", "give me the next block for a UCLID5 module that models a simple processor", "Generate the next block for a UCLID5 module that describes an infinite sequence", "write the transition relation for a UCLID5 module that represents an ATM", "give me the transition relation for a UCLID5 module that models a simple processor", "Generate the transition relation for a UCLID5 module that describes an infinite sequence"],
        "spec": ["write the specification for a UCLID5 module that represents an ATM", "give me the specification for a UCLID5 module that models a simple processor", "Generate the specification for a UCLID5 module that describes an infinite sequence"],
        "invalid": ["Who are you", "help me write Python code", "This is the worst day of my life."]
    }

    prompt = "Classify the request as either full, init, next, spec, or invalid.\n"
    for k, v in examples.items():
        for x in v:
            prompt += f"Query: \"{x}\"\n"
            prompt += f"Class: {k}\n"

    prompt += f"Query: \"{query}\"\n"
    prompt += f"Class: "

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0,
        max_tokens=1,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,

    )

    classification = response["choices"][0]["message"]["content"]

    if "full" == classification:
        return 0
    elif "init" == classification:
        return 1
    elif "next" == classification:
        return 2
    elif "spec" == classification:
        return 3
    else:
        return -1


def rewrite_prompt(q):
    inputs = [
        "program a UCLID5 module that randomly changes the value of a variable",
        "give me a UCLID5 module that models a simple processor",
        "Generate a UCLID5 module that describes an infinite sequence"
    ]
    outputs = [
        "Write Python code using the uclid5_api package to generate a module that randomly changes the value of a variable",
        "Use the uclid5_api package to write Python code to model a simple processor",
        "Represent a infinite sequence in Python using the uclid5_api package"
    ]

    rewrite = "Please rewrite the following queries and make sure the output requests Python code that uses the uclid5_api package.\n"

    for input, output in zip(inputs, outputs):
        rewrite += f"Original: \"{input}\"\n"
        rewrite += f"Rewritten: {output}\n"

    rewrite += f"Original: \"{q}\"\n"
    rewrite += f"Rewritten: "

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": rewrite}
        ],
        temperature=0,
        max_tokens=num_tokens_from_string(rewrite) + num_tokens_from_string(
            q) + num_tokens_from_string("Python code that uses the uclid5_api package"),
    )

    rewritten_prompt = response["choices"][0]["message"]["content"]

    return rewritten_prompt


def sys_description(rewritten_query):
    sd_prompt = "Here is a quick tutorial about the uclid5_api"
    sd_prompt += "\nThe first part of a UCLID5 module declares variables."
    sd_prompt += "\nThe first line must be \"from uclid5_api import *\"."
    sd_prompt += "\nThe second line must be \"m = Module(\"main\")\"."
    sd_prompt += "\nThe last line must be \"print(m)\"."
    sd_prompt += "\n\"Module\" is a class that models a transition system in UCLID5. You will use a single Module called \"m\"."
    sd_prompt += "\nThe \"Module\" method \"declare_var\" takes a name (string) and a UCLID5 type, and returns a new variable."
    sd_prompt += "\nFor example, \"x = m.declare_var(\"x\", integer())\" creates an integer variable called \"x\"."
    sd_prompt += "\nThis is the only method you will need to use."
    sd_prompt += "\nThe set of available types are: boolean(), integer(), real(), bitvector(width), and array(index, element)."
    sd_prompt += "\nYour output must be only executable Python code that declares variables."
    sd_prompt += "\nDo not add constraints or specifications."
    sd_prompt += "\nNo explanation needed."
    sd_prompt += "\nUse this tutorial of the uclid5_api to only create variables needed to solve: " + rewritten_query

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": sd_prompt}
        ],
        max_tokens=num_tokens_from_string(
            sd_prompt) + num_tokens_from_string(rewritten_query),
    )

    sd_python_code = response["choices"][0]["message"]["content"]
    return sd_python_code


def init_prompt(rewritten_query, python_code):
    init_prompt = "Here is a quick tutorial about the uclid5_api."
    init_prompt += "\nThe init block of UCLID5 defines the initial values of the declared variables in the module."
    init_prompt += "\nThe first line must be \"from uclid5_api import *\"."
    init_prompt += "\nThe second line must be \"m = Module(\"main\")\"."
    init_prompt += "\nThe last line must be \"print(m)\"."
    init_prompt += "\nDo not add constraints or specifications."
    init_prompt += "\nDo not declare variables in the init block."
    init_prompt += "\nDo not write helper functions."
    init_prompt += "\nThe \"init\" field of the module \"m\" is a SequentialBlock."
    init_prompt += "\nSequentialBlocks have two methods: \"assign\" and \"branch\"."
    init_prompt += "\nThese are the only two methods you will need to use."
    init_prompt += "\n\"assign\" takes two arguments: a variable, representing the left-hand-side of an assignment; and an expression, representing the right-hand-side of an assignment."
    init_prompt += "\nFor example, you can assign \"x\" the value \"0\" in the init block with \"m.init.assign(x, 0)\"."
    init_prompt += "\n\"branch\" takes one argument, a boolean expression, and returns two objects of type SequentialBlock, one for the then branch and one for the else branch."
    init_prompt += "\nFor example, \"then_, else_ = m.init.branch(x == 0)\" will create and return two new SequentialBlocks, one for when \"x == 0\" is true and the other for when \"x == 0\" is not true."
    init_prompt += "\nYour output must be only executable Python code and must continue from and include your pervious work."
    init_prompt += "\nHere was your previous work:\n" + python_code
    init_prompt += "\nUse this tutorial about the uclid5_api and your previous work to write the init block for module \"m\": " + rewritten_query
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": init_prompt}
        ],
        max_tokens=num_tokens_from_string(
            init_prompt) + num_tokens_from_string(rewritten_query),
    )

    init_python_code = response["choices"][0]["message"]["content"]

    return init_python_code


def next_prompt(rewritten_query, python_code):
    next_prompt = "Here is a quick tutorial about the uclid5_api next block."
    next_prompt += "\nThe next block defines the transition relation of the module."
    next_prompt += "\nThe first line must be \"from uclid5_api import *\"."
    next_prompt += "\nThe second line must be \"m = Module(\"main\")\"."
    next_prompt += "\nThe last line must be \"print(m)\"."
    next_prompt += "\nDo not add constraints or specifications."
    next_prompt += "\nDo not declare variables in the next block."
    next_prompt += "\nDo not write helper functions."
    next_prompt += "\nThe \"next\" field of the module \"m\" is a ConcurrentBlock."
    next_prompt += "\nConcurrentBlocks have two methods: \"assign\" and \"branch\"."
    next_prompt += "\nThese are the only two methods you will need to use."
    next_prompt += "\n\"assign\" takes two arguments: a variable, representing the left-hand-side of an assignment; and an expression, representing the right-hand-side of an assignment."
    next_prompt += "\nFor example, you can assign \"x\" the value \"0\" in the next block with \"m.next.assign(x, 0)\"."
    next_prompt += "\n\"branch\" takes one argument, a boolean expression, and returns two objects of type ConcurrentBlock, one for the then branch and one for the else branch."
    next_prompt += "\nFor example, \"then_, else_ = m.next.branch(x == 0)\" will create and return two new ConcurrentBlocks, one for when \"x == 0\" is true and the other for when \"x == 0\" is not true."
    next_prompt += "\nYour output must be only executable Python code and must continue from and include your pervious work."
    next_prompt += "\nHere was your previous work: \n" + python_code
    next_prompt += "\nUse this tutorial about the uclid5_api and your previous work to write the next block for module \"m\": " + rewritten_query

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": next_prompt}
        ],
        max_tokens=num_tokens_from_string(
            next_prompt) + num_tokens_from_string(rewritten_query),
    )

    next_python_code = response["choices"][0]["message"]["content"]

    return next_python_code


if __name__ == "__main__":
    original_query = sys.argv[1]
    failed = False
    out = ""

    todo = classify(original_query)
    print("Requested: " + str(todo))
    if todo == -1:
        print("Sorry, I can only handle queries that ask for UCLID5 code.")
        exit()

    print("-" * 80, "Rewritten Query")
    rewritten_query = rewrite_prompt(original_query).strip()
    print(rewritten_query)

    print("-" * 80, "Variable Declarations in Python")
    description = sys_description(rewritten_query)
    print(description)
    description = extract_python_code(description)
    try:
        print("-" * 80, "Variable Declarations in UCLID5")
        out = execute_python_code(description)
        print(out)
    except Exception as exception:
        print("There was an error in the generated variable declarations")
        print(exception)
        failed = True

    if (todo == 0 or todo == 1) and not failed:
        print("-" * 80, "Init Block in Python")
        init = init_prompt(rewritten_query, description)
        print(init)
        init = extract_python_code(init)
        try:
            print("-" * 80, "Init Block in UCLID5")
            out = execute_python_code(init)
            print(out)
        except Exception as exception:
            print("There was an error in the generated init block")
            print(exception)
            failed = True

    if (todo == 0 or todo == 2) and not failed:
        print("-" * 80, "Next Block in Python")
        next = next_prompt(rewritten_query, init) if todo == 0 else next_prompt(
            rewritten_query, description)
        print(next)
        next = extract_python_code(next)
        try:
            print("-" * 80, "Next Block in UCLID5")
            out = execute_python_code(next)
            print(out)
        except Exception as exception:
            print("There was an error in the generated next block")
            print(exception)
            failed = True

    if todo == 3 and not failed:
        print("Sorry, I cannot write specifications yet.")
        failed = True

    print("-" * 80, "Final UCLID5 Module")
    print(out)
