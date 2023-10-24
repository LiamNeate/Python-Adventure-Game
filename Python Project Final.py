import random
import time
import datetime
#Glob is used to get all the available text files when loading.
#Learnt about glob at https://docs.python.org/3/library/glob.html
import glob
loadGameName = ''
inventory = []
moneyTotal = 0
currentHp = 20
bossAvailable = False
pacifist = True
class Enemies():
    def goblin():
        hp = 20
        attack = 5
        crit = 7
        xp = 5
        loot = 'Horn'
        #weakness = complimemt
        return hp, attack, crit, xp, loot
    def slime():
        hp = 25
        attack = 5
        crit = 9
        xp = 8
        loot = 'Jelly'
        #weakness = insult
        return hp, attack, crit, xp, loot
    def warlock():
        hp = 30
        attack = 7
        crit = 10
        xp = 10
        loot = 'Tusk'
        #weakness = ignore
        return hp, attack, crit, xp, loot
    def centaur():
        hp = 100
        attack = 15
        crit = 25
        xp = 40
        loot = 'Head'
        #weakness = hug
        return hp, attack, crit, xp, loot

    def boss():
        hp = 80
        attack = 13
        crit = 15
        xp = 40
        loot = 'Parents'
        #weakness = not hurting anyone
        return hp, attack, crit, xp, loot

    def angryBoss():
        hp = 200
        attack = 20
        crit = 25
        xp = 50
        loot = 'Parents'
        #weakness: NONE!! I HAVE NO WEAKNESSES!! HOW DARE YOU!!!
        return hp, attack, crit, xp, loot
    
class Weapons():
    def starter():
        damage = 10
        crit = 14
        return(damage, crit)
    def swift():
        damage = 15
        crit = 17
        return(damage, crit)
    def long():
        damage = 18
        crit = 22
        return(damage, crit)
    def slayer():
        damage = 20
        crit = 25
        return(damage, crit)
    def ultima():
        damage = 25
        crit = 30
        return(damage, crit)
    
class User():
    def __init__(self, name, hp=20, strength=0, xp=14, level=0):
        self.hp = hp
        self.str = strength
        self.xp = xp
        self.level = level
        self.name = name
        
    def getStats(self):
        return(self.hp, self.str, self.level, self.xp, self.name)

    def levelUp(self):
        self.level+=1
        self.xp = self.xp - 15
        if self.level > 5:
            self.str+=4
            self.exp(0)
        else:
            self.str+=2
            self.exp(0)

class End():
    def neutral():
        print('Boom!! The king has been slain! You quickly find your parents and hold them close. You saved them!')
        time.sleep(2)
        print('\nCongratulations! You have defeated the beast! (Ending 1/3) Thank you for playing. The game will send you back to the menu where you can either keep playing and killing enemies, or save and quit!\n\n')
        time.sleep(2)
        return
    def good():
        time.sleep(2)
        print('\n\nCongratulations! You have befriended the beast! (Ending 2/3) Thank you for playing. The game will send you back to the menu where you can either keep playing and killing enemies, or save and quit!\n\n')
        time.sleep(2)
        return
    def bad():
        print('The king falls, his eyes filled with tears... He had failed his friends... The friends that you murdered...')
        time.sleep(2)
        print('\n\nCongratulations! You have killed all the enemies! (Ending 3/3) Thank you for playing. The game will send you back to the menu where you can either keep playing and killing enemies, or save and quit!\n\n')
        time.sleep(2)
        return

def enemyFeatures(enemy):
    stats = {"goblin":Enemies.goblin, "slime":Enemies.slime, "warlock":Enemies.warlock, "centaur":Enemies.centaur, "boss":Enemies.boss, "angryBoss":Enemies.angryBoss}
    return(stats[enemy]())

def userAttack(enemyStats, userStats, weaponStats):
    if random.randint(0,6) == 6:
        totalAttack = userStats[1] + weaponStats[1]
        print('Critical hit!')
    else:
        totalAttack = userStats[1] + weaponStats[0]
    enemyHealth = int(enemyStats[0]) - int(totalAttack)
    print('You did '+str(totalAttack)+' damage!')
    if enemyHealth <= 0:
        return(0)
    print('The enemy has '+str(enemyHealth)+' hp left!\n')
    return(enemyHealth)

def enemyTurn(enemyStats):
    if random.randint(0,6) == 6:
        attack = enemyStats[2] 
        print('Critical hit!')
    else:
        attack = enemyStats[1]
    global currentHp
    userHealth = int(currentHp) - int(attack)
    print('The enemy did '+str(attack)+' damage!')
    if userHealth <= 0:
        die()
    print('You have '+str(userHealth)+' hp left!')
    currentHp = userHealth
    
        
