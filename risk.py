from random import random
import time
import numpy as np
sampleAttacker = {
    "armies" : 10
}

sampleDefender = {
    "armies" : 12
}

#Return a sorted(highest) array of length number with random values 1-6
def makeDice(number):
    dice = []
    for i in range (number):
        dice.append(1 + int(6 * random()))
    dice.sort()
    dice.reverse()
    return dice

#Perform one dice roll
def rollDice(attacker, defender):

    if attacker["armies"] <= 1: raise ValueError("Attacker must have >1 Armies")
    if (attacker["armies"]-1 >= 3): attackerDice = makeDice(3)
    else: attackerDice = makeDice(attacker["armies"] - 1)
    if (defender["armies"] >= 2): defenderDice = makeDice(2)
    else: defenderDice = makeDice(defender["armies"])

    numberOfDice = len(defenderDice)
    if (len(attackerDice) < numberOfDice): numberOfDice -= 1

    for i in range (numberOfDice):
        if attackerDice[i] > defenderDice[i]:
            defender["armies"] -= 1
        else: attacker["armies"] -= 1


#Run all dice rolls until one loses
def blitzAttack(attacker, defender):
    while (attacker["armies"] > 1 and defender["armies"] > 0):
        rollDice(attacker, defender)
    if defender["armies"] < 1: return True
    else: return False


probabilityMatrix = [[0] * 50] * 50

def calculateOdds(aArmies, dArmies, sims):
    before = time.perf_counter()
    victories = 0
    for i in range (sims):
        if blitzAttack({"armies": aArmies}, {"armies": dArmies}): victories += 1
    after = time.perf_counter()

    return victories / sims, after - before





        
    



        





    

print("Start")


print(calculateOdds(5000, 5000, 10000))





