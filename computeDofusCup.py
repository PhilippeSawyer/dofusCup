import requests
from bs4 import BeautifulSoup
import time

classTranslate = ["feca", "osamodas", "enutrof", "sram", "Xelor", "ecaflip", "eniripsa", "iop", "cra", "sadida", "sacrieur", "pandawa", "roublard", "zobal", "steamer", "eliotrope", "huppermage", "ouginak"]

teamArray = []
playerArray = []
classArray = []
linkArray = []
teamLinkArray = []

teamForfait = []

topTeamArray = []
topPlayerArray = []
topClassArray = []
topLinkArray = []
topTeamLinkArray = []
topTeamPVA = []
topTeamPoints = []

def computeCup(baseUrl):

    pageNum = 1
    while computePage(baseUrl + str(pageNum)) == 1:
        print(pageNum)
        pageNum = pageNum + 1


def computePage(url):

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    teams = soup.findAll("tr", {"class": ["ak-bg-odd", "ak-bg-even"]})

    if len(teams) == 0:
        return 0

    for team in teams:
        computeTeam(team)

    return 1


def computeTeam(htmlInput):

    html = htmlInput.findAll('a')
    teamArray.append(html[0].get_text())
    playerArray.append([html[1].get('title'), html[2].get('title'), html[3].get('title')])
    linkArray.append([html[1].get('href'), html[2].get('href'), html[3].get('href')])
    classArray.append([getClass(html[1].find('span').get('class')[1]), getClass(html[2].find('span').get('class')[1]), getClass(html[3].find('span').get('class')[1])])
    teamLinkArray.append(html[0].get('href'))

    return 0


def getClass(string):

    # input: breed5_1  // breed10_1
    #   len:    8            9

    if len(string) == 9:
        a = string[5]
        b = string[6]
        c = a + b
        return classTranslate[int(c)-1]

    if len(string) == 8:
        a = string[5]
        return classTranslate[int(a)-1]

    return "error"


def statsClass():

    result = {}
    for classe in classTranslate:
        result[classe] = 0

    for team in classArray:
        for player in team:
            result[player] = result[player] + 1

    return result


def statsDuo():

    result = {}
    for team in classArray:
        duos = [[team[0], team[1]], [team[0], team[2]], [team[1], team[2]]]

        for duo in duos:
            if classTranslate.index(duo[1]) < classTranslate.index(duo[0]):
                temp = duo[0]
                duo[0] = duo[1]
                duo[1] = temp

            duo = tuple(duo)
            if duo in result:
                result[duo] = result[duo] + 1
            else:
                result[duo] = 1

    return result


def statsTrio():

    result = {}
    for team in classArray:
        trio = [team[0], team[1], team[2]]
        if classTranslate.index(team[0]) < classTranslate.index(team[1]) and classTranslate.index(team[0]) < classTranslate.index(team[2]):
            trio[0] = team[0]
            if classTranslate.index(team[1]) < classTranslate.index(team[2]):
                trio[1] = team[1]
                trio[2] = team[2]
            else:
                trio[1] = team[2]
                trio[2] = team[1]

        elif classTranslate.index(team[1]) < classTranslate.index(team[0]) and classTranslate.index(team[1]) < classTranslate.index(team[2]):
            trio[0] = team[1]
            if classTranslate.index(team[0]) < classTranslate.index(team[2]):
                trio[1] = team[0]
                trio[2] = team[2]
            else:
                trio[1] = team[2]
                trio[2] = team[0]
        else:
            trio[0] = team[2]
            if classTranslate.index(team[0]) < classTranslate.index(team[1]):
                trio[1] = team[0]
                trio[2] = team[1]
            else:
                trio[1] = team[1]
                trio[2] = team[0]

        trio = tuple(trio)
        if trio in result:
            result[trio] = result[trio] + 1
        else:
            result[trio] = 1

    return result


def sortStats(result):

    return sorted(result.items(), key=lambda x:x[1], reverse=True)


def removeForfait():

    index = 0
    for team in teamArray:

        link = "https://www.dofus.com/" + teamLinkArray[index]
        page = requests.get(link)
        soup = BeautifulSoup(page.content, 'html.parser')
        history = soup.findAll("div", {"class": "ak-battle-history"})
        results = history[0].findAll("span", {"class": "ak-match-type"})
        specialLinks = history[0].findAll('a')

        indexBis = 1
        for result in results:
            texte = result.get_text()
            texteResult = texte.split()[0]

            # Match nul
            if texteResult == "Défaite" or texteResult == "Match":
                newLink = "https://www.dofus.com/" + specialLinks[indexBis].get('href')
                page = requests.get(newLink)
                soup = BeautifulSoup(page.content, 'html.parser')
                target = soup.find("div", {"style": "padding-top:0;padding-bottom:0"})

                # IL Y A AU MOINS UN FORFAIT
                if "forfait" in target.getText():

                    teamForfait.append(str(teamArray.pop(index)) + ',' + str(playerArray.pop(index))+ ',' + str(classArray.pop(index))+ ',' + str(linkArray.pop(index))+ ',' + str(teamLinkArray.pop(index)))

                    time.sleep(1)
                    break


            indexBis = indexBis + 2

        index = index + 1

    return 0


