import pickle
import sys

upl = pickle.load(open('uniquePlayerList2016.pickle','rb'))
for player in upl.keys():
    sys.stdout.write(player+","+str(upl[player][0][0]))
    for team in upl[player]:
        sys.stdout.write(","+team[1])

    sys.stdout.write("\n")

