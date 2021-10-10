# This is the Beta for Queen's Demise. It's a 1v1 RPG with Legend of Zelda style items and
# exploration implemented.

import random, time, pickle
# random is to randomly choose enemies, stat ups, etc; time allows pause()s to let players read, and add emphasis
# pickle is to save the all of the info the game uses when the player needs to save and quit.

# inputFilter is a function for converting a string input into an integer without causing a crash.
# The parameter determines how many options you've listed for the player to choose from, and the
# input is then checked to see if it matches any of the numbered options available to choose from;
# if not, it asks them to re-input their choice until they DO choose a numbered option.
# It was made before I was aware of the ability to try:/except: things, so outdated but functional.
def inputFilter(optionAmount):
    goodInput = False
    convertedInput = ""
    while goodInput == False:
        optionNumber = 1
        goodInputB = False
        playerInput = input()
        inputRange = optionAmount - 1
        #Sets up range to correctly check input each loop, by looping once to check each
        #individual option that was possible (as defined by the coder, not the player).
        while inputRange != 0:
            if str(optionNumber) != playerInput or playerInput == "":
                #is the first option, "1", == to input? no: add one to option being checked, subtract
                #one from optionNumber. yes: input becomes an integer, no crashing, input = good.
                optionNumber = int(optionNumber) + 1
            if str(optionNumber) == playerInput and playerInput != "":
                convertedInput = int(playerInput)
                goodInput = True
            inputRange = inputRange - 1
        if goodInput != True:
            print("I didn't understand what you typed, please put in a number listed above.\n")
            continue
        #Forces player to input again until they use integer that is within the listed options.
        if str(convertedInput) == str(playerInput):
            return convertedInput
            goodInput = True
            #returns the input as an integer, avoids crashs. Problem solved!

# Creates timed pauses between certain things, I'll typically use it to pause between a character's action
# and when the results of the action occur.
def pause(pauseTime=3):
    time.sleep(pauseTime)

# Love the name. Just combines print and pause functions, very useful for giving players time to read.
def prause(string="",pauseTime=3):
    print(str(string))
    pause(pauseTime)

# Returns the FIRST key in the dictionary given.
# Works for getting the value of my movement and position dictionaries, which are 1 key dictionaries.
def key(dictionary):
    for key in dictionary:
        return key
    
# Give list of options as strings. Automatically determines number of options to print, then runs
# the inputFilter and returns it as an integer.
def listOptions(choiceDetails = None):
    if choiceDetails == None:
        choiceDetails == ["Yes","No"]
    else:
        optionAmount = len(choiceDetails)
        print()
        for i in range(1, optionAmount+1):
            print("\t"+str(i) + ": " + choiceDetails[i-1] + "\n")
        return inputFilter(optionAmount)
            
            
# Gives the player the chance to give their character a name; with the way that the stats displays,
# can only be 12 characters long, so that is explicitly told to the player during this function. 
def nameSelection():
    print("What is your character's name? (it can only be 12 characters long)\n")
    nameSuccess = False
    while nameSuccess == False:#one time code to test name length, and then set up spacing for later in battleStats (hence the 12 character limit)
        name=input()
        if len(name) >= 13:
            print("Your name has to be 12 characters or less, try putting in a new name.\n")
            continue
        elif " " in name:
            print("You can't have spaces in your name. Try another one.\n")
            continue
        elif len(name) < 13:
            if saveCreateNames(name) == True:#If the name given equals another save's name, retry.
                print("You can't pick that name, there's a save with that name already. Try another one.\n")
                continue
            print("Is " + name + " correct?")
            correctName = listOptions(["Yes", "No"])
            if correctName == 2:
                print("Alright, try typing your character's name one more time.\n")
                continue
            if correctName == 1:
                nameSuccess = True
    return name

# Asks the pronouns of the player, and returns a list of pronouns for use in strings later that refer
# to the player's character during gameplay. Also allows for neopronouns for non-binary people to input.
# If someone doesn't want to give their pronouns, it defaults to they/them.
def pronounCheck(name):
    pronounChosen = False
    while pronounChosen != True:
        print("Well, "+ name +", what are your pronouns?")
        pronounChoice = listOptions(["He/Him", "She/Her", "They/Them","Prefer not to answer"])
        if pronounChoice == 1:
            pronouns = ["he", "him", "his", "his", "is", "was","s"]    
        if pronounChoice == 2:
            pronouns = ["she", "her", "her", "hers", "is", "was","s"]    
        if pronounChoice == 3 or pronounChoice == 4:
            pronouns = ["they", "them", "their", "theirs", "are", "were",""]
        print("OK, is " + pronouns[0] + "/" + pronouns[1] + " correct, " + name + "?")
        tempInput = listOptions(["Yes","No"])
        if tempInput == 1:
            pronounChosen = True
            continue
        if tempInput == 2:
            print("Alright, let's try one more time.")
            pronounChosen = False
    return pronouns
    
# nameSpace() sets up a string to space the enemy's stats the right length away from the player's stats so that
# it lines up properly in the battle stats displaying loop later on.
def nameSpace(name):
    nameSpaceNum = 13 - len(name)
    nameSpace = " " * nameSpaceNum
    return nameSpace

# This was originally to decide between different classes, but since the abilities are now based on the
# key items the player has, it only has a difference in a handful of situations. Sets player stats as well.
def playerChoice(name,difficulty):
    playerType = "Unknown"
    while playerType == "Unknown":
        print("Choose your preferred title. (Doesn't affect stats or moves)")
        tempInput2 = listOptions(["Valkyrie","Paladin"])
        if tempInput2 == 1:
            playerType = "Valkyrie"
        if tempInput2 == 2:
            playerType = "Paladin"
    stats = [1,10,10,2,2,70,8,8,0,50]
    if difficulty == 1 or difficulty == 2:
        stats[2] += 5
        stats[1] += 5
        for stat in range(3,len(stats)-2):
            stats[stat] += 2
    playerStats = {"Name":name,"Level":stats[0],"Health Current":stats[1],
                   "Health Max":stats[2],"Strength":stats[3],"Speed":stats[4],
                   "Accuracy":stats[5], "Ability Current":stats[6],
                   "Ability Max":stats[7],"XP Current":stats[8],"XP Max":stats[9],
                   "Player Type":playerType,"Bonus Effect":["None",0]}
    return playerStats


# This is the current randomizer for enemies, it's used to decide what enemy the player faces. Considering that it's going to be
# a game with a world to traverse, we're going to have to change how enemies are selected. Might be good to add a section with
# enemy lists based on region, so they can be customized overall? 
def enemyDecide(info,boss=False):#randomizes the enemy itself, their stats (to an extent), and adds stat changing types; sets boss up
    enemyFirstAll = ["", "Frozen ", "Fire ", "Plagued ", "Giant ", "Demonic "]
    enemyLastAll = ["Slime", "Gnoll", "Ogre", "Dragon", "Mad Mage",
                    "Nighthound", "Aberration", "Elemental", "Possessed Armor"]
    BOSSNAMES = ["Demon Queen","Phase 1"]
    if info["Region"] == "forest":#1/4 chance of being giant
        enemyFirst = [enemyFirstAll[0],enemyFirstAll[0],enemyFirstAll[0],enemyFirstAll[4]]
        enemyLast = [enemyLastAll[0],enemyLastAll[1]]
        if info["Player Stats"]["Level"] >=5:
            enemyLast = [enemyLastAll[0],enemyLastAll[1],enemyLastAll[2]]
        maxEnemyLevel = 10
    if info["Region"] == "mountains":
        enemyFirst = [enemyFirstAll[0],enemyFirstAll[4],enemyFirstAll[2]]
        enemyLast = [enemyLastAll[2],enemyLastAll[3],enemyLastAll[4],enemyLastAll[7]]
        maxEnemyLevel = 15
    if info["Region"] == "tundra":
        enemyFirst = [enemyFirstAll[0],enemyFirstAll[1],enemyFirstAll[4]]
        enemyLast = [enemyLastAll[2],enemyLastAll[4],enemyLastAll[3],enemyLastAll[7]]
        maxEnemyLevel = 15
    if info["Region"] == "tower":
        enemyFirst = enemyFirstAll[1:]
        enemyLast = enemyLastAll[5:]
        maxEnemyLevel = 25
    playerStats = info["Player Stats"]
    name, pronouns = info["Name"],info["Pronouns"]
    bonusEffect = "None"
    if info["Region"] == "boss" and boss == True:
        try:
            info["Phase"] += 1
        except:
            info["Phase"] = 0
        if info["Phase"] == 1:
            decisionName = BOSSNAMES[:]
            defense = 40
            enemyStats = [800, 25, 25, 95, 30, 50]#boss queen stats baybeee
##      Removed from game.
##        elif info["Phase"] == 2:
##            defense = 10
##            enemyStats = [9999, 50, 50, 100, 50, 0]
##            decisionName = ["The Undying Queen"]
        else:
            defense = 30
            decisionName = ["Demon Queen"]
            enemyStats = [500, 20, 20, 90, 25, 25]
        decisionType = ""#Enemy is specified exactly as the Demon Queen.


    elif playerStats["Level"] == 1:#start with slime for the tutorial
        decisionName = "Slime"
        decisionType = ""
        enemyStats = [15, 2, 1, 90, 0, 1]#copying slime stats to use as a simple tutorial fight.
        defense = 0
    else:
        enemyFairFirst = False
        enemyFairSecond = False
        while enemyFairSecond == False:
            decisionName = random.choice(enemyLast)
            if "Slime" in decisionName:
                enemyStats = [15, 2, 1, 90, 0, 1]
                defense = 0
                enemyFairSecond = True
            if "Gnoll" in decisionName:
                enemyStats = [20, 4, 3, 80, 1, 3]
                defense = 1
                defense += round(playerStats["Level"]*0.5)
                enemyFairSecond = True
            if "Ogre" in decisionName:
                if info["Key Pieces"] == 0:
                    enemyStats = [55, 8, 5, 60, 4, 5]
                    defense = 3
                    defense += round(playerStats["Level"]*0.5)
                else:
                    enemyStats = [85, 12, 5, 65, 8, 5]
                    defense = 8
                    defense += round(playerStats["Level"]*1.25)
                enemyFairSecond = True
            if "Dragon" in decisionName:
                if info["Key Pieces"] == 0:
                    enemyStats = [60, 10, 10, 65, 2, 5]
                    defense = 4
                    defense += round(playerStats["Level"]*1.25)
                else:
                    enemyStats = [90, 15, 10, 70, 4, 5]
                    defense = 10
                    defense += round(playerStats["Level"]*1.5)
                enemyFairSecond = True
            if "Mad Mage" in decisionName:
                if info["Key Pieces"] == 0:
                    enemyStats = [70, 8, 18, 75, 2, 5]
                    defense = 4
                    defense += round(playerStats["Level"]*1.25)
                else:
                    enemyStats = [100, 12, 18, 80, 5, 5]
                    defense = 8
                    defense += round(playerStats["Level"]*1.5)
                enemyFairSecond = True
            if "Elemental" in decisionName:
                if info["Key Pieces"] == 0:
                    enemyStats = [75, 15, 20, 60, 5, 5]
                    defense = 4
                    defense += round(playerStats["Level"]*1.25)
                else:
                    enemyStats = [95, 18, 20, 60, 10, 5]
                    defense = 9
                    defense += round(playerStats["Level"]*1.5)
                enemyFairSecond = True
            if "Nighthound" in decisionName:
                enemyStats = [150, 15, 25, 80, 15, 10]
                defense = 12
                defense += round(playerStats["Level"]*1.5)
                enemyFairSecond = True
            if "Aberration" in decisionName:
                defense = 5
                defense += round(playerStats["Level"]*1.5)
                enemyFairSecond = True
                enemyStats = [220, 15, 25, 45, 10, 10]
            if "Possessed Armor" in decisionName:
                defense = 15
                defense += round(playerStats["Level"]*1.5)
                enemyFairSecond = True
                enemyStats = [100, 25, 10, 65, 25, 12]
        while enemyFairFirst == False:#rerolls until you get a fair enemy type for your playerStats["Level"]
            decisionType = random.choice(enemyFirst)
            if "Elemental" in decisionName:
                if info["Region"] == "tundra":
                    decisionType = "Frozen "
                elif info["Region"] == "mountains":
                    decisionType = "Fire "
                else:
                    decisionType = random.choice([enemyFirstAll[1],enemyFirstAll[2]])
            if decisionType == enemyFirstAll[0]:#if normal
                bonusEffect = "None"
                enemyFairFirst = True
            if "Frozen " in decisionType:
                bonusEffect = "Ice"
                enemyFairFirst = True
            if "Fire " in decisionType:
                bonusEffect = "Fire"
                enemyFairFirst = True
            if "Plagued " in decisionType and playerStats["Level"] >= 5:
                bonusEffect = "Poison"
                enemyFairFirst = True
            if "Giant " in decisionType and playerStats["Level"] >= 3:
                bonusEffect = "Giant"#no bonus effect, but stats get upped a lot
                enemyStats = [round(enemyStats[0] * 1.5), (enemyStats[1] + 5), (enemyStats[2] - 5), (enemyStats[3] - 15), enemyStats[4], enemyStats[5]]
                enemyFairFirst = True
            if "Demonic " in decisionType and playerStats["Level"] >= 10:
                bonusEffect = "Demonic"
                enemyStats = [round(enemyStats[0] * 1.5), (enemyStats[1] + 5), (enemyStats[2] + 5), (enemyStats[3] + 5), (enemyStats[4] + 1), enemyStats[5]]
                enemyFairFirst = True
                
    x = 0#loop to randomize enemy stats a bit after first battle.
    while x!=4 and playerStats["Level"] != 1 and boss == False:
        enemyStats[x] += random.randint(-1, 1)
        if enemyStats[x] <= 0 and x != 4:
            enemyStats[x] = 1
        if enemyStats[x] < 0 and x == 4:
            enemyStat[4] = 0
        x += 1
    #This loop gives enemies stat ups in a similar way to how the player levels up, to make them more
    #challenging when facing them.
    if enemyStats[5] < info["Player Stats"]["Level"]:
        if info["Difficulty"] == 2 or info["Difficulty"] == 1:#easy/story mode
            enemyLevelVariance = [-2,-1]
        elif info["Difficulty"] == 4:#hard
            enemyLevelVariance = [1,2,3,4]
        else:
            enemyLevelVariance = [-1,0,1]
        newEnemyLevel = info["Player Stats"]["Level"] + random.choice(enemyLevelVariance)
        while enemyStats[5] < maxEnemyLevel and enemyStats[5] < newEnemyLevel:
            enemyStats[5] += 1
            for x in range(0,5):
                enemyStats[x] += random.randint(0,2)
                if x == 0:
                    enemyStats[x] += 2
            if enemyStats[3] >= 90:
                enemyStats[3] = 90
        
    firstName = str(decisionType)
    lastName = str(decisionName)
    enemyInfo = {}
    if boss == False:
        enemyInfo["Enemy"] = firstName + lastName
    elif boss == True:
        enemyInfo["Enemy"] = decisionName[0]
        enemyInfo["Boss"] = str(decisionName)
    healthCurrent = enemyStats[0]
    enemyInfo["Health Max"] = enemyStats[0]
    enemyInfo["Health Current"] = healthCurrent
    enemyInfo["Strength"] = enemyStats[1]
    enemyInfo["Speed"] = enemyStats[2]
    enemyInfo["Accuracy"] = enemyStats[3]
    enemyInfo["Weapon"] = enemyStats[4]
    if bonusEffect == "Giant" or bonusEffect == "Demonic":
        enemyStats[5] += 2 #extra experience for player facing these two types.
    enemyInfo["Level"] = enemyStats[5]
    enemyInfo["Bonus"] = bonusEffect
    enemyInfo["Defense"] = defense
    return enemyInfo

# levelUp() is used after an enemy is defeated and XP is given to improve the player's stats by very slightly random amounts, and to set up the XP for the next level up.
def levelUp(info):#Most stats go up by random 1-2, but HP goes up by 5, level always by 1, and accuracy is limited to a max of 90.
    difficulty = info["Difficulty"]
    enemyInfo = info["Enemy Info"]
    playerStats = info["Player Stats"]
    name, pronouns = info["Name"],info["Pronouns"]
    playerStats["XP Current"] = playerStats["XP Current"] - playerStats["XP Max"]
    playerStats["XP Max"] += playerStats["Level"] * 25
    prause(name + " has leveled up!")
    statList = [playerStats["Level"], playerStats["Health Max"], playerStats["Strength"], playerStats["Speed"], playerStats["Accuracy"], playerStats["Ability Max"]]
    prause(name + "'s stats have changed:\nMax HP: " + str(statList[1]) + ", Str: " + str(statList[2]) + ", Spd: " + str(statList[3]) + ", Acc: " + str(statList[4]) + ", ABP: " + str(statList[5]) + ", to...")
    statList[0] += 1
    if difficulty == 3 or difficulty == 4:
        statIncrease = 2
    if difficulty == 1 or difficulty == 2:
        statIncrease = random.randint(2,3)
    for x in range(2,6):
        statList[x] += random.randint(1, statIncrease)
    if statList[4] >= 90:
        statList[4] = 90
    statList[1] += 5#makes the HP gain exactly 5 per level, instead of just 1 to 2.
    playerStats["Level"] = statList[0]
    playerStats["Health Max"] = statList[1]
    playerStats["Health Current"] = statList[1]
    playerStats["Strength"] = statList[2]
    playerStats["Speed"] = statList[3]
    playerStats["Accuracy"] = statList[4]
    playerStats["Ability Max"] = statList[5]
    playerStats["Ability Current"] = playerStats["Ability Max"]
    print("Max HP: " + str(statList[1]) + ", Str: " + str(statList[2]) + ", Spd: " + str(statList[3]) + ", Acc: " + str(statList[4]) + ", ABP: " + str(statList[5]))
    pause()
    return info
    
# testSpacing(x) takes x, the length of a string in battleStats, and turns it into a
# concatenated string of " " that turns each line of the battle stats into
# an equal amount (13, after the 6 characters used to describe the line's stats).
def testSpacing(x):#x is length of player stats before the enemy's stats show up, per line.
    tempSpace = " "
    tempLength = int(x)
    while tempLength < 12:
        tempSpace = tempSpace + " "
        tempLength = tempLength + 1
    return tempSpace

# Returns the enemy's XP value for the player if it is defeated; also used to give said XP to player.
def enemyXP(enemyLevel):
    return 25 + (enemyLevel * 25)

# This is the stats displaying function of this game; it's used in a loop, to display the stats and names
# of the characters. After each turn, the battleStats is repeated to display the new stats of the
# player and enemy. This repeats until one of the characters is defeated.
def battleStats(info):
    enemyInfo = info["Enemy Info"]
    playerStats = info["Player Stats"]
    name, pronouns = info["Name"], info["Pronouns"]
    poti = [call("Potions",info),call("Potions Max",info)]
    statSpace1 = testSpacing(len(str(playerStats["Health Current"])) + 1 +
                            len(str(playerStats["Health Max"])))
    statSpace2 = testSpacing(len(str(playerStats["Defense"])))
    statSpace3 = testSpacing(len(str(playerStats["Strength"])) + 2 +
                             len(str(playerStats["Weapon"])))
    statSpace4 = testSpacing(len(str(playerStats["Speed"])))
    statSpace5 = testSpacing(len(str(playerStats["Accuracy"])) + 1)
    statSpace6 = testSpacing(len(str(playerStats["Level"])))
    BORDER = "|------------------------------------------------------|"
    
             #line zero
    LINES = [("|Name:| " + name + nameSpace(name) + "| " + enemyInfo["Enemy"]),
             #line one
             ("|HP:  | " + str(playerStats["Health Current"]) + "/" +
              str(playerStats["Health Max"]) + statSpace1 + "| " +
              str(enemyInfo["Health Current"]) + "/" + str(enemyInfo["Health Max"])),
             #line two
             ("|Def: | " + str(playerStats["Defense"]) + statSpace2 + "| " +
              str(enemyInfo["Defense"])),
             #line three
             ("|Str: | " + str(playerStats["Strength"]) + " +" + str(playerStats["Weapon"]) +
              statSpace3 + "| " + str(enemyInfo["Strength"]) + " +" + str(enemyInfo["Weapon"])),
             #line four
             ("|Spd: | " + str(playerStats["Speed"]) + statSpace4 + "| " +
              str(enemyInfo["Speed"])),
             #line five
             ("|Acc: | " + str(playerStats["Accuracy"]) + "%" +
              statSpace5 + "| " + str(enemyInfo["Accuracy"]) + "%"),
             #line six
             ("|Lvl: | " + str(playerStats["Level"]) + statSpace6 + "| " +
              str(enemyInfo["Level"]) + ", worth " +
              str(enemyXP(enemyInfo["Level"])) + "XP"),
             #line seven
             ("|ABP: | " + str(playerStats["Ability Current"]) + "/" +
              str(playerStats["Ability Max"]) + " |Potion:| " + str(poti[0]) +
              "/"+str(poti[1]) + " |XP:| " + str(playerStats["XP Current"]) +
              "/" + str(playerStats["XP Max"]))]

    borLen = len(BORDER)
    statDisplayList = [("\t"+BORDER),"","","","","","","",
                         ("\n\t"+BORDER),"",("\n\t"+BORDER)]
    lineToChange = 1
    for lineNumber in range(len(LINES)):
        if lineToChange == 8:
            lineToChange += 1
        extraSpacing = borLen - len(LINES[lineNumber])
        correctEnd = (" "*(extraSpacing-1))+"|"
        correctStart = "\n\t"
        statDisplayList[lineToChange] = correctStart + LINES[lineNumber] + correctEnd
        lineToChange += 1
    statDisplayString = ""
    for line in statDisplayList:
        statDisplayString += str(line)
    print(str(statDisplayString))