def computeTopCup(points, url):

    pageNumber = 1
    while(computeTopPage(points, url + str(pageNumber)) is True):
        pageNumber = pageNumber + 1
        print(pageNumber)


def computeTopPage(points, url):

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    teams = soup.findAll("tr", {"class": ["ak-first-ladder", "ak-bg-even", "ak-bg-odd"]})

    index = 0
    for team in teams:
        target = teams[index].findAll('td')

        #Check if the team is above the points threshold
        if float(target[2].getText()) < points:
            return False

        teamName = target[1].getText()
        print(teamName)
        teamIndex = teamArray.index(teamName)
        topTeamArray.append(teamName)
        topClassArray.append([classArray[teamIndex][0], classArray[teamIndex][1], classArray[teamIndex][2]])
        topPlayerArray.append([playerArray[teamIndex][0], playerArray[teamIndex][1], playerArray[teamIndex][2]])
        topLinkArray.append(linkArray[teamIndex])
        topTeamLinkArray.append(teamLinkArray[teamIndex])
        
        index = index + 1
    return True


def computePosition(position, url):
    pageNumber = 1
    while (computePositionPage(position, url + str(pageNumber)) is True):
        pageNumber = pageNumber + 1
        print(pageNumber)


def computePositionPage(position, url):

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    teams = soup.findAll("tr", {"class": ["ak-first-ladder", "ak-bg-even", "ak-bg-odd"]})

    index = 0

    #check that we have at least one team:
    if len(teams) == 0:
        return False

    for team in teams:
        target = teams[index].findAll('td')


        teamName = target[1].getText()
        print(teamName)
        teamIndex = teamArray.index(teamName)
        topTeamArray.append(teamName)
        topClassArray.append([classArray[teamIndex][0], classArray[teamIndex][1], classArray[teamIndex][2]])
        topPlayerArray.append([playerArray[teamIndex][0], playerArray[teamIndex][1], playerArray[teamIndex][2]])
        topLinkArray.append(linkArray[teamIndex])
        topTeamLinkArray.append(teamLinkArray[teamIndex])

        topTeamPoints.append(target[2].getText())
        topTeamPVA.append(target[3].getText())


        index = index + 1

        #Check if we have enough team:
        if index >= position:
            return False

    return True


def writeOutput():

    output = open("output.txt", 'w', encoding="utf-8")

    for i in range(len(teamArray)):
        #newTeam = teamArray[i] + ',' + playerArray[i][0] + ' [' + classArray[i][0] + '], ' + playerArray[i][1] + ' [' + classArray[i][1] + '], ' + playerArray[i][2] + ' [' + classArray[i][2] + '],' + "dofus.com" + teamLinkArray[i] + '\n'
        newTeam = teamArray[i] + ';' + classArray[i][0] + ';' + classArray[i][1] + ';' + classArray[i][2] + ';' + playerArray[i][0] + ';' +  playerArray[i][1] + ';' + playerArray[i][2] + ';'

        if len(topTeamPVA) > 0:
            #replace the ',' in PVA for '.' in order to export it:
            topTeamPVA[i] = topTeamPVA[i].replace(',' , '.')

            newTeam += str(topTeamPoints[i]) + ';' + str(topTeamPVA[i]) + ';'

        newTeam += "dofus.com" + teamLinkArray[i] + '\n'

        output.write(newTeam)

    output.close()


def writeStats():

    output = open("stats.txt", 'w', encoding="utf-8")
    print(len(teamArray))
    print()
    output.write("Nombre d'équipe: " + str(len(teamArray)) + '\n')
    sortedStats = sortStats(statsClass())

    for classe in sortedStats:
        output.write(str(classe))
        output.write("  " + str(classe[1] / (len(teamArray) * 3)))
        output.write('\n')

    output.write(str(sortStats(statsDuo())) + '\n')
    output.write(str(sortStats(statsTrio())))

    output.close()


########################################################################################################################

#Dofus cup:
#baseUrl = "https://www.dofus.com/fr/mmorpg/communaute/tournois/dofus-cup/liste-equipes?page="

#Dofus world series 2017:
#baseUrl = "https://www.dofus.com/fr/mmorpg/communaute/tournois/dws/liste-equipes?page="

#Dofus cup 2019:
baseUrl = "https://www.dofus.com/fr/mmorpg/communaute/tournois/dofus-cup-2019/liste-equipes?page="
classementUrl = "https://www.dofus.com/fr/mmorpg/communaute/tournois/dofus-cup-2019/classement?page="


computeCup(baseUrl)

topFlag = True
#computeTopCup(14, classementUrl)
computePosition(64, classementUrl)


if topFlag == True:
    teamArray = topTeamArray
    playerArray = topPlayerArray
    classArray = topClassArray
    linkArray = topLinkArray
    teamLinkArray = topTeamLinkArray

#removeForfait(
writeStats()
writeOutput()
