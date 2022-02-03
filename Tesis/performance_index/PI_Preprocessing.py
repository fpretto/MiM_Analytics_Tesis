#####################################################################################################################
#
#
# Purpose: Proceso encargado de división de train/test y filtrado de valores para ILT
# Creator: Pablo Beltramone
#
#   Inputs:
#       Analitical record:
#
#   Outputs:
#       DF train Test
#
#  Notes: NA
#######################################################################################################################

import pandas as pd
import numpy as np

######################################################################
# DATA PREPARATION & FILTER
######################################################################

def filter_and_data_engineering(df_ar, rating_correction, correct_rating=False):

    # Filter players with at least 3 matches played
    df = df_ar[(df_ar['player_minutes'] >= 270) & (df_ar['player_id'] > 0)].copy()

    ## Per 90 stats
    # Attacking
    df['offsides_p90'] = df['offsides']/df['player_minutes']*90
    df['shots_p90'] = df['shots_total']/df['player_minutes']*90
    df['shooting_accuracy'] = np.where(df['shots_total']==0, 0, np.where(df['shots_total']<df['shots_on_goal'], 1,
                                                                         df['shots_on_goal']/df['shots_total']))
    df['goals_p90'] = df['goals_total']/df['player_minutes']*90
    df['np_goals_p90'] = np.where(df['goals_total']-df['penalty_scored']<0, 0,
                                  (df['goals_total']-df['penalty_scored'])/df['player_minutes']*90)
    df['goal_conversion'] = np.where(df['shots_total']==0, 0, df['goals_total']/df['shots_total'])
    df['goal_conversion_np'] = np.where(df['shots_total']==0, 0, (df['goals_total']-df['penalty_scored'])/df['shots_total'])
    df['assists_p90'] = df['goals_assists']/df['player_minutes']*90
    df['penalty_won_p90'] = df['penalty_won']/df['player_minutes']*90
    df['penalty_missed_p90'] = df['penalty_missed']/df['player_minutes']*90

    # Build-up
    df['passes_p90'] = df['passes_total']/df['player_minutes']*90
    df['passing_accuracy'] = np.where(df['passes_total']==0, 0, df['passes_completed']/df['passes_total'])
    df['key_passes_p90'] = df['passes_key']/df['player_minutes']*90
    df['fouls_drawn_p90'] = df['fouls_drawn']/df['player_minutes']*90

    # Defense
    df['tackles_p90'] = df['tackles_total_padj']/df['player_minutes']*90
    df['blocks_p90'] = df['tackles_blocks_padj']/df['player_minutes']*90
    df['interceptions_p90'] = df['tackles_interceptions_padj']/df['player_minutes']*90
    df['saves_p90'] = df['goals_saves_padj']/df['player_minutes']*90
    df['penalty_saves_p90'] = df['penalty_saved']/df['player_minutes']*90
    df['penalty_committed_p90'] = df['penalty_committed_padj']/df['player_minutes']*90
    df['goals_conceded_p90'] = df['goals_conceded_padj']/df['player_minutes']*90
    df['shots_on_goal_opp_p90'] = df['shots_on_goal_opp_padj']/df['player_minutes']*90
    df['goals_conceded_ratio'] = df['goals_conceded_p90']/df['shots_on_goal_opp_p90']
    df['fouls_committed_p90'] = df['fouls_committed_padj']/df['player_minutes']*90

    # One vs one
    df['duels_p90'] = df['duels_total_padj']/df['player_minutes']*90
    df['duels_success_ratio'] = np.where(df['duels_total_padj']==0, 0, df['duels_won_padj']/df['duels_total_padj'])
    df['dribbles_p90'] = df['dribbles_attemps']/df['player_minutes']*90
    df['dribbles_success_ratio'] = np.where(df['dribbles_attemps']==0, 0, df['dribbles_success']/df['dribbles_attemps'])
    df['dribbles_past_p90'] = df['dribbles_past_padj']/df['player_minutes']*90

    # General
    df['cards_yellow_p90'] = df['cards_yellow']/df['player_minutes']*90
    df['cards_red_p90'] = df['cards_red']/df['player_minutes']*90

    # Combined
    df['scoring_contribution'] = df['np_goals_p90']+df['assists_p90']

    if correct_rating:
        # Fill NAs rating with ratings from the same players in other seasons
        df = df.merge(rating_correction, on=['player_id'], how='left')
        df['wavg_player_rating'] = np.where(df['wavg_player_rating_x'].isna(), df['wavg_player_rating_y'], df['wavg_player_rating_x'])
        del df['wavg_player_rating_x'], df['wavg_player_rating_y']

        # Fill NAs rating with average rating of the position in the entire dataset
        df_ratings_pos = df[['player_preferred_position', 'wavg_player_rating']].groupby(['player_preferred_position']).median().rename(
            columns={'wavg_player_rating': 'wavg_position_rating'}).reset_index()
        df = df.merge(df_ratings_pos, on=['player_preferred_position'], how='left')
        df['wavg_player_rating'] = np.where(df['wavg_player_rating'].isna(), df['wavg_position_rating'], df['wavg_player_rating'])
        del df['wavg_position_rating']

    # Unification of optimizing direction
    df['fouls_committed_p90'] = df['fouls_committed_p90']*-1
    df['dribbles_past_p90'] = df['dribbles_past_p90']*-1
    df['penalty_committed_p90'] = df['penalty_committed_p90']*-1
    df['goals_conceded_p90'] = df['goals_conceded_p90']*-1

    return df


