#!/usr/bin/python
import pickle
import pandas

oldteam = {}
oldteam['ATL']='Atl'
oldteam['BOS']='Bos'
oldteam['BRK']='Bkn'
oldteam['CHI']='Chi'
oldteam['CHO']='Cha'
oldteam['CLE']='Cle'
oldteam['DAL']='Dal'
oldteam['DEN']='Den'
oldteam['DET']='Det'
oldteam['GSW']='GS'
oldteam['HOU']='Hou'
oldteam['IND']='Ind'
oldteam['LAC']='LAC'
oldteam['LAL']='LAL'
oldteam['MEM']='Mem'
oldteam['MIA']='Mia'
oldteam['MIL']='Mil'
oldteam['MIN']='Min'
oldteam['NOP']='NO'
oldteam['NYK']='NY'
oldteam['OKC']='OKC'
oldteam['ORL']='Orl'
oldteam['PHI']='Phi'
oldteam['PHO']='Pho'
oldteam['POR']='Por'
oldteam['SAC']='Sac'
oldteam['SAS']='SA'
oldteam['TOR']='Tor'
oldteam['UTA']='Uta'
oldteam['WAS']='Was'

df = pandas.read_csv('nba2016.csv')
playerdict = {}
playernum = 0
for i in range(df.shape[0]):
    thisrow = df.iloc[i]
    if thisrow['Player'] not in playerdict.keys():
        playerdict[thisrow['Player']] = []
        playernum += 1

    if thisrow['Tm'] != 'TOT':
        playerdict[thisrow['Player']].append((playernum,oldteam[thisrow['Tm']]))


# This dude played in China during the regular season,
# and then joined the Miami Heat for the playoffs!
playerdict['Dorell Wright'] = []
playerdict['Dorell Wright'].append((playernum,'Mia'))
playernum += 1

# This dude played in the D-Leagues all season,
# and then joined the Boston Celtics for the playoffs!
playerdict['John Holland'] = []
playerdict['John Holland'].append((playernum,'Bos'))
playernum += 1

pickle.dump(playerdict, open("uniquePlayerList2016.pickle","wb"))