# The player AND enemy's actions don't always go through; the character's accuracy is compared
# to the randomized chance to hit (an int between 0 and 100), if the character's accuracy is lower,
# the attack misses. dodge(hitChance,attacker,info) displays the actual roll of the die, calling
# it the dodge roll, and prints it in comparison to the attacker's accuracy. It determines
# which character's accuracy to use by checking the name of the character attacking.
def dodge(hitChance,attacker,info):
    enemyInfo = info["Enemy Info"]
    playerStats = info["Player Stats"]
    name, pronouns = info["Name"],info["Pronouns"]
    string = ("\n\t(Dodge Roll: " + str(hitChance))
    if attacker == name:
        accuracy = playerStats["Accuracy"]
    if attacker == enemyInfo["Enemy"]:
        accuracy = enemyInfo["Accuracy"]
    if hitChance > accuracy:
        string += ">"
    if hitChance <= accuracy:
        string += "<="
    string += (str(accuracy) + "% accuracy)\n")
    return string
    
#Options that the player has in combat.
def battleOptions(info):
    coolDownLine = ["","","","",""]
    for coolNum in range(len(info["Cooldowns"])):
        if info["Cooldowns"][coolNum] > 0:
            info["Cooldowns"][coolNum] -= 1
        if info["Cooldowns"][coolNum] != 0:
            sQuestion = "s"
            if info["Cooldowns"][coolNum] == 1:
                sQuestion = ""
            coolDownLine[coolNum] = (" COOLDOWN: " +
                                     str(info["Cooldowns"][coolNum])+
                                     " more turn"+sQuestion)
    poti = [info["Potions"], info["Potions Max"]]
    moveCost= [0,2,3,3,0]#Move Cost.
    moveSet = [("Swing Sword\n\t   ("+str(moveCost[0])+
                " ABP)\n\t   Attack the enemy with a basic sword strike."),
               ("Charged Sword Strike\n\t   ("+str(moveCost[1])+
                " ABP)" + coolDownLine[1] +
                "\n\t   Charge magic, and attack the enemy; +1.5 damage per level."),
               ("Flame Glove\n\t   ("
                +str(moveCost[2])+" ABP)"+coolDownLine[2]+
                "\n\t   Flames blast the enemy; +3 damage per level."),
               ("Bomb Bag\n\t   ("+str(moveCost[3])+
                " ABP)" + coolDownLine[3] +
                "\n\t   Creates an explosion! +2.5 damage per level, +5 accuracy."),
               ("Potion\n\t   ("+str(poti[0])+"/" + str(poti[1]) +
                " Potions left)\n\t   Use a potion to restore 80% of Max HP.")]
    if info["Equipment"]["Bomb Bag"] == False:
        moveSet[3] = "LOCKED"
    if info["Equipment"]["Flame Glove"] == False:
        moveSet[2] = "LOCKED"
    print("\nWhat do you want to do?")
    enemyInfo = info["Enemy Info"]
    playerStats = info["Player Stats"]
    name, pronouns = info["Name"],info["Pronouns"]
    choice = False
    while choice == False :
        choice = listOptions(moveSet)
        if playerStats["Ability Current"] < moveCost[choice-1] and choice != 5:
            print("You don't have enough ability points for that move; try picking a different option.")
            choice = False
        if info["Cooldowns"][choice-1] != 0:
            print("That move is on cooldown, choose another move!")
            choice = False
        if choice == 5:
            if info["Potions"] <= 0:
                print("You don't have any potions! Choose another option.")
                choice = False
            elif playerStats["Health Current"] == playerStats["Health Max"]:
                print("Your health is already full! Choose another option.")
                choice = False
        if choice == 3 and info["Equipment"]["Flame Glove"] == False:
            prause("That option is locked, choose another option.")
            choice = False
        if choice == 4 and info["Equipment"]["Bomb Bag"] == False:
            prause("That option is locked, choose another option.")
            choice = False
        if playerStats["Ability Current"] >= moveCost[choice-1] and choice != 5 and choice != False:
            playerStats["Ability Current"] -= moveCost[choice-1]
            
    hitChance = random.randint(0, 100)
    if choice == 1:
        prause((name + " swings " + pronouns[2] + " sword at the " + enemyInfo["Enemy"] + "!"))
        if hitChance > playerStats["Accuracy"]:
            prause((name + " missed the " + enemyInfo["Enemy"] + "!" + dodge(hitChance,name,info)))
        if hitChance <= playerStats["Accuracy"]:
            damage = playerStats["Strength"] + playerStats["Weapon"] - enemyInfo["Defense"]
            if damage <= 0:
                damage = 1
            prause((name + " hits the " + enemyInfo["Enemy"] + " for " + str(damage) + " damage!" + dodge(hitChance,name,info)))
            enemyInfo["Health Current"] = enemyInfo["Health Current"] - damage
    if choice == 2:
        info["Cooldowns"][choice-1] = 2
        prause((name + " raises " + pronouns[2] + " sword to the sky, imbuing it with a blue light..."))
        if hitChance > playerStats["Accuracy"]:
            prause((name + " slams the sword into the ground as the " + enemyInfo["Enemy"] + " dodges." + dodge(hitChance,name,info)))
        if hitChance <= playerStats["Accuracy"]:
            damage = playerStats["Strength"] + playerStats["Weapon"] + round(playerStats["Level"] * 1.5)
            damage = round(damage) - enemyInfo["Defense"]
            if damage <= 0:
                damage = 1
            prause((pronouns[0].title() + " then slam" + pronouns[6] + " it down upon the " + enemyInfo["Enemy"] + ", dealing " + str(damage) + " damage!" + dodge(hitChance,name,info)))
            enemyInfo["Health Current"] = enemyInfo["Health Current"] - damage
    if choice == 3:
        info["Cooldowns"][choice-1] = 3
        prause((name + " aims with the glove as the air erupts in flames..."))
        if hitChance > playerStats["Accuracy"]:
            prause((name + "'s flames just miss the " + enemyInfo["Enemy"] + ", doing no damage." + dodge(hitChance,name,info)))
        if hitChance <= playerStats["Accuracy"]:
            damage = playerStats["Strength"] + playerStats["Weapon"] + (3*playerStats["Level"])
            damage -= enemyInfo["Defense"]
            if damage <= 0:
                damage = 1
            if enemyInfo["Bonus"] == "Fire":
                damage = round(damage/2)
                print("\tIt's not very effective...")
            elif enemyInfo["Bonus"] == "Ice":
                print("\tSuper effective!")
                damage = round(damage*1.25)
            prause(("The flames singe and scar the " + enemyInfo["Enemy"] + ", dealing " + str(damage) + " damage to the enemy." + dodge(hitChance,name,info)))
            enemyInfo["Health Current"] -= damage
    if choice == 4:
        info["Cooldowns"][choice-1] = 3
        prause((name + " pulls a bomb out and throws it towards the " + enemyInfo["Enemy"] + "..."))
        playerStats["Accuracy"] += 5
        if hitChance > playerStats["Accuracy"]:
            prause(("The bomb's shrapnel misses the " + enemyInfo["Enemy"] + ", doing no damage." + dodge(hitChance,name,info)))
        if hitChance <= playerStats["Accuracy"]:
            damage = (playerStats["Strength"] + playerStats["Weapon"] + round(2.5*playerStats["Level"])) - enemyInfo["Defense"]
            if damage <= 0:
                damage = 1
            if enemyInfo["Bonus"] == "Ice":
                damage = round(damage/2)
                print("\tIt's not very effective...")
            elif enemyInfo["Bonus"] == "Fire":
                print("\tSuper effective!")
                damage = round(damage*1.25)
            prause(("The shrapnel pierces through the " + enemyInfo["Enemy"] + ", dealing " + str(damage) + " damage!" + dodge(hitChance,name,info)))
            enemyInfo["Health Current"] -= damage
        playerStats["Accuracy"] -= 5
    if choice == 5:
        heal = round(4 * (playerStats["Health Max"] / 5))
        print(name + " heals for " + str(heal) + " points, going from " + str(playerStats["Health Current"]) + " to ", end="")
        playerStats["Health Current"] = playerStats["Health Current"] + heal
        if playerStats["Health Current"] > playerStats["Health Max"]:
            playerStats["Health Current"] = playerStats["Health Max"]
        prause((str(playerStats["Health Current"]) + "!\n"))
        info["Potions"] -= 1
    return info

def enemyOptionSlime(info):#chooses what attack the enemy goes with, need to modify for different enemies with different attacks
    enemyInfo = info["Enemy Info"]
    playerStats = info["Player Stats"]
    name, pronouns = info["Name"],info["Pronouns"]
    damage = 0
    enemyAttack = random.randint(1, 3)#Overall odds are 2/3 chance to attack, 90% chance to hit if attack happens at all, and 1/3 chance to just jiggle in place.
    if enemyAttack == 1 or enemyAttack == 2:
        prause(("The " + enemyInfo["Enemy"] + " charges at " + name + "!"))
        hitChance = random.randint(0, 100)
        if hitChance > enemyInfo["Accuracy"]:
            prause(("The " + enemyInfo["Enemy"] + " missed " + name + "!" + dodge(hitChance,enemyInfo["Enemy"],info)))
        if hitChance <= enemyInfo["Accuracy"]:
            damage = enemyInfo["Strength"] + enemyInfo["Weapon"] - playerStats["Defense"]
            if damage <= 0:
                damage = 1
            prause(("The " + enemyInfo["Enemy"] + " slams into " + name + " for " + str(damage) + " damage!" + dodge(hitChance,enemyInfo["Enemy"],info)))
            playerStats["Health Current"] = playerStats["Health Current"] - damage
            if enemyInfo["Bonus"] in ["Fire","Ice","Poison"]:
                playerStats["Bonus Effect"] = [enemyInfo["Bonus"],random.randint(1,3)]
    if enemyAttack == 3:
        prause(("The " + enemyInfo["Enemy"] + " is... just jiggling?\n"))
    if damage != 0:#Only occurs if player is hit
        if enemyInfo["Bonus"] in ["Fire","Ice","Poison"]:
            if playerStats["Bonus Effect"] == ["None",0]:
                if random.randint(1,3) == 1:#only 1/3 chance of being effected
                    playerStats["Bonus Effect"] = [enemyInfo["Bonus"],random.randint(1,3)]
    return info

def enemyOptionGnoll(info):
    enemyInfo = info["Enemy Info"]
    playerStats = info["Player Stats"]
    name, pronouns = info["Name"],info["Pronouns"]
    damage = 0
    enemyAttack = random.randint(1, 5)#40% to target with cudgel, 40% to target with crossbow, 20% to go into rage
    hitChance = random.randint(0, 100)
    if enemyAttack == 1 or enemyAttack == 2:
        prause(("The " + enemyInfo["Enemy"] + " readies their cudgel..."))
        if hitChance > enemyInfo["Accuracy"]:
            prause(("The " + enemyInfo["Enemy"] + " missed " + name + "!" + dodge(hitChance,enemyInfo["Enemy"],info)))
        if hitChance <= enemyInfo["Accuracy"]:
            damage = enemyInfo["Strength"] + enemyInfo["Weapon"] - playerStats["Defense"]
            if damage <= 0:
                damage = 1
            prause(("The cudgel slams into " + name + " for " + str(damage) + " damage!" + dodge(hitChance,enemyInfo["Enemy"],info)))
            playerStats["Health Current"] = playerStats["Health Current"] - damage
    if enemyAttack == 3 or enemyAttack == 4:
        print("The " + enemyInfo["Enemy"] + " pulls out a crossbow and takes aim... (+5 Acc, 1 weapon damage)")
        pause()
        if hitChance > (enemyInfo["Accuracy"] + 5):
            prause(("The " + enemyInfo["Enemy"] + "'s arrow streaks past " + name + "!" + dodge(hitChance,enemyInfo["Enemy"],info)))
        if hitChance <= (enemyInfo["Accuracy"] + 5):
            damage = enemyInfo["Strength"] + 1 - playerStats["Defense"]
            if damage <= 0:
                damage = 1
            prause(("The arrow strikes true, dealing " + str(damage) + " to " + name + "!" + dodge(hitChance,enemyInfo["Enemy"],info)))
            playerStats["Health Current"] = playerStats["Health Current"] - damage
    if enemyAttack == 5:
        prause(("The gnoll smells your blood on the wind, and howls! +2 Strength, -8 accuracy.\n"))
        enemyInfo["Strength"] += 2
        enemyInfo["Accuracy"] -= 8
    if damage != 0:#Only occurs if player is hit
        if enemyInfo["Bonus"] in ["Fire","Ice","Poison"]:
            if playerStats["Bonus Effect"] == ["None",0]:
                if random.randint(1,3) == 1:#only 1/3 chance of being effected
                    playerStats["Bonus Effect"] = [enemyInfo["Bonus"],random.randint(1,3)]
    return info

def enemyOptionOgre(info):
    enemyInfo = info["Enemy Info"]
    playerStats = info["Player Stats"]
    name, pronouns = info["Name"],info["Pronouns"]
    enemyAttack = random.randint(1, 4)#ogre only has 50% chance of setting up a hit next turn
    hitChance = random.randint(0, 100)
    damage = 0
    if enemyInfo["Timer"] == 1:
        enemyAttack = 0
        prause(("The ogre brings down their club down with single-minded force!"))
        if hitChance > enemyInfo["Accuracy"]:
            prause(("... But the club missed by a wide margin, leaving a crater in the ground." + dodge(hitChance,enemyInfo["Enemy"],info)))
        if hitChance <= enemyInfo["Accuracy"]:
            damage = enemyInfo["Strength"] + enemyInfo["Weapon"] - playerStats["Defense"]
            if damage <= 0:
                damage = 1
            prause(("The club smashes into " + name + ", dealing " + str(damage) + " to " + pronouns[1] + "!" + dodge(hitChance,enemyInfo["Enemy"],info)))
            playerStats["Health Current"] = playerStats["Health Current"] - damage
    if enemyAttack == 1 or enemyAttack == 2:
        prause(("The " + enemyInfo["Enemy"] + " slowly raises their club, preparing to slam down next turn!\n"))
        enemyInfo["Timer"] = 2# Sets to two so that the attack goes off next turn
    if enemyAttack == 3 or enemyAttack == 4:
        prause((name + " manages to get behind the " + enemyInfo["Enemy"] + ", leaving them unable to attack this turn!\n"))
    if damage != 0:#Only occurs if player is hit
        if enemyInfo["Bonus"] in ["Fire","Ice","Poison"]:
            if playerStats["Bonus Effect"] == ["None",0]:
                if random.randint(1,3) == 1:#only 1/3 chance of being effected
                    playerStats["Bonus Effect"] = [enemyInfo["Bonus"],random.randint(1,3)]
    return info

def enemyOptionDragon(info):
    enemyInfo = info["Enemy Info"]
    playerStats = info["Player Stats"]
    name, pronouns = info["Name"],info["Pronouns"]
    enemyAttack = random.randint(1, 3)
    hitChance = random.randint(0, 100)
    damage = 0
    MISSLINE = ("The attack grazes past " + name + "'s face, leaving " + pronouns[1] + " frazzled, but unscathed...")
    if enemyInfo["Timer"] != 1:#3 equal chances: Claw attack, prep for energy blast, or increase accuracy.
        if enemyAttack == 3 and enemyInfo["Accuracy"] < 90:
            prause(("The " + enemyInfo["Enemy"] + " appears cautious, and focuses their attention on you... +5 Accuracy."))
            enemyInfo["Accuracy"] += 5
        elif enemyAttack == 3:
            enemyAttack = 1
        if enemyAttack == 1:
            prause(("The "+enemyInfo["Enemy"] + " lifts their claws, and flies forward!"))
            if hitChance > enemyInfo["Accuracy"]:
                prause(MISSLINE + dodge(hitChance,enemyInfo["Enemy"],info))
            if hitChance <= enemyInfo["Accuracy"]:
                damage = enemyInfo["Strength"] + enemyInfo["Weapon"] - playerStats["Defense"]
                if damage <= 0:
                    damage = 1
                prause(("The claws dig deep into " + name + ", dealing " + str(damage) + " damage!" + dodge(hitChance,enemyInfo["Enemy"],info)))
                playerStats["Health Current"] = playerStats["Health Current"] - damage
                if enemyInfo["Bonus"] in ["Fire","Ice","Poison"]:
                    if playerStats["Bonus Effect"] == ["None",0]:
                        if random.randint(1,3) == 1:#only 1/3 chance of being effected
                            playerStats["Bonus Effect"] = [enemyInfo["Bonus"],random.randint(1,3)]
        if enemyAttack == 2:
            prause(("The " + enemyInfo["Enemy"] + "'s jaw unhinges, and energy builds within their maw..."))
            enemyInfo["Timer"] = 2
    else:
        prause(("... Suddenly, a blast of energy erupts from the " + enemyInfo["Enemy"] + "'s mouth, heading towards " + name + "!"))
        enemyInfo["Accuracy"] -= 5
        if hitChance > enemyInfo["Accuracy"]:
            prause(MISSLINE + dodge(hitChance,enemyInfo["Enemy"],info))
        if hitChance <= enemyInfo["Accuracy"]:
            damage = round(enemyInfo["Strength"]*2.2) - playerStats["Defense"]
            if damage <= 0:
                damage = 1
            prause(("The blast catches " + name + ", launching " + pronouns[1] + " backward"+pronouns[6]+
                    " and dealing " + str(damage) + " damage!" + dodge(hitChance,enemyInfo["Enemy"],info)))
            playerStats["Health Current"] = playerStats["Health Current"] - damage
        enemyInfo["Accuracy"] += 5
    if damage != 0:#Only occurs if player is hit
        if enemyInfo["Bonus"] in ["Fire","Ice","Poison"]:
            if playerStats["Bonus Effect"] == ["None",0]:
                if random.randint(1,3) == 1:#only 1/3 chance of being effected
                    playerStats["Bonus Effect"] = [enemyInfo["Bonus"],random.randint(1,3)]
    return info

