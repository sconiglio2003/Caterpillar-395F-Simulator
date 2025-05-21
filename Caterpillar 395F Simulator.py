import random 
import time 
import os
# an array of items you can lift. Used in the items list. 
items = [
    'Corrugated Sewer Pipe',
    'Concrete Manhole',
    'Broken Pickup Truck',
    'Large Tree',
    'House',
    'Tractor',
    'Trailer',
    '56\" Natural Gas Pipe'
]



thingsToLift = []
# class of items you can lift. Gnerates a random item with random weight so you can just generate an array of 10 items with random weights. 
class Item: 
    # items you can lift: corrugated pipe, concrete manhole, broken pickup truck, 56" ID steel natural gas line, etc
    def __init__ (self): 
        self.weight = round(random.randrange(100,300000))
        self.name = random.choice(items)


class Excavator:
    def __init__(self):
        # FUEL
        self.fuelLevel = 100 #                  don't run out of fuel. 
        self.noFuelCode = "0xAAAA"
        self.fuelPumpVolume = 3 #               3 = working, 2 = longer crank time, 1 = stall under load, 0 = does not crank. 
        self.fuelPumpBrokenCode = "0xAAAB"
        self.fuelPumpBeltTension = 100 #        slowly decreases to 0. 
        self.fuelPumpBeltCode = "0xAAAC"
        self.fuelLineObstruction = 0 #          100 = obstructed fully. Restricts fuel flow. 
        self.fuelLineObstructionCode = "0xAAAD"
        self.fuelFilterObstruction = 0 #        100 = obstructed fully. Restricts fuel flow. 
        self.fuelFilterObstructionCode = "0xAAAE"
        self.DEFTank = 100 #                    running out of DEF results in extremely slow operation. 
        self.DEFTankEmptyCode = "0xAAAF"
        # ENGINE
        self.engineRPM = 0 #                    Probably determines lots of temps? idle = 700, working = 1800. 
        self.engineAirFilter = 0   #            100 = fully obstructed 
        self.engineAirFilterObstructedCode = "0xAABA"
        self.turboTemp = 50 #                    Overheats if you work too hard. Don't let it get above 1600* F
        self.turboBrokenCode = "0xAABB"
        self.turboGood = True  #                boolean for destroying the turbo
        self.engineBroken = False #             Why are you reading the description for such an obvious variable
        self.engineBrokenCode = "0xAABC"
        self.engineLife = 100 #                 0 = Engine worn out 
        # RADIATOR
        self.radiatorFanBelt = True #           belt for radiator fan. Can break / lose tension. 
        self.radiatorFanBeltTension = 100 #     0 = slips, must be re tightened. 
        self.radiatorFanBeltTensionCode = "0xAABD"
        self.radiatorFilter = 0 #               100 = fully obstructed
        self.radiatorFilterObstructedCode = "0xAABE"
        self.radiatorFins = 0 #                 100 = fully obstructed
        self.radiatorFinsObstructedCode = "0xAABF"
        self.radiatorSealed = True #            False = the radiator is leaking. 
        self.radiatorPuncturedCode = "0xAACA"
        self.radiatorPumpVolume = 3 #           3 = functional, 2 = hot radiator fluid, 1 = very hot fluid, 0 = pump not functioning. 
        self.radiatorPumpBrokenCode = "0xAACB"
        self.radiatorCoolantAmount = 100 #      Will decrease to 0 if there is a leak. 
        self.radiatorFluidEmptyCode = "0xAACC"
        self.radiatorPumpWorking = True #       False = radiator pump not working. 
        # ENGINE OIL
        self.engineOilLevel = 100 #             will start decreasing when engine gets too hot. Must be changed sometimes. Not changing it can lead to engine and oil pump being Broken.
        self.engineOilEmptyCode = "0xAACD"
        self.engineOilQuality = 100 #           always decreasing to 0, determines rate of engine wear and oil filter obstruction. 
        self.engineOilQualityCode = "0xAACE"
        self.engineOilFilter = 0  #             100 = fully obstructed
        self.engineOilFilterObstructedCode = "0xAACF"
        self.engineOilTemp = 50 #                steady around 200* F. Warnings at 270, 290, auto shutdown > 300* F
        self.engineOilOverheatCode = "0xAADA"
        self.maxEngineOilTemp = 1000 #          change this if the normal oil temp from unobstructed radiator is too hot.  
        # SAFETY
        self.safetyBarDown = False #            True = joysticks work. 
        self.lights = False #                   your lights will not work if the battery is dead. 
        # ELECTRONICS 
        self.computerOn = False #               Computer has to be True to use excavator. Turns on with key. 
        self.computerNotResponsiveCode = "0xAADB"
        self.batteryCharge = 100 #              Excavator will not start with battery < 5%
        self.batteryDeadCode = "0xAADC"
        self.batteryEndOfLifeCode = "0xAADC"
        self.alternatorWorking = True #         Alternator charges battery. 
        self.alternatorBrokenCode = "0xAADD"
        self.alternatorBeltTension = 100 #      Slowly decreases to 0. Once it gets below 90, the battery will charge less and less frequently. Electronics will flicker. 
        self.alternatorBeltBrokenCode = "0xAADE"
        self.keyOn = False #                    Must be true to enable operation. 
        # HYDRAULICS
        self.hydraulicOilLevel = 100 #          will only decrease if you have a leak. 
        self.hydraulicOilEmptyCode = "0xAADF"
        self.hydraulicOilPump = True #          True = fully functional
        self.hydraulicOilPumpBrokenCode = "0xAAEA"
        self.hydraulicOilPumpLife = 100 #       slowly decreases when used. 
        # LIFTING 
        self.liftCapacity = 205000 #            maximum lift capacity of the excavator
        self.itemsList = [] #                   a list of items the excavator can lift. there are 10 items of random weights. 
        self.liftedPounds = 0
        # COINS
        # user gets coins to fix excavator. 
        self.coins = 12000

        # used to wear the machine's parts down. 
        self.degradeRate = 1 #                  Used to detemermine how fast bad things happen. The smaller the number, 
                             #                  the quicker the machine wears out. 
        # ERROR CODES
        self.thrownErrorCodes = [] #            Error codes added to a list every time one happens. You can look them up in the manual to learn how to fix them. 
        # DIRT
        self.dirtMoved = 0 #                    labeling obvious variables is awesome. 
        self.statusString = ""

    def liftItem(self):
        # clear old items
        thingsToLift.clear() 
        choiceMade = False 
        quit = False 
        number = ""
        os.system("cls")
        print("CHOOSE AN ITEM TO LIFT")
        print("Name                     Weight")
        for i in range(10): 
            thing = Item()
            print(str(i) + "     " + thing.name + "               " + str(thing.weight) + " lbs")
            thingsToLift.append(thing)

        while choiceMade == False: 
            print("Choose an item by entering a number: ")
            number = input()
            if number.isnumeric(): 
                number = int(number)
                liftedItem = thingsToLift[number]
                choiceMade = True 
            else: 
                print("Must give number:")
        if choiceMade == True: 
            if self.keyOn == False:
                print("You must turn on the key first")
            if self.engineRPM == 0:
                print("You must first turn on the machine.")
            if self.keyOn == True and self.engineRPM > 0:
                if self.DEFTank > 1 and self.radiatorFanBelt == True and self.engineOilLevel > 0 and self.turboGood == True and self.engineBroken == False and self.keyOn == True and self.batteryCharge > 0 and self.fuelLevel > 0 and self.fuelPumpVolume > 0 and self.fuelFilterObstruction < 100 and self.fuelLineObstruction < 100:
                    # you can't lift witout the lap bar!
                    if self.toggleSafetyBar == False:
                        print("You move the controls, but nothing happens.")
                    else:
                        if liftedItem.weight < self.liftCapacity:
                            # if item is under weight, then you can lift it, award money
                            self.coins += round((liftedItem.weight / 10))
                            self.liftedPounds += liftedItem.weight 
                            self.backgroundUpdate() 
                            print("You were able to lift the " + liftedItem.name + " safely and easily. You gained " + str(round(liftedItem.weight / 10)) + " coins.")
                        else:
                            # otherwise, break
                            # hydraulic pump
                            # drain hydraulic fluid
                            # stall engine
                            # break turbo
                            # alert user to what happened
                            print("As you lift up on the " + liftedItem.name + " the excavator starts to tilt, ",end="")
                            for i in range (4):
                                print("and tilt, ",end="")
                            print("\n")
                            print("Until the excavator has fallen over! The engine has stopped. There is hydraulic oil everywhere. This doesn't look good!")
                            self.engineRPM = 0
                            self.engineBroken = True 
                            self.hydraulicOilLevel = 0
                            self.hydraulicOilPump = False 
                            self.turboGood = False 
                            # throw error codes
                            self.throwErrorCode(self.engineBrokenCode)
                            self.throwErrorCode(self.hydraulicOilPumpBrokenCode)
                            self.throwErrorCode(self.turboBrokenCode)
                            self.throwErrorCode(self.hydraulicOilEmptyCode)
                else:
                    print("Something doesn't seem right. You look at the screen, and there are " + str(len(self.thrownErrorCodes)) + " error codes active") 
        input() 

    def throwErrorCode(self,inputCode):
        if self.thrownErrorCodes.__contains__(inputCode) == False:
            self.thrownErrorCodes.append(inputCode)
            print("Error Code Thrown!")
            input()

    def showStatus(self):
        os.system('cls')
        print("GAUGES")
        if self.keyOn == True:
            print("Key:           "+  "ON")
            # fuel
            print("Fuel:          " + str(self.fuelLevel)+"gal")
            # fuel pump pressure
            print("Fuel Pressure: " + str((self.fuelPumpVolume * 100) / (1 + self.fuelLineObstruction + self.fuelFilterObstruction)) + "gpm")
            # DEF
            print("DEF:           " + str(self.DEFTank)+ "gal")
            # Engine
            print("Engine:        " + str(self.engineRPM)+"rpm")
            # Turbo
            print("Turbo Temp:    " + str(self.turboTemp))
            # A fake uptime designed to signal when the engine is bad
            print("Engine Hours:  " + str(100-self.engineLife)+ "hrs")
            # radiator pump
            print("Radiator Pump: " + str(self.radiatorPumpVolume)+"gpm")
            # engine oil temperature
            print("Oil Temp:      " + str(self.engineOilTemp)+"* F")
            # lights
            if self.lights == True:
                print("Lights:        "+ "ON")
            else:
                print("Lights:        " +"OFF")
            # battery
            print("Battery:       "+ str(self.batteryCharge))
            print(str(len(self.thrownErrorCodes)) + "             ERRORS")
            print("Dirt Moved:    " + str(self.dirtMoved))
            print(self.statusString)
        else:
            print("Key:           " + "OFF")
        print("COINS: " + str(self.coins))
        print("Total lifted lbs:  " + str(self.liftedPounds))

    # fix error codes (requires perfect entry of the number)
    # a switch case based on error codes, which will reset variable values as needed once correct error code has been given. 
    def fixPart(self):
        canAfford = False 
        print("Enter the error code to fix:\nNOTE: it must exactly match, or it won't work.")
        userInput = input()
        # using the user input, determine which variables to reset. 
        match userInput:
            case self.noFuelCode:
                dieselCost = (random.randrange(1,5))
                # only fill tank if enough money
                if self.coins > (322 * dieselCost):
                    self.fuelLevel = 100
                    self.coins -= (dieselCost * 322)
                    canAfford = True 
                    print("You filled up the excavators fuel tank with diesel. It cost $" + str((dieselCost * 322)) + ", and you have $" + str(self.coins) + " left." + " \nENTER = continue")
                else:
                    print("Diesel currently costs $" + str(dieselCost) + " / gallon. You only have $" + str(self.coins) + ", and can only purchase " + str(self.coins / dieselCost) + " gallons.")
                    print("Coming back to this again later will change the price of diesel fuel.")

            case self.fuelPumpBrokenCode:
                pumpCost = (random.randrange(25,1000))
                # only buy pump if they can afford it. 
                if self.coins > pumpCost: 
                    self.fuelPumpVolume = 3
                    self.coins -= pumpCost
                    canAfford = True 
                    print("You bought a new fuel pump. It cost $" + str(pumpCost) + ", and you have $" + str(self.coins) + " left." + " \nENTER = continue")
                else: 
                    print("A new fuel pump currently costs $" + str(pumpCost) + ", and you only have $" + str(self.coins) + " Come back later for a different price.")

            case self.fuelPumpBeltCode:
                beltCost = random.randrange(100,400)
                if self.coins > beltCost: 
                    # you have enough money
                    self.coins -= beltCost
                    self.fuelPumpBeltTension = 100
                    canAfford = True 
                    print("You successfully purchased a new belt and installed it. It cost $" + str(beltCost) + ", and you have $" + str(self.coins) + " left." + " \nENTER = continue")
                else: 
                    print("You only have $" + str(self.coins) + " and a new fuel pump belt costs $" + str(beltCost) + ", come back later for a different price.")
                # It cost $" + str((dieselCost * 322)) + ", and you have $" + str(self.coins) + " left." + " \nENTER = continue"
            case self.fuelLineObstructionCode:
                fuelLineCost = random.randrange(100,400)
                if self.coins > fuelLineCost:
                    self.fuelLineObstruction = 0
                    self.coins -= fuelLineCost
                    canAfford = True 
                    print("You purchased and successfully installed new fuel lines for your excavator. It cost $" + str(fuelLineCost) + ", and you have $" + str(self.coins) + " left." + " \nENTER = continue")
                else: 
                    print("A new fuel line costs $" + str(fuelLineCost) + ", and you only have $" + str(self.coins) + ", come back later for a different price.")

            case self.fuelFilterObstructionCode:
                fuelFilterCost = random.randrange(100,400)
                if self.coins > fuelLineCost:
                    self.fuelFilterObstruction = 0
                    self.coins -= fuelFilterCost
                    canAfford = True 
                    print("You purchased and installed a new fuel filter for your excavator. It cost $" + str(fuelFilterCost) + ", and you have $" + str(self.coins) + " left." + "\n ENTER = continue")
                else:
                    print("It costs $" + str(fuelFilterCost) + " to buy a new fuel filter, and you only have $" + str(self.coins) + ", come back later for a different price.")

            case self.DEFTankEmptyCode:
                DEFcost = random.randrange(2,10)
                if self.coins > (DEFcost * 100):
                    self.DEFTank = 100
                    self.coins -= (DEFcost * 100) 
                    canAfford = True 
                    print("You filled up your excavator's DEF tank. It cost $" + str(DEFcost * 100) + ", and you have $" + str(self.coins) + " left." + "\n ENTER = continue")
                else:
                    print("It costs $" + str(DEFcost * 100) + " to fill your DEF tank, and you only have $" + str(self.coins) + ", come back later for a different price.")

            case self.engineAirFilterObstructedCode:
                engineAirFilterCost = random.randrange(100,3000)
                if self.coins > (engineAirFilterCost * 100):
                    self.engineAirFilter = 0
                    self.coins -= (DEFcost * 100) 
                    canAfford = True 
                    print("You successfully purchased a new engine air filter and installed it. It cost $" + str(engineAirFilterCost) + ", and you have $" + str(self.coins) + " left." + "\n ENTER = continue")
                else:
                    print("It costs $" + str(fuelFilterCost) + " to buy a new engine air filter, and you only have $" + str(self.coins) + ", come back later for a different price.")

            case self.turboBrokenCode:
                turboCost = random.randrange(1000,3000)
                if self.coins > (turboCost):
                    self.turboGood = True
                    self.turboTemp = 50
                    self.coins -= (turboCost)
                    canAfford = True 
                    print("Successfully purchased a new turbo for the engine and installed it. It cost $" + str(turboCost) + ", and you have $" + str(self.coins) + " left." + "\n ENTER = continue")
                else:
                    print("It costs $" + str(turboCost) + " to buy a new engine turbo, and you only have $" + str(self.coins) + ", come back later for a different price.")

            case self.engineBrokenCode:
                engineCost = random.randrange(10000,30000)
                if self.coins > (engineCost):
                    self.engineBroken = False
                    self.engineLife = 100
                    self.coins -= (engineCost) 
                    canAfford = True 
                    print("Successfully purchased a new engine for the excavator and installed it. It cost $" + str(engineCost) + ", and you have $" + str(self.coins) + " left." + "\n ENTER = continue")
                else:
                    print("It costs $" + str(engineCost) + " to buy a new engine, and you only have $" + str(self.coins) + ", come back later for a different price.")

            case self.radiatorFanBeltTensionCode:
                radiatorBeltCost = random.randrange(50,200)
                if self.coins > radiatorBeltCost:
                # make a lbs lifted in lifetime that increases as you lift things. 
                # add enter = continue to the ones you didnt add it to. 
                # allow preventative maintenance so they can get new parts before things fail. 
                    self.radiatorFanBeltTension = 100
                    self.radiatorFanBelt = True 
                    self.coins -= radiatorBeltCost
                    canAfford = True 
                    print("You purchased and installed a radiator fan belt. It cost $" + str(radiatorBeltCost) + ", and you have $" + str(self.coins) + " left. ")
                else: 
                    print("A  new radiator fan belt costs $" + str(radiatorBeltCost) + ", and you only have " + str(self.coins) + ", come back later for a different price.")

            case self.radiatorFilterObstructedCode:
                radiatorFilterCost = random.randrange(2000,3000)
                if self.coins > radiatorFilterCost:
                    self.radiatorFilter = 0
                    self.coins -= radiatorFilterCost
                    canAfford = True 
                    print("You successfully purchased and installed a new radiator filter. It cost $" + str(radiatorFilterCost) + ", and you have $" + str(self.coins) + " left. ")
                else:
                    print("You only have $" + str(self.coins) + ", and a new radiator filter costs $" + str(radiatorFilterCost) + ", come back later for a different price.")

            case self.radiatorFinsObstructedCode:
                self.radiatorFins = 0
                print("You clear away the gunk around your engine coolant radiator. It looks much better now.")

            case self.radiatorPuncturedCode:
                radiatorCost = random.randrange(10000,20000)
                if self.coins > radiatorCost:
                    self.radiatorSealed = True
                    self.radiatorCoolantAmount = 100
                    self.coins -= radiatorCost
                    canAfford = True 
                    print("Succcessfully purchased and installed a new radiator. It cost $" + str(radiatorCost) + ", and you have $" + str(self.coins) + " left." )
                else:
                    print("It costs $" + str(radiatorCost) + " to buy a new radiator, and you only have $" + str(self.coins) + ", come back later for a different price.")   
                        
            case self.radiatorFluidEmptyCode:
                coolantCost = random.randrange(100,250)
                if self.coins > coolantCost:
                    self.radiatorSealed = True
                    self.radiatorCoolantAmount = 100
                    self.coins -= coolantCost
                    canAfford = True 
                    print("You successfully purchased radiator fluid and filled your radiator. It cost $" + str(coolantCost) + ", and you have $" + str(self.coins) + " left. \nENTER = continue")
                else:
                    print("It costs $" + str(coolantCost) + " to buy more radiator coolant fluid, and you only have $" + str(self.coins) + ", come back later for a different price. ")

            case self.radiatorPumpBrokenCode:
                radiatorPumpCost = random.randrange(500,1000)
                if self.coins > radiatorPumpCost:
                    self.radiatorPumpWorking = True 
                    self.radiatorPumpVolume = 3
                    self.coins -= radiatorPumpCost
                    canAfford = True 
                    print("You successfully purchased and installed a new radiator pump. It cost $" + str(radiatorPumpCost) + ", and you have $" + str(self.coins) + " left. \nENTER = continue")
                else:
                    print("It costs $" + str(radiatorPumpCost) + " to buy a new radiator pump, and you only have $" + str(self.coins) + ", come back later for a different price.")

            case self.engineOilEmptyCode:
                engineOilCost = random.randrange(300,1000)
                if self.coins > engineOilCost:
                    self.engineOilLevel = 100
                    self.engineOilQuality = 100
                    self.coins -= engineOilCost
                    canAfford = True 
                    print("You successfully puchased new engine oil and put it into the engine. It cost $" + str(engineOilCost) + ", and you have $" + str(self.coins) + " left. \nENTER = continue")
                else: 
                    print("It costs $" + str(engineOilCost ) + " to get more engine oil, and you only have $" + str(self.coins) + ", come back later for a different price.")
                
            case self.engineOilQualityCode:
                engineOilCost = random.randrange(300,1000)
                if self.coins > engineOilCost:
                    self.engineOilLevel = 100
                    self.engineOilQuality = 100
                    self.coins -= engineOilCost
                    canAfford = True 
                    print("You successfully puchased new engine oil and put it into the engine. It cost $" + str(engineOilCost) + ", and you have $" + str(self.coins) + " left. \nENTER = continue")
                else: 
                    print("It costs $" + str(engineOilCost ) + " to get more engine oil, and you only have $" + str(self.coins) + ", come back later for a different price.")

            case self.engineOilFilterObstructedCode:
                oilFilterCost = random.randrange(100,200)
                if self.coins > oilFilterCost:
                    self.engineOilFilter = 0
                    self.coins -= oilFilterCost
                    canAfford = True 
                    print("You successfully purchased and installed a new engine oil filter. It cost $" + str(oilFilterCost) + ", and you have $" + str(self.coins) + " left. \nENTER = continue")
                else:
                    print("It costs $" + str(oilFilterCost) + " to buy a new engine oil filter, and you only have $" + str(self.coins) + ", come back later for a different price.")

            case self.batteryDeadCode:
                batteryCost = random.randrange(450, 1000)
                if self.coins > batteryCost:
                    self.coins -= batteryCost
                    self.batteryCharge = 100
                    canAfford = True 
                    print("Successfully purchased and installed two new batteries. It cost $" + str(batteryCost) + ", and you have $" + str(self.coins) + " left. \nENTER = continue")
                else:
                    print("It costs $" + str(batteryCost) + " to purchase the new batteries, and you only have $" + str(self.coins) + ", come back later for a different price.")

            case self.alternatorBeltBrokenCode:
                alternatorBeltCost = random.randrange(30,75)
                if self.coins > alternatorBeltCost:
                    self.coins -= alternatorBeltCost
                    canAfford = True 
                    self.alternatorBeltTension = 100
                    print("Successfully purchased and installed a new alternator belt for $" + str(alternatorBeltCost) + ", and you have $" + str(self.coins) + " left. \nENTER = continue")
                else:
                    print("It costs $" + str(alternatorBeltCost) + " to buy a new alternator belt, and you only have $" + str(self.coins) + ", come back again later for a different price.")

            case  self.alternatorBrokenCode:
                alternatorCost = random.randrange(250,350)
                if self.coins > alternatorCost:
                    self.coins -= alternatorCost
                    self.alternatorWorking = True 
                    canAfford = True 
                    print("You successfully purchased and installed a new alternator for $" + str(alternatorCost) + ", and you have $" + str(self.coins) + " left. \nENTER = continue")
                else:
                    print("It costs $" + str(alternatorCost) + " to buy a new alternator, and you only have $" + str(self.coins) + ", come back again later for a different price.")
            
            case self.hydraulicOilEmptyCode:
                hydraulicOilCost = random.randrange(500,1000)
                if self.coins > hydraulicOilCost:
                    self.coins -=hydraulicOilCost
                    self.hydraulicOilLevel = 100
                    canAfford = True 
                    print("You successfully purchased new hydraulic oil and put it into the excavator. It cost $" + str(hydraulicOilCost) + ", and you have $" + str(self.coins) + " left. \nENTER = continue")
                else:
                    print("It costs $" + str(alternatorBeltCost) + " to buy a new alternator belt, and you only have $" + str(self.coins) + ", come back again later for a different price.")
                
            case self.hydraulicOilPumpBrokenCode:
                hydrPumpCost = random.randrange(5000,10000)
                if self.coins > hydrPumpCost:
                    self.coins -= hydrPumpCost
                    self.hydraulicOilPump = True 
                    self.hydraulicOilPumpLife = 100
                    canAfford = True 
                    print("Successfully purchased and installed a brand new OEM hydraulic pump for the 395 Excavator. It cost $" + str(hydrPumpCost) + ", and you have $" + str(self.coins) + " left. \nENTER = continue")
                else:
                    print("It costs $" + str(hydrPumpCost) + " to buy a new hydraulic oil pump, and you only have $" + str(self.coins) + ", come back later for a different price. ")
            case _:
                if self.thrownErrorCodes.__contains__(userInput) == False:
                    print("You may have typed the code incorrectly.")
        
        if canAfford == True: 
            if self.thrownErrorCodes.__contains__(userInput):
                self.thrownErrorCodes.remove(userInput)
        if len(self.thrownErrorCodes) > 0:
            print(str(len(self.thrownErrorCodes)) + " Unfixed codes remain.")
        else: 
            print("NO ERRORS")
        input()

    # update excavator without any output.
    def backgroundUpdate(self):
        # when running, everything degrades. 
        # this simple if statement is important because it determines if the machine is able to keep running. 
        # this if statement checks the critical path: engine, fuel, battery, key, fuel pump, fuel lines, etc. 
        if self.engineBroken == False and self.keyOn == True and self.batteryCharge > 0 and self.fuelLevel > 0 and self.fuelPumpVolume > 0 and self.fuelFilterObstruction < 100 and self.fuelLineObstruction < 100:
            # Math for cooling a fluid through a radiator  behind an air filter. Any radiator uses its unobstructed area to cool the fluid inside it.  
            # radiator fluid pump volume --> radiator - obstruction          --> cool by air through filter      --> air filter obstruction percentage
            # 3 gallons                  --> 10sq ft - 1ft obstruction = 9ft --> 10sq ft filter -1ft obstruction -->  
            #                                subtracts heat from fluid based on air filter non obstruction AND radiator obstruction
            # heat subtracted from radiator coolant = pump volume * (unobstructed air filter sq ft * unobstructed radiator sq ft)
            # all engine RPM related logic goes here. 
            #update engine RPM based on above catagories
            # Only if DEF is full though. 
            if self.engineRPM > 0:
                # kill engine if the engine oil gets too hot
                if self.engineOilTemp > self.maxEngineOilTemp:
                    self.engineRPM = 0
                    if self.thrownErrorCodes.__contains__(self.engineBrokenCode) == False:
                        self.throwErrorCode(self.engineBrokenCode)
                        print("There is a terrible screeching sound! The machine suddenly stops moving, and the engine is off. You can smell something like burning oil.")
                        input()
                # losen radiator fan belt
                if self.radiatorFanBeltTension > 0:
                    self.radiatorFanBeltTension -=  random.randrange(1,10) * (self.degradeRate / 10) # belts slowly loosen
                else:
                    if self.thrownErrorCodes.__contains__(self.radiatorFanBeltTensionCode) == False:
                        self.throwErrorCode(self.radiatorFanBeltTensionCode)
                        print("You hear something flopping around in the back of the excavator.")
                        input()
                # disable radiator fan belt if it is too lose:
                if self.radiatorFanBeltTension < 1: 
                    if self.thrownErrorCodes.__contains__(self.radiatorFanBeltTensionCode) == False:
                        self.throwErrorCode(self.radiatorFanBeltTensionCode)
                        self.radiatorFanBelt = False
                        print("You hear something flopping around in the back of the excavator.")
                        input()
                    if self.thrownErrorCodes.__contains__(self.radiatorPumpBrokenCode) == False:
                        self.throwErrorCode(self.radiatorPumpBrokenCode)
                        self.radiatorPumpWorking = False 
                
                # losen alternator belt
                if self.alternatorBeltTension > 0:
                    self.alternatorBeltTension -=  random.randrange(1,10) * (self.degradeRate / 10) # belts slowly loosen
                else: # disable alternator if the belt is too lose
                    if self.thrownErrorCodes.__contains__(self.alternatorBrokenCode) == False:
                        self.throwErrorCode(self.alternatorBrokenCode)
                        self.alternatorWorking = False 
                        print("You hear something flopping around in the back of the excavator.")
                        input()

                # heat engine oil based on RPM
                self.engineOilTemp += 10
                # wear out engine
                if self.engineLife > 0:
                    self.engineLife -= random.randrange(1,10) * ((self.degradeRate / 1000) * self.engineOilQuality) # slowly wear out engine, sped up by bad oil
                else:
                    if self.thrownErrorCodes.__contains__(self.engineBrokenCode) == False:
                        self.throwErrorCode(self.engineBrokenCode)
                        self.keyOn = False 
                        self.engineBroken = True
                        self.engineRPM = 0
                        print("There is a terrible screeching sound! The machine suddenly stops moving, and the engine is off. You can smell something like burning oil.")
                        self.engineOilQuality = 0
                        input()
                # obstruct fuel filter
                if self.fuelFilterObstruction < 100:
                    self.fuelFilterObstruction +=  random.randrange(1,10) * (self.degradeRate / 1000) # very slowly clog fuel filter
                else:
                    if self.thrownErrorCodes.__contains__(self.fuelFilterObstructionCode) == False:
                        self.throwErrorCode(self.fuelFilterObstructionCode)
                        self.engineRPM = 0
                        print("The engine slowly winds down, until it eventually stops")
                        input()
                        self.keyOn = False 
                # obstruct fuel lines
                if self.fuelLineObstruction < 100:
                    self.fuelLineObstruction +=  random.randrange(1,10) * (self.degradeRate / 1000) # very slowly clog fuel lines
                else:
                    self.engineRPM = 0
                    if self.thrownErrorCodes.__contains__(self.fuelLineObstructionCode) == False:
                        self.throwErrorCode(self.fuelLineObstructionCode)
                        print("The engine slowly winds down, until it eventually stops")
                        input()
                        self.keyOn = False 
                #losen fuel pump belt
                if self.fuelPumpBeltTension > 0:
                    self.fuelPumpBeltTension -=  random.randrange(1,10) * (self.degradeRate / 100) # slowy reduce belt tension
                else:
                    self.engineRPM = 0
                    if self.thrownErrorCodes.__contains__(self.fuelPumpBeltCode) == False:
                        self.throwErrorCode(self.fuelPumpBeltCode)
                        print("You hear something flopping around in the back of the excavator, and the excavator slowly crawls to a stop. The engine has died.")
                        input()
                        self.keyOn = False 
                # obstruct engine air filter
                if self.engineAirFilter < 100:
                    self.engineAirFilter += random.randrange(1,10) * (self.degradeRate / 50) # slowly clog engine air filter
                else:
                    self.engineRPM = 0
                    if self.thrownErrorCodes.__contains__(self.engineAirFilterObstructedCode) == False:
                        self.throwErrorCode(self.engineAirFilterObstructedCode)
                        self.statusString+= "You hear the engine start to wind down quickly. The engine breather sounds strange."
                        input()
                        self.keyOn = False 
                # obstruct engine oil filter
                if self.engineOilFilter < 100:
                    self.engineOilFilter +=  (self.degradeRate * ((random.randrange(1,10) / 1000) * self.engineOilQuality)) # engine oil quality impactts engine oil filter. 
                else:
                    if self.thrownErrorCodes.__contains__(self.engineOilFilterObstructedCode) == False:
                        self.throwErrorCode(self.engineOilFilterObstructedCode)
                    # obstructed oil filter leads to engine siezing
                    self.engineLife = 0
                    self.engineRPM = 0
                    self.engineBroken = True
                    print("There is a terrible screeching sound! The machine suddenly stops moving, and the engine is off. You can smell something like burning oil.")
                    input()
                    self.engineOilTemp = 3000
                    self.keyOn = False  

                # lower engine oil quality
                if self.engineOilQuality > 0:
                    self.engineOilQuality -=  random.randrange(1,10) * ( (random.randrange(1,10) / 1000) * self.degradeRate) # engine oil degrades based on randoe number between 1 and 10 multiplied by a hundredth of the degrade rate. 
                else:
                    if self.thrownErrorCodes.__contains__(self.engineOilQualityCode) == False:
                        self.throwErrorCode(self.engineOilQualityCode)
                    # Bad oil is reallly bad for the engine.
                    self.engineLife -= 2
                    print("Is that white smoke coming out of the exhaust?")
                    input()

                # drain fuel
                if self.fuelLevel > 0:
                    self.fuelLevel -= 1
                else:
                    self.engineRPM = 0
                    if self.thrownErrorCodes.__contains__(self.noFuelCode) == False:
                        self.throwErrorCode(self.noFuelCode)
                        print("The excavator starts choking, until it finally comes to a full stop.")
                        input()
                    self.keyOn = False 
                # drain DEF
                self.DEFTank -= 1

                # if radiator has a leak, empty coolant tank
                if self.radiatorSealed == False:
                    self.radiatorCoolantAmount -= 1
                    if self.thrownErrorCodes.__contains__(self.radiatorPuncturedCode) == False: 
                        self.throwErrorCode(self.radiatorPuncturedCode)
                        print("That sure is a funny smell coming from behind the excavator . . .Is that green fluid on the ground?")
                        input()
                # drastically heat oil if the radiator is empty
                if self.radiatorCoolantAmount < 1:
                    self.engineOilTemp += 100
                    print("You see your engine oil temperature rising drastically! You should stop the excavator!")
                    input()

                # obstruct filters while engine running
                # obstruct radiator air filter
                if self.radiatorFilter < 100:
                    self.radiatorFilter += random.randrange(1,10) * ((random.randrange(1,10) / 1000) * self.degradeRate) # clog the air filter on the radiator based on a random number between 1 and 10 multiplied by a tenth of the degrade rate. 
                else:
                    if self.thrownErrorCodes.__contains__(self.radiatorFilterObstructedCode) == False:
                        self.throwErrorCode(self.radiatorFilterObstructedCode)
                    # overheat engine oil
                    self.engineOilTemp += 20
                    print("You see the engine oil temperature is rising quickly.")
                    input()
                # obstruct radiator
                if self.radiatorFins < 100:
                    self.radiatorFins +=  random.randrange(1,10) * ((random.randrange(1,10) / 1000) * self.degradeRate)
                else:
                    if self.thrownErrorCodes.__contains__(self.radiatorFinsObstructedCode) == False:
                        self.throwErrorCode(self.radiatorFinsObstructedCode)
                    # overheat engine oil
                    self.engineOilTemp += 20
                    print("You see the engine oil temperature is rising quickly.")
                    input()

                self.turboTemp = 1200


                # fuel line obstfuction affects engine rpm                
                if self.DEFTank > 0:
                    self.engineRPM = (10 + self.fuelPumpVolume * (100- self.engineAirFilter)) + ((100 - self.fuelFilterObstruction) + (100-self.fuelLineObstruction))
                else: 
                    # limit engine RPM
                    self.engineRPM = 100
                    if self.thrownErrorCodes.__contains__(self.DEFTankEmptyCode) == False:
                        self.throwErrorCode(self.DEFTankEmptyCode)
                    print("The machine moves very sluggishly. The RPM is very low.")
                    input()
                if self.alternatorWorking == True: 
                    self.batteryCharge = 100
                    self.computerOn = True
                    self.lights = True 
            
                if self.radiatorPumpWorking == True:
                    if self.radiatorFanBelt == True:
                        if (self.engineOilTemp - (self.radiatorPumpVolume * (((100 - self.radiatorFilter) * (100- self.radiatorFins)) / 100))) > 50:
                            self.engineOilTemp -= (self.radiatorPumpVolume * (((100 - self.radiatorFilter) * (100- self.radiatorFins)) / 100))
                        else: 
                            self.engineOilTemp = 50
                    else:
                        # the radiator fan belt has become lose, and now the engine will overheat. 
                        self.engineOilTemp += 20
                        print("You see the engine oil temperature is rising quickly.")
                        input()
                else:
                    # radiator pump isnt working, now engine will overheat. 
                    self.engineOilTemp += 20
                    print("You see the engine oil temperature is rising quickly.")
                    input()
            else: 
                # check if the user shut down the machine while it was too hot. 
                if self.turboTemp > 1000 and self.engineRPM > 0:
                    self.turboGood = False
                    if self.thrownErrorCodes.__contains__(self.turboBrokenCode) == False:
                        self.thrownErrorCodes.append(self.turboBrokenCode)
                    print("SCREEECH! There is a terrible noise behind you.")
                    input()
                if self.engineOilTemp > self.maxEngineOilTemp:
                    self.engineBroken = True 
                    if self.thrownErrorCodes.__contains__(self.engineBrokenCode) == False:  
                        self.thrownErrorCodes.append(self.engineBrokenCode)

        # things that happen whenever the machine is updated (conditions checked, etc)
        
        # turbo gets Broken if you don't let it cool down before shutting off machine. 
        if self.turboTemp > 1000 and self.keyOn == False:
            self.turboGood = False 
            if self.thrownErrorCodes.__contains__(self.turboBrokenCode) == False:
                self.thrownErrorCodes.append(self.turboBrokenCode)
        # keep this batery depletion.
        # kill battery if the alternator dies. 
        if self.alternatorWorking == False and self.keyOn == True:
            if self.thrownErrorCodes.__contains__(self.alternatorBrokenCode) == False:
                self.thrownErrorCodes.append(self.alternatorBrokenCode)
            if self.batteryCharge > 0:
                self.batteryCharge -= 0.1

        # RANDOM EVENTS:
        #   leaks happen in radiator ( 1 in 100)
        #   hydraulic pump, fuel pump,  radiator pump can just break without warning (1 in 100)
        #   hydraulic lines burst (1 in 100)
        #   the alternator can just fail
        randomNum = round(random.randrange(0,600))
        if randomNum == 90:
            self.radiatorSealed = False # working here
            print("Do you smell that? That's a funny smell. . . ") 
            input()
        randomNum = round(random.randrange(0,600))
        if randomNum == 80:
            self.fuelPumpVolume = 0
            print("You hear a loud snap behind you. The excavator engine slowly winds to a halt.")
            input()
            self.engineRPM = 0
            self.keyOn = False
        
        randomNum = round(random.randrange(0,600))
        if randomNum == 70:
            self.hydraulicOilPump = False
            print("You hear a loud screeching and scraping sound. The hydraulics have stopped working. The machine is still running.")
            input()

        randomNum = round(random.randrange(0,600))
        if randomNum == 60:
            self.radiatorPumpWorking = False 
            print("You hear a very loud snap behind you. You notice your engine oil temperature rising very quickly.")
            input()

        randomNum = round(random.randrange(0,600))
        if randomNum == 50:
            self.alternatorWorking = False 
            print("You notice your battery draining quickly.")
            input()

                
    def start(self):
                # if there's no fuel, throw error codes and show symptoms
        if self.fuelLevel < 1:
            if self.thrownErrorCodes.__contains__(self.noFuelCode) == False:
                self.thrownErrorCodes.append(self.noFuelCode)
            print("The engine tries to crank, but no smoke comes from the smoke stack.")
          
        if self.engineOilLevel > 0 and self.turboGood == True and self.engineBroken == False and self.keyOn == True and self.batteryCharge > 0 and self.fuelLevel > 0 and self.fuelPumpVolume > 0 and self.fuelFilterObstruction < 100 and self.fuelLineObstruction < 100:
            self.keyOn = True 
            self.engineRPM += 100
            if self.engineRPM != 0:
                if self.fuelPumpVolume == 1:
                    print("Chug, chug, chuuugugugugugugggaa",end="")
                    time.sleep(2)
                    print("VROOOM! \nThe Caterpillar 395 Excavator roars to life!")
                    self.engineRPM  = 1000
                elif self.fuelPumpVolume == 2:
                    print("Chuguguguga, ",end="")
                    time.sleep(1)
                    print("VROOOM! \nThe Caterpillar 395 Excavator roars to life!")
                    self.engineRPM  = 1400
                elif self.fuelPumpVolume == 3:
                    print("VROOOM! \nThe Caterpillar 395 Excavator roars to life!")
                    self.engineRPM  = 1800
            else:
                print("The engine is already on.")
        # if the key is on, but the excavator didn't start, check for error codes that need to be thrown. 
        else:
            print("The machine did not start. ")
            if self.turboGood == False: 
                print("You hear something like a fan scraping on metal.")
                
            # if the battery is dead, throw error codes and show symptoms. 
            if self.batteryCharge < 1:
                if self.thrownErrorCodes.__contains__(self.batteryDeadCode) == False:
                    self.thrownErrorCodes.append(self.batteryDeadCode)
                print("You turn the key, but all you hear is a quiet click sound. The machine does not turn on. The gauges are all at 0.")

            if self.engineOilLevel < 1:
                print("A slight buzzing sound happens when you turn the key, but the engine doesn't start.")
                if self.thrownErrorCodes.__contains__(self.engineOilEmptyCode) == False: 
                    self.throwErrorCode(self.engineOilEmptyCode)
                    self.engineOilTemp += 100 
            
            # if the fuel pump isn't delivering fuel, throw error codes and show symptoms. 
            if self.fuelPumpVolume == 0:
                if self.thrownErrorCodes.__contains__(self.fuelPumpBrokenCode) == False:
                    self.thrownErrorCodes.append(self.fuelPumpBrokenCode)
                print("Chug, chug, chug\nThe engine did not start.")
            
            # if the fuel filter is obstructed, throw error codes and show symptoms. 
            if self.fuelFilterObstruction > 99:
                if self.thrownErrorCodes.__contains__(self.fuelFilterObstructionCode) == False:
                    self.thrownErrorCodes.append(self.fuelFilterObstructionCode)
                print("WHIRRRRRRRRRRRRRRRRRRRRVVVVVVVVVVVVVVVVVV\nThe engine did not start.")
            
            #if the fuel lines are obstructed, throw error codes and show symptoms
            if self.fuelLineObstruction > 99:
                print("RRRRRRRRRRRRRRRRMMMMMMMMMMMMMVVVVVVVVVVVVVVVVVEEERRRRRRRRRRRRRRRRR\nThe engine did not start, no matter how long you hold the key.")
                if self.thrownErrorCodes.__contains__(self.fuelLineObstructionCode) == False:
                    self.thrownErrorCodes.append(self.fuelLineObstructionCode)

            # if the engine is broken, throw that error code. show symptoms
            if self.engineBroken == True:
                if self.thrownErrorCodes.__contains__(self.engineBrokenCode) == False:
                    self.thrownErrorCodes.append(self.engineBrokenCode)
                    print("SCREECH!\nYou hear something like gears grinding on metal in the back of the engine compartment.")
        input()

    def toggleSafetyBar(self):
        if self.safetyBarDown == True:
            print("Safety bar up. Hydraulics are locked out.")
            self.safetyBarDown = False
        else:
            self.safetyBarDown = True
            print("Safety bar down. Hydraulics are activated.")
        input()

    # this method needed because some errors only show up when the machine is working. 
    def dig(self):
        if self.hydraulicOilLevel < 1: 
            if self.thrownErrorCodes.__contains__(self.hydraulicOilEmptyCode) == False:
                self.thrownErrorCodes.append(self.hydraulicOilEmptyCode)
        if self.hydraulicOilPump == False:
            if self.thrownErrorCodes.__contains__(self.hydraulicOilPumpBrokenCode) == False:
                self.thrownErrorCodes.append(self.hydraulicOilPumpBrokenCode)

        if self.engineRPM > 0 and self.fuelLevel > 0:
            if self.keyOn == True:
                if self.hydraulicOilPump == True and self.hydraulicOilLevel > 0: # you need the hydralic oil pump and oil to dig. 
                    # safety bar must be down
                    # you can't dig if you don't have DEF in your tank.
                    if self.safetyBarDown == True:
                        if self.DEFTank > 0:
                            # user can dig
                            if self.engineBroken == False and self.turboGood == True and self.fuelLevel > 0 and self.fuelLineObstruction < 100 and self.fuelFilterObstruction < 100:
                                self.backgroundUpdate()
                                # hydraulic oil pump wears out. 
                                if self.hydraulicOilPumpLife > 0:
                                    self.hydraulicOilPumpLife -=  random.randrange(1,10) / self.degradeRate
                                else: # the pump is fully worn out
                                    self.hydraulicOilPump = False 
                                    if self.thrownErrorCodes.__contains__(self.hydraulicOilPumpBrokenCode) == False:
                                        self.throwErrorCode(self.hydraulicOilPumpBrokenCode)
                                self.dirtMoved += 6.8 # increase dirt moved
                                self.coins += round(random.randrange(0,100)) # award random amount of coins. 
                                print("The 395F is digging happily") 
                                input()
                        else:
                            print("The machine digs very slowly, and the controls are not that responsive. The engine RPM is only " + str(self.engineRPM))
                            if self.thrownErrorCodes.__contains__(self.DEFTankEmptyCode) == False:
                                self.thrownErrorCodes.append(self.DEFTankEmptyCode)
                                self.coins += round(random.randrange(0,10)) # award random amount of coins. 
                                print("You don't make very much money moving this slow.")
                            input()
                    else:
                        print("You move the controls, but the machine doesn't move at all.")
                        input()
                else:
                    print("GHRKCRUNCHHHHGRIINNDDDDCRUNCHHHHH!\nA terrible grinding noise happens behind you as you move the joysticks.")
                    input() 
        else:
            if self.keyOn == False: 
                if self.engineBroken == True:
                    print("The engine has shut off.")
                    input()
                else: 
                    self.engineRPM = 0
                    self.turboGood = False
                    print("wirrrrrRRRRR....SCREEECH!")
                    input()
                    if self.thrownErrorCodes.__contains__(self.turboBrokenCode) == False: 
                        self.thrownErrorCodes.append(self.turboBrokenCode)
                    if self.engineOilTemp > self.maxEngineOilTemp:
                        self.engineBroken = True 
                        print("SCREECHEERUURRRRAARRCHHHH\nThe engine suddenly halts.")
                        if self.thrownErrorCodes.__contains__(self.engineBrokenCode) == False:
                            self.thrownErrorCodes.append(self.engineBrokenCode)
                            input()
        # wear and tear increases
        # controls must be responsive

    # cool down machine before shutting down automatically.
    def coolDown(self):
        # cool turbo
        # cool engine?
        doneCooling = False
        while doneCooling == False:
            self.turboTemp = 50
            for i in range (9):
                print("Cooling turbo down . . . ")
                time.sleep(0.50)
            self.engineOilTemp  = 50
            for i in range (9):
                print("Cooling engine oil . . . ")
                time.sleep(0.50)
            doneCooling = True 
                
        if doneCooling == True:
            print("You have " + str(self.fuelLevel) + " gallons of fuel left.")
            # shut off machine.
            self.toggleKey()
            self.engineRPM = 0
        input()

    def stop(self):
        if self.keyOn == False: 
            print("The key is off.")
        else: 
            if self.engineBroken == True:
                print("The engine has shut off.")
            else: 
                print("Do not shut down if the machine hasn't been cooled off! The turbo will burn up!\n (y = SHUT DOWN, n = COOL DOWN)")
                print("Turbo Temperature: " + str(self.turboTemp) + "* F")
                choice = input()
                if choice == 'y':
                    self.keyOn = False
                    print("Stopping machine . . . ")
                    self.engineRPM = 0
                    # check if the user shut down the machine while it was too hot. 
                    if self.turboTemp > 1000:
                        self.turboGood = False
                        print("wirrrrrRRRRR....SCREEECH!")
                        self.thrownErrorCodes.append(self.turboBrokenCode)
                    if self.engineOilTemp > self.maxEngineOilTemp:
                        self.engineBroken = True 
                        print("SCREECHEERUURRRRAARRCHHHH\nThe engine suddenly halts.")
                        self.thrownErrorCodes.append(self.engineBrokenCode)
                if choice == 'n':
                    self.coolDown()
        input() 

    # turn key off or on. 
    def toggleKey(self):
        if self.keyOn == False:
            self.keyOn = True
            print("The key is on. ")
        else:
            self.keyOn = False
            self.engineRPM = 0
            print("The key is off. ")
        input()  

    def inspectMachine(self):
        if self.engineRPM > 0:
            print("You must shut off the machine before you can inspect it. This means the engine must not be running.")
        else:
            os.system('cls')
            checkingParts = True 
            while checkingParts == True:
                print("Enter Part Number to Check it's status.\ne = exit")
                print("1.   Fuel Level")
                print("2.   Fuel Lines")
                print("3.   Inspect Fuel Pump Belt")
                print("4.   Engine Air Filter")
                print("5.   Engine")
                print("6.   Engine Oil Filter")
                print("7.   Fuel Filter")
                print("8.   Hydraulic Oil Pump")
                print("9.   DEF (Diesel Exhaust Fluid)")       
                print("10.  Radiator Fan Belt")
                print("11.  Radiator Pump")
                print("12.  Alternator")
                print("13.  Battery")
                print("14.  Turbo")
                chosenPart = input()
                match chosenPart:
                    # exit inspecting parts. 
                    case 'e':
                        checkingParts = False 

                    # check how much fuel you have
                    case '1':
                        if self.fuelLevel > 70:
                            print("You open the fuel cap. It's pretty full.")
                        elif self.fuelLevel > 45:
                            print("You open the fuel cap. It's about half full.")
                        elif self.fuelLevel > 30:
                            print("You open the fuel cap. There's a some fuel in the tank.")
                        elif self.fuelLevel < 1:
                            print("You open the fuel cap and look inside. There is no fuel.")
                        input()

                    # inspect fuel lines
                    case '2':
                        print("You remove the fuel lines and see they are " + str(self.fuelLineObstruction) + " percent blocked. ")
                        input()

                    # the fuel pump belt inspection
                    case "3":
                        if self.fuelPumpBeltTension > 70:
                            print("The belt is in perfect condition, and will not need maintenance soon.")
                        elif self.fuelPumpBeltTension > 40:
                            print("You inspect the fuel pump belt. It seems okay for a few more digs.")
                        elif self.fuelPumpBeltTension > 10:
                            print("The fuel pump belt is not very tight.")
                        elif self.fuelPumpBeltTension < 10 and self.fuelPumpBeltTension > 1:
                            print("The fuel pump belt must be tightened soon.")
                        elif self.fuelPumpBeltTension < 1:
                            print("The belt has been broken.")
                        input()

                    # inspect engine air filter    
                    case "4":
                        if self.engineAirFilter > 99:
                            print("The engine air filter is so dusty no air can get through. It must be cleaned.")
                        elif self.engineAirFilter > 70:
                            print("The engine air filter is so dusty you can scrape dust particles off of it. It is barely functioning.")
                        elif self.engineAirFilter > 50:
                            print("The engine air filter is about halfway dirty.")
                        elif self.engineAirFilter > 20:
                            print("The engine air filter is pretty new.")
                        elif self.engineAirFilter < 20:
                            print("The engine air filter is brand new, and doesn't need cleaning.")
                        input()

                    # inspect engine ( also tells if belts are broken, if radiator is broken, if hydraulic pump is broken)
                    case '5':
                        if self.engineRPM > 0:
                            print("The engine is running.")
                        if self.engineBroken ==  True:
                            print("The engine block has a crack in its side. You can see internal parts that shouldn't be exposed. This doesn't look good. It is broken.")
                        if self.engineRPM == 100: 
                            print("The engine is idling.")
                        if self.engineRPM == 0:
                            print("The engine is not running.")
                        if self.engineOilTemp > 100:
                            print("The engine is very warm.")
                        # oil will be everywhere if the hydraulic pump is trashed
                        if self.hydraulicOilPumpLife < 1:
                            print("There is hydraulic oil everywhere.")
                        # radiator leaks will be evident from here
                        if self.radiatorSealed == False: 
                            print("There is radiator coolant everywhere.")
                        # engine oil leaks will be evident here
                        if self.engineOilLevel < 1:
                            print("There is engine oil everywhere.")
                        # any belt that is broken will be evident here
                        input()

                    # inspect the engine oil filter (also tells oil quality)
                    case '6':
                        statement = ""
                        # some oil / oil full 
                        if self.engineOilLevel > 0:
                            if self.engineOilTemp > 100:
                                statement += "Careful! The oil is very hot. "
                            statement += "The oil drips down your hands as you unscrew the filter. "
                            if self.engineOilFilter > 99:
                                statement+= "The engine oil filter is completely clogged. It must be replaced."
                            elif self.engineOilFilter > 90:
                                statement += " As You look inside the filter, you see it is full of particles"
                            elif self.engineOilFilter > 30:
                                statement += " As you look inside the filter, you see it is pretty dirty"
                            elif self.engineOilFilter <= 30:
                                statement += " You look inside the engine oil filter. It is perfectly clean "
                            # add statements about engine oil quality. 
                            if self.engineOilQuality > 90:
                                statement += ", and the oil is nearly perfectly clear. "
                            elif self.engineOilQuality > 50:
                                statement += ", and the oil is a gray color. "
                            elif self.engineOilQuality > 10:
                                statement += ", and the oil is dark black. It will need to be replaced soon. "
                            elif self.engineOilQuality < 1:
                                statement += ", and the oil is dark black and thick to the touch. There are shiny flakes of metal in it. It  must be replaced. "
                        # no oil
                        elif self.engineOilLevel < 1:
                            print("You unscrew the engine oil filter, but there is no oil in it at all. There is a burning smell in the air. The oil must be refilled. It is likely that there are other problems. The engine is likely destroyed.")
                        # details about the temperature of the oil
                        print(statement)
                        input()

                    # check fuel filter obstruction
                    case '7':
                        if self.fuelFilterObstruction > 99:
                            print("You unscrew the fuel filter, and see it is completely full of gummy diesel fuel. It needs replaced.")
                        elif self.fuelFilterObstruction > 70:
                            print("You unscrew the fuel filter and see it is functional but pretty dirty.")
                        elif self.fuelFilterObstruction > 20:
                            print("You unscrew the fuel filter, and see that it is relatively new.")
                        if self.fuelFilterObstruction > 0:
                            print("The fuel filter is brand new. It does not need replacing.")
                        input()

                    # inspect hydraulic oil pump
                    case '8':
                        # things that will be evident here include: empty hydraulic oil tank, broken pump
                        # you are out of oil
                        if self.hydraulicOilLevel > 0:
                            print("You get out your 1 inch allen wrench and unscrew the side panel of the hydraulic oil pump. The oil drips out on your hands. ")
                        # there is hydraulic oil. 
                        else: 
                            print("You get out your 1 inch allen wrench and unscrew the side panel of the hydraulic oil pump. There is no oil inside of it. ")
                        
                        # pump not broken - state condition based on hydraulic oil pump life (a number). 
                        if self.hydraulicOilPump == True:
                            if self.hydraulicOilPumpLife > 90:
                                print("You inspect the pump: the blades look brand new and shiny.")
                            elif self.hydraulicOilPumpLife > 60:
                                print("The hydraulic oil pump is in good condition.")
                            elif self.hydraulicOilPumpLife > 20:
                                print("The pump is well used, but it is still functioning.")
                            elif self.hydraulicOilPumpLife > 0 and self.hydraulicOilPumpLife < 20:
                                print("The pump is still functioning but has served for a long time.")
                        # hydraulic oil pump broken
                        else:
                            print("The blades of the pump are destroyed; the pump will need replacing.") 
                        input()

                    # Check DEF Tank
                    case '9':
                        print("You walk to the side of the machine to check the level of the DEF tank. You unscrew the lid and ")
                        if self.DEFTank > 90:
                            print(" see the DEF is full.")
                        elif self.DEFTank > 50:
                            print(" see the DEF tank is about half full.")
                        elif self.DEFTank > 20:
                            print(" see that the DEF Tank is lower than 1/3 full. ")
                        elif self.DEFTank < 20 and self.DEFTank > 1:
                            print("You will need to refill the DEF very soon.")
                        elif self.DEFTank < 1:
                            print("You do not see any DEF in the tank.")
                        input()

                    # check radiator fan belt tension
                    case '10':
                        # check radiator fan belt tension
                        print("You open the side of the excavator to inspect the radiator fan belt tension.")
                        if self.radiatorFanBeltTension > 90:
                            print("The belt is perfectly fine. You shouldn't have to worry about it for a while.")
                        elif self.radiatorFanBeltTension > 60:
                            print("The belt is pretty tight.")
                        elif self.radiatorFanBeltTension > 30:
                            print("The belt is relatively tight. You should keep an eye on it. ")
                        elif self.radiatorFanBelt > 20:
                            print("The belt is pretty lose. You should keep an eye on it.")
                        elif self.radiatorFanBeltTension < 1:
                            print("The belt is too lose or degraded to operate.")

                        # Stuff you'll notice if there are other problems.
                        # you will see if there's a radiator leak. 
                        if self.radiatorSealed == False:
                            print("There is radiator fluid inside the machine. The radiator is leaking, and could be empty. If it is, starting the machine could destroy the engine.",end="")
                        # you'll see if the engine is broken
                        if self.engineBroken == True:
                            print("The engine smells burnt. There is obvious damage on the engine block.")
                        # you'll see if the radiator fins are blocked
                        if self.radiatorFins > 99:
                            print("The radiator fins are so blocked that you cannot see the metal, just caked dust and mud. The radiator cannot cool engine if it is like this. It must be cleaned.",end="")
                        elif self.radiatorFins > 80:
                            print("The radiator fins are very dirty. They will not cool the engine well like this. ")
                        elif self.radiatorFins > 40:
                            print("The radiator is pretty dirty and won\'t work well in this condition. ")
                        elif self.radiatorFins > 20:
                            print("The radiator fins are a little dirty, but they are fine.")
                        elif self.radiatorFins < 20:
                            print("The radiator fins are very clean. It shouldn't need cleaned for a while. ")

                        # you'll see if the radiator filter is clogged too.
                        if self.radiatorFilter > 99:
                            print("The radiator filter is very dirty. No air can get through it. It will need to be cleaned.")
                        elif self.radiatorFilter > 70:
                            print("The radiator is pretty dirty and will need to be cleaned soon. ")
                        elif self.radiatorFilter > 40:
                            print("The radiator relatively dirty. It will need to be cleaned eventually.")
                        elif self.radiatorFilter > 20:
                            print("The radiator is clean.")
                        elif self.radiatorFilter < 20:
                            print("The radiator is very clean. You dont need to worry about it right now.")
                        input()

                    # check radiator pump
                    case '11':
                        print("You get your 1/2 inch allen wrench set to take apart the radiator pump and inspect it.")
                        # you'll see if the radiator is empty
                        if self.radiatorCoolantAmount < 1:
                            print(" The radiator pump is bone dry. ")
                        else:
                            print(" The radiator fluid spills on your gloves. ")
                        if self.radiatorPumpWorking == True:
                            # radiator pump working
                            print(" The pump is functional")
                            # you can see how worn out the radiator pump is. 
                            if self.radiatorPumpVolume == 1:
                                print(", but the blades are very worn out. It is on the brink of failure.")
                            elif self.radiatorPumpVolume == 2:
                                print(" but has seen some  better days. It is about ready to be replaced.")
                            elif self.radiatorPumpVolume == 3:
                                print(", and it is in perfect condition.")
                        else:
                            # radiator pump broken
                            print("The pump blades are broken. They will need to be replaced. ")


                        # you'll see if the engine is broken
                        # you'll see if there's a radiator leak
                        # Stuff you'll notice if there are other problems.
                        # you will see if there's a radiator leak. 
                        if self.radiatorSealed == False:
                            print("There is radiator fluid inside the machine. The radiator is leaking, and could be empty. If it is, starting the machine could destroy the engine.",end="")
                        # you'll see if the engine is broken
                        if self.engineBroken == True:
                            print("The engine smells burnt. There is obvious damage on the engine block.")
                        # you'll see if the radiator fins are blocked
                        if self.radiatorFins > 99:
                            print("The radiator fins are so blocked that you cannot see the metal, just caked dust and mud. The radiator cannot cool engine if it is like this. It must be cleaned.",end="")
                        elif self.radiatorFins > 80:
                            print("The radiator fins are very dirty. They will not cool the engine well like this. ")
                        elif self.radiatorFins > 40:
                            print("The radiator is pretty dirty and won\'t work well in this condition. ")
                        elif self.radiatorFins > 20:
                            print("The radiator fins are a little dirty, but we\re working outside after all. ")
                        elif self.radiatorFins < 20:
                            print("The radiator fins are very clean. It shouldn't need cleaned for a while. ")

                        # you'll see if the radiator filter is clogged too.
                        if self.radiatorFilter > 99:
                            print("The radiator filter is very dirty. No air can get through it. It will need to be cleaned.")
                        elif self.radiatorFilter > 70:
                            print("The radiator is pretty dirty and will need to be cleaned soon. ")
                        elif self.radiatorFilter > 40:
                            print("The radiator relatively dirty. It will need to be cleaned eventually.")
                        elif self.radiatorFilter > 20:
                            print("The radiator is clean.")
                        elif self.radiatorFilter < 20:
                            print("The radiator is very clean. You dont need to worry about it right now.")
                        input()

                    # Check the alternator to see if its working.
                    case '12':
                        print("You check the alternator with a voltmeter. It ",end="")
                        if self.alternatorWorking == True:
                            print("is working fine. ")
                        else:
                            print("has no voltage across its wires. It has burned up and needs replaced.")
                        # check belt tension
                        if self.alternatorBeltTension > 90:
                            print("The alternator belt is perfectly tight. You shouldn\t have to worry about it for a while.")
                        elif self.alternatorBeltTension > 70:
                            print("The alterntor belt is tight enough for now.")
                        elif self.alternatorBeltTension > 40:
                            print("The alterntor belt is getting lose. You will have to tighten it eventually.")
                        elif self.alternatorBeltTension > 10:
                            print("The alternator belt is pretty lose. You will have to tighten it soon.")
                        elif self.alternatorBeltTension < 10 and self.alternatorBeltTension > 1:
                            print("You will need to tighten the belt very soon.")
                        if self.alternatorBeltTension < 1:
                            print("The alternator belt is too lose to turn the alternator.")
                        # any leaks or engine damage will be apparent. 
                        if self.engineBroken == True:
                            print("There is obvious damage to the engine. It may need inspected more closely.")
                        if self.radiatorSealed == False:
                            print("There is radiator fluid all over the machine. You should inspect the radiator.")
                        input()

                    # Check the battery
                    case '13':
                        print("You place your voltmeter leads across the battery terminals.")
                        if self.batteryCharge > 80:
                            print("The battery is sufficiently charged.")
                        elif self.batteryCharge > 50:
                            print("The battery is half charged. You may want to check the alternator.")
                        elif self.batteryCharge > 20:
                            print("You may have battery or alternator issues. It is only " + str(self.batteryCharge) + " percent full.")
                        elif self.batteryCharge < 20 and self.batteryCharge > 1:
                            print("The battery is almost dead.")
                        elif self.batteryCharge < 1:
                            print("The battery is dead, and will need to be replaced. ")
                        input() 

                    case '14':
                        print("You open the turbo and look inside it.")
                        if self.turboGood == False: 
                            print("The blades of the turbo are melted and sagging.")
                        else: 
                            print("The turbo fan spins freely. It is in good working order. ")
                        input()
        input() 
    # show error codes method
    #def showErrorCodes(self):
    #    if len(self.thrownErrorCodes) == 0:
    #        print("There are no error codes.")
    #    else:
    #        print("ACTIVE ERROR CODES:")
    #        for errorCode in self.thrownErrorCodes:
    #            print(errorCode)
    #    input() 

    def showWearStatus(self):
        print("VARIABLES")
        print("Fuel Pump Volume:              " + str(self.fuelPumpVolume))
        print("Fuel pump Belt Tension:        " + str(self.fuelPumpBeltTension))
        print("Fuel Line Obstruction:         " + str(self.fuelLineObstruction))
        print("Fuel Filter Obstruction:       " + str(self.fuelFilterObstruction))
        print("Engine Air filter Obstruction: " + str(self.engineAirFilter))
        print("Turbo:                         " + str(self.turboGood))
        print("Engine:                        " + str(self.engineBroken) + " (False = engine OK)")
        print("Engine Life:                   " + str(self.engineLife))
        print("Radiator Fan Belt Tension:     " + str(self.radiatorFanBeltTension))
        print("Radiator Filter:               " + str(self.radiatorFilter))
        print("Radiator Fins:                 " + str(self.radiatorFins))
        print("Radiator Sealed:               " + str(self.radiatorSealed))
        print("Radiator Pump Volume:          " + str(self.radiatorPumpVolume))
        print("Radiator Pump:                 " + str(self.radiatorPumpWorking))
        print("Radiator Coolant Amount:       " + str(self.radiatorCoolantAmount))
        print("Engine Oil Level:              " + str(self.engineOilLevel))
        print("Engine Oil Life:               " + str(self.engineOilQuality))
        print("Engine Oil Filter:             " + str(self.engineOilFilter))
        print("Alternator:                    " + str(self.alternatorWorking))
        print("Alternator Belt Tension:       " + str(self.alternatorBeltTension))
        print("Hydraulic Oil Level:           " + str(self.hydraulicOilLevel))
        print("Hydrualic Oil Pump Life:       " + str(self.hydraulicOilPumpLife))

samsExcavator = Excavator() 
intro = True
print("Press enter to start.")
while True:
    samsExcavator.backgroundUpdate()
    samsExcavator.showStatus()
    #samsExcavator.showWearStatus() 
    print("\n1.    Start Excavator\n2.    Stop Excavator\n3.    Dig\n4.    Toggle Safety Bar.\n5.    Turn Key\n6.    Fix Part\n7.    View Error Codes\n8.    Inspect Machine.\n9.    Lift Item\n10.   Developer Options")
    choice = input()
    if choice == "1":
        samsExcavator.start()

    if choice == "2":
        samsExcavator.stop()

    if choice == "3":
        samsExcavator.dig()

    if choice == "4":
        samsExcavator.toggleSafetyBar()

    if choice == "5":
        samsExcavator.toggleKey()

    if choice == "6":
        samsExcavator.fixPart()

    if choice == "7":
        #samsExcavator.showErrorCodes()
        print("Silly goose! That's for developers only . . . ")
    if choice == "8":
        samsExcavator.inspectMachine()

    if choice == "9": 
        samsExcavator.liftItem()

    if choice == "10":
        samsExcavator = Excavator()


        