def rareity(enemies):
    pickEnemy=[]
    for i in range (len(enemies)):
        for j in range (enemies[i][1]):
            pickEnemy.append(enemies[i][0])
    return(random.choice(pickEnemy))
        
def getDmg():
    weapo = {"Starter":Weapons.starter, "Swift":Weapons.swift, "Long":Weapons.long, "Slayer":Weapons.slayer, "Ultima":Weapons.ultima}
    weapoName = inventory[0][0]
    return(weapo[weapoName]())


def setUp(userStats):
    if userStats[2] < 1:
        enemyList=[['goblin', 15],['slime', 12],['warlock', 0],['centaur', 0]]
        enemy = rareity(enemyList)
    elif 1 <= userStats[2] < 4:
        enemyList=[['goblin', 15],['slime', 12],['warlock', 5],['centaur', 0]]
        enemy = rareity(enemyList)
    else:
        enemyList=[['goblin', 15],['slime', 12],['warlock', 5],['centaur', 3]]
        enemy = rareity(enemyList)
    return(enemy)

#Creating a class for loot system
def loot(enemy, enemyLoot, enemyXp, userStats, userInfo, rooms):
    #Setting options so that the centaur only drops 1 loot as he is harder to kill
    if pacifist == False:
        if enemy != 'centaur':
            amm = random.randint(1, 4)
        else:
            amm = 1
    else:
        amm = 0
    moneyGain = random.randint(5, 10)
    #Setting it to find the global variable (The place where the money is stored)
    global moneyTotal
    moneyTotal += moneyGain
    if enemyLoot == 'Parents':
        amm = 2
        print('You got your parents back,', end=' ')
    else:
        print('You got '+str(amm), str(enemyLoot)+',', end=' ')
    print(str(moneyGain)+' money and', end=' ')
    print(str(enemyXp)+' xp!\n')
    #Creating a variable to say wether or not loot gets added since it will check with each item in the list to see if
    #the item is already in there and then change the ammount of said item
    added = False
    for i in range(len(inventory)):
        if(inventory[i][0] == str(enemyLoot)):
            #Adding a new item with the more updated ammount
            inventory.append([enemyLoot,((inventory[i][1]) + amm)])
            #Removing the old item from the list
            inventory.remove([(inventory[i][0]),(inventory[i][1])])
            added = True
    #Regular adding item to the list and setting variables back for next use
    if added == False:
        inventory.append([enemyLoot, amm])
    else:
        added = True
    Play(name=userStats[4], info=userInfo.getStats, rooms=rooms)
        
def exp(xp):
    newLevels = 0
    while xp >= 15:
        newLevels += 1
        xp = xp - 15
    return(newLevels, xp)

def levelUp(level):
    level += 1
    if level > 5:
        return(1, 3)
    else:
        return(2, 2)

def showEnemyStats(enemyName,enemySt):
    print('Enemy type: '+enemyName)
    print('Hp: '+str(enemySt[0]))
    print('Damage: '+str(enemySt[1]))
    print('Critical Damage: '+str(enemySt[2])+'\n')
   