def normalize_by_position(df, dict_cols, scaler='Robust'):

    from sklearn.preprocessing import MinMaxScaler, RobustScaler, StandardScaler

    dict_scalers = {"Robust": RobustScaler, "Standard": StandardScaler, "MinMax": MinMaxScaler}

    df_fw_0 = df[df['player_preferred_position'] == 'F'][dict_cols['player_cols'] + dict_cols['F']].copy()
    df_mf_0 = df[df['player_preferred_position'] == 'M'][dict_cols['player_cols'] + dict_cols['M']].copy()
    df_df_0 = df[df['player_preferred_position'] == 'D'][dict_cols['player_cols'] + dict_cols['D']].copy()
    df_gk_0 = df[df['player_preferred_position'] == 'G'][dict_cols['player_cols'] + dict_cols['G']].copy()

    scaler_fw = dict_scalers[scaler]()
    scaler_fw = scaler_fw.fit(df_fw_0[dict_cols['F']])
    df_fw = pd.concat([df_fw_0[dict_cols['player_cols']].reset_index(drop=True),
                       pd.DataFrame(scaler_fw.transform(df_fw_0[dict_cols['F']]),
                                    columns=dict_cols['F'])], axis=1)

    scaler_mf = dict_scalers[scaler]()
    scaler_mf = scaler_mf.fit(df_mf_0[dict_cols['M']])
    df_mf = pd.concat([df_mf_0[dict_cols['player_cols']].reset_index(drop=True),
                       pd.DataFrame(scaler_mf.transform(df_mf_0[dict_cols['M']]),
                                    columns=dict_cols['M'])], axis=1)

    scaler_df = dict_scalers[scaler]()
    scaler_df = scaler_df.fit(df_df_0[dict_cols['D']])
    df_df = pd.concat([df_df_0[dict_cols['player_cols']].reset_index(drop=True),
                       pd.DataFrame(scaler_df.transform(df_df_0[dict_cols['D']]),
                                    columns=dict_cols['D'])], axis=1)

    scaler_gk = dict_scalers[scaler]()
    scaler_gk = scaler_gk.fit(df_gk_0[dict_cols['G']])
    df_gk = pd.concat([df_gk_0[dict_cols['player_cols']].reset_index(drop=True),
                       pd.DataFrame(scaler_gk.transform(df_gk_0[dict_cols['G']]),
                                    columns=dict_cols['G'])], axis=1)

    dict_scalers = {'F': scaler_fw, 'M': scaler_mf, 'D': scaler_df, 'G': scaler_gk}

    return df_gk, df_df, df_mf, df_fw, dict_scalers