def enemyOptionMadMage(info): 
    enemyInfo = info["Enemy Info"]
    playerStats = info["Player Stats"]
    name, pronouns = info["Name"],info["Pronouns"]
    enemyAttack = random.randint(0, 4)
    hitChance = random.randint(0, 100)
    damage = 0
    targetName = "Not a possible name ever"
    MISSLINE = ("The magical blast misses, leaving a glowing trail in it's wake.")
    MAGEOPTIONS = ["pink","blue","yellow","red"]
    if enemyAttack == 4:
        prause(("The " + enemyInfo["Enemy"] + " cackles maniacally, seemingly forgetting about " + name + " for a moment..."))
    else:
        enemyAttack = MAGEOPTIONS[enemyAttack]
        print("A " + enemyAttack + " blast erupts from the " + enemyInfo["Enemy"] + "'s staff, heading towards", end ="")
        target = random.choice([enemyInfo,playerStats])
        if target == enemyInfo:
            targetName = enemyInfo["Enemy"]
            prause("... themself?!")
        else:
            targetName = target["Name"]
            prause((" " + name + "!"))
        if hitChance > enemyInfo["Accuracy"]:
            prause(MISSLINE + dodge(hitChance,enemyInfo["Enemy"],info))
        if hitChance <= enemyInfo["Accuracy"]:
            if enemyAttack == "pink":
                prause(("The blast connects, and " + targetName + " gets a health boost!"))
                target["Health Current"] += round(target["Level"]*3.5)
                if target["Health Current"] > target["Health Max"]:
                    target["Health Current"] = target["Health Max"]
            else:
                multiplier = 1
                if enemyAttack == "blue":
                    multiplier = 0.5
                if enemyAttack == "yellow":
                    multiplier = 1.5
                if enemyAttack == "red":
                    multiplier = 2.5
                damage = round(enemyInfo["Strength"]*multiplier) + enemyInfo["Weapon"] - target["Defense"]
                if damage <= 0:
                    damage = 1
                prause(("The blast catches " + targetName + ", dealing " + str(damage) + " damage!" + dodge(hitChance,enemyInfo["Enemy"],info)))
                target["Health Current"] = target["Health Current"] - damage
    if targetName == name and damage != 0:#Only occurs if player is hit
        if enemyInfo["Bonus"] in ["Fire","Ice","Poison"]:
            if playerStats["Bonus Effect"] == ["None",0]:
                if random.randint(1,3) == 1:#only 1/3 chance of being effected
                    playerStats["Bonus Effect"] = [enemyInfo["Bonus"],random.randint(1,3)]
    return info

def enemyOptionElemental(info):
    enemyInfo = info["Enemy Info"]
    playerStats = info["Player Stats"]
    name, pronouns = info["Name"],info["Pronouns"]
    bonus = enemyInfo["Bonus"]
    enemyAttack = random.randint(1, 3)
    hitChance = random.randint(0, 100)
    damage = 0
    MISSLINE = ("The " + bonus + " attack can be felt passing by " + name + ", but thankfully misses " + pronouns[1] + ".")
    MISSLINE2 = (name + " manages to dodge to the side as a massive spire of " + bonus + " appears where " + pronouns[0] + " just stood!")
    if enemyInfo["Timer"] != 2 and enemyInfo["Timer"] != 1:
        if enemyAttack == 1:
            prause(("The "+enemyInfo["Enemy"] + " lifts their arm, and begins to form it into a lance of some sort..."))
            enemyInfo["Timer"] = 3
        if enemyAttack == 2:
            prause((name + " suddenly feels " + bonus + " forming around " + pronouns[1] + " feet!"))
            if hitChance > enemyInfo["Accuracy"]:
                prause(MISSLINE2 + dodge(hitChance,enemyInfo["Enemy"],info))
            if hitChance <= enemyInfo["Accuracy"]:
                damage = enemyInfo["Strength"] + enemyInfo["Weapon"] - playerStats["Defense"]
                if damage <= 0:
                    damage = 1
                prause(("A spire of " + bonus + " envelops " + name + ", dealing " + str(damage) +
                        " damage while " + pronouns[0] + " breaks " + pronouns[1] + "self out of it!"
                        + dodge(hitChance,enemyInfo["Enemy"],info)))
                playerStats["Health Current"] = playerStats["Health Current"] - damage
        if enemyAttack == 3:
            print(enemyInfo["Enemy"] + " pulls energy from the air to build up their " + bonus + " body.",end="")
            attempt = False
            while attempt == False:
                try:
                    gainAmount = round(((enemyInfo["Defense Max"]*5)/6)/4)#Converts the defense max to 20% of OG defense, divides by 4.
                    if enemyInfo["Defense Max"] != enemyInfo["Defense"]:
                        prause((" They gain " + str(gainAmount) + " defense!"))
                        enemyInfo["Defense"] += gainAmount
                    if enemyInfo["Defense"] > enemyInfo["Defense Max"]:
                        enemyInfo["Defense"] = enemyInfo["Defense Max"]
                    else:
                        prause((".. But they're too big, and can't get more defense! They take " + str(gainAmount) + " damage!"))
                        enemyInfo["Health Current"] -= gainAmount
                    attempt = True
                except:
                    maxDefense = round(enemyInfo["Defense"]*1.2)
                    enemyInfo.setdefault("Defense Max",maxDefense)
    if enemyInfo["Timer"] == 2:
        prause(("The " + bonus + " lance is almost fully formed!"))
    if enemyInfo["Timer"] == 1:
        prause(("The " + enemyInfo["Enemy"] + " launches the " + bonus + " lance directly at " + name + "'s face!"))
        enemyInfo["Accuracy"] -= 10
        if hitChance > enemyInfo["Accuracy"]:
            prause(MISSLINE + dodge(hitChance,enemyInfo["Enemy"],info))
        if hitChance <= enemyInfo["Accuracy"]:
            damage = round(enemyInfo["Strength"]*3.5) - playerStats["Defense"]
            if damage <= 0:
                damage = 1
            prause(("The blast catches " + name + ", launching " + pronouns[1] + " backward"+pronouns[6]+
                    " and dealing " + str(damage) + " damage!" + dodge(hitChance,enemyInfo["Enemy"],info)))
            playerStats["Health Current"] = playerStats["Health Current"] - damage
        enemyInfo["Accuracy"] += 10
    if damage != 0:#Only occurs if player is hit
        if enemyInfo["Bonus"] in ["Fire","Ice","Poison"]:
            if playerStats["Bonus Effect"] == ["None",0]:
                if random.randint(1,3) == 1:#only 1/3 chance of being effected
                    playerStats["Bonus Effect"] = [enemyInfo["Bonus"],random.randint(1,3)]
    return info

def enemyOptionNighthound(info):
    enemyInfo = info["Enemy Info"]
    playerStats = info["Player Stats"]
    name, pronouns = info["Name"],info["Pronouns"]
    enemyAttack = random.randint(1, 4)
    hitChance = random.randint(0, 100)
    damage = 0
    MISSLINE = ("But " + name + " manages to leap out of the " + enemyInfo["Enemy"] + "'s path in the last moment!")
    if enemyAttack == 1:
        prause(("The " + enemyInfo["Enemy"] + "'s entire head unhinges, revealing a maw of shadows, and attempts to bite " + name + "!"))
        if hitChance > enemyInfo["Accuracy"]:
            prause((MISSLINE + dodge(hitChance,enemyInfo["Enemy"],info)))
        if hitChance <= enemyInfo["Accuracy"]:
            damage = enemyInfo["Strength"] + enemyInfo["Weapon"] - playerStats["Defense"]
            if damage <= 0:
                damage = 1
            prause(("The shadows envelop " + name + ", siphoning " + str(damage) + " life from " + pronouns[1] + "!" + dodge(hitChance,enemyInfo["Enemy"],info)))
            playerStats["Health Current"] = playerStats["Health Current"] - damage
            enemyInfo["Health Current"] += round(damage / 2)
            if enemyInfo["Health Current"] > enemyInfo["Health Max"]:
                enemyInfo["Health Current"] = enemyInfo["Health Max"]
    if enemyAttack == 2 or enemyAttack == 3:
        prause(("The " + enemyInfo["Enemy"] + " liquifies into the shadows, and suddenly launches from " + name + "'s blind spot!"))
        if hitChance > enemyInfo["Accuracy"]:
            prause((MISSLINE + dodge(hitChance,enemyInfo["Enemy"],info)))
        if hitChance <= enemyInfo["Accuracy"]:
            damage = enemyInfo["Strength"] + enemyInfo["Weapon"] - playerStats["Defense"]
            if damage <= 0:
                damage = 1
            prause(("The dark claws slice through " + name + ", dealing " + str(damage) + " damage to " + pronouns[1] + "!" + dodge(hitChance,enemyInfo["Enemy"],info)))
            playerStats["Health Current"] = playerStats["Health Current"] - damage
    if enemyAttack == 4:
        prause((enemyInfo["Enemy"] + " howls with the sounds of a thousand screams, increasing their strength by 10%!\n"))
        enemyInfo["Strength"] = round(1.1*enemyInfo["Strength"])
    if damage != 0:#Only occurs if player is hit
        if enemyInfo["Bonus"] in ["Fire","Ice","Poison"]:
            if playerStats["Bonus Effect"] == ["None",0]:
                if random.randint(1,3) == 1:#only 1/3 chance of being effected
                    playerStats["Bonus Effect"] = [enemyInfo["Bonus"],random.randint(1,3)]
    return info

def enemyOptionAberration(info):
    enemyInfo = info["Enemy Info"]
    playerStats = info["Player Stats"]
    name, pronouns = info["Name"],info["Pronouns"]
    damage = 0
    enemyAttack = random.randint(1, 7)
    hitChance = random.randint(0, 100)
    prause(("The " + enemyInfo["Enemy"] + " is mutating...!"),2)
    MISSLINE = "But the aberration suddenly seizes, unable to finish the attack!"
    if enemyAttack == 1:
        prause(("The " + enemyInfo["Enemy"] + " ogre QUICKLY raises their club, preparing to slam down!"))
        if hitChance > enemyInfo["Accuracy"]:
            prause(("... But the club missed by a wide margin, leaving a crater in the ground." + dodge(hitChance,enemyInfo["Enemy"],info)))
        if hitChance <= enemyInfo["Accuracy"]:
            damage = enemyInfo["Strength"] + enemyInfo["Weapon"] - playerStats["Defense"]
            if damage <= 0:
                damage = 1
            prause(("The club smashes into " + name + ", dealing " + str(damage) + " to " + pronouns[1] + "!" + dodge(hitChance,enemyInfo["Enemy"],info)))
            playerStats["Health Current"] = playerStats["Health Current"] - damage
    if enemyAttack == 2:
        MISSLINE = ("But " + name + " manages to leap out of the " + enemyInfo["Enemy"] + " nighthound's path in the last moment!")
        prause(("The " + enemyInfo["Enemy"] + " nighthound's entire head unhinges, revealing a maw of shadows, and attempts to bite " + name + "!"))
        if hitChance > enemyInfo["Accuracy"]:
            prause((MISSLINE + dodge(hitChance,enemyInfo["Enemy"],info)))
        if hitChance <= enemyInfo["Accuracy"]:
            damage = enemyInfo["Strength"] + enemyInfo["Weapon"] - playerStats["Defense"]
            if damage <= 0:
                damage = 1
            prause(("The " + enemyInfo["Enemy"] + "'s shadows envelop " + name + ", siphoning " + str(damage) + " life from " + pronouns[1] + "!" + dodge(hitChance,enemyInfo["Enemy"],info)))
            playerStats["Health Current"] = playerStats["Health Current"] - damage
            enemyInfo["Health Current"] += round(damage / 2)
            if enemyInfo["Health Current"] > enemyInfo["Health Max"]:
                enemyInfo["Health Current"] = enemyInfo["Health Max"]
    if enemyAttack == 3:
        bonus = random.choice(["Fire","Ice"])
        MISSLINE2 = (name + " manages to dodge to the side as a massive spire of " + bonus + " appears where " + pronouns[0] + " just stood!")
        prause((name + " suddenly feels " + bonus + " forming around " + pronouns[1] + " feet!"))
        if hitChance > enemyInfo["Accuracy"]:
            prause(MISSLINE2 + dodge(hitChance,enemyInfo["Enemy"],info))
        if hitChance <= enemyInfo["Accuracy"]:
            damage = enemyInfo["Strength"] + enemyInfo["Weapon"] - playerStats["Defense"]
            if damage <= 0:
                damage = 1
            prause(("A spire of " + bonus + " envelops " + name + ", dealing " + str(damage) +
                    " damage while " + pronouns[0] + " desperately break" + pronouns[6] + " " + pronouns[1] + "self out of it!"
                    + dodge(hitChance,enemyInfo["Enemy"],info)))
            playerStats["Health Current"] = playerStats["Health Current"] - damage 
    if enemyAttack == 4:
        prause((name + " sees the form of a small child, crying... The child- no, the " + enemyInfo["Enemy"] + " screams, before mutating again!"))
    if enemyAttack == 5:
        MISSLINE = ("The attack grazes past " + name + "'s face, leaving " + pronouns[1] + " frazzled, but unscathed...")
        prause(("The "+enemyInfo["Enemy"] + " dragon lifts their claws, and flies forward!"))
        if hitChance > enemyInfo["Accuracy"]:
            prause(MISSLINE + dodge(hitChance,enemyInfo["Enemy"],info))
        if hitChance <= enemyInfo["Accuracy"]:
            damage = enemyInfo["Strength"] + enemyInfo["Weapon"] - playerStats["Defense"]
            if damage <= 0:
                damage = 1
            prause(("The claws dig deep into " + name + ", dealing " + str(damage) + " damage!" + dodge(hitChance,enemyInfo["Enemy"],info)))
            playerStats["Health Current"] = playerStats["Health Current"] - damage
    if enemyAttack == 6:
        prause(("The " + enemyInfo["Enemy"] + " gnoll readies their cudgel..."))
        if hitChance > enemyInfo["Accuracy"]:
            prause(("The " + enemyInfo["Enemy"] + " gnoll missed " + name + "!" + dodge(hitChance,enemyInfo["Enemy"],info)))
        if hitChance <= enemyInfo["Accuracy"]:
            damage = enemyInfo["Strength"] + enemyInfo["Weapon"] - playerStats["Defense"]
            if damage <= 0:
                damage = 1
            prause(("The aberration's cudgel slams into " + name + " for " + str(damage) + " damage!" + dodge(hitChance,enemyInfo["Enemy"],info)))
            playerStats["Health Current"] = playerStats["Health Current"] - damage
    if enemyAttack == 7:
        prause(("\tThat's...!"),1)
        prause(("The aberration " + name + " raises " + pronouns[2] + " sword to the sky, imbuing it with a corrupted purple light..."))
        if hitChance > enemyInfo["Accuracy"]:
            prause(("The aberration " + name + " slams the sword into the ground as " + name + " dodges!" + dodge(hitChance,enemyInfo["Enemy"],info)))
        if hitChance <= enemyInfo["Accuracy"]:
            damage = round((enemyInfo["Strength"] + enemyInfo["Weapon"] + round(enemyInfo["Level"] * 1.5))/1.75)
            damage = round(damage) - playerStats["Defense"]
            if damage <= 0:
                damage = 1
            prause((pronouns[0].title() + " then slam" + pronouns[6] + " it down upon the actual " + name + ", dealing " + str(damage) + " damage!" + dodge(hitChance,enemyInfo["Enemy"],info)))
            playerStats["Health Current"] = playerStats["Health Current"] - damage
    if damage != 0:#Only occurs if player is hit
        if enemyInfo["Bonus"] in ["Fire","Ice","Poison"]:
            if playerStats["Bonus Effect"] == ["None",0]:
                if random.randint(1,3) == 1:#only 1/3 chance of being effected
                    playerStats["Bonus Effect"] = [enemyInfo["Bonus"],random.randint(1,3)]
    return info

def enemyOptionArmor(info):
    enemyInfo = info["Enemy Info"]
    playerStats = info["Player Stats"]
    name, pronouns = info["Name"],info["Pronouns"]
    enemyAttack = random.randint(1, 3)
    hitChance = random.randint(0, 100)
    graize = random.randint(0,1)
    damage = 0
    graizeDamage = round((enemyInfo["Strength"] + enemyInfo["Weapon"])/10)
    if enemyAttack == 1:
        prause(("The " + enemyInfo["Enemy"] + " suddenly swings their Waraxe!"))
        if hitChance > enemyInfo["Accuracy"]:
            prause((name + " barely manages to dodge the slice, nearly being cut in half..." + dodge(hitChance,enemyInfo["Enemy"],info)))
            if graize == 1:
                prause(("... but " + name + " was graized by the attack, taking " + str(graizeDamage) + " damage!"))
                playerStats["Health Current"] = playerStats["Health Current"] - graizeDamage
        if hitChance <= enemyInfo["Accuracy"]:
            damage = enemyInfo["Strength"] + enemyInfo["Weapon"] - playerStats["Defense"]
            if damage <= 0:
                damage = 1
            prause(("The axe slices deep into " + name + ", dealing " + str(damage) + " to " + pronouns[1] + "!" + dodge(hitChance,enemyInfo["Enemy"],info)))
            playerStats["Health Current"] = playerStats["Health Current"] - damage
    if enemyAttack == 2:
        prause(("The " + enemyInfo["Enemy"] + " launches forward, grabbing " + name + " by the throat!"))
        if hitChance > enemyInfo["Accuracy"]:
            print((name + " slashes the " + enemyInfo["Enemy"] + "'s gauntlet, and manages to break free..." + dodge(hitChance,enemyInfo["Enemy"],info)))
            enemyDamage = playerStats["Weapon"]
            prause((enemyInfo["Enemy"] + " takes " + str(enemyDamage) + " damage from " + name + "'s sword!"))
            enemyInfo["Health Current"] -= enemyDamage
            if enemyInfo["Health Current"] <= 0:
                enemyInfo["Health Current"] = 1
            if graize == 1:
                prause(("... but " + name + "'s throat was nearly crushed, dealing " + str(graizeDamage) + " damage!"))
                playerStats["Health Current"] = playerStats["Health Current"] - graizeDamage
        if hitChance <= enemyInfo["Accuracy"]:
            damage = enemyInfo["Strength"] + 10 - playerStats["Defense"]
            if damage <= 0:
                damage = 1
            prause(("The " + enemyInfo["Enemy"] + " slams " + name + " into the ground and then throws " +
                    pronouns[1] + " across the room, dealing " + str(damage) + " damage!" + dodge(hitChance,enemyInfo["Enemy"],info)))
            playerStats["Health Current"] = playerStats["Health Current"] - damage
    if enemyAttack == 3:
        prause(("The " + enemyInfo["Enemy"] + " seems to harden, and their Waraxe sharpens! +3 Defense, +3 Strength, +3 Weapon Strength!"))
        enemyInfo["Defense"] += 3
        enemyInfo["Strength"] += 3
        enemyInfo["Weapon"] += 3
    if damage != 0:#Only occurs if player is hit
        if enemyInfo["Bonus"] in ["Fire","Ice","Poison"]:
            if playerStats["Bonus Effect"] == ["None",0]:
                if random.randint(1,3) == 1:#only 1/3 chance of being effected
                    playerStats["Bonus Effect"] = [enemyInfo["Bonus"],random.randint(1,3)]
    return info


def enemyOptionQueen(info):# NEED TO CHANGE 
    enemyInfo = info["Enemy Info"]
    playerStats = info["Player Stats"]
    name, pronouns = info["Name"],info["Pronouns"]
    enemyAttack = random.randint(1, 3)
    hitChance = random.randint(0, 100)
    MISSLINE = ("The Queen's claws nearly hit, but just slip past " + name + ".")
    MISSLINE2 = (name + " barely avoids the Shadow Spike as it pierces through the wall of the Tower.")
    MISSLINE3 = (name + " uses the Flame Glove to launch " + pronouns[1] + "self over the blast and safely land!")
    if enemyInfo["Timer"] == 1:
        prause(("A massive wave of shadows bursts forth from the Queen's hands!"))
        enemyInfo["Accuracy"] -= 5
        if hitChance > enemyInfo["Accuracy"]:
            prause(MISSLINE3 + dodge(hitChance,enemyInfo["Enemy"],info))
        if hitChance <= enemyInfo["Accuracy"]:
            damage = round(enemyInfo["Strength"]*1.5) + enemyInfo["Weapon"] - playerStats["Defense"]
            if damage <= 0:
                damage = 1
            prause(("The blast wave launches " + name + " backward and into the wall, " +
                    "dealing " + str(damage) + " damage!" + dodge(hitChance,enemyInfo["Enemy"],info)))
            playerStats["Health Current"] = playerStats["Health Current"] - damage
        enemyInfo["Accuracy"] += 5
    else:
        if enemyAttack == 1:
            prause(("The Queen pools energy into her hands..."))
            enemyInfo["Timer"] = 2
        if enemyAttack == 2:
            prause(("The shape of the Queen blurs, and she appears directly in front of " + name + ", claws at the ready!"))
            if hitChance > enemyInfo["Accuracy"]:
                prause(MISSLINE + dodge(hitChance,enemyInfo["Enemy"],info))
            if hitChance <= enemyInfo["Accuracy"]:
                damage = enemyInfo["Strength"] + enemyInfo["Weapon"] + round(enemyInfo["Speed"]*0.2) - playerStats["Defense"]
                if damage <= 0:
                    damage = 1
                prause(("She's too fast for " + name + " to dodge, and her claw rips into " + pronouns[2] +
                        " armor for " + str(damage) + " damage!" + dodge(hitChance,enemyInfo["Enemy"],info)))
                playerStats["Health Current"] = playerStats["Health Current"] - damage
        if enemyAttack == 3:
            prause(("The queen forms a spike with dark energy, and it launches towards " + name + "!"))
            if hitChance > enemyInfo["Accuracy"]:
                prause(MISSLINE2 + dodge(hitChance,enemyInfo["Enemy"],info))
            if hitChance <= enemyInfo["Accuracy"]:
                damage = round(enemyInfo["Strength"]+enemyInfo["Weapon"]+5) - playerStats["Defense"]
                if damage <= 0:
                    damage = 1
                prause(("The spike hits " + name + " in the side, " +
                        "dealing " + str(damage) + " damage!" + dodge(hitChance,enemyInfo["Enemy"],info)))
                playerStats["Health Current"] = playerStats["Health Current"] - damage

    return info