def fightMenu(userStats, rooms, bossTime = False):
    startHp = userStats()[0]
    if bossTime == True:
        print('As you enter the castle, you hear your parents scream in a disrtant room. As you begin to run closer, the screams get louder and it starts to becom apparent that there is another voice as well...')
        print("Suddenly, the screams stop, just as you thought they couldn't get any louder. The door barges open and out comes...")
        time.sleep(2)
        print("\nKING ODWOLA!\n")
        if inventory[0][0] == 'Ultima':
            print('The king notices the sword in your hand. His face turns red with anger from knowing you turned his best friend into a sword. This will not be an easy battle...')
            enemy='angryBoss'
        else:
            enemy='boss'
        enemyStats = list(enemyFeatures(enemy))
        userStats = list(userStats())
        weapStats = list(getDmg())
    else:
        print('You adventure on, through the woods, then suddenly...\n')
        time.sleep(1)
        userStats = list(userStats())
        enemy = setUp(userStats)
        enemyStats = list(enemyFeatures(enemy))
        userStats = list(userStats)
        weapStats = list(getDmg())
        print('You encounter a '+enemy+' in your path!\n')
    while True:
        action = int(input("""What do you do?\n
        0 - Inventory
        1 - Attack
        2 - Talk
        3 - View Stats

Your choice: """))
        if action == 0:
            invent(userStats)
        elif action == 1:
            print('You choose to attack the '+enemy+'!')
            enemyHp = userAttack(enemyStats, userStats, weapStats)
            if enemyHp == 0:
                global pacifist
                if pacifist == True:
                    pacifist = False
                if bossTime == True and enemy == 'boss':
                    End.neutral()
                if bossTime == True and enemy == 'angryBoss':
                    End.bad()
                print('Enemy defeted!! Well done!')
                expGain = (enemyStats[3]+userStats[3])
                newLevels, newExp = exp(expGain)
                newLevel = userStats[2]
                newStrength = userStats[1]
                newHealth = startHp
                for i in range (newLevels):
                    (adStrength, adHealth) = levelUp(userStats[2])
                    newLevel += 1
                    newStrength += adStrength
                    newHealth += adHealth
                    global currentHp
                    currentHp = newHealth
                    levelUpSpeach="\nCongratulations! You leveled up to level {}! You're strength increased by {} and your health increased by {}!\n".format(newLevel, adStrength, adHealth)
                    print(levelUpSpeach)
                currentStats = userStats
                userInfo = User(userStats[4], hp=newHealth, strength=newStrength, xp=newExp, level=newLevel)
                userStats = userInfo.getStats
                userStats=userStats()
                loot(enemy, enemyStats[4], enemyStats[3], userStats, userInfo, rooms)
                #Play(name=userStats[4], info=userInfo.getStats, rooms=rooms)
            else:
                enemyStats[0] = enemyHp
                enemyTurn(enemyStats)
        elif action == 2:
            userInfo = User(userStats[4], userStats[0], userStats[1], userStats[3], userStats[2])
            talkMenu(enemy, enemyStats, userStats, userInfo, rooms, bossTime)
        elif action == 3:
            showEnemyStats(enemy,enemyStats)
        else:
            print('Not a valid choice!')
            
def talkMenu(enemy, enemyStats, userStats, userInfo, rooms, bossTime):
    print('''
    0 - Return
    1 - Compliment
    2 - Hug
    3 - Ignore
    4 - Insult
    ''')
    if bossTime == True and pacifist == True: 
        print('''
    5 - Family
''')
    talk = int(input("Your choice: "))
    if talk == 0:
            print('Going back to fight menu!\n')
    if talk == 1 and enemy == 'goblin':
        print('Your compliment brings the goblin to tears. "No one has ever said that to me", they say, whilst weeping into their arms. A thank you leaves their mouth as they scurrie away...\nEnemy Defeated!')
        loot(enemy, enemyStats[4], 0, userStats, userInfo, rooms)
        return
    elif talk == 1:
        fail(enemyStats)
        return
    elif talk == 2 and enemy == 'centaur':
        print('The centaur is stunned to silence. "W-what are you doing" he mutters. The hug begins to remind him of home, and his mother... The Centaur runs away, probably back to his home, leaving you with a brisk thank you...\nEnemy  Defeated!')
        loot(enemy, enemyStats[4], 0, userStats, userInfo, rooms)
        return
    elif talk == 2:
        fail(enemyStats)
        return
    elif talk == 3 and enemy == 'warlock':
        print('The warlock looks strangely at you. He tries roaring and showing his swords to get your attention. He looks glummly at the floor and walks away')
        loot(enemy, enemyStats[4], 0, userStats, userInfo, rooms)
        return
    elif talk == 3:
        fail(enemyStats)
        return
    elif talk == 4 and enemy == 'slime':
        print("The slime takes your insult to heart. They realise what you say is true and that they need to be better, and more truthful to the themselves. The slime walks away with it's slimey chin held high")
        loot(enemy, enemyStats[4], 0, userStats, userInfo, rooms)
        return
    elif talk == 4:
        fail(enemyStats)
        return
    elif talk == 5 and enemy == 'boss' and pacifist == True:
        print('You talk to the king about how much your family means to you. While at first, he seems unbothered, he soon shows signs of weakness and starts to open up about his family, the monsters we spared. Your bond together and the king lets your family go and apologises. He gives a you a harty handshake and says goodbye...')
        End.good()
        loot(enemy, enemyStats[4], 0, userStats, userInfo, rooms)

def fail(enemyStats):
    print('The monster laughs at your feeble attempt! The monster attacks in retaliation!')
    enemyTurn(enemyStats)

def die():
    print('Ah!')
    print('The final strike from the enemy hits harder than the rest...')
    time.sleep(2)
    print('\nYou fall to the ground... ')
    time.sleep(2)
    print('\nYour Journey is over...')
    time.sleep(2)
    print('You have died!')
    print('Better luck next time! Press enter to close the program. If you would like to play again, please re open the program!')
    input('')
    exit()
    
