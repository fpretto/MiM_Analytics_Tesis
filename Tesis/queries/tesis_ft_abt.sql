SELECT 
-- Match Info
	 matches.country_name,
	 matches.country_code,
	 matches.league_id,
	 matches.league_name,
	 matches.league_type,
	 matches.league_season,
	 matches.league_round,
	 matches.league_round_number,
	 matches.fixture_id,
	 matches.referee,
	 matches.date_tz,
	 matches.date_match,
	 matches.time_match,
	 matches.venue_id,
	 matches.teams_home_id,
	 matches.teams_home_name,
	 matches.teams_away_id,
	 matches.teams_away_name,
	 matches.target,
-- Form
	home_form.form AS home_form,
	home_form.points_won_pct_l5 AS home_points_won_l5,
	home_form.form AS home_ha_form,
	home_form.ha_form AS home_ha_points_won_l5,
	away_form.ha_points_won_pct_l5 AS away_form,
	away_form.points_won_pct_l5 AS away_points_won_l5,
	away_form.ha_form AS away_ha_form,
	away_form.ha_points_won_pct_l5 AS away_ha_points_won_l5,
	
-- Match History (Home)
	 home_stats.matches_hist_cnt AS home_matches_cnt,
	 away_stats.matches_hist_cnt AS away_matches_cnt,
	 home_stats.shots_on_goal_l5 AS home_shots_on_goal_l5,
	 home_stats.shots_off_goal_l5 AS home_shots_off_goal_l5,
	 home_stats.total_shots_l5 AS home_total_shots_l5,
	 home_stats.blocked_shots_l5 AS home_blocked_shots_l5,
	 home_stats.shots_insidebox_l5 AS home_shots_insidebox_l5,
	 home_stats.shots_outsidebox_l5 AS home_shots_outsidebox_l5,
	 home_stats.fouls_l5 AS home_fouls_l5,
	 home_stats.corner_kicks_l5 AS home_corner_kicks_l5,
	 home_stats.offsides_l5 AS home_offsides_l5,
	 home_stats.ball_possesion_l5 AS home_ball_possesion_l5,
	 home_stats.yellow_cards_l5 AS home_yellow_cards_l5,
	 home_stats.red_cards_l5 AS home_red_cards_l5,
	 home_stats.goalkeeper_saves_l5 AS home_gk_saves_l5,
	 home_stats.total_passes_l5 AS home_total_passes_l5,
	 home_stats.passes_accurate_l5 AS home_passes_acc_l5,
	 home_stats.passes_pct_l5 AS home_passes_pct_l5,
	 home_stats.fouls_opp_l5 AS home_fouls_opp_l5,
	 home_stats.yellow_cards_opp_l5 AS home_yellow_cards_opp_l5,
	 home_stats.red_cards_opp_l5 AS home_red_cards_opp_l5,
	 home_stats.total_shots_opp_l5 AS home_total_shots_opp_l5,
	 home_stats.shots_on_goal_opp_l5 AS home_shots_on_goal_opp_l5,
	 home_stats.shots_off_goal_opp_l5 AS home_shots_off_goal_opp_l5,
	 home_stats.shots_insidebox_opp_l5 AS home_shots_outsidebox_opp_l5,
	 home_stats.blocked_shots_opp_l5 AS home_blocked_shots_opp_l5,
	 home_stats.corner_kicks_opp_l5 AS home_corner_kicks_opp_l5,
-- Match History (Away)
	 away_stats.shots_on_goal_l5 AS away_shots_on_goal_l5,
	 away_stats.shots_off_goal_l5 AS away_shots_off_goal_l5,
	 away_stats.total_shots_l5 AS away_total_shots_l5,
	 away_stats.blocked_shots_l5 AS away_blocked_shots_l5,
	 away_stats.shots_insidebox_l5 AS away_shots_insidebox_l5,
	 away_stats.shots_outsidebox_l5 AS away_shots_outsidebox_l5,
	 away_stats.fouls_l5 AS away_fouls_l5,
	 away_stats.corner_kicks_l5 AS away_corner_kicks_l5,
	 away_stats.offsides_l5 AS away_offsides_l5,
	 away_stats.ball_possesion_l5 AS away_ball_possesion_l5,
	 away_stats.yellow_cards_l5 AS away_yellow_cards_l5,
	 away_stats.red_cards_l5 AS away_red_cards_l5,
	 away_stats.goalkeeper_saves_l5 AS away_gk_saves_l5,
	 away_stats.total_passes_l5 AS away_total_passes_l5,
	 away_stats.passes_accurate_l5 AS away_passes_acc_l5,
	 away_stats.passes_pct_l5 AS away_passes_pct_l5,
	 away_stats.fouls_opp_l5 AS away_fouls_opp_l5,
	 away_stats.yellow_cards_opp_l5 AS away_yellow_cards_opp_l5,
	 away_stats.red_cards_opp_l5 AS away_red_cards_opp_l5,
	 away_stats.total_shots_opp_l5 AS away_total_shots_opp_l5,
	 away_stats.shots_on_goal_opp_l5 AS away_shots_on_goal_opp_l5,
	 away_stats.shots_off_goal_opp_l5 AS away_shots_off_goal_opp_l5,
	 away_stats.shots_insidebox_opp_l5 AS away_shots_outsidebox_opp_l5,
	 away_stats.blocked_shots_opp_l5 AS away_blocked_shots_opp_l5,
	 away_stats.corner_kicks_opp_l5 AS away_corner_kicks_opp_l5
	 	 


FROM fdm.tesis_ft_matches AS matches
LEFT JOIN (SELECT * FROM fdm.tesis_lk_match_stats WHERE fl_home=true) AS home_stats
	ON matches.fixture_id=home_stats.fixture_id
LEFT JOIN (SELECT * FROM fdm.tesis_lk_match_stats WHERE fl_home=false) AS away_stats
	ON matches.fixture_id=away_stats.fixture_id
LEFT JOIN (SELECT * FROM fdm.tesis_lk_past_performance WHERE home_away='Home') AS home_form
	ON matches.fixture_id=home_form.fixture_id
LEFT JOIN (SELECT * FROM fdm.tesis_lk_past_performance WHERE home_away='Away') AS away_form
	ON matches.fixture_id=away_form.fixture_id
-- agregar stats de home y away

--SELECT * FROM fdm.tesis_lk_past_performance
--order by league_id, league_season, fixture_id