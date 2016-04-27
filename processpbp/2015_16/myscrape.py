#!/usr/bin/python
import os
import csv
import string
import numpy
import pickle
import time

from bs4 import BeautifulSoup
from bs4 import Comment

playerDict = {}
playerDict['Jose Barea'] = 'J.J. Barea'
playerDict['Tim Hardaway'] = 'Tim Hardaway Jr.'
playerDict['Luc Mbah a Moute'] = 'Luc Richard Mbah a Moute'
playerDict['JaKarr Sampson'] = 'Jakarr Sampson'
playerDict['Patrick Mills'] = 'Patty Mills'
playerDict['Glen Rice'] = 'Glen Rice Jr.'
playerDict['Larry Drew'] = 'Larry Drew II'
playerDict['John Lucas'] = 'John Lucas III'
playerDict['Glenn Robinson'] = 'Glenn Robinson III'
playerDict['Louis Williams'] = 'Lou Williams'
playerDict['Roy Devyn Marble'] = 'Devyn Marble'

teamTable={}
teamTable['Atlanta Hawks']='Atl'       
teamTable['Brooklyn Nets']='Bkn'
teamTable['Boston Celtics']='Bos'
teamTable['Charlotte Hornets']='Cha'
teamTable['Chicago Bulls']='Chi'
teamTable['Cleveland Cavaliers']='Cle'
teamTable['Dallas Mavericks']='Dal'
teamTable['Denver Nuggets']='Den'
teamTable['Detroit Pistons']='Det'
teamTable['Golden State Warriors']='GS'
teamTable['Houston Rockets']='Hou'
teamTable['Indiana Pacers']='Ind'
teamTable['Los Angeles Clippers']='LAC'
teamTable['Los Angeles Lakers']='LAL'
teamTable['Memphis Grizzlies']='Mem'     
teamTable['Miami Heat']='Mia'
teamTable['Milwaukee Bucks']='Mil'
teamTable['Minnesota Timberwolves']='Min'
teamTable['New Orleans Pelicans']='NO'
teamTable['New York Knicks']='NY'        
teamTable['Oklahoma City Thunder']='OKC' 
teamTable['Orlando Magic']='Orl'         
teamTable['Philadelphia 76ers']='Phi'    
teamTable['Phoenix Suns']='Pho'          
teamTable['Portland Trail Blazers']='Por'
teamTable['Sacramento Kings']='Sac'      
teamTable['San Antonio Spurs']='SA'      
teamTable['Toronto Raptors']='Tor'       
teamTable['Utah Jazz']='Uta'             
teamTable['Washington Wizards']='Was'

teamdict={}
teamdict['01']='ATL'
teamdict['02']='BOS'
teamdict['03']='NOP'
teamdict['04']='CHI'
teamdict['05']='CLE'
teamdict['06']='DAL'
teamdict['07']='DEN'
teamdict['08']='DET'
teamdict['09']='GSW'
teamdict['10']='HOU'
teamdict['11']='IND'
teamdict['12']='LAC'
teamdict['13']='LAL'
teamdict['14']='MIA'
teamdict['15']='MIL'
teamdict['16']='MIN'
teamdict['17']='BRK'
teamdict['18']='NYK'
teamdict['19']='ORL'
teamdict['20']='PHI'
teamdict['21']='PHO'
teamdict['22']='POR'
teamdict['23']='SAC'
teamdict['24']='SAS'
teamdict['25']='OKC'
teamdict['26']='UTA'
teamdict['27']='WAS'
teamdict['28']='TOR'
teamdict['29']='MEM'
teamdict['30']='CHO'

teamlist={}
teamlist['ATL']='Atl'
teamlist['BOS']='Bos'
teamlist['NOP']='NO'
teamlist['CHI']='Chi'
teamlist['CLE']='Cle'
teamlist['DAL']='Dal'
teamlist['DEN']='Den'
teamlist['DET']='Det'
teamlist['GSW']='GS'
teamlist['HOU']='Hou'
teamlist['IND']='Ind'
teamlist['LAC']='LAC'
teamlist['LAL']='LAL'
teamlist['MIA']='Mia'
teamlist['MIL']='Mil'
teamlist['MIN']='Min'
teamlist['BRK']='Bkn'
teamlist['NYK']='NY'
teamlist['ORL']='Orl'
teamlist['PHI']='Phi'
teamlist['PHO']='Pho'
teamlist['POR']='Por'
teamlist['SAC']='Sac'
teamlist['SAS']='SA'
teamlist['OKC']='OKC'
teamlist['UTA']='Uta'
teamlist['WAS']='Was'
teamlist['TOR']='Tor'
teamlist['MEM']='Mem'
teamlist['CHO']='Cha'