# Extra move for Phase 2.
def enemyOptionQueenOne(info):
    enemyInfo = info["Enemy Info"]
    playerStats = info["Player Stats"]
    name, pronouns = info["Name"],info["Pronouns"]
    hitChance = random.randint(0, 100)
    MISSLINE = (name + " dodges the wind attacks, but can't get close for a counterattack...")
    MISSLINE2 = (name + " manages to duck as the blade gives " + name + " a haircut...")
    if enemyInfo["Timer"] == 2:
        prause(("While she's building energy, she uses her wings to launch gusts of air at " + name + "!"))
        if hitChance > enemyInfo["Accuracy"]:
            prause(MISSLINE + dodge(hitChance,enemyInfo["Enemy"],info))
        if hitChance <= enemyInfo["Accuracy"]:
            landedHits = random.randint(1,3)
            damage = round(enemyInfo["Strength"]*0.75) + enemyInfo["Weapon"] - playerStats["Defense"]
            if damage <= 0:
                damage = 1
            prause((name + " is hit by " + str(landedHits) + " of the blasts, taking " + str(damage) + " damage per hit!" + dodge(hitChance,enemyInfo["Enemy"],info)))
            playerStats["Health Current"] = playerStats["Health Current"] - (damage*landedHits)
    elif enemyInfo["Timer"] == 1:
        prause(("Just as " + name + " recovers from the blast wave, the Queen leaps forward with a massive shadow Greatsword!"))
        if hitChance > enemyInfo["Accuracy"]:
            prause(MISSLINE2 + dodge(hitChance,enemyInfo["Enemy"],info))
        if hitChance <= enemyInfo["Accuracy"]:
            damage = enemyInfo["Strength"] + enemyInfo["Weapon"] - playerStats["Defense"]
            if damage <= 0:
                damage = 1
            prause((name + " partially blocks it with " + pronouns[2] + " sword, but is still thrown to the side and takes " +
                    str(damage) + " damage." + dodge(hitChance,enemyInfo["Enemy"],info)))
            playerStats["Health Current"] = playerStats["Health Current"] - (damage)
    else:
        prause(("Before " + name + " can get " + pronouns[2] + " footing, the Queen goes for a roundhouse kick!"))
        if hitChance > enemyInfo["Accuracy"]:
            prause((name + " ducks under the kick and rolls away, narrowly keeping " + pronouns[2] +
                    " head intact." + dodge(hitChance,enemyInfo["Enemy"],info)))
        if hitChance <= enemyInfo["Accuracy"]:
            damage = round(enemyInfo["Strength"]*0.75) + enemyInfo["Weapon"] - playerStats["Defense"]
            if damage <= 0:
                damage = 1
            prause((name + " blocks the blow with " + pronouns[2] + " sword, but still takes " + str(damage) + " damage!" + dodge(hitChance,enemyInfo["Enemy"],info)))
            playerStats["Health Current"] = playerStats["Health Current"] - damage
    return info

##def enemyOptionQueenTwo(info):#NEED TO CHANGE
##    enemyInfo = info["Enemy Info"]
##    playerStats = info["Player Stats"]
##    name, pronouns = info["Name"],info["Pronouns"]
##    enemyAttack = random.randint(1, 3)
##    hitChance = random.randint(0, 100)
##    MISSLINE = ("The " + bonus + " attack can be felt passing by " + name + ", but thankfully misses " + pronouns[1] + ".")
##    MISSLINE2 = (name + " manages to dodge to the side as a massive spire of " + bonus + " appears where " + pronouns[0] + " just stood!")
##    if enemyInfo["Timer"] != 2 and enemyInfo["Timer"] != 1:
##        if enemyAttack == 1:
##            prause(("The "+enemyInfo["Enemy"] + " lifts their arm, and begins to form it into a lance of some sort..."))
##            enemyInfo["Timer"] = 3
##        if enemyAttack == 2:
##            prause((name + " suddenly feels " + bonus + " forming around " + pronouns[1] + " feet!"))
##            if hitChance > enemyInfo["Accuracy"]:
##                prause(MISSLINE2 + dodge(hitChance,enemyInfo["Enemy"],info))
##            if hitChance <= enemyInfo["Accuracy"]:
##                damage = enemyInfo["Strength"] + enemyInfo["Weapon"] - playerStats["Defense"]
##                if damage <= 0:
##                    damage = 1
##                prause(("A spire of " + bonus + " envelops " + name + ", dealing " + str(damage) +
##                        " damage while " + pronouns[0] + " breaks " + pronouns[1] + "self out of it!"
##                        + dodge(hitChance,enemyInfo["Enemy"],info)))
##                playerStats["Health Current"] = playerStats["Health Current"] - damage
##        if enemyAttack == 3:
##            print(enemyInfo["Enemy"] + " pulls energy from the air to build up their " + bonus + " body.",end="")
##            attempt = False
##            while attempt == False:
##                try:
##                    gainAmount = round(((enemyInfo["Defense Max"]*5)/6)/4)#Converts the defense max to 20% of OG defense, divides by 4.
##                    if enemyInfo["Defense Max"] != enemyInfo["Defense"]:
##                        prause((" They gain " + str(gainAmount) + " defense!"))
##                        enemyInfo["Defense"] += gainAmount
##                    if enemyInfo["Defense"] > enemyInfo["Defense Max"]:
##                        enemyInfo["Defense"] = enemyInfo["Defense Max"]
##                    else:
##                        prause((".. But they're too big, and can't get more defense! They take " + str(gainAmount) + " damage!"))
##                        enemyInfo["Health Current"] -= gainAmount
##                    attempt = True
##                except:
##                    maxDefense = round(enemyInfo["Defense"]*1.2)
##                    enemyInfo.setdefault("Defense Max",maxDefense)
##    if enemyInfo["Timer"] == 2:
##        prause(("The " + bonus + " lance is almost fully formed!"))
##    if enemyInfo["Timer"] == 1:
##        prause(("The " + enemyInfo["Enemy"] + " launches the " + bonus + " lance directly at " + name + "'s face!"))
##        enemyInfo["Accuracy"] -= 10
##        if hitChance > enemyInfo["Accuracy"]:
##            prause(MISSLINE + dodge(hitChance,enemyInfo["Enemy"],info))
##        if hitChance <= enemyInfo["Accuracy"]:
##            damage = round(enemyInfo["Strength"]*3.5) - playerStats["Defense"]
##            if damage <= 0:
##                damage = 1
##            prause(("The blast catches " + name + ", launching " + pronouns[1] + " backward"+pronouns[6]+
##                    " and dealing " + str(damage) + " damage!" + dodge(hitChance,enemyInfo["Enemy"],info)))
##            playerStats["Health Current"] = playerStats["Health Current"] - damage
##        enemyInfo["Accuracy"] += 10
##    return info

# Chooses which enemyOption to use based on the name of the enemy itself. Requires info
# to change player health and whatnot.
def enemyOption(info,boss=False):
    enemyInfo = info["Enemy Info"]
    if boss == False:
        if "Slime" in enemyInfo["Enemy"]:
            enemyOptionSlime(info)
        if "Gnoll" in enemyInfo["Enemy"]:
            enemyOptionGnoll(info)
        if "Ogre" in enemyInfo["Enemy"]:
            enemyOptionOgre(info)
        if "Dragon" in enemyInfo["Enemy"]:
            enemyOptionDragon(info)
        if "Mad Mage" in enemyInfo["Enemy"]:
            enemyOptionMadMage(info)
        if "Nighthound" in enemyInfo["Enemy"]:
            enemyOptionNighthound(info)
        if "Aberration" in enemyInfo["Enemy"]:
            enemyOptionAberration(info)
            if random.randint(0,1) == 1:
                enemyOptionAberration(info)
        if "Elemental" in enemyInfo["Enemy"]:
            enemyOptionElemental(info)
        if "Possessed Armor" in enemyInfo["Enemy"]:
            enemyOptionArmor(info)
    else:
        if "Queen" in enemyInfo["Enemy"]:
            enemyOptionQueen(info)
            if info["Phase"] != 0:
                enemyOptionQueenOne(info)#Boss gets extra moves in 2nd battle
    info = bonusEffect(info)
    return info

# This takes whatever bonus effect the enemy has dealt the player, and
# affects the player appropriately until the effect wears off.
# format for "Bonus Damage" is [effect,timeLeft]; ex: ["fire",2]
# When hit, the player is given the bonusEffect the enemy has, and a
# randomized turn amount that the enemy's effect will last for.
# Runs at the end of the enemy's turn, in enemyOptions().
def bonusEffect(info):
    name = info["Name"]
    pronouns = info["Pronouns"]
    playerStats = info["Player Stats"]
    try:
        bonusType = playerStats["Bonus Effect"][0]
        bonusTurns = playerStats["Bonus Effect"][1]
    except:
        bonusType = "None"
        bonusTurns = 0
    if bonusType == "None":
        info["Old Value"] = -1#Set to an impossible value to make sure func works.
    if bonusTurns == 0:
        bonusLine = ""
        if bonusType == "Fire":
            bonusLine = "on fire"
        elif bonusType == "Ice":
            bonusLine = "frozen"
            playerStats["Speed"] = info["Old Value"]
        elif bonusType == "Poison":
            bonusLine = "poisoned"
            playerStats["Strength"] = info["Old Value"]
        if bonusType != "None":
            prause((name + " is no longer " + bonusLine + "!"))
            playerStats["Bonus Effect"] = ["None",0]
    else:
        damage = round(info["Player Stats"]["Health Max"]/20)
        if bonusType == "Fire":
            prause((name + " is on fire! " + pronouns[0].title() + " take" +
                    pronouns[6] + " " + str(damage) + " damage!"))
            info["Player Stats"]["Health Current"] -= damage
        if bonusType == "Ice":
            prause((name + " is frozen! " + pronouns[0].title() + " " +
                    pronouns[4] + " slowed down!"))
            if info["Old Value"] == -1:
                info["Old Value"] = playerStats["Speed"]
                playerStats["Speed"] = 1
        if bonusType == "Poison":
            prause((name + " is poisoned! " + pronouns[0].title() + " take" +
                    pronouns[6] + " " + str(damage) + " and loses " + pronouns[2] +
                    " strength!"))
            info["Player Stats"]["Health Current"] -= damage
            if info["Old Value"] == -1:
                info["Old Value"] = playerStats["Strength"]
                playerStats["Strength"] = round(info["Old Value"]/5)
        bonusTurns -= 1
        playerStats["Bonus Effect"][1] = bonusTurns
    return info
    
# after an enemy dies, this sets the player's HP and ABP to their max, and 1/4 times gives a potion if you don't have the full amount.
def victoryCheck(info):
    enemyInfo = info["Enemy Info"]
    playerStats = info["Player Stats"]
    name, pronouns = info["Name"],info["Pronouns"]
    if enemyInfo["Health Current"] <= 0:
        prause(("You have defeated the " + enemyInfo["Enemy"] + "! Your HP and ABP are fully restored.\n"))
        playerStats["Health Current"] = playerStats["Health Max"]
        playerStats["Ability Current"] = playerStats["Ability Max"]
        playerStats["XP Current"] += enemyXP(enemyInfo["Level"])
        if info["Potions"] != info["Potions Max"]:
            if random.randint(1,info["Difficulty"]) == 1:
                prause("\tYou found a potion! Added to your inventory.\n")
                info["Potions"] += 1
            if info["Potions"] > info["Potions Max"]:
                info["Potions"] = info["Potions Max"]
        while playerStats["XP Current"] >= playerStats["XP Max"]:
            info = levelUp(info)
    return info

# If the player dies in battle during the battleLoop, then defeatCheck() activates and quits out.
def defeatCheck(info):
    enemyInfo = info["Enemy Info"]
    playerStats = info["Player Stats"]
    name, pronouns = info["Name"],info["Pronouns"]
    if playerStats["Health Current"] <= 0:
        playerStats["Health Current"] = 0
        prause("You fall to the ground, heavily injured...")
        if info["Potions"] >= 1:
            prause("You reach into your potions bag, grab one, and chug the crimson liquid inside.")
            info["Potions"] -= 1
            playerStats["Health Current"] = round(playerStats["Health Max"] * 0.8)
        else:
            prause("You try reaching for a potion, but your bag is empty!")
            prause("As you panic, the " + enemyInfo["Enemy"] + " approaches to end your life.")
            info["DEMISE"]["Player"] = True
    return info

# Sword Source: asciiart.eu/weapons/swords
# Other art is 9x9.
def asciiArt(info):
    #(to be clear this is not my art, source is "asciiart.eu/weapons/swords")
    #if info["Equipment"]["Weapon"] == "Simple Sword":
    SWORD = """
    ,_,_,_,_,_,_,_,_,_,_|___________________________________________________
    | | | | | | | | | | |__________________________________________________/
    '-'-'-'-'-'-'-'-'-'-|-------------------------------------------------"""
##    FIERCE = """
##                 ____________    ____________
##                / __________ \  / __________ \\\\
##     __________/ /          \ \/ /          \ \\\\
##     *--------*\ \__________/ /\ \__________/ //
##                \____________/  \____________//
##"""
##    FIERCEVER2 = """
##                 ____________     ____________
##                / __________ \   / __________ \\\\
##     __________/ /          \ \ / /          \ \\\\
##    |_________|=<            >=X=<            >==>
##     '--------'\ \__________/ / \ \__________/ //
##                \____________/   \____________//
##"""
##    PLAYER = """
##"""
    return SWORD

# This is the overall loop for battles.
def battleLoop(info,boss=False,damageType=False):#basic loop that determines attack order, keeps eye on HP of characters in battle
    enemyInfo = enemyDecide(info,boss)
    info["Enemy Info"] = enemyInfo
    if damageType != False:
        damage = 0
        if damageType == "fire":
            damage = (info["Player Stats"]["Level"] * 2)
        if damageType == "bomb":
            damage = (info["Player Stats"]["Level"] * 2)
        info["Enemy Info"]["Health Current"] = call("Health Current",enemyInfo) - damage
        if info["Enemy Info"]["Health Current"] <= 0:
            info["Enemy Info"]["Health Current"] = 1
    prause("An enemy approaches, prepare for battle!")
    print()
    playerStats = info["Player Stats"]
    info["Cooldowns"] = [0,0,0,0,0]
    enemyInfo["Timer"] = 0
    name, pronouns = info["Name"],info["Pronouns"]
    print(asciiArt(info))
    while playerStats["Health Current"] > 0 and enemyInfo["Health Current"] > 0:
        if playerStats["Ability Current"] < 0:
            playerStats["Ability Current"] = 0
        if enemyInfo["Timer"] > 0:
            enemyInfo["Timer"] -= 1
        battleStats(info)
        if playerStats["Speed"] >= enemyInfo["Speed"]:
            info = battleOptions(info)
            info = victoryCheck(info)
            if enemyInfo["Health Current"] <= 0:
                break
            info = enemyOption(info,boss)
            info = defeatCheck(info)
            if info["DEMISE"]["Player"] == True:
                break
        if enemyInfo["Speed"] > playerStats["Speed"]:
            prause("\n\tThe enemy gets to move first...\n")
            info = enemyOption(info,boss)
            info = defeatCheck(info)
            if info["DEMISE"]["Player"] == True:
                break
            info = battleOptions(info)
            info = victoryCheck(info)
    return info

# Checks what the destination's character is (?1, i3, etc) and returns the loot that is in the
# specific character's container, so to speak.
def roomCont(destination,info):
    playerX = info["Position"]["U1"]["X"]
    playerY = info["Position"]["U1"]["Y"]
    destX = destination[1][0]
    destY = destination[1][1]
    destChar = destination[0]
    roomNumber = info["Room Number"]
    successLoot = {destChar:{"Nothing":"Nothing."}}
    #if info["Region"] == "forest":
    if roomNumber == [3,4]:
        loot = {"?1":{"Weapon":"Simple Sword"}}
    if roomNumber == [2,6]:
        loot = {"i1":{"Armor":"Upgrade"}}
    if roomNumber == [3,6]:
        loot = {"i1":{"Armor":"Upgrade"}}
    if roomNumber == [5,7]:
        loot = {"i1":{"Gold":1000}}
    if roomNumber == [7,4]:
        loot = {"i1":{"Weapon":"Upgrade"}}
    if roomNumber == [7,6]:
        loot = {"i1":{"Armor":"Upgrade"}}
    if roomNumber == [4,10]:
        loot = {"i1":{"Weapon":"Upgrade"}}
    if roomNumber == [6,2]:
        loot = {"?1":{"Key Pieces":1}}
    if roomNumber == [5,9]:
        loot = {"?1":{"Key Pieces":1}}
    if roomNumber == [8,6]:
        destChar = "?1"
        if destY == 2 and destX == 4:
            loot = {"?1":{"...":"crushed dogtag"}}
        elif destY == 4 and destX == 7:
            loot = {"?1":{"...":"letter to a lover"}}
        elif destY == 9 and destX == 7:
            loot = {"?1":{"...":"wedding ring"}}
        else:
            destChar = "i1"
            loot = {"i1":{"Weapon":"Upgrade"}}
    try:
        if destChar in loot:
            successLoot = loot[destChar]
            #del info["Position"][destChar]
    except:
        successLoot = {"Potion":1}
    return successLoot

