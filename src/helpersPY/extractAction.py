import re #RegeX based searching

class ExecutableAction:
    def __init__(self, type, args):
        self.type = type #String of 'clickElement'|'setValue'|'finish'
        self.args = args #Dictionary of 'id' and 'value' (value optional)

class ExtractedAction:
    def __init__(self, thought, action, executableAction):
        self.thought = thought #String
        self.action = action #String
        self.executableAction = executableAction #ExecutableAction Class

# Takes the query generated from the AI
# Query should have thoughts in format <Thought></Thought
# And Action in format <Action></Action>
# Returns an object of Extracted Action
def extractAction(text):
    #Use RegeX pattern search to find the thought and action in the response
    match = re.search(r"<Thought>(.*?)<\/Thought>", text)
    thought = match.group(1) if match else None
    match = re.search(r"<Action>(.*?)<\/Action>", text)
    action = match.group(1) if match else None
    #Return None if either is not found
    if ((thought is None) or (action is None)):
        return None
    #Find the action type to be either of the three
    actionType = re.search(r"(click|setValue|finish)\(", action).group(1)\
        if match else None
    
    executableAction = None
    if (actionType is None):
        return None
    elif (actionType == "click"):
        #Find the set of numbers after click
        index = re.search(r"click\((\d+)\)", action).group(1)\
            if match else None
        if (index is None):
            return None
        executableAction = ExecutableAction('clickElement', {'id': int(index)})
    elif (actionType == "setValue"):
        #Find the next two set of numbers after setValue
        index = re.search(r"setValue\((\d+),\s*(.*?)\)", action).group(1)\
            if match else None
        value = re.search(r"setValue\((\d+),\s*(.*?)\)", action).group(2)\
            if match else None
        if ((index is None) or (value is None)):
            return None
        executableAction = ExecutableAction('setValue',
                                            {'id': int(index), 'value': value})
    elif (actionType == "finish"):
        executableAction =  ExecutableAction('finish', {})
    
    if (executableAction is None):
        return None
    #ELSE
    return ExtractedAction(thought, action, executableAction)



