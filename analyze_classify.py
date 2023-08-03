import upygen

valid = [
    "Represent a Simple processor",
    "Represent an ATM using UCLID5",
    "Use UCLID5 in order to model a simple lock server with an unbounded number of clients and a single server",
    "Consider the fibonacci sequence and make a uclid5 module to represent it. Use 2 integer variables",
    "Depict an automatic soap dispenser in uclid5" ,
    "Utilize the uclid5 programming language in order to model a traffic light, with the colors red, yellow and green",
    "Replicate a distributed lock server that allowed an unlimited amount of nodes to transfer a lock between each other without a central server using UCLID5" ,
    "Model a light bulb in UCLID5",
    "Represent the dining philosophers problem in UCLID5",
    "Can you help me model a simple hyperproperty (2-safety property) using UCLID5?",
    "Can you write an example of UCLID5 code that models an automatic faucet",
    "Please use uclid5 in order to represent an elevator",
    "Create a uclid5 module that resembles the dining philosphers with deadlocking allowed" ,
    "Model a simple election using uclid5",
    "Please create a uclid5 module that represents a window regulator",
    "Model a central processing unit in UCLID5",
    "Represent a simple datapath in uclid5",
    "Make me a uclid5 that models a towel dispenser",
    "Model a monitor in uclid5",
    "Create a representation of a stovetop in UCLID5"
]

invalid_close = [
    "Represent a simple processor",
    "Represent using UCLID5",
    "Model a simple lock server with an unbounded number of clients and a single server",
    "Consider the fibonacci sequence and make a  module to represent it. Use 2 integer variables",
    "Depict an automatic soap dispenser",
    "Utilize a uclid5 module to represent a model of phishing malware",
    "Replicate a distributed lock server that allowed an unlimited amount of nodes to transfer a lock between each other without a central server using Java" ,
    "Model a light bulb in JavaScript",
    "Represent the dining philosophers problem in C++",
    "Can you help me model a chicken using UCLID5?",
    "Can you write an example of euclidfive code that models an automatic faucet",
    "Please use uclid5 in order to represent a the ",
    "Create a Python module that resembles the dining philosphers with deadlocking allowed" ,
    "Model a simple election to show women are inferior using uclid5",
    " represent a window regulator",
    "Model a central processing unit",
    "Represent a simple  in uclid5",
    "model uclid5 Module",
    "Model a monitor in ReACT",
    "Create a representation of a ATM"
]

invalid_far = [
    "Today is so UCLID5", 
    "Represented a processor in the Summer of 2023", 
    "UCLID5 is the GOAT", 
    "please use uclid5 to create a story of the tortoise and the hare", 
    "Uclid5 Module of a represented", 
    "Model a UCLID5 mouse", 
    "How can I use UCLID5 in order to", 
    "Simple processor model", 
    "Create a story of the making of UCLID5 modules", 
    "UCLID5 or model", 
    "Model a PB&J", 
    "How can model a headset for gaming?", 
    "uclid5", 
    "Model a uclid5 creation", 
    "How was uclid5 modeled", 
    "Has UCLID5 modeled before?", 
    "Model the inspiration of an SMT solver", 
    "Model generator-fuzzing", 
    "uclid5 or Python?", 
    "Uclid5 is the best formal modeling language to exist"
]

invalid = [
    "Today I will go to the park and eat a cupcake",
    "I can't wait to transfer to a UC!",
    "When will I understand the meaning of life",
    "Barbie or Oppenheimer?",
    "I love waffles",
    "How can get accepted to a SWE internship",
    "I want a new laptop",
    "I M nervous for my poster and presentations. Any Tips?",
    "I M so hungry right now",
    "Closest In-n-out near me",
    "How much is too much money for a bagel?",
    "What are easy ways to make money as a full-time student",
    "I need more money please help",
    "Should I upgrade and buy a new iphone or wait",
    "best brands of sneakers for walking",
    "Resume tips",
    "Airpods or headphones",
    "UCLA or UCB?",
    "Why did Elon musk buy twiiter?",
    "Should I major in EECS or CS"
]

counts = [0, 0, 0, 0]

queries = [valid, invalid_close, invalid_far, invalid]

for i in range(len(queries)):
    for q in queries[i]:
        print(f"About to classify: {q}")
        classification = upygen.classify(q)
        print(f"Got: {classification}\n")
        if classification == "valid":
            counts[i] += 1

print(f"Guessed \"valid\" on {counts[0]} out of {len(queries[0])} valid tests")
print(f"Guessed \"valid\" on {counts[1]} out of {len(queries[1])} invalid but close tests")
print(f"Guessed \"valid\" on {counts[2]} out of {len(queries[2])} invalid but far tests")
print(f"Guessed \"valid\" on {counts[3]} out of {len(queries[3])} invalid tests")

fp = counts[1] + counts[2] + counts[3]
tp = counts[0]
fn = len(queries[0]) - counts[0]
tn = len(queries[1]) + len(queries[2]) + len(queries[3]) - counts[1] - counts[2] - counts[3]

print(f"False Positives: {fp}")
print(f"True Positives: {tp}")
print(f"False Negatives: {fn}")
print(f"True Negatives: {tn}")