# This function stores all of the default copies of each room in the game, using standard cartesian coordinates
# to determine which room to load. Only used the first time a player enters each room.
def roomDefaultCopy(info):
##            A= "|---------|"
##            B= "|         |"
##            C= "|         |"
##            D= "|         |"
##            E= "|         |"
##            F= "|         |"
##            G= "|         |"
##            H= "|         |"
##            I= "|         |"
##            J= "|         |"
##            K= "|---------|"
    # U = player, G is a glacier, requiring fire to unblock the path. B is a bombable Boulder blocking paths.
    # Player; D = door or path; R = region change, similar to door; e/E = enemies, inact/active. ! is quest giver/event.
    # ? = item of interest or unknown; i/I = item, like gold or equipment. x,-,| are walls. N = NPC.
    # Naming for base strings based on coordinate system; 00 is bottom left, 01 one right, 11 one up + one right, etc.
    # set up this way to keep the default values for a map set up.
    roomCall = info["Room Number"]
    if info["Region"] == "forest":
        if [3,4] == roomCall:
            #starting room
            A= "|----D----|"
            B= "|XXXX XXXX|"
            C= "|XXx e  XX|"
            D= "|Xx      X|"
            E= "|X       X|"
            F= "|x   | |xX|"
            G= "|Xx  | |xX|"
            H= "|XXXx|?|XX|"
            I= "|X      xX|"
            J= "|x     xXX|"
            K= "|---------|"
                    
        if [3,5] == roomCall:
            A= "|----D----|"
            B= "|XXXX XXXX|"
            C= "|XXXX XXXX|"
            D= "|XXXxBxXXX|"
            E= "|xxx   xXX|"
            F= "D xXx   XX|"
            G= "| Xx e  XX|"
            H= "|ex  X  XX|"
            I= "| x Xx xXX|"
            J= "|e  X  XXX|"
            K= "|----D----|"
        if [2,5] == roomCall:
            A= "|----D----|"
            B= "|XXXX  XXX|"
            C= "|XX  e  XX|"
            D= "|X      XX|"
            E= "|X  XXXXXX|"
            F= "|XeXX e X D"
            G= "|X XX   X |"
            H= "|X    X Xe|"
            I= "|X XX   X |"
            J= "|X    X   |"
            K= "|---------|"
        if [2,6] == roomCall:
            A= "|---------|"
            B= "|XXXXXXXGi|"
            C= "|XXXXXXX X|"
            D= "|XX   e   |"
            E= "|         |"
            F= "| X   XXX D"
            G= "|    XXXXX|"
            H= "|   XXXXXX|"
            I= "| Xe XXXXX|"
            J= "| e   XXXX|"
            K= "|----D----|"
        if [3,6] == roomCall:
            A= "|---------|"
            B= "|XXXXXXXXX|"
            C= "|XX XX XXX|"
            D= "|X     XXX|"
            E= "|     XXX |"
            F= "D         R"
            G= "|     XXX |"
            H= "|X XX  XX |"
            I= "|XXXXBXXXX|"
            J= "|Xi   XXXX|"
            K= "|----D----|"
    if info["Region"] == "village":
        if [4,6] == roomCall:
            #first part of village
            A= "|-D-----D-|"
            B= "|   N     D"
            C= "|    X    D"
            D= "|N       N|"
            E= "|XXN      |"
            F= "R         |"
            G= "|XXN     N|"
            H= "||-|  N|-||"
            I= "||S     T||"
            J= "||-|N  |-||"
            K= "|---------|"
        if [4,7] == roomCall:
            #path to tundra
            A= "|----R----|"
            B= "|XXXX XXXX|"
            C= "|XXXXGXXXX|"
            D= "|xx N N xx|"
            E= "|         |"
            F= "|         |"
            G= "|--- - ---|"
            H= "|N   |   x|"
            I= "|x   |N   |"
            J= "|    |    |"
            K= "|-D-----D-|"
        if [5,6] == roomCall:
            #tavern
            A= "|---DDD---|"
            B= "D  N   N  D"
            C= "D         D"
            D= "|---X X---|"
            E= "| xN   | x|"
            F= "|      N x|"
            G= "|NxN   ---|"
            H= "|         |"
            I= "|NxN  N   |"
            J= "|    NxN x|"
            K= "|---------|"
            # soldiers a  b  b  c  c  d  d  d  owner
            #56: 31 71 34 16 36 18 38 68 59 79 75
        if [5,7] == roomCall:
            #Mayor's office
            A= "|---------|"
            B= "|    N    |"
            C= "|   XxX   |"
            D= "|         |"
            E= "|XXXX XXXX|"
            F= "|   N N   |"
            G= "|         |"
            H= "| N     N |"
            I= "|x       x|"
            J= "|XXx   xXX|"
            K= "|---DDD---|"
            # mayor   soldiers
            #57: 51 45 65 27 87
        if [6,6] == roomCall:
            A= "|---------|"
            B= "D        !D"
            C= "D        !D"
            D= "|     N   |"
            E= "|XXXX XXXX|"
            F= "|   | |   |"
            G= "|N--| |--N|"
            H= "|         |"
            I= "|   | |   |"
            J= "|  x| | x |"
            K= "|XXXXDXXXX|"
            #soldier merchants
            #66: 63  15 95
        if [6,5] == roomCall:
            A= "|----D----|"
            B= "|XX   xxXX|"
            C= "|XX   xxXX|"
            D= "| xx      |"
            E= "|  xx     |"
            F= "|         |"
            G= "|   N N   |"
            H= "|xxx   xxx|"
            I= "|XXXXBXXXX|"
            J= "|XXX   XXX|"
            K= "|----R----|"
            #soldiers
            #65: 46 66
        if [7,6] == roomCall:
            A= "|---------|"
            B= "D  NXXXXXX|"
            C= "D   NXXXXX|"
            D= "|X   XX XX|"
            E= "|XN NXN NX|"
            F= "|X        R"
            G= "|XN NXN NX|"
            H= "|X   XXiXX|"
            I= "|XN NXXXXX|"
            J= "|X N XXXXX|"
            K= "|---------|"

    if info["Region"] == "mountains":
        if [6,4] == roomCall:
            A= "|----R----|"
            B= "|XX     XX|"
            C= "|XXX   XXX|"
            D= "|  Xx xX  |"
            E= "|   eB    |"
            F= "|     XXXX|"
            G= "|  XXX    |"
            H= "|BeBe     D"
            I= "|XXX      D"
            J= "|XXXX XX  D"
            K= "|---------|"
        if [7,4] == roomCall:
            A= "|---------|"
            B= "|| Be   B D"
            C= "||L|--|eB D"
            D= "||   K|xxx|"
            E= "|| |--|Xe D"
            F= "|X   XXXXX|"
            G= "| Xx  XXi D"
            H= "D  XxBBXXX|"
            I= "D    eXX  D"
            J= "D   XX  e D"
            K= "|-----DDD-|"
        if [8,4] == roomCall:
            A= "|---------|"
            B= "D  xXXe  K|"
            C= "D   BX XXX|"
            D= "|XXxBXe Be|"
            E= "D eXe XX| |"
            F= "|X Xx  x| |"
            G= "D e  X  |e|"
            H= "|XXXLX|e| |"
            I= "D  L   K| |"
            J= "D  xXx    |"
            K= "|---------|"
        if [7,3] == roomCall:
            A= "|-----DDD-|"
            B= "|XXXx    X|"
            C= "|XXx  xXX D"
            D= "|  eBxX   D"
            E= "|exXXXX  X|"
            F= "|B xXXXx X|"
            G= "|x e  Be x|"
            H= "|---------|"
            I= "D   eB    D"
            J= "D   XXX   D"
            K= "|---------|"
        if [8,3] == roomCall:
            A= "|---------|"
            B= "|XXXXX| Be|"
            C= "D  |XK| | |"
            D= "D  |X | | |"
            E= "|  |X   | |"
            F= "|BB|x  x|B|"
            G= "|   e  X e|"
            H= "|---xXX  x|"
            I= "D   L eBxX|"
            J= "D    xXXXX|"
            K= "|---------|"
        if [6,3] == roomCall:
            A= "|----D----|"
            B= "|     | eB|"
            C= "| |---- X |"
            D= "| |Xx eBX |"
            E= "| |x  xXx |"
            F= "| |B BXXBe|"
            G= "| |BBBXX x|"
            H= "| |X e Xe |"
            I= "| |XxBxX  D"
            J= "| |Xx xX  D"
            K= "|D---D----|"
        if [6,2] == roomCall:
            # BOSS ROOM of Mountains!... not implemented yet.
            A= "|D---D----|"
            B= "| |      -|"
            C= "| |      ||"
            D= "| |     -||"
            E= "| |     |||"
            F= "| |-   -|||"
            G= "| ||   ||||"
            H= "| ||- -||||"
            I= "| |||?|||||"
            J= "|     |||||"
            K= "|---------|"

    if info["Region"] == "tundra":
        if [4,8] == roomCall:
            A= "|-------DD|"
            B= "|X|G  |X  |"
            C= "|X|e|e|   |"
            D= "|X|G|G| xx|"
            E= "|X|G|G|eG |"
            F= "|X|G| |xx |"
            G= "|X|G|     |"
            H= "|X  xXXXXX|"
            I= "|X   xXXXX|"
            J= "|XX   xXXX|"
            K= "|----R----|"
        if [4,9] == roomCall:
            A= "|-------DD|"
            B= "| GG GG e |"
            C= "|L--------|"
            D= "|     eK|X|"
            E= "|x e xxXXx|"
            F= "|Xx XXX K |"
            G= "|--L--|  x|"
            H= "| G     xX|"
            I= "| G|------|"
            J= "|    GeG  |"
            K= "|-------DD|"
        if [4,10] == roomCall:
            A= "|---------|"
            B= "|    eGG  D"
            C= "|iX----|  D"
            D= "|XxXxKx|--|"
            E= "| Ge   |KG|"
            F= "|e||---|| D"
            G= "|G||  G|| D"
            H= "| || | eGL|"
            I= "| || |----|"
            J= "|  GGe    |"
            K= "|-------DD|"
        if [5,10] == roomCall:
            A= "|---------|"
            B= "D e  GGG  D"
            C= "D  |------|"
            D= "|--|    L |"
            E= "| GGe|-G-G|"
            F= "D  | |KG| |"
            G= "D  | |--|e|"
            H= "|--|G| eL |"
            I= "|KX|G| |--|"
            J= "|eG  | e  D"
            K= "|---------|"
        if [5,9] == roomCall:
            # BOSS ROOM of Tundra... bosses aren't implemented yet sadly.
            A= "|---------|"
            B= "|--------||"
            C= "|------|  |"
            D= "|----|    |"
            E= "|--|      |"
            F= "D ?       |"
            G= "|--|      |"
            H= "|----|    |"
            I= "|------|  |"
            J= "|--------||"
            K= "|---------|"
        if [6,9] == roomCall:
            A= "|-------DD|"
            B= "|XXXeGe|  |"
            C= "|X|- - -| |"
            D= "|e eG|G |G|"
            E= "|L|---| |G|"
            F= "D |xxxx |G|"
            G= "|--xXKx |G|"
            H= "|  GGGx |e|"
            I= "| -xxxx |G|"
            J= "|e GGG    |"
            K= "|---------|"
        if [6,10] == roomCall:
            A= "|---------|"
            B= "D xXXx L G|"
            C= "| xxxx |-G|"
            D= "| Gee  |  |"
            E= "|------- -|"
            F= "|  e |   L|"
            G= "| X|G|G||G|"
            H= "| e|G|e||G|"
            I= "|X | |G||e|"
            J= "D  |K  |  |"
            K= "|-------DD|"
    
    if info["Region"] == "tower":
        #first room is between village and tower;
        #here to provide a bit of an emotional gut punch.
        if [8,6] == roomCall:
            A= "|---------|"
            B= "|XX      x|"
            C= "|XX ? | xX|"
            D= "|XX   |  x|"
            E= "|XX|-  ?xX|"
            F= "R  |      D"
            G= "|X |-   xX|"
            H= "|X    |  x|"
            I= "|XX   | xX|"
            J= "|XX    ?ix|"
            K= "|---------|"


        if [9,6] == roomCall:
            A= "|----D----|"
            B= "|XXXx xXXX|"
            C= "|Xx  e  xX|"
            D= "|Xx     xX|"
            E= "|X       X|"
            F= "D       e D"
            G= "|X       x|"
            H= "|Xx     xX|"
            I= "|XXXxxxXXX|"
            J= "|XXXXXXXXX|"
            K= "|---------|"
        if [9,7] == roomCall:
            A= "|---------|"
            B= "|   XxXxXx|"
            C= "| x GexXxX|"
            D= "|GXxX  xXx|"
            E= "|GxXxBB GG|"
            F= "|eBB eXx  |"
            G= "|  XxXxX  |"
            H= "|  xXxXxee|"
            I= "|BBXxXxX  |"
            J= "| GGe  x K|"
            K= "|----D----|"#8
        if [10,6] == roomCall:
            A= "|--D---D--|"
            B= "|x e xX Xx|"
            C= "|X   Xx e D"
            D= "|xeBexXxXx|"
            E= "|Xx xXxXxX|"
            F= "D X XxXx  D"
            G= "|Lx  GeG  D"
            H= "|eXxXxXxXx|"
            I= "|GxXxXxe  D"
            J= "|GB  eGB  D"
            K= "|---------|"#15
        if [10,7] == roomCall:
            A= "|-DD------|"
            B= "|x  XxXxXx|"
            C= "|XxLxXxX  D"
            D= "|x   GeG  D"#28
            E= "|XxXxXxXxX|"#-
            F= "|xXxXxXxXx|"
            G= "|XxB  GGe |"
            H= "|G eXxXxX |"
            I= "|GxXxXx eB|"
            J= "|   XxX Xx|"
            K= "|--D---D--|"#18
        if [11,6] == roomCall:
            A= "|------DD-|"
            B= "|xXxXxX  x|"
            C= "D  eGGBe X|"
            D= "|    BXxXx|"
            E= "|XxXxXxXxX|"
            F= "D  eGGG   |"
            G= "D   xXx  e|"
            H= "|xXxXxXxX |"
            I= "D    BeGGG|"
            J= "D     BxXx|"
            K= "|---------|"#23
        if [11,7] == roomCall:
            A= "|---------|"
            B= "|xXx     K|"
            C= "D xX XxXxX|"
            D= "D Xx GeG e|"
            E= "| xXxXxXxG|"
            F= "| XxeB    |"
            G= "|GxX XxXxX|"
            H= "|GXx GeG  |"
            I= "|GxXxXxXBB|"
            J= "|         |"
            K= "|------DD-|"#27
        if [10,8] == roomCall:
            A= "|-DD------|"
            B= "|xeBXxXxXx|"
            C= "|XB  GeG  |"
            D= "|xXxXxXxX |"
            E= "|Be  BeB  |"
            F= "| XxXxXxXx|"
            G= "|ee GGG eG|"
            H= "|xXxXxXxXG|"
            I= "|X   Be   |"
            J= "|x  XxXxXx|"
            K= "|-DD------|"#36
        if [10,9] == roomCall:
            A= "|----R----|"
            B= "|xXx ! xXx|"
            C= "|XxX      |"
            D= "|xXxXxXxX |"
            E= "|         |"
            F= "| XxXxXxXx|"
            G= "|         |"
            H= "|xXxXxXxX |"
            I= "|X        |"
            J= "|x  XxXxXx|"
            K= "|-DD------|"

        # QUEEN'S CHAMBERS!
    if info["Region"] == "boss":
        if [10,10] == roomCall:
            A= "|---------|"
            B= "|XXXXXXXXX|"
            C= "|xxxxxxxxx|"
            D= "|x       x|"
            E= "|x       x|"
            F= "|x   Q   x|"
            G= "|x       x|"
            H= "|xx     xx|"
            I= "|Xxx   xxX|"
            J= "|XXxx xxXX|"
            K= "|---------|"
            
    try:
        editableRoom = [A,B,C,D,E,F,G,H,I,J,K]
    except:
        print("The roomCall is not correct, double check it.")
    return editableRoom

# i in 7,4;

# mapDisplay puts together the current map with space/X in between columns where approp, and prints it line by line.
def mapDisplay(info,fake = "False"):
    if fake != "False":
        currentRoom = fake
    else:
        currentRoom = info["Current Room"]
    MAPGUIDE = " 123456789 "
    dispRoom = []
    currentLine = "\t  "
    lengMap = len(currentRoom[0])
    for m in range(1,10):
        currentLine += (MAPGUIDE[m]+" ")
    dispRoom.append(currentLine)
    for i in range(0,11):
        currentLine="\t" + MAPGUIDE[i]
        for x in range(0,len(currentRoom[i])):
            element = currentRoom[i]
            currentLine+=element[x]
            if x == 0 or x == lengMap-1 or x == (lengMap-2):
                continue
            elif element[x].upper() == "X" and element[x+1].upper() == "X":
                currentElement = element[x]
                nextElement = element[x+1]
                whatToAdd = "X"
                if currentElement == "x" and nextElement == "x":
                    whatToAdd = "x"
                if currentElement == "x" and nextElement == "X":
                    whatToAdd = "x"
                if currentElement == "X" and nextElement == "x":
                    whatToAdd = "x"
                currentLine += whatToAdd
            elif element[x] == "-" and element[x+1] == "-":
                currentLine += "-"
            else:
                currentLine += " "
        currentLine+=MAPGUIDE[i]
        dispRoom.append(currentLine)
    currentLine = "\t  "
    for m in range(1,10):
        currentLine += (MAPGUIDE[m]+" ")
    dispRoom.append(currentLine)
    region = info["Region"]
    try:
        if info["Keys"][region] != 0:
            currentLine = "\t Keys: " + str(info["Keys"][region])
            dispRoom.append(currentLine)
    except:
        info["Keys"].setdefault(str(region),0)
    stringRoom = ""
    for i in range(0,len(dispRoom)):
        stringRoom += (dispRoom[i] + "\n")
    print(stringRoom)

# Filters inputs that aren't allowed in the movement section, and returns the move if it is allowed.
# Also redisplays the current map after 10 failed inputs. Loops infinitely until returned.
def moveInput(info):
    ALLOWEDINPUT = "wasdiefq"
    MOVEOPTIONS = "wasd"
    INVENTORY = "i"
    ITEMOPTIONS = "ef"
    SAVE = "q"
    goodInput = False
    NOMOVE = {"U1":{"X":0,"Y":0}}
    itemUsed = "None"
    i = 0
    # Move input loops until the player puts in a valid command.
    while goodInput == False:
        i += 1
        key = input().lower()
        if len(key)> 2:
            goodInput = False
        elif len(key) == 2:
            if key[0] not in ALLOWEDINPUT or key[1] not in ALLOWEDINPUT:
                goodInput = False
            for loop in range(2):#checks that one letter inputted is direction, other letter is item.
                if goodInput == True:
                    continue
                keySwap = [key[1],key[0]]
                key = keySwap
                if key[0] in MOVEOPTIONS and key[1] in ITEMOPTIONS:
                    if key[1] == "e" and info["Equipment"]["Bomb Bag"] == False:
                        goodInput = False
                        continue
                    if key[1] == "f" and info["Equipment"]["Flame Glove"] == False:
                        goodInput = False
                        continue
                    direction = key[0]
                    itemUsed = key[1]
                    action = "item"
                    goodInput = True
        elif len(key) == 1:
            if key in MOVEOPTIONS or key in INVENTORY or key in SAVE:
                direction = key
                action = "move"
                goodInput = True
        if goodInput == False:
            print("Try another command.")
            if i==9:
                mapDisplay(info)
                i=0
    key = direction
    if key == "i":#inventory
        info = displayInventory(info)
        move = NOMOVE
    if key == "q":
        move = NOMOVE
        if info["Room Number"] == [10,10]:
            prause("You can't save here!")
        else:
            info = saveAndQuit(info)
    if key == "w":#move up
        move = {"U1":{"X":0,"Y":-1}}
    if key == "s":#move down
        move = {"U1":{"X":0,"Y":1}}
    if key == "a":#move left
        move = {"U1":{"X":-1,"Y":0}}
    if key == "d":#move right
        move = {"U1":{"X":1,"Y":0}}
        
    actionFull = [action,move,itemUsed]
    # If player puts in valid command, it'll either be a "move" action or "item" action along with the movement/itemUsed.
    # the system then returns that information so the moveManager can deal with how to handle it.
    return actionFull

# Uses the same action format as above: ["item",movement dictionary, and which item they're using.]
# It takes info and the action that was generated by moveInput (as above), and acts upon that info.
# Explosives will be placed, flames will be used, etc. # Also, if enemy is hit by flames, a battle will immediately start and have the enemy damaged by the blast.
def itemUse(action,info):
    # Item actions will activate an item in direction of player's choosing.
    currentRoom = info["Current Room"][:]
    directionMove = action[1]["U1"]
    playerPosition = info["Position"]["U1"]
    itemUsing = action[2]
    itemLocationIntended = {" 1":{"X":(directionMove["X"] + playerPosition["X"]),"Y":(directionMove["Y"] + playerPosition["Y"])}}
    if itemUsing == "e":#explosives
        destination = destCheck(itemLocationIntended,info,True)
        positionsList = str(roomInfoCheck(currentRoom).keys())
        if " " in str(key(destination)) and "." not in positionsList and "o" not in positionsList and "O" not in positionsList:
            currentRoom = rewriteSpecificLine(".",itemLocationIntended,currentRoom)
            info["Current Room"] = currentRoom
        else:
            prause("Can only place bombs on empty spaces, and only one bomb at a time!")
    if itemUsing == "f":#flameglove
        fakeCurrentRoom = info["Current Room"][:]
        numberEnemiesHit = 0
        for i in range(3):
            destination = destCheck(itemLocationIntended,info,True)
            # Up to 3 times, will write F (flame) to a fake currentRoom that displays at the end for a moment, then updates any glaciers to be destroyed.
            if " " in str(key(destination)) or "G" in str(key(destination)) or "e" in str(key(destination)):
                fakeCurrentRoom = rewriteSpecificLine("F",itemLocationIntended,fakeCurrentRoom)
                if "e" in str(key(destination)).lower():
                    numberEnemiesHit += 1
                    currentRoom = rewriteSpecificLine(" ",itemLocationIntended.copy(),currentRoom)
                    info["Current Room"] = currentRoom[:]
                if "G" in str(key(destination)):
                    currentRoom = rewriteSpecificLine(" ",itemLocationIntended,currentRoom)
                    info["Current Room"] = currentRoom[:]
                X = call("X",itemLocationIntended) + directionMove["X"]
                Y = call("Y",itemLocationIntended) + directionMove["Y"]
                itemLocationIntended = {" 1":{"X":X,"Y":Y}}
            else:
                i = 3
        mapDisplay(info,fake=fakeCurrentRoom)
        pause(0.8)
        if numberEnemiesHit > 0:
            for enemyNumber in range(numberEnemiesHit):
                print("You hit an enemy with the flame blast! ",end="")
                info = battleLoop(info,False,"fire")
                if info["DEMISE"]["Player"] == True:
                    return info
    info["Current Room"] = currentRoom
    return info

