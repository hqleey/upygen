#!/usr/bin/python3

import os
import sys
import openai
import tiktoken

openai.api_key = os.environ["OPENAI_API_KEY"]

def num_tokens_from_string(string: str, encoding_name="cl100k_base") -> int:
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def classify(query):
    examples = {
        "valid": ["write a UCLID5 module that represents an ATM", "give me a UCLID5 module that models a simple processor", "Generate a UCLID5 module that describes an infinite sequence"],
        "invalid": ["Who are you", "help me write Python code", "This is the worst day of my life."]
    }

    prompt = "Classify the query as either valid or invalid. " 
    prompt += "The query should only be valid if it asks for UCLID5 code.\n"
    for k,v in examples.items():
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

    if not ("valid" in classification and not "invalid" in classification):
        return False
    else:
        return True

def rewrite_prompt(q):
    inputs =  [
        "program a UCLID5 module that randomly changes the value of a variable",
        "give me a UCLID5 module that models a simple processor", 
        "Generate a UCLID5 module that describes an infinite sequence"
    ]
    outputs =  [
        "Write Python code using the uclid5_api package to generate a module that randomly changes the value of a variable", 
        "Use the uclid5_api package to write Python code to model a simple processor", 
        "Represent a infinite sequence in Python using the uclid5_api package"
    ]

    rewrite = "Please rewrite the following queries and make sure the output requests Python code that uses the uclid5_api package.\n" 

    for input,output in zip(inputs,outputs):
        rewrite += f"Original: \"{input}\"\n"
        rewrite += f"Rewritten: {output}\n"

    rewrite += f"Original: \"{q}\"\n"
    rewrite += f"Rewritten: "

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": rewrite}
        ],
        max_tokens=num_tokens_from_string(rewrite) + num_tokens_from_string(q) + num_tokens_from_string("Python code that uses the uclid5_api package") ,
        frequency_penalty=-2.0,
        presence_penalty=-2.0,

    )

    rewritten_prompt = response["choices"][0]["message"]["content"]

    return rewritten_prompt

def run_query(query):
    api_prompt = query
    api_prompt += "\nThe first line must be \"from uclid5_api import *\"."
    api_prompt += "\nThe second line must be \"m = Module(\"main\")\"."
    api_prompt += "\nThe last line must be \"print(m)\"."
    api_prompt += "\n\"Module\" is a class that models a transition system in UCLID5. You will use a single Module called \"m\"."
    api_prompt += "\nThe \"Module\" method \"declare_var\" takes a name (string) and a UCLID5 type, and returns a new variable."
    api_prompt += "\nFor example, \"x = m.declare_var(\"x\", integer())\" creates an integer variable called \"x\"."
    api_prompt += "\nThe \"Module\" field \"init\" represents the initialization block of the transition system."
    api_prompt += "\nThe \"Module\" field \"next\" represents the transition relation block of the transition system."
    api_prompt += "\nBoth \"init\" and \"next\" are object of type \"Block\"."
    api_prompt += "\n\"Block\" objects have two methods: \"assign\" and \"branch\"."
    api_prompt += "\n\"assign\" takes two arguments: a variable, representing the left-hand-side of an assignment; and an expression, representing the right-hand-side of an assignment."
    api_prompt += "\nFor example, you can assign \"x\" the value \"0\" in the init block with \"m.init.assign(x, 0)\"."
    api_prompt += "\nFor example, you can assign \"x\" the value \"x + x\" in the next block with \"m.next.assign(x, x + x)\"."
    api_prompt += "\n\"branch\" takes one argument, a boolean expression, and returns two objects of type \"Block\"."
    api_prompt += "\nFor example, you can branch on the value of \"x\" being greater than zero with \"then_, else_ = m.next.branch(x > 0)\"."
    api_prompt += "\nNow use this information about the uclid5_api to write the correct Python code."

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": api_prompt}
        ],
        max_tokens=num_tokens_from_string(api_prompt) + num_tokens_from_string(query),
    )

    python_code = response["choices"][0]["message"]["content"]

    return python_code




if __name__ == "__main__":
    original_query = sys.argv[1]

    if not classify(original_query):
        print("Sorry, I can only handle queries that ask for UCLID5 code.")

    rewritten_query = rewrite_prompt(original_query).strip()

    code = run_query(rewritten_query)

    print("\\\\ Rewritten query: ")
    print("\\\\ " + "\n\\\\ ".join(rewritten_query.splitlines()))
    print("\\\\ Python code to run: ")
    print("\\\\" + "\n\\\\ ".join(code.splitlines()))
    print("\\\\ Resulting UCLID5 code: ")

    try:
        exec(code)
    except:
        print("Ooops, there was an error in the generated Python code :(")