def checkStatus(stats):
    print('\n----Your Stats---')
    print('Hp: '+str(currentHp)+'/'+str(stats[0]))
    print('Strength: '+str(stats[1]))
    print('Level: '+str(stats[2]))
    print('Xp: '+str(stats[3]))
    print('Weapon: '+inventory[0][0]+' Sword')
    weapStats = (getDmg())
    print('Weapon damage: '+str(weapStats[0]))
    print('Weapon crit: '+str(weapStats[1]))
    
class Menu():
    def __init__(self, name, stats, rooms):
        self.date = datetime.date.today()
        self.stats = stats()
        self.name = name
        self.rooms = rooms
        while True:
            print("""
            0 - Return
            1 - Go to shop
            2 - Save
            3 - Quit (Make sure to save before you quit!!)""")
            if bossAvailable == True:
                print('''
            4 - Boss
            ''')
            move = int(input('Your choice: '))
            if move == 0:
                break
            elif move == 1:
                self.shop()
            elif move == 2:
                self.checkSave()
            elif move == 3:
                print('Thanks for playing!')
                exit()
            elif move == 4 and bossAvailable == True:
                fightMenu(stats, self.rooms, bossTime=True)

    def shop(self):
        print('As you wonder through the forest, you come across a strange shop...')
        while True:
            print('''
Welcome to the shop! Here you can spend money on potions or upgrade your gear with loot!

            0 - Return
            1 - Potion (20 money)
            2 - Swift Sword (5 goblin horns)
            3 - Long Sword (5 slime jelly)
            4 - Slayer Sword (5 warlock tusks)
            5 - Ultima Sword (1 centaur head)
            ''')
            shopChoice = int(input('Your choice: '))
            if shopChoice == 0:
                break
            elif shopChoice == 1:
                global moneyTotal
                if moneyTotal >= 20:
                    inventory[1][1] = inventory[1][1] + 1
                    moneyTotal = moneyTotal - 20
                    print('Purchased!')
                else:
                    print('You need more money!')
            elif shopChoice == 2:
                self.ammCheck('Horn', 'Swift')
            elif shopChoice == 3:
                self.ammCheck('Jelly', 'Long')
            elif shopChoice == 4:
                self.ammCheck('Tusk', 'Slayer')
            elif shopChoice == 5:
                self.ammCheck('Head', 'Ultima', ammountNeed = 1)

    def ammCheck(self, loot, sword, ammountNeed = 5):
        ammount = 0
        for j in range(len(inventory)):
            if inventory[j][0] == loot:
                num = j
                ammount = inventory[j][1]
            else:
                pass
        if ammount < ammountNeed:
            print('Not enough '+loot+'!')
        elif ammount >= ammountNeed and inventory[0][0] != sword:
            print('Purchased!')
            inventory[num][1] = inventory[num][1] - 5
            inventory[0][0] = sword
        else:
            print('You already have this sword!')

    def checkSave(self):
        if loadGameName ==  '':
            i=0
            fileName = self.name + 'usrdata.txt'
            while True:
                try:
                    f = open(fileName, 'r')
                    f.close()
                    fileName = self.name + ' #' + str(i+2) + '.txt'
                    i+=1
                except:
                    self.saving(fileName)
                    break
        else:
            fileName = loadGameName
            self.saving(fileName)
                
    def saving(self, fileName):
        f = open(fileName, 'w')
        inventString = ''
        for i in inventory:
            inventString+=str(i[0])
            inventString+=str(' ')
            inventString+=str(i[1])
            if i != inventory[(len(inventory)-1)]:
                inventString+='%'
        saveData = (('{}${}${}${}${}${}${}${}').format(self.date, inventString, self.stats, self.rooms, moneyTotal, currentHp, pacifist, bossAvailable))
        #First writing the date to the file so the user knows when last edited
        f.write(saveData)
        f.close()
        print('File saved!')
        global loadGameName
        loadGameName = fileName