# Takes whatever the move is, checks whatever is at the location the character is moving to,
# and then returns the info/position of the destination.
# Input: {mover:{"X":mov1,"Y":mov2}}, allInfo.
def destCheck(move,info,positionKnown=False):
    mover = key(move)
    if positionKnown == False:
        moveX, moveY = move[mover]["X"],move[mover]["Y"]
        origX, origY = info["Position"][mover]["X"],info["Position"][mover]["Y"]
        destX = moveX + origX
        destY = moveY + origY
    if positionKnown == True:
        destX = call("X",move)
        destY = call("Y",move)
    infoCheck = False
    for character in info["Position"]:
        if info["Position"][character]["X"] == destX and info["Position"][character]["Y"] == destY:
            destination = {character:{"X":destX,"Y":destY}}
            infoCheck = True
    if infoCheck != True:
        currentRoom = info["Current Room"]
        #characterInfo = [mover,[origX,origY]]
        destinationRow = currentRoom[destY]
        destChar = destinationRow[destX]
        destination = {destChar+"1":{"X":destX,"Y":destY}}
    return destination

def roomInfoCheck(currentRoom):
    CHARACTERS = "UieE?DR!STN.oOQ"
    positionInfo = {}
    for rowNumber in range(len(currentRoom)):
        row = currentRoom[rowNumber]
        for elementNumber in range(len(row)):
            element = row[elementNumber]
            if element in CHARACTERS:
                i=1
                added = False
                while added == False:
                    if element+str(i) in positionInfo:
                        i += 1
                    else:
                        positionInfo[element+str(i)] = {"X":elementNumber,"Y":rowNumber}
                        added = True
    return positionInfo#returns positions of all non-wall characters

# Used to update the map after character moves.
def moveManager(info):
    #modifies: currentRoom,region
    region = info["Region"]
    currentRoom = info["Current Room"]
    NOMOVE = {"U1":{"X":0,"Y":0}}
    while info["Region"] == region:
        for goalKey in info["DEMISE"]:
            if info["DEMISE"][goalKey] == True:
                return info
        currentRoom = info["Current Room"]
        info["Position"] = roomInfoCheck(currentRoom)#returns dic of all icons:dic of x,y
        mapDisplay(info)
        action = moveInput(info)#returns [action,{"U1":{"X":moveX,"Y":moveY}}, and what item is used if the action isn't "move".]
        if action[0] == "move":
            moveNew = action[1]
        elif action[0] == "item":
            moveNew = NOMOVE
            info = itemUse(action,info)
            if info["DEMISE"]["Player"] == True:
                return info
            info["Position"] = roomInfoCheck(currentRoom)
            currentRoom = info["Current Room"]
        STOP = "-|xXDRBSTNL.oO!G"
        USE = " eE?iHD!RBSTNKGLQ"
        destNew = destCheck(moveNew,info)
        destOld = convertToOld(destNew)
        if destOld[0][0] in STOP:
            moveNew[key(moveNew)] = {"X":0,"Y":0}
        #for element in USE:
        if destOld[0][0] in USE:
            info = interact(moveNew,destNew,info)
        moveOld = convertToOld(moveNew)
        if moveOld[1] != [0,0]:#if moving, rewrite currentRoom
            info = rewriteRoom(moveNew,destNew,info)
        info = explodeCheck(info)
    return info

    #for characterNumber in range(0,len(totalListOfCharactersAndPositions),3):
        #characterBeingChecked = totalList[characterNumber:characterNumber+3]
        #if "E" in characterBeingChecked:
            #do rando movement for characterBeingChecked
    #moveWrite(all movement results)

# Checks if there's a bomb in the map (./o/O) and upgrades to the next step, or causes explosion.
def explodeCheck(info):
    update = False
    stepsExplode = [".","o","O"," "]
    originalPositions = str(info["Position"].keys())
    for stepNum in range(3):
        if stepsExplode[stepNum] in originalPositions:
            currentStep = stepsExplode[stepNum]
            nextBombStep = stepsExplode[stepNum+1]
            update = True
    if update == True:
        bombPosition = {currentStep:info["Position"][(currentStep + "1")].copy()}
        info["Current Room"] = rewriteSpecificLine(nextBombStep,bombPosition,info["Current Room"])
        currentRoom = info["Current Room"][:]
        if currentStep == "O":
            fakeCurrentRoom = info["Current Room"][:]
            fakeMovements = [[-1,1],[0,1],[1,1],[-1,0],[0,0],[1,0],[-1,-1],[0,-1],[1,-1]]
            explosionEffects = "%#*@!$<>"
            numberEnemiesHit = 0
            for i in range(9):
                fakePosition = convertToOld(bombPosition.copy())
                fakePosition[1][0] += fakeMovements[i][0]
                fakePosition[1][1] += fakeMovements[i][1]
                fakePosition = convertToNew(fakePosition)
                fakeCurrentRoom = rewriteSpecificLine(random.choice(explosionEffects),fakePosition,fakeCurrentRoom)
                destination = destCheck(fakePosition,info,True)
                if "B" in str(key(destination)) or "e" in str(key(destination)):
                    if "e" in str(key(destination)):
                        numberEnemiesHit += 1
                    currentRoom = rewriteSpecificLine(" ",fakePosition.copy(),currentRoom)
                    info["Current Room"] = currentRoom[:]
            mapDisplay(info,fake=fakeCurrentRoom)
            pause(1)
            if numberEnemiesHit > 0:
                for enemyNumber in range(numberEnemiesHit):
                    print("You hit an enemy with the explosion! ",end="")
                    info = battleLoop(info,False,"fire")
                    if info["DEMISE"]["Player"] == True:
                        return info
    return info
            
                                                       
                                                       
# Old Format: ["U1",[2,9]]; New Format: {"U1":{"X":2,"Y":9}}
# These 2 functions just convert back and forth so I don't have to rewrite anything
# anymore, I swear I've rewritten all this code like 12 times...
def convertToOld(dic1):
    lis1 = [key(dic1),[call("X",dic1),call("Y",dic1)]]
    return lis1
def convertToNew(lis1):
    dic1 = {}
    dic1[lis1[0]] = {"X":lis1[1][0],"Y":lis1[1][1]}
    return dic1

# writeChar: " "; position: {"U1":{"X":2,"Y":9}}; room is the room you're changing.
# does one thing only: takes a room, and changes the original position given so that
# the character you give it is at the location. Updates the room and returns it.
# Can be used on info["Current Room"], OR on a fake room for display purposes.
def rewriteSpecificLine(writeChar,position,roomOriginal):
    positionOld = convertToOld(position)#[U1,[2,9]]
    positionOld[0] = positionOld[0][0]#[U,[2,9]]
    positionX = positionOld[1][0]#2
    positionY = positionOld[1][1]#9
    oldRow = roomOriginal[positionY]#[U  XX  Xi], for example
    newRow = oldRow[0]#First character of the row added to newRow.
    for i in range(1,len(oldRow)):
        if i != positionX:#if not at the position:
            newRow += oldRow[i]#add the oldRow character to newRow.
        else:#if at position:
            newRow += writeChar#Write the writeChar to the position in the row.
    roomOriginal[positionY] = newRow
    return roomOriginal#Now modified room is sent back up.
    
# Takes the current room, dest, and character info, and returns info updated.
def rewriteRoom(moveNew,destination,info,roomChange=False):
    destOld = convertToOld(destination)
    moveOld = convertToOld(moveNew)
    charOld = convertToOld(moveNew)
    destOld[0] = destOld[0][0]
    moveOld[0] = moveOld[0][0]
    charOld[1][0] = call(charOld[0],info)["X"]
    charOld[1][1] = call(charOld[0],info)["Y"]
    charOld[0] = charOld[0][0]# Deletes the number in the character's info to be able to write to room
    currentRoom = info["Current Room"]
    characterInfo = charOld
    destination = destOld
    move = moveOld
    characterColumn   =characterInfo[1][0]#char's x
    characterRow      =characterInfo[1][1]#char's y
    destinationColumn =destination[1][0]#destination's x
    destinationRow    =destination[1][1]#destination's y
    if characterColumn != destinationColumn:#if change in x:
        oldRow        = currentRoom[characterRow]#New row = char's row.
        newRow = oldRow[0]#start new row with old row's 0 element
        for i in range(1,len(oldRow)):
            if i!=characterColumn and i!=destinationColumn:#if not at the character or destination:
                newRow+=oldRow[i]#add the oldRow element to the newRow
            if i==characterColumn:#if at character:
                if roomChange == False:#if room is not changing:
                    newRow+=" "# write empty space to position.
                else:#if room IS changing:
                    newRow+=oldRow[i]#add the oldRow element to newRow. Protects oldRow items from being unintentionally deleted.
            if i==destinationColumn:#if at destination:
                newRow+=characterInfo[0][0]#write the character that's moving to the newRow.
        currentRoom[destinationRow] = newRow#apply the new row to the room.
    if characterRow != destinationRow:#if change in y:
        oldRowOrigin = currentRoom[characterRow]#char's original row
        newRowOrigin = oldRowOrigin[0]          #char's new row
        oldRowDestin = currentRoom[destinationRow]#destin's orig. row
        newRowDestin = oldRowDestin[0]   #destination's new row
        for i in range(1,len(oldRowOrigin)):#Changes original row
            if i!=characterColumn and i!=destinationColumn:#if not at the character or destination:
                newRowOrigin+=oldRowOrigin[i]#write original character to the new row
            if i==characterColumn:#if at character: 
                if roomChange == False:#and room not changing:
                    newRowOrigin+=" "#write empty space to position.
                else:#If moving to new room: keep door.
                    newRowOrigin+=oldRowOrigin[i]
        for i in range(1,len(oldRowDestin)):#Changes destination row
            if i!=characterColumn and i!=destinationColumn:#if not at the character or destination:
                newRowDestin+=oldRowDestin[i]#add original character to row
            if i==destinationColumn:#if at destination:
                newRowDestin+=characterInfo[0][0]#add new character
        currentRoom[destinationRow] = newRowDestin
        currentRoom[characterRow] = newRowOrigin
    info["Position"][move[0]] = {"X":destinationColumn,"Y":destinationRow}
    info["Current Room"] = currentRoom
    return info

# Changes the region info so that the roomChangeManager works properly when swapping from region to region.
def changeRegionWalking(regionCurrent,roomNumber,info):
    if roomNumber in [[3,6],[4,6]]:
        REGIONS = {"forest":"village",
                   "village":"forest"}
    if roomNumber in [[6,5],[6,4]]:
        REGIONS = {"village":"mountains",
                   "mountains":"village"}
    if roomNumber in [[4,7],[4,8]]:
        REGIONS = {"village":"tundra",
                   "tundra":"village"}
    if roomNumber in [[7,6],[8,6]]:
        REGIONS = {"village":"tower",
                   "tower":"village"}
    if roomNumber in [[10,9],[10,10]]:
        REGIONS = {"tower":"boss",
                   "boss":"tower"}
    info["Region"] = REGIONS[regionCurrent]
##    for region in REGIONS:
##        if info["Room Number"] in REGIONS[region][0]:
##            roomNumber = info["Room Number"]
##            info["Region"] = REGIONS[region][1]

##    if regionCurrent == "forest":
##        if roomNumber == [1,2]:
##            if destCharacter == "R1":
##                regionNew = "village"
##                roomCorrect = [0,1]
##    if regionCurrent == "village":
##        if roomNumber == [0,1]:
##            if destCharacter == "R1":
##                regionNew = "forest"
##                roomCorrect = [1,2]
    #info["Region"] = regionNew
    #info["Room Number"] = roomCorrect
    return info

# Saves the old room and position info (minus the player), and then pulls the new room and updates it to have the player in there.
def roomChangeManager(characterMove, destNew, info,regionChange=False):
    currentRoom = info["Current Room"]
    destination = convertToOld(destNew)
    mover = convertToOld(characterMove)
    region = info["Region"]
    roomNumber = info["Room Number"]
    name = info["Name"]
    info["Old Rooms"][region].setdefault(str(roomNumber),{})
    oldRoom = info["Current Room"]
    playerPosition = info["Position"]["U1"].copy()
    info["Old Rooms"][region][str(roomNumber)]["Room"] = rewriteSpecificLine(" ",playerPosition,oldRoom)
    del info["Position"]["U1"]
    info["Old Rooms"][region][str(roomNumber)]["Position"] = info["Position"].copy()
    #at this point, all old room data is safely saved.

    #time to clear out the current room's data, and get started on setting up the next room's data.
    info["Position"].clear()
    info["Position"]["U1"] = playerPosition.copy()
    destX = destination[1][0]#10
    destY = destination[1][1]#5
    if destY == 0:#if old door was at top of map:
        newPlayer = {"U1":{"X":destX,"Y":10}}
        changeY = -1
        changeX = 0
    elif destY == 10:#if old door was at bottom of map:
        newPlayer = {"U1":{"X":destX,"Y":0}}
        changeY = 1
        changeX = 0
    elif destX == 0:#if old door was at left of map:
        newPlayer = {"U1":{"X":10,"Y":destY}}
        changeX = -1
        changeY = 0
    elif destX == 10:#if old door was at right of map:
        newPlayer = {"U1":{"X":0,"Y":destY}}
        changeX = 1
        changeY = 0
        
    info["Room Number"] = [roomNumber[0]+changeX,roomNumber[1]-changeY]
    roomNumber = info["Room Number"]
    if regionChange == True:#if changing regions, set region based on roomNumber and region
        info = changeRegionWalking(region,roomNumber,info)
        region = info["Region"]
    try:
        info["Current Room"] = info["Old Rooms"][region][str(roomNumber)]["Room"]
        info["Position"] = roomInfoCheck(info["Current Room"])
    except:
        info["Current Room"] = roomDefaultCopy(info)
        info["Position"] = roomInfoCheck(info["Current Room"])
    info["Position"]["U1"] = newPlayer["U1"]
    moveRoomTransition = {"U1":{"X":changeX,"Y":changeY}}
    destNew = destCheck(moveRoomTransition,info)
    info = rewriteRoom(moveRoomTransition, destNew, info, True)
    return info

# Manages specific events when the player is in certain rooms, and handles inventory
# management and item pickups.
def eventManager(destination, info):
    roomNumber = info["Room Number"]
    destinationLoot = roomCont(destination,info)#Returns loot that is at destination.
    
    #This section is for the first sword the player gets.
    if roomNumber == [3,4]:#loot format is {ItemType: ItemName}, with some exceptions.
        dialogue(info,3,5)
        info = equipItem(destinationLoot,info,tell=False)
        dialogue(info,6,8)
        info = battleLoop(info)
        if info["DEMISE"]["Player"] == True:
            return info
        dialogue(info,9,10)
    #This one is for picking up items in the tower courtyard.
    else:
        if roomNumber == [8,6] and "i" not in destination[0]:
            prause("... Amidst the remains, you find something.")
        else:
            prause("You found a chest!")
        description = ""
        loop = 1
        for lootKey in destinationLoot:
            if lootKey != "Armor" and lootKey != "Weapon":
                if lootKey == "Gold":
                    #gold's format is {"Gold":1000}, hence this exception.
                    description += ("bag of " + str(destinationLoot[lootKey]) + " " + lootKey)
                elif lootKey == "...":
                    description += destinationLoot[lootKey]
                else:
                    description += lootKey
            elif lootKey == "Armor":
                description += "new set of armor"
            elif lootKey == "Weapon":
                description += "new sword"
            else:#ie, if it's a key item or "..."
                description += destinationLoot[lootKey]
            if loop != len(destinationLoot):
                description += " and a "
            loop += 1
        if lootKey == "...":
            prause(("... It's a " + str(description) + "..."))
        elif lootKey == "Key Pieces":
            prause(("You found a piece of a large key!"))
            if info["Key Pieces"] == 0:
                prause(("... This seems to be half of a key; it has a demon emblem on it..."))
                prause(("Perhaps the Mayor knows what this is; it'd be best to check with her."))
        else:
            prause(("You open it to find a "+str(description)+"!"))
        info = addInventory(destinationLoot,info)
    return info
    
# Checks during moveStep to see what the item the character is running into is,
# and then interacts with it if possible.
def interact(characterMove, destNew, info):
    currentRoom = info["Current Room"]
    destination = convertToOld(destNew)
    mover = convertToOld(characterMove)
    region = info["Region"]
    roomNumber = info["Room Number"]
    name = info["Name"]
    pronouns = info["Pronouns"]
    # These are the interactions that happen if the player is moving.
    if "U" in mover[0]:
        if "N" in destination[0]:#NPC interactions, all managed within here.
            info = dialogueNPCManage(destNew,info)

        if "R" in destination[0]:#Region and door changes use the same sets of functions
            info = roomChangeManager(characterMove, destNew, info,True)
        if "D" in destination[0]:
            info = roomChangeManager(characterMove, destNew, info)
            
        #Interactions for Boulders and Glaciers
        if "B" in destination[0]:
            prause("A cracked boulder blocks the way.")
        if "G" in destination[0]:
            prause("A small glacier blocks the way.")

        #Interactions for items and ?s are handled the same.
        if "?" in destination[0] or "i" in destination[0]:
            info = eventManager(destination,info)

        #Enemy interactions, designed to work when enemy OR player is moving.
        if "e" in destination[0].lower() and "U" in mover[0]:#if enemy catches player
            info = battleLoop(info)
        if "e" in mover[0].lower() and "U" in destination[0]:#if player catches enemy
            info = battleLoop(info)
            
        if "Q" in destination[0]:#Boss interaction! Final battle!
            SECTIONLIST = ["intro","phase1","phase1p2","death"]#"phase2" taken out
            for section in SECTIONLIST:
                if info["DEMISE"]["Player"] == True:
                    break

                if section == "death":
                    dialogue(info,19,20)
                elif section == "phase1":
                    dialogue(info,11)#Phase 1 dialogue goes first, queen talks, battle skipped...
                elif section == "phase1p2":
                    dialogue(info,12,15)#then part 2 dialogue goes, queen talks, battle starts.
                    
                dialogueNPC(destNew,info,section,True)

##              Removed from game, 2 phases is enough.
##                if section == "phase2":
##                    dialogue(info,16,18)
                if section != "death" and section != "phase1":
                    info = battleLoop(info,boss=True)
                if section == "death":
                    dialogue(info,21,22)
                    
            if info["DEMISE"]["Player"] != True:
                info["DEMISE"]["Queen"] = True#If player's not dead, then the queen must be.
        for demise in info["DEMISE"]:#Checks if any of the demise statuses are True.
            if info["DEMISE"][demise] == True:
                return info
        
        if "!" in destination[0]:
            if info["Room Number"] != [10,9]:
                if info["Key Pieces"] < 2:
                    prause("The doors to the Tower gate are locked. 'No Civilians Allowed' is printed across the doors.")
                if info["Key Pieces"] >= 2:
                    prause("The doors are now unlocked, it seems that the mayor had the soldiers unlock it for you...")
                    info["Current Room"] = rewriteSpecificLine(" ",destNew,info["Current Room"])
            else:
                prause(("The final door... " + name + " takes each key piece, and places them in the lock..."))
                prause(("The lock falls to the floor with a loud metallic clang... Hopefully, your battle will not end just as suddenly."))
                info["Current Room"] = rewriteSpecificLine(" ",destNew,info["Current Room"])
            print()
        if "S" in destination[0]:
            info = saveAndQuit(info)
        if "K" in destination[0]:
            info["Keys"][region] += 1
        if "L" in destination[0]:
            if info["Keys"][region] == 0:
                prause("This door is locked, you'll need a key from this region to get in.")
            if info["Keys"][region] > 0:
                print("Use key?")
                keyDecision = listOptions(["Yes","No"])
                if keyDecision == 1:
                    info["Keys"][region] -= 1
                    info["Current Room"] = rewriteSpecificLine(" ",destNew,info["Current Room"])
    return info


