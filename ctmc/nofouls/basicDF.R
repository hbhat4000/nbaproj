rm(list=ls(all=TRUE))

basicDF = read.csv('./rawdata.csv',header=FALSE,stringsAsFactors=FALSE)
names(basicDF) = c("rawdate","Hteam","Vteam","H1","H2","H3","H4","H5","V1","V2","V3","V4","V5","timePlayed","SO","SI","F_SO","F_SI","Hevents","Vevents","Tevents","Hscore","Vscore","scoreDiff","FH1","FH2","FH3","FH4","FH5","FV1","FV2","FV3","FV4","FV5","homeFcommitted","homeFreceived","visitFcommitted","visitFreceived")
save(basicDF,file='basicDF.RData')

# players with more than one team have "T1,T2,..." as team list instead of T1,T2,...
pL = read.csv('./pL2016.csv',header=FALSE,stringsAsFactors=FALSE)

matchups = basicDF[,2:3]
teams = unique(basicDF[,2])
save(teams,file='teams.RData')
save(matchups,file='matchups.RData')

team_pL = list()
team_col = strsplit(pL[,3],",")
for (i in teams)
{
	# team pL
    rows = unlist(lapply(team_col, function(x) (i %in% x)))
	tmp1 = pL[rows,1]
	tmp2 = pL[rows,2]
	team_pL[[i]] = data.frame(tmp1,tmp2)
}
save(team_pL,file='team_pL.RData')

team_obs = list()
for (i in teams)
{
	t_obs_i = c(which(matchups[,1] == i), which(matchups[,2] == i))
	t_obs = basicDF[t_obs_i,]
	team_obs[[i]] = list(t_obs,t_obs_i)
}
save(team_obs,file='team_obs.RData')