# calculates time played for an observation
def getTimeDiff(cur, past, quarter):
    cur = int(cur[:cur.index(':')])*60 + (60*(4 - quarter)*12) + int(cur[cur.index(':')+1:])
    past = int(past[0][:past[0].index(':')])*60 + (60*(4 - past[1])*12) + int(past[0][past[0].index(':')+1:])
    return(past-cur)

# every new quarter, get new starting lineup
def checkObs(quarter, pmTable):
    quarter -= 1
    teamTag = pmTable.div 
    obs = {}
    while teamTag:
        team = teamTable[teamTag.div.string.encode("ascii","ignore")]
        obs[team] = []
        sizes = teamTag.div.next_sibling.next_sibling.div
        sizeList = []
        while sizes:
            style = sizes['style']
            sizeList.append(int(style[style.index(':')+1:style.index('px')]))
            sizes = sizes.next_sibling.next_sibling
        playerTag = teamTag.div.next_sibling.next_sibling.next_sibling.next_sibling
        while playerTag:
            thisCheck = 7
            for i in range(0,quarter):
                thisCheck += sizeList[i]    
            startCheck = playerTag.next_sibling.next_sibling.div
            checker1 = 0
            checker2 = 0
            tmp1Start = startCheck
            tmp2Start = startCheck
            while checker1 < thisCheck-6:
                style = tmp1Start['style']
                checker1 += int(style[style.index(':')+1:style.index('px')])
                toCheck1 = tmp1Start
                tmp1Start = tmp1Start.next_sibling.next_sibling
            while checker2 < thisCheck:
                style = tmp2Start['style']
                checker2 += int(style[style.index(':')+1:style.index('px')])
                toCheck2 = tmp2Start
                tmp2Start = tmp2Start.next_sibling.next_sibling
            if toCheck1.string.encode("ascii","ignore") != '' or toCheck2.string.encode("ascii","ignore") != '':
                tmpPlayer = playerTag.span.string.encode("ascii","ignore")
                if tmpPlayer in playerDict:
                    tmpPlayer = playerDict[tmpPlayer]
                obs[team].append(playerList[tmpPlayer][0][0])
            playerTag = playerTag.next_sibling.next_sibling.next_sibling.next_sibling
        teamTag = teamTag.next_sibling.next_sibling
    return obs

playerList = pickle.load(open('./uniquePlayerList2016.pickle','rb'))
dirList = os.listdir('/home/hbhat/Dropbox/nbaproj/fixedpbpfiles2016/')