def saveAndQuit(info):
    print("Would you like to save?")
    saveQuestion = listOptions(["Yes","No"])
    if saveQuestion != 1:
        prause("Alright, onward!")
    else:
        whichSave = info["Save Number"]
        save = open(str("save"+str(whichSave)+".dat"),"wb")
        pickle.dump(info,save,3)
        save.close()
        
        saveNames=open("saveNames.txt","r")
        namesList = saveNames.readlines()
        saveNames.close()

        changeNames = open("saveNames.txt","w")
        namesList[whichSave-1] = info["Name"] + "\n"#whichSave is 1,2,or 3, needs -1.
        namesString = namesList[0] + namesList[1] + namesList[2]
        changeNames.writelines(namesString)
        changeNames.close()
        
        print("Save completed; would you like to quit the game as well?")
        quitQuestion = listOptions(["Yes","No"])
        if quitQuestion == 1:
            prause(("Quitting out..."),1)
            info["DEMISE"]["Quit"] = True
    return info

            
# Runs the forest intro, then returns the starting player position for mapping.
def forestIntro(info):
    region = info["Region"]
    dialogue(info,0,2)
    prause("\n\tTo move, input a command one at a time using WASD directions. You can also input I to check inventory.")
    prause("\tYou can also save at any time by inputting Q! Make sure to do so often.")
    prause("\t'U': That's you! 'e': Enemies! '?' and 'i': Items and equipment! 'X','|', and '-': Walls, can't be traversed.")
    prause("\t'D' and 'R': doors and region changes. 'B': Bombable boulders; 'G': Meltable ice blocks.\n\t'K': Keys, used to unlock 'L': Locked doors.\n")
    playerPosition = {"U1":{"X":2,"Y":9}}
    info["Position"] = playerPosition
    info["Current Room"] = roomDefaultCopy(info)
    info["Current Room"] = rewriteSpecificLine("U",playerPosition,info["Current Room"])
    info["First Time"]["forest"] = False
    return info

def loadIntoGame(info):
    info["Load"] = False
    #prause("\t\tWelcome back!",2)
    return info

# Function for displaying lines during the intro, first time the player enters regions, etc.
# Was written early on before I developed the dialogueNPC functions that work a lot better for dialogue,
# but I rewrote it to function decently for its current use.
def dialogue(info,lineFirst,lineLast=-1,newL=0,pauseNum=3):
    region = info["Region"]
    try:
        name = info["Name"]
        pronouns = info["Pronouns"]
        playerType = info["Player Stats"]["Player Type"]
    except:
        name = "none"
        pronouns = ["none","none","none","none","none","none","none","none","none"]
        playerType = "playerType"
    try:
        weaponName = info["Equipment"]["Weapon"]
        if weaponName == "None":
            weaponName = "Simple Sword"
    except:
        weaponName = "Simple Sword"

    if region == "intro":
        LINES = [("You have set upon a great quest to defeat the Demon Queen, the ruler of Mayd'ahp'landia!"),
                 ("\tShe leads with an iron claw, leaving countless lives ruined in her wake."),
                 ("\t    The people of the land are defeated and hopeless."),
                 ("\t\t\tCan you stop her?")]

    if region == "forest":
        LINES = [(name + " awakens in a forest, lying on " + pronouns[2] + " back. The sun is shining, and the leaves rustle in the wind."),
                 (name + " looks around, and " + pronouns[0] + " see" + pronouns[6] + " the walls of a village to the North; it seems to be the only thing for miles."),
                 ("Seeing no other option, " + pronouns[0] + " head" + pronouns[6] + " towards it, hoping to figure out where " + pronouns[0] + " " + pronouns[4] + "."),
                 (name + " sees " + pronouns[2] + " weapon sticking out of the ground. " + pronouns[0].title() + " isn't sure how it got there, but it's likely that " + pronouns[0] + " will need it."),
                 (pronouns[0].title() + " grab" + pronouns[6] +" it, and pull" + pronouns[6] +" it out."),
                 (name + " got the " + str(weaponName) + "!"),
                 ("As " + name + " equips the weapon, " + pronouns[0] + " see" + pronouns[6] + " something move out of the corner of " + pronouns[2] + " eye."),
                 ("Turning, " + pronouns[0] + " realize" + pronouns[6] + " that it's a viscous slime, about half of " + pronouns[2] + " height."),
                 ("It seems to undulate for a moment, considering " + pronouns[1] + ", before lunging forward and attempting to strike!"),
                 ("The remaining goop of the slime dissolves, leaving nothing but dew in the grass."),
                 ("The village is closer now, and although there are more monsters lurking on the way there, " + name + " forges ahead.")]

    if region == "village":
        LINES = [(name + " arrives to the entrance of a small village; a guard on lookout sees you, and seems startled."),
                 ("\t|Soldier: Hey! That's not a monster, open the gate!|"),
                 ("As the gate closes behind " + name + ", " + pronouns[0] + " realize" + pronouns[6]+ " the village is dense with refugees and starving stragglers."),
                 ("\t|Soldier: I haven't seen anyone come out of that forest in years. If you can survive that...|"),
                 ("\t|Soldier: Then you need to meet the mayor. Directly East of here is the Mayor's Office. She'll be expecting you.|")]
        
    if region == "tundra":
        LINES = [("As the gate closes behind " + name + ", " + pronouns[0] + " suddenly realize" + pronouns[6] + " how biting the cold is. " + name + " look" + pronouns[6] + " around..."),
                 ("There's spires of ice and frozen caves dotting the white landscape; large walls of ice prevent " + name + " from climbing above and getting around easily."),
                 (pronouns[0].title() + " decides to head through the caves and see what " + pronouns[0] + " can find inside. Hopefully, a fire or some warm clothes...")]
        
    if region == "mountains":
        LINES = [("As the gate closes behind " + name + ", " + pronouns[0] + " notice" + pronouns[6] + " a massive increase in the temperature around " + pronouns[1] + "."),
                 ("There are massive cliffs and mountainsides, but there's also pools of magma and geysers of steam throughout the region."),
                 ("Any false step could lead to " + pronouns[2] + " early grave; caution is going to be essential, especially with the bombs that " + pronouns[0] + " " + pronouns[5] + " carrying...")]

    if region == "tower" or region == "boss":
        if info["Room Number"] == [10,10]:
                     #First boss dialogue section upon entering room.
            LINES = [("\n\tAs " + name + " enter the final room of the Tower, " + pronouns[0] + " notice" + pronouns[6] +
                      " how massive the last floor is..."),
                     (name + " can just barely see doors on some of the walls, likely to the Queen's chambers."),
                     ("There is a subtle elegance to the purple and black color scheme, far less monolithic and dungeon-esque than the rest of the tower."),
                     ("In the center of the room, there's...!"),
                     ("Now that " + name + "'s eyes have properly adjusted, " + pronouns[0] + " can see someone standing there!"),
                     ("An ice cold stare, with crimson eyes... She wears a simple, dark purple leather chestpiece and pants, with no weapons at her side."),
                     ("She also seems to have pale, white skin... Though it looks metallic or scale-like; that may be why she has so little armor..."),
                     ("Her hands end in sharp, dagger-like claws, and she has... A black and purple crown!"),
                     (name + " almost pulls " + pronouns[2] + " sword out, but the woman motions to stop... And beckons you forward."),
                     (name + " doesn't see any traps or other enemies in the room... She seems like she wants to talk, face to face."),
                     ("As " + name + " steps forward, " + pronouns[0] + " steels her resolve for a fierce fight."),
                     #Second section, first line delivered on it's own, rest after queen speaks.
                     ("The queen stumbles backwards, but regains her footing!"),
                     ("She...!"),
                     ("Pitch black wings sprout from her back, and her skin seems to be regenerating her wounds...!"),
                     ("Parts of her skin change to black and seem to thicken, armoring her even more!"),
                     ("Purple streaks of light flow from her clawtips up to her wrists, and a massive pitch black Greatsword appears on her hip!"),
                     #Third section, final phase! Queen responds in anger, then fully transforms.
                     #No longer used in game, left in to avoid any errors in dialogue.
                     ("Even after all that-! A darkness envelops the room for a moment..."),
                     ("The light returns, revealing her dragonic form; pitch black scales, searing hatred, and an overwhelming power!"),
                     ("There's no escape, no turning back... The Dragon charges forward!"),
                     #Final section, first two lines just after defeating the queen, rest after her monologue.
                     ("With that, both " + name + " and the Queen collapse, the Queen returned to the form you first saw her as..."),
                     ("She has gashes and bruises all across her body, and her regeneration is no longer working."),
                     ("... " + name + " hears her final request, and obliges with a quick downward strike."),
                     (pronouns[0].title() + " limp" + pronouns[6] + " through the room's exit, and begin" + pronouns[6] +
                      " the long trek back to the Village.")]
        else:
            LINES = [("The gate closes, leaving nothing but a barren wasteland in front of " + name + ". The dark grey sky and howling wind are barely noticeable considering the landscape."),
                     ("Bodies cover the flatland. Some, particularly by the village walls, are fresh; others are bare skeletons, fated to dust. Every few meters has at least one."),
                     ("The sheer amount of death is overwhelming; nothing has survived the Queen's onslaught, not even a single weed.\n"),
                     ("The tower looms in the distance, a gravestone for all.\n"),
                     (name + " considers " + pronouns[2] + " odds, going alone to the source of this scourge... But turning back is not an option. " + name + " marches on.")]
    if region == "ending":
        LINES = [("The town, finally freed from the danger of the Queen, celebrates " + name + " as a true hero."),
                 (name + " takes a week to recover, and then sets off through the forest to return home."),
                 ("The people of the land will never forget the bravery of the heroic " +
                  playerType + " that saved them...")]
    if str(lineLast) != "all":
        if lineLast == -1:
            lineLast = lineFirst
        print()
        for lineNumber in range(lineFirst,lineLast+1):
            prause(("\t"+ LINES[lineNumber]),pauseNum)
        for newL in range(newL, 0, -1):
            print()
    else:
        print()
        for line in LINES:
            prause(("\t" + line),pauseNum)
        print()

# npcInfo will be {"N1":{"X":xval,"Y":yval}}; can just pull from destination.
# Determines NPC based in their location, returns the name of the NPC for use in NPCLines and dialogueNPC.
def determineWhichNPC(npcInfo,info):
    npcTitle = key(npcInfo)
    if info["Region"] == "village":
        if info["Room Number"] == [4,6]:
            npcSpecifics = {"Soldier Gate":["N4","N5"],"Hungry Woman":["N1","N6"],"Inn Keeper":["N8"],"Peculiar Mage":["N7"],
                            "Soldier Generic":["N3"], "Old Man":["N2"]}
        if info["Room Number"] == [4,7]:
            npcSpecifics = {"Soldier Tundra":["N1","N2"],"Hungry Woman":["N3"],"Old Man":["N4"]}
        if info["Room Number"] == [5,6]:
            npcSpecifics = {"Soldier Office":["N1","N2"],"Lone Patron":["N3"],"Tavernkeep":["N4"],
                            "Patron":["N5","N6","N7","N8","N9","N10","N11"]}
        if info["Room Number"] == [5,7]:
            npcSpecifics = {"Mayor Madeline":["N1"],"Soldier Office":["N2","N3","N4","N5"]}
        if info["Room Number"] == [6,6]:
            npcSpecifics = {"Soldier Shops":["N1"],"Yogurt":["N2"],"Bow":["N3"]}
        if info["Room Number"] == [6,5]:
            npcSpecifics = {"Soldier Mountains":["N1","N2"]}
        if info["Room Number"] == [7,6]:
            npcSpecifics = {"Soldier Tower":["N1","N2","N3","N4","N5","N6","N7",
                                             "N8","N9","N10","N11","N12","N13"]}
    if info["Region"] == "tower" or info["Region"] == "boss":
        npcSpecifics = {"The Demon Queen":["Q1"]}
    for enPeeCee in npcSpecifics:#enPeeCee is the name of an npc in the current room.
        if npcTitle in npcSpecifics[enPeeCee]:
            whichNPC = enPeeCee
    try:
        return whichNPC
    except:
        return "Error"
            #65: 46 66

# {"N1":{"X":xval,"Y":yval}}
def NPCLines(npcInfo,info,specific=False):
    name = info["Name"]
    pronouns = info["Pronouns"]
    weaponName = info["Equipment"]["Weapon"]
    playerType = call("Player Type",info)
    whichNPC = determineWhichNPC(npcInfo,info)
    bombBagCost = 1000
    flameCost = 1000
    LINESQUEEN = {"The Demon Queen":{"intro":[("... So you're the one that I've been getting reports about."),
                                              ("You must think we're all evil monsters, terrorizing the world, no?"),
                                              ("That's all they'll call me: a monster. I'd prefer it if they called me by my title."),
                                              ("Oh, where are my manners? My apologies, it's been a long time since I've had a guest."),
                                              ("MY name is Velverosa, The Queen of Demons."),
                                              ("Now that you know mine, I'd like to know the name of the one who has broken into my home..."),
                                              ("Ravaged my armies, destroyed the entirety of my tower, and is moments from being ripped limb from limb!?"),
                                              ("... WELL?! ANSWER!"),
                                              ("... " + name + ", is it? I will remember that name. Now, I must ask you to leave... Permanently.")],
                                     "phase1":[("Hah! You are a feisty one, aren't you? Well, let's see how you like it when I'm actually trying!")],
                                     "phase1p2":[("WHAT DO YOU THINK NOW, PUNY ONE?! I'LL GIVE YOU CREDIT, MOST OF MY ENEMIES HAVE DIED COWARDS..."),
                                                 ("BUT YOU AT LEAST HAVE THE DIGNITY TO PUT ON A SHOW!")],
##                                     "phase2":[("NO... I WILL NOT BE ENDED SO EASILY. MY RULE HAS LASTED 23 YEARS, I HAVE SO MUCH MORE TO DO!"),
##                                               ("YOU... " + name.upper() + "!!! YOU WILL FACE MY UNDYING WRATH!")],
                                     "death":[("... *cough* So this is how it ends... Damn you... I just wanted to..."),
                                              ("... make a place for the 'monsters' you so revile... a place to be safe..."),
                                              ("We've been hunted... enslaved... and slaughtered, for so long..."),
                                              ("I know I've... done the same to them... I thought it was justice, but it was blind revenge..."),
                                              ("Please, end me... I'd rather die with some honor than... bleed to death alone...")]}}
    LINESYOGURT = {"Yogurt":{"intro":[("Welcome to Yogurt's Merchandazing Shop, where the real money from the game is made!")],
                             "askItem":[("Want a bomb bag? Last one, get them while they're hot!"),
                                        ("... Not literally hot, at least, not until they... Well, explode. The kids love this one!"),
                                        ("... What, there's nothing wrong with giving explosives to children!... Yes, I know how stupid that sounded."),
                                        ("ANYHOO, if you'd like one, it's only "+str(bombBagCost)+" Gold!")],
                             "cancel":[("No? Of course, please come again!")],
                             "buy":[("Excellent purchase, you won't regret it! *ahem* No refunds.")],
                             "notEnough":[("Excellent choi- Hey, you don't have enough money! Beat it!")],
                             "nothing":[("I'm sorry, I don't have anything to sell right now. Come back again!")]}}
    LINESBOW = {"Bow":{"intro":[("Welcome to Bow's Quiver, your one stop shop for Magical Items. Yes, the name doesn't match what we sell, get over it.")],
                       "askItem":[("Want to buy a Flame Glove? Lets you spray fire in any direction, only "+str(flameCost)+". How about it?")],
                       "cancel":[("Alright, your loss. It'll be here when you want it.")],
                       "buy":[("Excellent choice, here you go.")],
                       "notEnough":[("Uh, looking light on gold there. Next time, check your wallet.")],
                       "nothing":[("I've got nothing else to sell, sorry.")]}}
    LINESMAYOR = {"Mayor Madeline":{"intro":[("Ah, you must be the " + playerType + " that came from the Forest, please, come in."),
                                             ("I am Mayor Madeline, we are a small and humble village, and the last safe haven from her forces."),
                                             ("... What do you mean \"Who's 'her'?\" I mean the Demon Queen! Her Coven has ripped our homes to shreds!"),
                                             ("The Demon Queen has slaughtered countless soldiers, civilians, children, innocent animals, you name it."),
                                             ("We can barely hold the walls of our village, most of my soldiers are wounded or protecting the gates."),
                                             ("I need someone like yourself to venture outside of the village and fight back against the monsters besieging us."),
                                             ("If you're willing, I can have the soldiers let you come and go as you please; my only request is that you help us."),
                                             ("And one more thing: you're going to need equipment. Check the merchant shops in the South East end of the village."),
                                             ("Here's some gold for you to buy one of the items you'll need. I can't spare more than that until you prove you can handle it.")],
                                    "first":[("You're back, and you have a piece of the key to the Queen's Tower! We might have a chance."),
                                             ("The other key piece must be in the region you haven't cleared yet..."),
                                             ("If you get that, then the Queen's Tower would be open to you! Please, head out immediately!")],
                                    "second":[("You have both pieces! Perfect. I'll have the guards let you through to the Queen's Tower."),
                                              ("Best of luck fighting her; she is not the Queen for nothing. Many of my best soldiers had no chance against her."),
                                              ("Even my wife, one of the fiercest fighters our country has seen, only lasted 10 seconds. So... Be careful.")],
                                    "moregold":[("Here's some extra gold to buy another item, you'll need it to get any farther.")],
                                    "nothing":[("I'm sorry, but I have my hands full right now and I don't have anything specific for you at the moment.")]}}

    LINESINN = {"Inn Keeper":{"intro":[("My word, you look exhausted! Please, come inside, there are beds for everybody."),
                                       ("I'm the Inn Keeper; don't worry, you won't have to pay a coin. I can't charge in these times."),
                                       ("Please, rest! (Resting here will save your progress.)"),
                                       ("(You can also input 'q' while moving to save anywhere in the game.)")],
                              "nothing":[("Do you need to rest up? Head inside, I'll show you to a room.")]}}
        
    LINESRANDOM = {"Soldier Gate":[("We guard the gate here to protect the village from the Queen's forces."),
                                   ("The Queen's monsters attack constantly, and the gate is always a hotspot."),
                                   ("It's a dangerous job, and there are fewer guards every day...")],
                   "Soldier Office":[("This is the mayor's office, please knock before entering her chambers."),
                                     ("Ah, so you're the rumored " + playerType + ". Welcome to the Mayor's office.")],
                   "Soldier Tundra":[("This is the northern gate, it leads to the Frozen Tundra."),
                                     ("You'll need a Flame Glove to get anywhere in the Tundra.")],
                   "Soldier Mountains":[("This is the southern gate, the Molten Mountains are behind these walls."),
                                        ("You're going to need bombs, boulders block all of the paths through there.")],
                   "Soldier Tower":[("You shouldn't be here, this is the gate to the Queen's Tower, it isn't safe."),
                                    ("We've been attacked so many times today that I've lost count."),
                                    ("Don't go through here unless you have a death wish."),
                                    ("You'd need a ton of equipment to even GET to her tower from here, let alone survive...")],
                   "Soldier Generic":[("If you need items, go to the merchants' shops. They always have interesting finds."),
                                      ("Need something? I'm on lunch, sorry."),
                                      ("I heard that they sell Bomb Bags at one of the shops; I could use one of those.")],
                   "Soldier Shops":[("The shops are just south from here. Don't even think of stealing anything."),
                                    ("I wish I had better boots, mine are worn down from how many thieves I've chased down."),
                                    ("The doors to the East go to the Queen's Tower gate, it's constantly besieged.")],
                   "Hungry Woman":[("Please, friend, spare a gold coin for a starving lady?"),
                                   ("Can't move... Need food...")],
                   "Lone Patron":[("... Oh, sorry, can I help you? I was engrossed in my reading."),
                                  ("Sorry, I'm busy reading, is there something I can help with?")],
                   "Patron":[("... so I tell them, \"Gender? I hardly KNOW 'er!\""),
                             ("... and then the doctor says, \"What do you MEAN my watch is in his kidney?!\""),
                             ("... and so then the dentist comes back, and says \"Wait, where's my dentures?\""),
                             ("... so when the pirate comes back, he points at the table and asks the carpenter, \"What'd ye do to my peg leg?!\"")],
                   "Old Man":[("... (He appears to be sleeping.)")],
                   "Peculiar Mage":[("... What, you want to use the teleporter? It's been broken since the war started, sorry.")],
                   "Tavernkeep":[("... Hmph."),
                                 ("... What d'ya want?"),
                                 ("... No ID? No drinks.")]}
    if "Error" in whichNPC:
        linesToReturn = {"Error":["Uh oh, something went wrong with determining the NPC you're talking to. Uh... Whoops."]}    
    elif specific == True:
        if "Yogurt" in whichNPC:
            linesToReturn = LINESYOGURT
        if "Bow" in whichNPC:
            linesToReturn = LINESBOW
        if "Mayor Madeline" in whichNPC:
            linesToReturn = LINESMAYOR
        if "Inn Keeper" in whichNPC:
            linesToReturn = LINESINN
        if "The Demon Queen" in whichNPC:
            linesToReturn = LINESQUEEN
    else:
        linesToReturn = LINESRANDOM
    linesInfo = [whichNPC,linesToReturn]
    return linesInfo

