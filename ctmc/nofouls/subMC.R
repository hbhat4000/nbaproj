rm(list=ls(all=TRUE))

load("./team_obs.RData")
load("./team_pL.RData")

# creates substitution MC

team_lineups = list()
team_subMC = list()
team_lineup_times = list()

for (teamT in names(team_obs))
{
	my_T = team_obs[[teamT]][[1]]

	Hlines = which(my_T$Hteam == teamT)
	Hlines = Hlines[which(my_T[Hlines,"timePlayed"] != 0)]
	tmpDF1 = t(apply(my_T[Hlines,4:8],1,sort))

	Vlines = which(my_T$Vteam == teamT)
	Vlines = Vlines[which(my_T[Vlines,"timePlayed"] != 0)]
	tmpDF2 = t(apply(my_T[Vlines,9:13],1,sort))
	tmp_lineups = unique(rbind(tmpDF1,tmpDF2))

	team_lineups[[teamT]] = tmp_lineups
	
	n_lineups = dim(tmp_lineups)[1]
	lineup_transitions = matrix(0,n_lineups,n_lineups)
	time_lineups = rep(0,n_lineups)

	past_LU = 0
	curr_G = 0
	for (L in Hlines)
	{
		tmp = as.integer(sort(my_T[L,4:8]))
		lineup_index = which(apply(tmp_lineups,1, function(x) identical(x,tmp)))
		time_lineups[lineup_index] = time_lineups[lineup_index] + my_T[L,"timePlayed"]

		if ((curr_G == my_T[L,"rawdate"]) && (past_LU != 0) && (past_LU != lineup_index))
		{
			lineup_transitions[past_LU, lineup_index] = lineup_transitions[past_LU, lineup_index] + 1
		}

		past_LU = lineup_index
		curr_G = my_T[L,"rawdate"]
	}

	past_LU = 0
	curr_G = 0
	for (L in Vlines)
	{
		tmp = as.integer(sort(my_T[L,9:13]))
		lineup_index = which(apply(tmp_lineups,1, function(x) identical(x,tmp)))
		time_lineups[lineup_index] = time_lineups[lineup_index] + my_T[L,"timePlayed"]

		if ((curr_G == my_T[L,"rawdate"]) && (past_LU != 0) && (past_LU != lineup_index))
		{
			lineup_transitions[past_LU, lineup_index] = lineup_transitions[past_LU, lineup_index] + 1
		}

		past_LU = lineup_index
		curr_G = my_T[L,"rawdate"]
	}

	#for (i in n_lineups)
	#{
	#	lineup_transitions[i,] = lineup_transitions[i,] / time_lineups[i]
	#	lineup_transitions[i,i] = -sum(lineup_transitions[i,])
	#}

	team_lineup_times[[teamT]] = time_lineups
	team_subMC[[teamT]] = lineup_transitions
}

save(team_subMC, file = "team_subMC.RData")
save(team_lineups, file = "team_lineups.RData")
save(team_lineup_times, file = "team_lineup_times.RData")
