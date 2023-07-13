#!/usr/bin/python3

import os
import sys
import openai
import tiktoken

openai.api_key = os.environ["OPENAI_API_KEY"]

query = sys.argv[1]

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

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0,
        max_tokens=1,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["\"\"\""]
    )

    classification = response["choices"][0]["text"]

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

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=rewrite,
        max_tokens=num_tokens_from_string(rewrite) + num_tokens_from_string(q) + num_tokens_from_string("Python code that uses the uclid5_api package") ,
        frequency_penalty=-2.0,
        presence_penalty=-2.0,
        stop=["\"\"\""]
    )

    rewritten_prompt = response["choices"][0]["text"]

    return rewritten_prompt


if __name__ == "__main__":
    if classify(query):
        query2 = rewrite_prompt(query).strip()
        # TODO: actually run the query now. Need to:
        # - Add info about uclid5_api to prompt
        # - Maybe add COT structure or something
        print(query2)
    else:
        print("Sorry, I can only handle queries that ask for UCLID5 code.")

