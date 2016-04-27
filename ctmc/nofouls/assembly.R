# order to recreate things for the substitution CTMC model

source('basicDF.R')
# as inputs, this needs rawdata.csv and pL.csv
# as outputs, creates the follwing:
# - basicDF.RData
# - teams.RData
# - matchups.RData
# - team_pL.RData
# - team_obs.RData

source('basicCounting.R')
# as inputs, this needs above 5 .RData files
# as outputs, creates the following:
# - times_starting.RData
# - times_sub_in.RData
# - times_sub_out.RData
# - player_transitions.RData

source('subMC.R')
# now we move to mc_old/subMC.R
# as inputs, this needs team_obs.RData and team_pL.RData
# as outputs, creates the following:
# - team_subMC.RData
# - team_lineups.RData
# - team_lineup_times.RData

source('myRidge.R')
# now we move to mc_old/myRidge.R
# as inputs, this needs team_obs.RData and team_lineups.RData
# as outputs, creates the following:
# - team_lineup_coef.RData
# - team_lineup_starting.RData

source('sim_sub.R')
# now we move to mc_old/sim_sub.R
# as inputs, this needs the following:
# - team_subMC.RData
# - team_pL.RData
# - team_lineups.RData
# - team_lineup_times.RData
# - team_lineup_starting.RData
# as outputs, this creates the following:
# - team_numSubs.RData
# - team_lineup_sim.RData
# - sim_player_times.RData
# - real_player_times.RData
# - lineups_sim.png
# - player_sim.png


