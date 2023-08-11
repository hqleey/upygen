import subprocess
import upygen

def is_correct_syntax(code):
    with open("temp.ucl", 'w') as f:
        f.write(code)

    result = subprocess.run(
            ["uclid", "-g", "tmp", "temp.ucl"],
            capture_output = True,
            text = True)
    
    if "Syntax error" in result.stdout:
        return False

    return True

error = [0,0,0]
def where_error_occurred(code):
    if "//there was an error in the generated  variable declaration" in code:
        error[0] += 1

    elif "//there was an error in the generated init block" in code:
        error[1] +=1
    elif "//there was an error in the generated next block" in code:
        error[2] +=1
    else:
        print("No Syntax errors detected")




valid_queries = [
    "represent a simple processor using UCLID5",
"Represent an ATM using UCLID5",
"Use UCLID5 in order to model a simple lock server with an unbounded number of clients and a single server",
"Consider the fibonacci sequence and make a uclid5 module to represent it. Use 2 integer variables",
"Depict an automatic soap dispenser in uclid5", 
"Utilize the uclid5 programming language in order to model a traffic light, with the colors red, yellow and green",
"Replicate a distributed lock server that allowed an unlimited amount of nodes to transfer a lock between each other without a central server using UCLID5", 
"Model a light bulb in UCLID5",
"Represent the dining philosophers problem in UCLID5",
"Can you help me model a simple hyperproperty (2-safety property) using UCLID5?",
"Can you write an example of UCLID5 code that models an automatic faucet",
"Please use uclid5 in order to represent an elevator",
"Create a uclid5 module that resembles the dining philosphers with deadlocking allowed", 
"Model a simple election using uclid5",
"Please create a uclid5 module that represents a window regulator",
"Model a central processing unit in UCLID5",
"Represent a simple datapath in uclid5",
"Make me a uclid5 that models a towel dispenser",
"Model a monitor in uclid5",
"Create a representation of a stovetop in UCLID5"

# "Represent a traffic light in UCLID5",
# "Represent a traffic light in UCLID5",
# "Represent a traffic light in UCLID5",
# "Represent a traffic light in UCLID5",
# "Represent a traffic light in UCLID5",
# "Represent a traffic light in UCLID5",
# "Represent a traffic light in UCLID5",
# "Represent a traffic light in UCLID5",
# "Represent a traffic light in UCLID5",
# "Represent a traffic light in UCLID5",
# "Represent a traffic light in UCLID5",
# "Represent a traffic light in UCLID5",
# "Represent a traffic light in UCLID5",
# "Represent a traffic light in UCLID5",
# "Represent a traffic light in UCLID5"


    ]




# code = upygen.generate(...)
# if is_correct_syntax(code):
#     ...
     

# Need some valid prompts

# Need to run generate on each prompt

good_syntax = 0
bad_syntax = 0
for str in valid_queries:
    print(str)
    code = upygen.generate(str)
    print(is_correct_syntax(code))
    where_error_occurred(code)
    if is_correct_syntax(code) == True:
        good_syntax+= 1
    else:
        bad_syntax +=1

print(f"The upygen generator produced syntactically correct code {good_syntax} many times for {len(valid_queries)}")
print(f"The upygen generator produced syntactically incorrect code {bad_syntax} many times for {len(valid_queries)}")
print(f"Errors occured in  variable declaration: {error[0]}, \nErrors occured in init block {error[1]}, \nErrors occured in next block {error[2]}")



       

# After generating, need to check if syntactically correct. But how?! By calling "is_correct_syntax"
