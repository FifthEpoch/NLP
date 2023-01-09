import re
from random import randrange

def rogerian_resp(_input):

    _input = _input.lower()

    responses = {0: "Tell me more.",
                 1: "What makes you say that?",
                 2: "Could you give me an example?",
                 3: "Hmm. Why would that be?",
                 4: "Please, go on.",
                 5: "Help me understand more.",
                 6: "Mhm. "}

    m = re.match(".*i.*(?:feeling|feel|felt).*(depressed|sad|down|upset|irrated|mad|crazy|angry|anxious|stressed|bad|blue).*", _input)
    if m:
        comp = re.compile(r".*i.*(?:feeling|feel|felt).*(depressed|sad|down|upset|irrated|mad|crazy|angry|anxious|stressed|bad|blue).*")
        output = comp.sub(r"Why do you think you feel \1?", _input)
        return output.capitalize()

    m = re.match(".*i.*(depressed|sad|down|upset|irrated|mad|crazy|angry|anxious|stressed|bad|blue).*", _input)
    if m:
        comp = re.compile(r".*i(?:'m)?.*(depressed|sad|down|upset|irrated|mad|crazy|angry|anxious|stressed|bad|blue).*")
        output = comp.sub(r"I'm sorry to hear that you're \1.", _input)
        return output.capitalize()

    m = re.match(".*i.*(?:feeling|feel|felt).*(glad|happy|grateful|up|optimistic|good|excited|great|well).*",
                 _input)
    if m:
        comp = re.compile(
            r".*i.*(?:feeling|feel|felt).*(glad|happy|grateful|up|optimistic|good|excited|great|well).*")
        output = comp.sub(r"I'm glad to hear that. Why do you think you feel \1?", _input)
        return output.capitalize()

    m = re.match(".* all .*", _input)
    if m:
        comp = re.compile(r".* all .*")
        output = comp.sub(r"In what way?", _input)
        return output

    m = re.match(".* always .*", _input)
    if m:
        comp = re.compile(r".* always .*")
        output = comp.sub(r"Can you think of a specific example?", _input)
        return output

    m = re.match("(?:^|.*) (i|my|me) ", _input)
    if m:
        if len(_input) > 35:
            randint = randrange(6)
            return responses[randint]
        comp_strip = re.compile(r".*(?:but|however|though|although|and|because|,|\.) (.*)")
        output = comp_strip.sub(r"\1", _input)

        comp_i = re.compile(r"\b(i)\b")
        comp_am = re.compile(r"\b(am)\b")
        comp_my = re.compile(r"\b(my)\b")
        comp_me = re.compile(r"\b(me)\b")
        output = comp_i.sub(r"you", output)
        output = comp_am.sub(r"are", output)
        output = comp_my.sub(r"your", output)
        output = comp_me.sub(r"you", output)

        return output.capitalize()

    m = re.match(".*\b(hi|hello|hey)\b.*", _input)
    if m:
        comp = re.compile(r".*\b(hi|hello|hey)\b.*")
        output = comp.sub(r"\1. Could you tell me more about what brought you here today?", _input)
        return output.capitalize()

    m = re.match(".*\?$", _input)
    if m:
        comp = re.compile(r".*(?:., |, |; |! |\? )(.+)\?$")
        output = comp.sub(r"\1.", _input)
        return output.capitalize()

    randint = randrange(7)
    return responses[randint]

def respond():
    user_input = input("USER: ")
    output = rogerian_resp(user_input)
    print(f"ELIZ: {output}")

while True:
    respond()