# Handles all interactions with NPCs; if they're generic NPCs, random line from their overall lines.
# If they're a specific NPC, then the function determines which part of the conversation
# they should say (if not specified), and does so.
# It also repeats the dialogue printing section until the specific conversation in question is done.
def dialogueNPC(npcInfo,info,section = "nothing",specific = False):
    linesInfo = NPCLines(npcInfo,info,specific)
    npcName = linesInfo[0]
    linesDictionary = linesInfo[1]
    linesCharacter = linesDictionary[npcName]
    if "Error" in npcName:
        specific = False
    if "Soldier" in npcName:
        npcName = "Soldier"
    if specific == True:#Big ol loop to make sure all events are covered with NPC conversations.
        conversationDone = False
        oneMoreConversation = False
        while conversationDone == False:#first loop: section is either intro, or nothing.
            #Determining what section of dialogue the current event is in, and whether to stop the conversation loop after this one.
            if npcName == "Mayor Madeline":

                if info["Key Pieces"] == 1 and section == "intro":#can only happen AFTER the intro, so no need to bulletproof
                    section = "first"
                    oneMoreConversation = True

                if info["Key Pieces"] == 2 and section == "intro":#same as above comment, can ONLY happen after the above loop.
                    section = "second"

            if npcName == "Inn Keeper" or npcName == "Mayor Madeline":
                try:
                    whichMeeting = info["NPC"][npcName][section]
                except:
                    try:
                        info["NPC"][npcName][section] = True
                    except:
                        info["NPC"].setdefault(npcName,{section:True})
                    whichMeeting = False

                if whichMeeting == True:
                    section = "nothing"
                    oneMoreConversation = False
            
            #Actually printing said dialogue.
            for line in linesCharacter[section]:
                print("\t|" + npcName + ": " + str(line) + " |")
                pause(5)

            
            #Determining whether the conversation has ended or not based on the section and player responses.
            if npcName == "Yogurt" or npcName == "Bow":#Merchant Options.
                character = [["Yogurt","Bomb Bag"],["Bow","Flame Glove"]]#Item Sellers and their respective items
                if npcName == "Yogurt":
                    i = 0
                if npcName == "Bow":
                    i = 1
                #intro always comes first, nothing becomes default if you have their item.

                if section == "buy":
                    if npcName == "Yogurt":
                        itemToBuy = {"Bomb Bag":True}
                    if npcName == "Bow":
                        itemToBuy = {"Flame Glove":True}
                    itemKey = key(itemToBuy)
                    prause(("\nYou got the " + itemKey + "!"))
                    info = equipItem(itemToBuy, info)
                
                if section == "askItem":
                    print("\n\tGold Bag: " + str(info["Gold"]))
                    buyChoice = listOptions(["Buy","Cancel"])
                    oneMoreConversation = True
                    
                    if buyChoice == 1:#Buy/Not Enough Cash
                        if info["Gold"] >= 1000:
                            info["Gold"] -= 1000
                            section = "buy"
                                
                        else:
                            section = "notEnough"
                    elif buyChoice == 2:#Cancel
                        section = "cancel"
                    else:#if somehow the listoptions failed, cancel is returned.
                        section = "cancel"
                                        
                if npcName == character[i][0] and info["Equipment"][character[i][1]] == True and section == "intro":#If you have the seller's item? You get nothing!
                    section = "nothing"
                    oneMoreConversation = True
                if npcName == character[i][0] and info["Equipment"][character[i][1]] == False and section == "intro":#Don't have it yet? Set section to askItem
                    section = "askItem"
                    oneMoreConversation = True
            if npcName == "Mayor Madeline":
                if section == "intro":#Intro section has more gold in lines, so it just spawns 1000 gold for player.
                    info["Current Room"] = rewriteSpecificLine("i",{" ":{"X":2,"Y":2}},info["Current Room"])
                if section == "first":#First key causes another item chest with 1000 gold, and a new convo under moreGold.
                    section = "moregold"
                    info["Current Room"] = rewriteSpecificLine("i",{" ":{"X":8,"Y":2}},info["Current Room"])

            #If you need another loop around, conversation continues. Otherwise, ends loop.
            if oneMoreConversation == True:
                oneMoreConversation = False
                conversationDone = False
            else:
                conversationDone = True
                print()
    else:
        randomLine = random.choice(linesCharacter)
        print(("\t|" + npcName + ": " + randomLine + " |\n"))
        pause(3)
    return info

# This is the general function for managing which lines to display when interacting with them.
# Automatically changes section to nothing/intro depending on whether the player has met the
# non-shopkeep character before.
def dialogueNPCManage(npcInfo,info):
    section = "intro"
    firstMeeting = False
    SHOPKEEP = (("Yogurt"),("Bow"))
    CHARACTER = (("Mayor Madeline"),("Inn Keeper"),("The Demon Queen"))
    #I don't think that I use this function when talking with the demon queen anyway,
    #but I have it in here as a precaution.
    whichNPC = determineWhichNPC(npcInfo,info)
    if whichNPC in SHOPKEEP:
        specific = True
    elif whichNPC in CHARACTER:
        specific = True
    else:
        specific = False#if the character is not defined as above, specific = False.

##    if specific == True:
##        #Mayor and Inn Keeper 
##        if whichNPC not in SHOPKEEP:#sets exception for these two, as I want their intros to always play.
##            try:
##                firstMeeting = info["NPC"][whichNPC]["intro"]
##                print(firstMeeting)
##                section = "nothing"
##                print(section)
##            except:#If the NPC hasn't been set as true yet, sets it now.
##                info["NPC"].setdefault(whichNPC,{"intro":True})
    info = dialogueNPC(npcInfo,info,section,specific)
    return info
    
# item should be the dictionary with only the item type as a key, and the item name itself.
def equipmentStats(itemToEquip):#should be {"Weapon":"Upgrade"}
    itemType = key(itemToEquip)
    itemName = itemToEquip[itemType]
    allWeapons = {"Simple Sword":{"Weapon":3},"Steel Broadsword":{"Weapon":8},"Golden Edge":{"Weapon":15},"Fierce Deity Sword":{"Weapon":35}}
    allArmors =  {"Basic Clothes":{"Defense":1},"Leather Armorset":{"Defense":8},"Platinum Armorset":{"Defense":15},"Fierce Deity Armorset":{"Defense":30}}
    if itemType == "Weapon":
        equipStats = allWeapons[itemName]
    if itemType == "Armor":
        equipStats = allArmors[itemName]
    try:
        test = equipStats
    except:
        prause("Value sent to equipmentStats did not match the database of equipment.")
        equipStats = "cancel"
    return equipStats

# Equips an item to the player and applies the stats it provides. Format should be {"Weapon":"Upgrade"}/similar.
def equipItem(itemToEquip,info,tell=True):
    oldEquips = info["Equipment"].copy()
    ALLWEAPONS = ["Simple Sword","Steel Broadsword","Golden Edge","Fierce Deity Sword"]
    ALLARMORS =  ["Basic Clothes","Leather Armorset","Platinum Armorset","Fierce Deity Armorset"]
    itemKey = key(itemToEquip)
    itemEquip = itemToEquip[itemKey]
    for equipKey in oldEquips:
        if itemKey == equipKey:
            oldItem = {equipKey:oldEquips[equipKey]}
    if itemEquip == "Upgrade":
        if itemKey == "Weapon":
            allUpgrades = ALLWEAPONS
        if itemKey == "Armor":
            allUpgrades = ALLARMORS
        for current in range(len(allUpgrades)):
            if info["Equipment"][itemKey] == allUpgrades[current]:
                itemEquip = allUpgrades[current+1]
                itemToEquip = {itemKey:itemEquip}
                break
    info["Equipment"][itemKey] = itemEquip
    if itemKey != "Bomb Bag" and itemKey != "Flame Glove":
        if tell == True:
            prause(("You equip the " + str(itemEquip) + "."))
## Formerly used to send equipped items to inventory; player can't manually
## equip items anymore, so old equipment is discarded. No reason to keep old
## weapons that have no benefit over current weapon. Same for armor.
##    if oldEquips[itemKey] != "None":
##        info = addInventory({itemKey:oldEquips[itemKey]},info)
        itemStats = equipmentStats(itemToEquip)
        if itemStats == "cancel":
            print()
        else:
            itemStatsKey = key(itemStats)
            info["Player Stats"][itemStatsKey] = itemStats.get(itemStatsKey)
    else:
        prause("You equip it, and realize there's an instruction manual attached to it.")
        if itemKey == "Bomb Bag":
            prause("\tWhen moving through the world, type your direction with WASD and the 'E' key.")
            prause("\tThat will place a bomb, which will detonate and destroy nearby Boulders after 3 moves.")
            prause("\tHave fun!\t\t-Yogurt")
        if itemKey == "Flame Glove":
            prause("\tWhen moving through the world, type your direction with WASD and the 'F' key.")
            prause("\tThat will spray flames! I can't believe Yogurt isn't selling this, the kids love that!")
            prause("\tAnyway, it can melt glaciers, so use it in the Tundra.")
    return info

def displayInventory(info):
    print("\tInventory:\n\t\t", end="")
    isThereInventory = False
    loop = 1
    for itemType in info["Inventory"]:
        loopTwo = 1
        isThereInventory = True
        print(itemType,": ",end="")
        for item in info["Inventory"][itemType]:
            if loopTwo == len(info["Inventory"][itemType]):
                print(item,end="\n\t\t")
            else:
                print(item,end="\n\t\t\t")
            loopTwo += 1
        if loop == len(info["Inventory"]):
            print()
        loop += 1
    if isThereInventory == False and info["Key Pieces"] == 0:
        print("Nothing.")
    else:
        print("\n\t\tPieces of the Tower Key: " + str(info["Key Pieces"]) + "/2\n\t\t")
    print()
    print("\tYour bags:\n\t\t",end="")
    print("Gold Bag: " + str(info["Gold"]) + "; Potion Bag: " + str(info["Potions"]) + "/" + str(info["Potions Max"]))
    print("\n\tYour equipped items:\n\t\t",end="")
    for item in info["Equipment"]:
        if item == "Bomb Bag" or item == "Flame Glove":
            if info["Equipment"][item] == True:
                print(item,end = "\n\t\t")
        else:
            print(item + ": " + str(info["Equipment"][item]), end="\n\t\t")
    prause("\n")
    return info
    
# Adds whatever is in the "chest" to the info dictionaries, typically inventory, can also take gold.
def addInventory(chest,info):
    # "Description":" 100 Gold and a Small Ruby"}
    for thing in chest:
        if thing in info:
            info[thing] += chest[thing]
        elif thing in info["Equipment"]:
            info = equipItem({thing:chest[thing]}, info, tell = True)
        else:
            if thing not in info["Inventory"]:
                info["Inventory"][thing] = []
            info["Inventory"][thing] += [chest[thing]]
    return info

    
# Fixes loaded lines by removing the \n and returning the line without it.
def loadFix(element="\n"):
    eLen = len(element)
    element = element[0:(eLen-1)]
    return element
  
# First call checks that a text file with the names in each save exists.
# If not, it creates the file with "New Save" as each name.
# Second call then returns the name of each save file for use
# in displaying the saves available.
def saveCreateNames(playerName = None):
    try:
        save=open("saveNames.txt","r")
        names = []
        for i in range(3):
            names += [loadFix(save.readline())]
        save.close()
    except:
        save=open("saveNames.txt","w")
        save.write("New Save\nNew Save\nNew Save\n")
        save.close()
    if playerName != None:#If given list of names in the save files, check if the player's name exists.
        otherNameCheck = False
        for name in names:
            if playerName == name:#Is playerName in names? Return True so the nameSelection loops to ask for a new name.
                otherNameCheck = True
        return otherNameCheck

# Calls saveStart once to create the files at first run, then lists
# the file names for player to choose from.
def saveLoadChoice():
    saveCreateNames()
    names =[]
    print("\nWelcome to Queen's Demise! Pick a save file to play by typing in the number of the save.\n")
    saveNames=open("saveNames.txt","r")#Because each line is returned with a \n at the end, the loadFix is used to remove it.
    for i in range(1,4):
        names += [loadFix(saveNames.readline())]
    saveNames.close()
    choice = listOptions(names)
    saveChoice = [choice,names]
    return saveChoice

# Just asks the player what difficulty they want and returns the integer for the option.
def difficultySelect():
    print("Select your difficulty.\n")
    difficulty = listOptions(["Story Mode (lower stats on enemies, potions are infinite, better player stats)",
                              "Easy (lower stats on enemies, more potions than normal, better player stats)",
                              "Normal (intended difficulty)",
                              "Hard (Same as normal, but higher enemy stats)"])
    return difficulty

# Called at the beginning of the game, does a LOT: If player is loading a save after death,
# It ditches the info created so far and returns the old, saved data from earlier.
# Otherwise, it shows the save options and asks the player to choose a save. If new,
# it creates ALL the base info needed for the game to work properly, set up as a nested dictionary
# with a whole bunch of other data types nested within it. That info is passed all throughout the game.
# If the player selects an old save, it loads their old save data; at the very end, the info is sent to main.
def createAllInfo(restartOrReload = False,info=None):
    load = False
    if restartOrReload == "reload":
        choice = info["Save Number"]
        load = True
    if restartOrReload != "reload":
        loadChoice = saveLoadChoice()
        choice = loadChoice[0]
        saveName = loadChoice[1][choice-1]
        if saveName == "New Save":#applies stats from selections
            difficulty = difficultySelect()
            name = nameSelection()
            pronouns = pronounCheck(name)
            playerStats = playerChoice(name,difficulty) 
            region="forest"
            if difficulty == 1:#storymode
                potionsAmount = 99
            if difficulty == 2:#easy
                potionsAmount = 7
            if difficulty == 3 or difficulty == 4:#normal/hard have same potions
                potionsAmount = 3
            
                
            firstTime={"forest":True,"village":True,"tundra":True,"mountains":True,"wasteland":True,"mines":True,
                       "castle":True,"tower":True,"boss":True}
            allGameInfo = {"Player Stats":playerStats,"Region":region,"First Time":firstTime,
                           "Name":name,"Pronouns":pronouns,"Gold":0,"Potions":potionsAmount,
                           "Potions Max":potionsAmount,"Equipment":{"Armor":"None","Weapon":"None","Bomb Bag":False,"Flame Glove":False},
                           "Inventory":{},"Difficulty":difficulty,"NPC":{},"Keys":{"tundra":0,"tower":0,"mountains":0,"forest":0,"village":0},
                           "Load":False,"Save Number":loadChoice[0],"Old Value":-1,"Bonus Damage":["None",0],
                           "Key Pieces":0}
            allGameInfo["Old Rooms"] = {"forest":{},"village":{},"tundra":{},
                                        "mountains":{},"wasteland":{},"tower":{},
                                        "boss":{}}
            allGameInfo = equipItem({"Armor":"Basic Clothes"},allGameInfo,tell=False)
            prause(("OK, " + allGameInfo["Name"] + ", your " +
                    allGameInfo["Player Stats"]["Player Type"] + "'s quest begins!\n"))

            save = open(str("save"+str(choice)+".dat"),"wb")
            pickle.dump(allGameInfo,save,3)
            save.close()
        else:
            load = True
    if load == True:
        save = open("save"+str(choice)+".dat", "rb")
        allGameInfo = pickle.load(save)
        save.close()
        allGameInfo["Load"] = True
    allGameInfo["DEMISE"] = {"Queen":False,"Player":False,"Quit":False}
    return allGameInfo

# Takes a key that you call for, and returns the value. Only works for 2 layers deep, and
# because there's separate dictionaries with the same key values inside the main info dictionary,
# this function is somewhat limited in use. Helpful if you're not sure what the key is to get to
# a deeper nested dictionary one layer in.
def call(valueNeeded,dictionary):
    called = None
    while called == None:
        try:
            called = dictionary[valueNeeded]
        except:
            keys = list(dictionary.keys())
            keyAttempt = 0
            for key in keys:
                try:
                    called = dictionary[key][valueNeeded]
                except:
                    keyAttempt += 1
                    if keyAttempt == len(keys):
                        called = "Failed Call!"
    return called

# Where all the magic happens. Manages the saving and loading, and then when the Gold Statement is met
# (either through player death, queen death, or quitting), it determines what to do for the player.
def main():
    quitGame = False
    restartOrReload = False
    while quitGame == False:
        if restartOrReload == False:
            info = {"Region":"intro"}
            dialogue(info,0,3,0,4)
        #starts by doing all the things necessary for new/old players, loading a game/starting a new one.
        info = createAllInfo(restartOrReload,info)#3 options: False, restart, reload. False means normal loading, reload loads player's save.
        if info["Load"] == True:
            info = loadIntoGame(info)
        while True not in info["DEMISE"].values():#when queen or player dies, or player quits after saving, loop ends.
            region = call("Region",info)
            if call("First Time",info)[region] == True:
                if region == "forest":
                    info["Room Number"] = [3,4]
                    currentRoom = roomDefaultCopy(info)
                    info["Current Room"] = currentRoom
                    info = forestIntro(info)
                elif region == "boss":
                    dialogue(info,0,10,pauseNum=6)
                else:
                    dialogue(info,0,"all",pauseNum=5)
                info["First Time"][region] = False
            info = moveManager(info)

        ENDINGQUESTIONS = {"restart":("Would you like to play again?"),
                           "reload":("Reload your last save?")}
        if info["DEMISE"]["Queen"] == True:
            info["Region"] = "ending"
            print("\n\n")
            if "..." in info["Inventory"]:
                prause((info["Name"] + ", upon returning, gives the Mayor the items that were in the wasteland."))
                for item in info["Inventory"]["..."]:
                    if item == "wedding ring":
                        prause(("Upon seeing the wedding ring, the mayor starts sobbing... \nShe thanks " +
                                info["Name"] + " for bringing her wife's ring back to her."),8)
                  
            dialogue(info,0,"all")
            pause(3)
            restartOrReload = "restart"
        if info["DEMISE"]["Player"] == True:
            prause("The enemy finishes you off, leaving you to bleed out.")
            prause("The hopes of this world die with you...")
            restartOrReload = "reload"
        if info["DEMISE"]["Quit"] == True:
            quitGame = True
            continue
        print(ENDINGQUESTIONS[restartOrReload])
        replayAnswer = listOptions(["Yes","No"])
        if replayAnswer == 1:
            for demiseElement in info["DEMISE"]:
                info["DEMISE"][demiseElement] = False
            quitGame = False
        else:
            quitGame = True
    prause("Thanks for playing the game!")

main()
