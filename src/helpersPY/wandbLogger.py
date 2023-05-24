import wandb
import random

#Initialise wandb, to be called once at the start of the program
def initWandB():
    # start a new wandb run to track this script
    wandb.init(
        # set the wandb project where this run will be logged
        project="taxyAI-Browser-Chrome",
        
        config={}
    )

# Takes the number of actions, total length of queries, 
# and length of instruction into wandb
def logDataIntoWandB(numberOfActions, lengthOfQueries, lengthOfInstruction):
    report = {
        "action numbers": numberOfActions,
        "total queries length": lengthOfQueries,
        "length of instruction": lengthOfInstruction
    }
    wandb.log(report)

#Testing
initWandB()
for i in range(30):
    numberOfActions = random.randint(1,10)
    lengthOfQueries = random.randint(200,400)
    lengthOfInstruction = random.randint(20,40)
    logDataIntoWandB(numberOfActions, lengthOfQueries, lengthOfInstruction)