class Play():
    def __init__(self, name, info, rooms=0):
        self.rooms=rooms
        self.name = name
        self.info = info
        if self.rooms == 0:
            self.__opening()
        else:
            self.__makeMove()

    def __opening(self):
        speach = '''
Welcome Traveler, to the enchanting world of Pruvia!
What was it you said your name was again... {}, was it?
Well {}, let me set the stage...

Our adventure begins in a small cottage, deep in the woods of Pruvia...
It was a dark stormy night when our hero (that's you {}!) was awoken
by a terriying screaming they heard from outside.
Our hero, in a panick, quickly leapt out of bed to investigate, only to
find their parents... missing!

Our hero leaves the house with their fathers trusty sword! This is where
you begin {}, how you will find them, is up to you now!\n
            '''.format(self.name, self.name, self.name, self.name)
        print(speach)
        self.__starter()
        self.__makeMove()

    def __starter(self):
        inventory.append(['Starter', 1])
        inventory.append(['Potion', 1])
        global moneyTotal
        moneyTotal = moneyTotal + 20
        
    def __makeMove(self):
        print('What will you do? ')
        while True:
            print("""
            0 - Menu
            1 - Check Inventory
            2 - Check Stats
            3 - Adventure on
            """)
            move = int(input('Your choice: '))
            if move == 0:
                Menu(self.name, self.info, self.rooms)
            elif move == 1:
                invent(self.info())
            elif move == 2:
                checkStatus(self.info())
            elif move == 3:
                self.rooms+=1
                if self.rooms == 5:
                    global bossAvailable
                    bossAvailable = True
                    print('\n...As you slowly start to lose hope, you come up to a big, towering castle! You hear a faint scream of your parents come from inside...')
                    print('Dare you enter? (If you do not enter now, you can go through the menu to come back at an point, but make sure you save before you enter!)\n')
                    if (input('Your choice (y/n): ')).lower() == 'y':
                        fightMenu(self.info, self.rooms, bossTime=True)
                    else:
                        fightMenu(self.info, self.rooms)
                else:
                    fightMenu(self.info, self.rooms)
                
def invent(info):
    info = list(info)
    print('\n----Your Inventory----')
    print(inventory[0][0]+' Sword')
    for i in range((len(inventory))-1):
        print(inventory[(i+1)][0]+': '+str(inventory[(i+1)][1]))           
    print('Money: '+str(moneyTotal))
    global currentHp
    while (int(info[0]) != int(currentHp)) and (inventory[1][1] > 0):
        print('You currently have '+str(currentHp)+' hp left out of '+str(info[0])+'!')
        potionUse = input('Would you like to use a potion? (y/n)')
        if ((potionUse.lower()) == 'y'):
            currentHp += 10
            inventory[1][1] = inventory[1][1] - 1
            if currentHp > info[0]:
                currentHp = info[0]
                print('Healed to full health!')
            else:
                print('You now have '+str(currentHp)+' hp!')
            break
        else:
            break
                    
        
def newGame():
    adventurer = input('What be your name, traveler? ')
    userInfo = User(adventurer)
    Play(name = adventurer, info = userInfo.getStats)

def loadGame():
    allNames=[]
    i=1
    print('Which adventurer are you? ')
    print('0). Return')
    for name in glob.glob('*usrdata.txt'):
        print(str(i)+'). ', end='')
        fileName = name[0:((len(name)-11))]
        print(fileName, end=' ')
        f = open(name, 'r')
        reading = f.read()
        date = reading.split('$')
        print('(Last Saved '+str(date[0])+')')
        f.close()
        i+=1
        allNames.append(name)
    try:
        loadNum = int(input('Which number are you? '))
    except:
        return
    if loadNum == 0:
        return
    global loadGameName
    loadGameName = (allNames[loadNum-1])
    f = open((allNames[loadNum-1]), 'r')
    reading = f.read()
    date, newInven, stats, rooms, newMoney, curHp, pacif, bossTF = reading.split('$')
    global bossAvailable
    bossAvailable = bool(bossTF)
    global pacifist
    pacifist = bool(pacif)
    global currentHp
    currentHp = curHp
    global moneyTotal
    moneyTotal = int(newMoney)
    newStats = (stats[1:(len(stats)-1)])
    statistics = newStats.split(', ')
    print('\nLoaded!\n')
    newInventory = newInven.split('%')
    for i in newInventory:
        li = list(i.split(' '))
        inventory.append([li[0],int(li[1])])
    userInfo = User(((statistics[4])[1:(len(statistics[4])-1)]), hp=int(statistics[0]), strength=int(statistics[1]), xp=int(statistics[3]), level=int(statistics[2]))
    Play(name = name, info = userInfo.getStats, rooms=int(rooms))
    #print(str(allNames[loadNum-1])+', is this is you?')
    
def main():
    choice = None
    print("""
    Welcome to Pruvia!""")
    while choice != 0:
        print("""
        0 - Quit
        1 - Start a new adventure
        2 - Load a previous adventure
        """)
        try:
            choice = int(input('Your choice: '))
        except:
            choice = None
        if choice == 1:
            start = newGame()
        elif choice == 2:
            start = loadGame()

main()