for htmlFile in dirList:
    print "Starting: ",htmlFile
    # get pmFile
    rawdate = htmlFile[:htmlFile.index('.')-2]
    hometeam = teamdict[htmlFile[htmlFile.index('.')-2:htmlFile.index('.')]]
    Hteam = teamlist[hometeam]
    Vteam = ""
    pmFile = BeautifulSoup(open('/home/hbhat/Dropbox/nbaproj/pmFiles2016/' + rawdate + hometeam + ".html"),"html.parser") 
    pmTable = pmFile.body.div.div.next_sibling.next_sibling.next_sibling.next_sibling.table.tr.td.div.next_sibling.div.next_sibling.next_sibling
    # get pbpFile
    fullfile = open('/home/hbhat/Dropbox/nbaproj/fixedpbpfiles2016/'+htmlFile)
    alllines = fullfile.read()
    ffstart = alllines.find('<!--START SHORT PBP')
    ffalmostend = alllines.find('TITLE TEAMS')
    keepGoing = True
    while (keepGoing):
        ffalmostend += 1
        if (alllines[ffalmostend] == '>'):
            keepGoing = False

    ffend = ffalmostend + 1
    myhtmlfile = alllines[ffstart:ffend]

    soup = BeautifulSoup(myhtmlfile,"html.parser")
    diff = (0,0)
    time = ("12:00",1)
    tmpObs = {}
    obs = {} 
    fouls = {}
    foulsLineup = {}
    nEvents = {}
    tEvents = 0
    upsideDownFlag = 0
    startTag = soup.tr.next_sibling.next_sibling
    topQuarter = startTag.td.string.encode("ascii","ignore")
    # if pbp is upsideDown
    if topQuarter != "1":
        upsideDownFlag = 1
        while startTag.next_sibling:
            startTag = startTag.next_sibling 
        topQuarter = startTag.td.string.encode("ascii","ignore")
    topQuarter = int(topQuarter)
    pbpTag = ""
    # checks required for starting lineup parsing
    if upsideDownFlag == 0:
        if "Starting Lineup" in startTag.td.next_sibling.next_sibling.next_sibling.string.encode("ascii","ignore"):
            checker = 1
        else:
            checker = 0
    else:
        if "Start of the 1st Quarter" not in startTag.td.next_sibling.next_sibling.next_sibling.string.encode("ascii","ignore"):
            checker = 1
        else:
            checker = 0
    # start parsing starting lineup
    while checker:
        tempTag = startTag.td.next_sibling.next_sibling
        team = tempTag.string.encode("ascii","ignore")
        # if unwanted tag move to next line and update checker
        if team == 'Team':
            if upsideDownFlag == 0:
                startTag = startTag.next_sibling
            else:
                startTag = startTag.previous_sibling
            # update checker
            if upsideDownFlag == 0:
                if "Starting Lineup" in startTag.td.next_sibling.next_sibling.next_sibling.string.encode("ascii","ignore"):
                    checker = 1
                else:
                    checker = 0
            else:
                if "Start of the 1st Quarter" not in startTag.td.next_sibling.next_sibling.next_sibling.string.encode("ascii","ignore"):
                    checker = 1
                else:
                    checker = 0
            continue    
        if team not in nEvents:
            if team != Hteam:
                Vteam = team
            obs[team] = []
            nEvents[team] = 0
        temp = tempTag.next_sibling.string.encode("ascii","ignore")
        # if starting lineup add player to obs
        if "Starting Lineup" in temp:
            player = temp[temp.index('-')+2:]
            obs[team].append(playerList[player][0][0])
        # move to next line
        if upsideDownFlag == 0:
            startTag = startTag.next_sibling
        else:
            startTag = startTag.previous_sibling
        # if unwanted tag
        if startTag.a:
            break
        # update checker
        if upsideDownFlag == 0:
            if "Starting Lineup" in startTag.td.next_sibling.next_sibling.next_sibling.string.encode("ascii","ignore"):
                checker = 1
            else:
                checker = 0
        else:
            if "Start of the 1st Quarter" not in startTag.td.next_sibling.next_sibling.next_sibling.string.encode("ascii","ignore"):
                checker = 1
            else:
                checker = 0
    # move to Start of 1st Quarter line
    if upsideDownFlag == 0:
        pbpTag = startTag.next_sibling.next_sibling
    else:
        pbpTag = startTag
    timeDiff = 0
    quarter = 1
    fouls[Hteam] = {}
    fouls[Vteam] = {}
    for ii in obs:
        for jj in obs[ii]:
            fouls[ii][jj] = 0
    # fouls commited, fouls recieved
    foulsLineup[Hteam] = [0, 0]
    foulsLineup[Vteam] = [0, 0]
    # start pbp parser
    while pbpTag:
        # if Comment tag in pbp
        #print pbpTag
        if type(pbpTag) is Comment:
            if upsideDownFlag == 0:
                pbpTag = pbpTag.next_sibling 
            else:
                pbpTag = pbpTag.previous_sibling
            continue
        # if unwanted tag in pbp
        if pbpTag.a:
            if upsideDownFlag == 0:
                pbpTag = pbpTag.next_sibling 
            else:
                pbpTag = pbpTag.previous_sibling
            continue
        thisCall = pbpTag.td.next_sibling.next_sibling.next_sibling.string.encode("ascii","ignore")
        # record team1
        if "Start of the 1st Quarter" in thisCall:
            team1 = pbpTag.td.next_sibling.next_sibling.string.encode("ascii","ignore")
        # game ends and break
        if "End of Game" in thisCall:
            # when game ends, record obs
            timeDiff = getTimeDiff("00:00",time,quarter)
            scoreDiff = 0
            #if timeDiff != 0:
	    score2 = int(pbpTag.td.next_sibling.next_sibling.next_sibling.next_sibling.string.encode("ascii","ignore"))
	    score1 = int(pbpTag.td.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.string.encode("ascii","ignore"))
	    pscore1 = diff[0]
	    pscore2 = diff[1]
	    scoreDiff = (score1-pscore1)-(score2-pscore2)
	    with open('rawdata.csv','a') as outfile:
	        rowWriter = csv.writer(outfile,delimiter=',')
	        rowWriter.writerow([rawdate,Hteam,Vteam,obs[Hteam][0],obs[Hteam][1],obs[Hteam][2],obs[Hteam][3],obs[Hteam][4],obs[Vteam][0],obs[Vteam][1],obs[Vteam][2],obs[Vteam][3],obs[Vteam][4],timeDiff,0,0,-1,-1,nEvents[Hteam],nEvents[Vteam],tEvents,score1,score2,scoreDiff,fouls[Hteam][obs[Hteam][0]],fouls[Hteam][obs[Hteam][1]],fouls[Hteam][obs[Hteam][2]],fouls[Hteam][obs[Hteam][3]],fouls[Hteam][obs[Hteam][4]],fouls[Vteam][obs[Vteam][0]],fouls[Vteam][obs[Vteam][1]],fouls[Vteam][obs[Vteam][2]],fouls[Vteam][obs[Vteam][3]],fouls[Vteam][obs[Vteam][4]],foulsLineup[Hteam][0],foulsLineup[Hteam][1],foulsLineup[Vteam][0],foulsLineup[Vteam][1]])
            break
        # if unwanted tag in pbp
        if "Event" in thisCall:
            if upsideDownFlag == 0:
                pbpTag = pbpTag.next_sibling 
            else:
                pbpTag = pbpTag.previous_sibling
            continue
        thisQuarter = pbpTag.td.string.encode("ascii","ignore")
        if "OT" in thisQuarter:
            if thisQuarter == "OT":
                thisQuarter = 5
            else:
                thisQuarter = 4 + int(thisQuarter[:thisQuarter.index('OT')])
        thisQuarter = int(thisQuarter)
        thisTime = pbpTag.td.next_sibling.string.encode("ascii","ignore")
        thisTeam = pbpTag.td.next_sibling.next_sibling.string.encode("ascii","ignore")
        # update quarter and check player roster
        if quarter != thisQuarter:
            quarter = thisQuarter
            tmpObs = checkObs(quarter, pmTable)
            # if player roster has changed, record obs and update
            if tmpObs != obs:
                timeDiff = getTimeDiff("12:00",time,quarter)
                time = ("12:00",quarter)
                scoreDiff = 0
                #if timeDiff != 0:
                score2 = int(pbpTag.td.next_sibling.next_sibling.next_sibling.next_sibling.string.encode("ascii","ignore"))
                score1 = int(pbpTag.td.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.string.encode("ascii","ignore"))
                pscore1 = diff[0]
                pscore2 = diff[1]
                scoreDiff = (score1-pscore1)-(score2-pscore2)
                diff = (score1,score2)
                with open('rawdata.csv','a') as outfile:
                    rowWriter = csv.writer(outfile,delimiter=',')
                    rowWriter.writerow([rawdate,Hteam,Vteam,obs[Hteam][0],obs[Hteam][1],obs[Hteam][2],obs[Hteam][3],obs[Hteam][4],obs[Vteam][0],obs[Vteam][1],obs[Vteam][2],obs[Vteam][3],obs[Vteam][4],timeDiff,0,0,-1,-1,nEvents[Hteam],nEvents[Vteam],tEvents,score1,score2,scoreDiff,fouls[Hteam][obs[Hteam][0]],fouls[Hteam][obs[Hteam][1]],fouls[Hteam][obs[Hteam][2]],fouls[Hteam][obs[Hteam][3]],fouls[Hteam][obs[Hteam][4]],fouls[Vteam][obs[Vteam][0]],fouls[Vteam][obs[Vteam][1]],fouls[Vteam][obs[Vteam][2]],fouls[Vteam][obs[Vteam][3]],fouls[Vteam][obs[Vteam][4]],foulsLineup[Hteam][0],foulsLineup[Hteam][1],foulsLineup[Vteam][0],foulsLineup[Vteam][1]])
                if tmpObs[Hteam] != obs[Hteam]:
                    nEvents[Hteam] = 0
		    foulsLineup[Hteam] = [0, 0]
                if tmpObs[Vteam] != obs[Vteam]:
                    nEvents[Vteam] = 0
		    foulsLineup[Vteam] = [0, 0]
                tEvents = 0
                obs = tmpObs
                for ii in obs:
		    if len(obs[ii]) != 5:
			print 'BREAKING ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ'
                    for jj in obs[ii]:
                        if jj not in fouls[ii]:
                            fouls[ii][jj] = 0
	# track fouls commited by players
	if 'foul committed by ' in thisCall:
	    #print thisCall
            tmppPlayer = thisCall[thisCall.index('by ')+3:len(thisCall)-1]
            if tmppPlayer in playerDict:
                tmppPlayer = playerDict[tmppPlayer]
	    try:
	        tmpPlayer = playerList[tmppPlayer][0][0]
	        fouls[thisTeam][tmpPlayer] += 1
	    except KeyError:
		print tmppPlayer
	    if thisTeam == Hteam:
		foulsLineup[Hteam][0] += 1
		foulsLineup[Vteam][1] += 1
	    else:
		foulsLineup[Hteam][1] += 1
		foulsLineup[Vteam][0] += 1
        # Substitution: record obs and create new obs to record
        if "Substitution: " in thisCall:
            playerIN = thisCall[thisCall.index(': ')+2:thisCall.index(' in ')]
            if playerIN in playerDict:
                playerIN = playerDict[playerIN]
            playerOUT = thisCall[thisCall.index(' for ')+5:len(thisCall)-1]
            if playerList[playerIN][0][0] not in obs[thisTeam]:
                timeDiff = getTimeDiff(thisTime,time,quarter)
                time = (thisTime,quarter)
                scoreDiff = 0
                #if timeDiff != 0:
                score2 = int(pbpTag.td.next_sibling.next_sibling.next_sibling.next_sibling.string.encode("ascii","ignore"))
                score1 = int(pbpTag.td.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.string.encode("ascii","ignore"))
                pscore1 = diff[0]
                pscore2 = diff[1]
                scoreDiff = (score1-pscore1)-(score2-pscore2)
                diff = (score1,score2)
		if playerList[playerIN][0][0] not in fouls[thisTeam]:
                    fouls[thisTeam][playerList[playerIN][0][0]] = 0
                with open('rawdata.csv','a') as outfile:
                    rowWriter = csv.writer(outfile,delimiter=',')
                    rowWriter.writerow([rawdate,Hteam,Vteam,obs[Hteam][0],obs[Hteam][1],obs[Hteam][2],obs[Hteam][3],obs[Hteam][4],obs[Vteam][0],obs[Vteam][1],obs[Vteam][2],obs[Vteam][3],obs[Vteam][4],timeDiff,playerList[playerOUT][0][0],playerList[playerIN][0][0],fouls[thisTeam][playerList[playerOUT][0][0]],fouls[thisTeam][playerList[playerIN][0][0]],nEvents[Hteam],nEvents[Vteam],tEvents,score1,score2,scoreDiff,fouls[Hteam][obs[Hteam][0]],fouls[Hteam][obs[Hteam][1]],fouls[Hteam][obs[Hteam][2]],fouls[Hteam][obs[Hteam][3]],fouls[Hteam][obs[Hteam][4]],fouls[Vteam][obs[Vteam][0]],fouls[Vteam][obs[Vteam][1]],fouls[Vteam][obs[Vteam][2]],fouls[Vteam][obs[Vteam][3]],fouls[Vteam][obs[Vteam][4]],foulsLineup[Hteam][0],foulsLineup[Hteam][1],foulsLineup[Vteam][0],foulsLineup[Vteam][1]])
                nEvents[thisTeam] = 0
		foulsLineup[thisTeam] = [0, 0]
                tEvents = 0
                obs[thisTeam].insert(obs[thisTeam].index(playerList[playerOUT][0][0]),playerList[playerIN][0][0])
		obs[thisTeam].remove(playerList[playerOUT][0][0])
            else:
                f = open('mismatch6.txt','ab')
                string = htmlFile + ", " + thisCall + "\n"
                f.write(string)
        if "Substitution: " not in thisCall and "Start of the " not in thisCall and "End of the " not in thisCall and "Event" not in thisCall and "timeout" not in thisCall:
            nEvents[thisTeam] += 1
            tEvents += 1
        # if upsideDown
        if upsideDownFlag == 0:
            pbpTag = pbpTag.next_sibling 
        else:
            pbpTag = pbpTag.previous_sibling
