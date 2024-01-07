import time

class Tree:
    def __init__(self, attackerTroops, defenderTroops, odds):
        self.children = []
        self.attackerTroops = attackerTroops
        self.defenderTroops = defenderTroops
        self.odds = odds

    
    def __str__(self, level=0):
        ret = "\t"*level+repr(self)+"\n"
        for child in self.children:
            ret += child.__str__(level+1)
        return ret

    def __repr__(self):
        return f'{self.attackerTroops}v{self.defenderTroops}, {self.odds}'   



def rollOff(attackerArmies, defenderArmies):
    if attackerArmies < 2: raise ValueError("Attacker must have more than 1 army to attack")
    if defenderArmies < 1: raise ValueError("Defender must have more than 0 armies to defend")
    before = time.perf_counter()
    attackerDice = []
    for x in range(1,7):
        if attackerArmies > 2:
            for y in range(1,7):
                if attackerArmies > 3:
                    for z in range(1,7):
                        attackerDice.append([x,y,z])
                else:
                    attackerDice.append([x,y])
        else: 
            attackerDice.append([x])

    defenderDice = []
    for x in range(1,7):
        if defenderArmies > 1:
            for y in range(1,7):
                defenderDice.append([x,y])
        else: 
            defenderDice.append([x])

    samplespace = []
    for a in attackerDice:
        for d in defenderDice:
            samplespace.append([a, d])

    lengths = [len(attackerDice[0]), len(defenderDice[0])]
    lengths.sort()
    numberOfLosses = lengths[0]

    outcomes = []

    for matchup in samplespace:
        matchup[0].sort()
        matchup[1].sort()
        matchup[0].reverse()
        matchup[1].reverse()

        outcome = [0,0]
        for i in range (numberOfLosses):
            if matchup[0][i] > matchup[1][i]: outcome[1] += 1 #Attacker wins roll
            else: outcome[0] += 1 #Defender wins roll
        outcomes.append(outcome)

    output = {
        "A-1" : outcomes.count([1,0]),
        "D-1" : outcomes.count([0,1]),
        "A-2" : outcomes.count([2,0]),
        "D-2" : outcomes.count([0,2]),
        "T" : outcomes.count([1,1]),
        "total" : len(outcomes)
    }
    
    after = time.perf_counter()
    return output, after - before


def rollOffBaked(attackerArmies,defenderArmies):
    if attackerArmies < 2: raise ValueError("Attacker must have more than 1 army to attack")
    if defenderArmies < 1: raise ValueError("Defender must have more than 0 armies to defend")
    if attackerArmies > 3 and defenderArmies > 1: return {'A-1': 0, 'D-1': 0, 'A-2': 2275, 'D-2': 2890, 'T': 2611, 'total': 7776} #3v2 diceroll
    elif attackerArmies > 3 and defenderArmies == 1: return {'A-1': 441, 'D-1': 855, 'A-2': 0, 'D-2': 0, 'T': 0, 'total': 1296} #3v1 diceroll
    elif attackerArmies == 3 and defenderArmies > 1: return {'A-1': 0, 'D-1': 0, 'A-2': 581, 'D-2': 295, 'T': 420, 'total': 1296} #2v2 diceroll
    elif attackerArmies == 3 and defenderArmies == 1: return {'A-1': 91, 'D-1': 125, 'A-2': 0, 'D-2': 0, 'T': 0, 'total': 216} #2v1 diceroll
    elif attackerArmies == 2 and defenderArmies > 1: return {'A-1': 161, 'D-1': 55, 'A-2': 0, 'D-2': 0, 'T': 0, 'total': 216} #1v2 diceroll
    elif attackerArmies == 2 and defenderArmies == 1: return {'A-1': 21, 'D-1': 15, 'A-2': 0, 'D-2': 0, 'T': 0, 'total': 36} #1v1 diceroll



def blitzSampleSpace(attackerArmies, defenderArmies):
    before = time.perf_counter()
    samplespace = Tree(attackerArmies, defenderArmies, [1,1])
    output =  blitzSampleSpaceRecursion(attackerArmies, defenderArmies, samplespace, [])
    after = time.perf_counter()
    return output, after - before


def blitzSampleSpaceRecursion(attackerArmies, defenderArmies, parent, completed):

    if (attackerArmies < 2 or defenderArmies < 1):
        return Tree(attackerArmies, defenderArmies, parent.odds)
    
    matches = [node for node in completed if (node.attackerTroops == attackerArmies and node.defenderTroops == defenderArmies)]
    if len(matches) > 0:
        found = Tree(matches[0].attackerTroops, matches[0].defenderTroops, parent.odds)
        found.children.append(matches[0].children)
        return found
    
    level = rollOffBaked(attackerArmies, defenderArmies)
    total = level["total"]

    for key in level:
        if key == "A-1":
            if level[key] < 1: continue
            child = Tree(attackerArmies - 1, defenderArmies, [level["A-1"], total])
            child = blitzSampleSpaceRecursion(child.attackerTroops, child.defenderTroops, child, completed)
            parent.children.append(child)
        if key == "D-1":
            if level[key] < 1: continue
            child = Tree(attackerArmies, defenderArmies - 1, [level["D-1"], total])
            child = blitzSampleSpaceRecursion(child.attackerTroops, child.defenderTroops, child, completed)
            parent.children.append(child)
        if key == "A-2":
            if level[key] < 1: continue
            child = Tree(attackerArmies - 2, defenderArmies, [level["A-2"], total])
            child = blitzSampleSpaceRecursion(child.attackerTroops, child.defenderTroops, child, completed)
            parent.children.append(child)
        if key == "D-2":
            if level[key] < 1: continue
            child = Tree(attackerArmies, defenderArmies - 2, [level["D-2"], total])
            child = blitzSampleSpaceRecursion(child.attackerTroops, child.defenderTroops, child, completed)
            parent.children.append(child)
        if key == "T":
            if level[key] < 1: continue
            child = Tree(attackerArmies - 1, defenderArmies - 1, [level["T"], total])
            child = blitzSampleSpaceRecursion(child.attackerTroops, child.defenderTroops, child, completed)
            parent.children.append(child)
    

    completed.append(parent)
    return parent





a = blitzSampleSpace(200,200)
print(a[1])

print(a[1])





        












