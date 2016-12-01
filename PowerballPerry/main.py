import random
import copy

# Intakes first and last name of employee.
#   Returns name (string) of first and last name.
def getName():
    firstName = raw_input('Enter your first name: ')
    lastName = raw_input('Enter your last name: ')
    name = firstName + ' ' + lastName
    return name

# Intakes favorite numbers and powerball number.
# Employers error checking for bounds, and favorite numbers for uniqueness.
#   Returns favoriteList, where the powerball number is the last in the list.
def getFavoriteNumbers():
    placementText = ''
    exclusionText = ''
    favoriteList = list()
    loopThis = True

    for loop in range(6):
        if (loop + 1) == 1:
            placementText = 'Select 1st #'
            exclusionText = '): '
        elif (loop + 1) == 2:
            placementText = 'Select 2nd #'
            exclusionText = ') excluding ' + str(favoriteList[0]) + ': '
        elif (loop + 1) == 3:
            placementText = 'Select 3rd #'
            exclusionText = ') excluding ' + str(favoriteList[0]) + ' and ' + str(favoriteList[1]) + ': '
        else:
            placementText = 'Select ' + str(loop + 1) + 'th #'
            myString = ','.join(map(str, favoriteList))
            firstHalf = myString.rsplit(',', 1)[0]
            secondHalf = myString.rsplit(',', 1)[1]
            myNewString = firstHalf + ', and ' + secondHalf
            exclusionText = ') excluding ' + myNewString + ': '

        #If picking the Powerball number...
        if len(favoriteList) == 5:
            loopThis = True

            while (loopThis):
                number = raw_input('Select Powerball # (1 thru 26):')

                # check if number in bounds
                if (int(number) > 0) & (int(number) < 27):
                    favoriteList.append(int(number))
                    loopThis = False
                else:
                    print 'Number not in bounds.'
        #If picking the 1st-5th numbers
        else:
            loopThis = True

            while (loopThis):
                number = raw_input(placementText + '(1 thru 69' + exclusionText)

                # check if number in bounds
                if (int(number) > 0) & (int(number) < 70):
                    if int(number) in favoriteList:
                        print 'Number has already been chosen'
                    else:
                        favoriteList.append(int(number))
                        loopThis = False
                else:
                    print 'Number not in bounds.'

    return favoriteList

# Displays each employee name, along with their favorite number and powerball number.
#   Returns nothing.
def displayAllEmployees(employeeDict):
    stringDisplay = ''
    empList = list()
    employeeDictCopy = copy.deepcopy(employeeDict)
    for key in employeeDictCopy:
        stringDisplay = key

        #save list of values associated with that key
        empList = employeeDictCopy[key]
        myString = ' '.join(map(str, empList))
        # Everything before the last space - the first five numbers
        firstHalf = myString.rsplit(' ', 1)[0]
        # Everything after the last space - the Powerball number
        secondHalf = myString.rsplit(' ', 1)[1]

        stringDisplay += ' ' + firstHalf + ' Powerball: ' + secondHalf
        print stringDisplay

        # clears list for next key
        del empList[:]


# Uses two dictionaries of key (number chosen) and value (occurrences of number chosen).
# Calls:
#   - findTopFiveNumbers - determines the five most frequent numbers of the favorite numbers
#   - findPowerballNumber - determines the most frequently chosen powerball number
# Displays the resulting Powerball winning number based on the frequency of other employee picks.
#   Returns nothing
def generatePowerballTicket(employeeDict):
    employeeDictCopy = copy.deepcopy(employeeDict)
    # Dictionaries are (x:y) or (number: number of occurrences)
    favDict = dict.fromkeys(range(1, 70), 0)                    # Holds counts for Favorite Numbers 1 - 5
    powerballDict = dict.fromkeys(range(1, 27), 0)              # Holds counts for Powerball number
    fullList = list()
    powerballMaxList = list()                                   # Holds all tied Max result Powerball numbers
    loopTie = True
    powerballString = ''

    # Populate the two dictionaries with the occurrence counts of each number
    for key in employeeDictCopy:
        fullList = employeeDictCopy[key]
        loopIt = 0
        for index in fullList:
            value = fullList[loopIt]
            #if on the last number in the list
            if (loopIt == 5):
               powerballDict[value] += 1
            else:
               favDict[value] += 1

            loopIt += 1
    print 'Powerball winning number:'
    finalList = findTopFiveNumbers(favDict)
    finalPowerballNumber = findPowerballNumber(powerballDict)
    powerballString = ' '.join(map(str, finalList))
    powerballString += ' ' + 'Powerball: ' + str(finalPowerballNumber)
    print powerballString

# Chooses the top five favorite numbers based on frequency of occurrence.  Any ties are solved through randomized picks.
#   Returns list of top five numbers.
def findTopFiveNumbers(favDict):
    finalList = list()
    finalListCount = 0
    favMaxList = list()  # Holds all tied Max result Favorite numbers
    loopTie = True

    while (finalListCount < 5):
        loopTie = True
        # Find most frequent Powerball number count
        resultPower = max(favDict, key=lambda i: favDict[i])
        resultPowerCount = favDict[resultPower]
        favMaxList.append(resultPower)
        # set the found max count to 0, so can find the next max
        favDict[resultPower] = 0

        # Check if one or more powerball numbers are tied in the count
        while (loopTie):
            resultPower1 = max(favDict, key=lambda i: favDict[i])
            resultPowerCount1 = favDict[resultPower1]

            if (resultPowerCount1 == resultPowerCount):
                favMaxList.append(resultPower1)
                # set the found max count to 0, so can find the next max
                favDict[resultPower1] = 0
                loopTie = True
            else:
                loopTie = False

        #If ties were found...
        if len(favMaxList) > 1:
            while(len(favMaxList) > 0):
                answer = random.choice(favMaxList)
                favMaxList.remove(answer)
                finalList.append(answer)
                finalListCount += 1
                if(finalListCount == 5):
                    del favMaxList[:]
        #If only one in the list...
        else:
            answer = favMaxList[0]
            del favMaxList[:]
            finalList.append(answer)
            finalListCount += 1

    return finalList

# Chooses the top powerball number based on frequency of occurrence.  Any ties are solved through randomized picks.
#   Returns top number.
def findPowerballNumber(powerballDict):
    powerballMaxList = list()  # Holds all tied Max result Powerball numbers
    loopTie = True

    # Find most frequent Powerball number count
    resultPower = max(powerballDict, key=lambda i: powerballDict[i])
    resultPowerCount = powerballDict[resultPower]
    powerballMaxList.append(resultPower)
    # set the found max count to 0, so can find the next max
    powerballDict[resultPower] = 0

    # Check if one or more powerball numbers are tied in the count
    while (loopTie):
        resultPower1 = max(powerballDict, key=lambda i: powerballDict[i])
        resultPowerCount1 = powerballDict[resultPower1]

        if (resultPowerCount1 == resultPowerCount):
            powerballMaxList.append(resultPower1)
            # set the found max count to 0, so can find the next max
            powerballDict[resultPower1] = 0
            loopTie = True
        else:
            loopTie = False

    answer = random.choice(powerballMaxList)
    return answer

if __name__ == '__main__':
    addEmployee = True
    employeeDict = dict()

    while addEmployee:
        name = getName()
        favList = getFavoriteNumbers()
        employeeDict[name] = favList
        answer = raw_input('Do you wish to add another employee? Y/N: ')
        if ("Y" in answer.upper()):
            addEmployee = True
        else:
            addEmployee = False
    displayAllEmployees(employeeDict)
    generatePowerballTicket(employeeDict)

