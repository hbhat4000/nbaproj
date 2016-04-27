rm(list=ls(all=TRUE))

load('team_subMC.RData')
load('team_pL.RData')
load('team_lineups.RData')
load('team_lineup_times.RData')
load('team_lineup_starting.RData')
# load('team_player_foul_coef2.RData')

# simulates 82 games for a team and plots time played per lineup and players for all teams

team_numSubs = list()
team_lineup_sim = list()
sim_player_times = rep(0, 492)
real_player_times = rep(0, 492)

for (team in names(team_subMC))
{
	tMC = team_subMC[[team]]
	tLU = team_lineups[[team]]
	tLT = team_lineup_times[[team]]
	tLS = team_lineup_starting[[team]]
	#mu  = mean(rowSums(hold_times[[T]]))
	tPL = team_pL[[team]][,2]

	LU_sim = rep(0,dim(tMC)[1])

	numSubs = 0
	for (i in c(1:8200))
	{
		print(paste("Game", i, "for team", team))

		state = sample(1:length(tLS), 1, prob = tLS/sum(tLS))
		T = 0
		while (T < (48*60))
		{
			trans_prob = tMC[state,-state] / tLT[state]	

			while (sum(trans_prob) == 0)
			{
				trans_prob = tMC[-state,state] / tLT[state]
				rate_prob = rexp(length(trans_prob), trans_prob)

				# hacky way of making NA values not be chosen as next state
				rate_prob[is.na(rate_prob)] = max(rate_prob[!is.na(rate_prob)]) + 1

				stateN = which.min(rate_prob)
				if (stateN >= state)
                    stateN = stateN + 1
                state = stateN

                trans_prob = tMC[state,-state] / tLT[state]	
			}

			#T = T + rexp(mu)
			rate_prob = rexp(length(trans_prob), trans_prob)
			rate_prob[is.na(rate_prob)] = max(rate_prob[!is.na(rate_prob)]) + 1

			T = T + min(rate_prob)
			stateN = which.min(rate_prob)
			if (stateN >= state)
				stateN = stateN + 1
			
			LU_sim[state] = LU_sim[state] + min(rate_prob)			
			#for (j in c(1:5))
			#{
			#	sim_player_times[tLU[state,j]] = sim_player_times[tLU[state,j]] + min(rate_prob)
			#}

			state = stateN
			numSubs = numSubs + 1
		}
	}

	for (i in c(1:dim(tLU)[1]))
	{
		for (p in tLU[i,])
		{
			real_player_times[p] = real_player_times[p] + tLT[i]
		}
	}


	team_numSubs[[team]] = numSubs/100
	team_lineup_sim[[team]] = LU_sim/100
}

for (team in names(team_lineups))
{
	tLU = team_lineups[[team]]
	tLT = team_lineup_sim[[team]]

	for (i in c(1:dim(tLU)[1]))
	{
		for (p in tLU[i,])
		{
			sim_player_times[p] = sim_player_times[p] + tLT[i]
		}
	}
}

save(team_numSubs, file = 'team_numSubs.RData')
save(team_lineup_sim, file = 'team_lineup_sim.RData')
save(sim_player_times, file = 'sim_player_times.RData')
save(real_player_times, file = 'real_player_times.RData')

real = unlist(team_lineup_times)
simulated = unlist(team_lineup_sim)
png("lineups_sim.png")
plot(log(simulated), log(real), main="lineups", xlab="simulated playing time", ylab="true playing time")
abline(0,1,col='red')
dev.off()


png("player_sim.png")
plot(sim_player_times, real_player_times, main="players", xlab="simulated playing time", ylab="true playing time")
abline(0,1,col='red')
dev.off()

