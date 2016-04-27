rm(list=ls(all=TRUE))

load('basicDF.RData')
load('teams.RData')
load('matchups.RData')
load('team_obs.RData')
load('team_pL.RData')

player_transitions = list()
 
times_starting = list()
times_sub_in = list()
times_sub_out = list()

for (teamT in teams)
{
	T = team_obs[[teamT]]
	T_pL = team_pL[[teamT]]

	# rows: subbed in	cols: subbed out
	player_transitions_t = matrix(0, length(unique(T_pL[,2])), length(unique(T_pL[,2])))

	times_starting_t = data.frame()
	times_sub_in_t = data.frame()
	times_sub_out_t = data.frame()

	# for every player in a team
	for (i in unique(T_pL[,2]))
	{
		tmp_V1 = c(i,0)
		tmp_V2 = c(i,0)
		tmp_V3 = c(i,0)

		# check if subbed in
		tmp_V2[2] = length(which(T[[1]][,"SI"] == i))
		tmp_V3[3] = length(which(T[[1]][,"SO"] == i))

		tmp = which(T[[1]][,"SO"] == i)
		for (j in tmp)
		{
			k = T[[1]][j,'SI']
			player_transitions_t[which(unique(T_pL[,2]) == k), which(unique(T_pL[,2]) == i)] = player_transitions_t[which(unique(T_pL[,2]) == k), which(unique(T_pL[,2]) == i)] + 1		
		}

		#tmp1 = sort(c(which(i == T[[1]]$H1), which(i == T[[1]]$H2), which(i == T[[1]]$H3), which(i == T[[1]]$H4), which(i == T[[1]]$H5), which(i == T[[1]]$V1), which(i == T[[1]]$V2), which(i == T[[1]]$V3), which(i == T[[1]]$V4), which(i == T[[1]]$V5)))
		tmp = c(1:dim(T[[1]])[1])[apply(T[[1]][,4:13], 1, function (x) (i %in% x) )]

		for (j in tmp)
		{
			# check if in starting lineup
			if (j == 1)
			{	
				tmp_V1[2] = tmp_V1[2] + 1
			}
			else if (T[[1]]$rawdate[j-1] != T[[1]]$rawdate[j])
			{
				tmp_V1[2] = tmp_V1[2] + 1
			}
			# check if subbed in
			else if (!((j-1) %in% tmp) && T[[1]]$SI[j-1] == 0)
			{
				tmp_V2[2] = tmp_V2[2] + 1
			}
			
			# check if subbed out (first check if not at end of T[[1]] object)
			if (!is.na(T[[1]]$rawdate[j+1]))
			{
				if (T[[1]]$rawdate[j] == T[[1]]$rawdate[j+1])
				{
					if (!((j+1) %in% tmp))
					{
						if (T[[1]]$SO[j] == 0)
						{
							tmp_V3[2] = tmp_V3[2] + 1
						}
					}
				}
			}
		}

		times_starting_t = rbind(times_starting_t,tmp_V1)
		times_sub_in_t = rbind(times_sub_in_t,tmp_V2)
		times_sub_out_t = rbind(times_sub_out_t,tmp_V3)
	}

	names(times_starting_t) = c("player", "times starting")
	names(times_sub_in_t) = c("player", "times subbed in")
	names(times_sub_out_t) = c("player", "times subbed out")

	times_starting[[teamT]] = times_starting_t
	times_sub_in[[teamT]] = times_sub_in_t
	times_sub_out[[teamT]] = times_sub_out_t

	player_transitions[[teamT]] = player_transitions_t 
}

save(times_starting,file='times_starting.RData')
save(times_sub_in,file='times_sub_in.RData')
save(times_sub_out,file='times_sub_out.RData')
save(player_transitions,file='player_transitions.RData')

