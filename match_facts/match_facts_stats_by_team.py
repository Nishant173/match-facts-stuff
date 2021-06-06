from typing import Union
import numpy as np
import pandas as pd
import filters
import utils


def get_avg_possession(data: pd.DataFrame, team: str) -> Union[int, float]:
    """Gets average possession of given team (Expects DataFrame having MatchFacts data)"""
    home_possession_values = data[(data['HomeTeam'] == team)]['HomePossession'].tolist()
    away_possession_values = data[(data['AwayTeam'] == team)]['AwayPossession'].tolist()
    avg_possession = np.mean(home_possession_values + away_possession_values)
    return avg_possession


def get_avg_shots(data: pd.DataFrame, team: str) -> Union[int, float]:
    """Gets average shots of given team (Expects DataFrame having MatchFacts data)"""
    home_shots_values = data[(data['HomeTeam'] == team)]['HomeShots'].tolist()
    away_shots_values = data[(data['AwayTeam'] == team)]['AwayShots'].tolist()
    avg_shots = np.mean(home_shots_values + away_shots_values)
    return avg_shots


def get_avg_shots_on_target(data: pd.DataFrame, team: str) -> Union[int, float]:
    """Gets average shots on target of given team (Expects DataFrame having MatchFacts data)"""
    home_sot = data[(data['HomeTeam'] == team)]['HomeShotsOnTarget'].tolist()
    away_sot = data[(data['AwayTeam'] == team)]['AwayShotsOnTarget'].tolist()
    avg_shots_on_target = np.mean(home_sot + away_sot)
    return avg_shots_on_target


def get_avg_shot_accuracy(data: pd.DataFrame, team: str) -> Union[int, float]:
    """Gets average shot accuracy of given team (Expects DataFrame having MatchFacts data)"""
    home_shot_accuracy = data[(data['HomeTeam'] == team)]['HomeShotAccuracy'].tolist()
    away_shot_accuracy = data[(data['AwayTeam'] == team)]['AwayShotAccuracy'].tolist()
    avg_shot_accuracy = np.mean(home_shot_accuracy + away_shot_accuracy)
    return avg_shot_accuracy


def get_avg_pass_accuracy(data: pd.DataFrame, team: str) -> Union[int, float]:
    """Gets average pass accuracy of given team (Expects DataFrame having MatchFacts data)"""
    home_pass_accuracy = data[(data['HomeTeam'] == team)]['HomePassAccuracy'].tolist()
    away_pass_accuracy = data[(data['AwayTeam'] == team)]['AwayPassAccuracy'].tolist()
    avg_pass_accuracy = np.mean(home_pass_accuracy + away_pass_accuracy)
    return avg_pass_accuracy


def get_avg_tackles(data: pd.DataFrame, team: str) -> Union[int, float]:
    """Gets average tackles of given team (Expects DataFrame having MatchFacts data)"""
    home_tackles = data[(data['HomeTeam'] == team)]['HomeTackles'].tolist()
    away_tackles = data[(data['AwayTeam'] == team)]['AwayTackles'].tolist()
    avg_tackles = np.mean(home_tackles + away_tackles)
    return avg_tackles


def get_avg_fouls(data: pd.DataFrame, team: str) -> Union[int, float]:
    """Gets average fouls of given team (Expects DataFrame having MatchFacts data)"""
    home_fouls = data[(data['HomeTeam'] == team)]['HomeFouls'].tolist()
    away_fouls = data[(data['AwayTeam'] == team)]['AwayFouls'].tolist()
    avg_fouls = np.mean(home_fouls + away_fouls)
    return avg_fouls


def __drop_result_based_columns(df_mf_stats: pd.DataFrame) -> pd.DataFrame:
    """Takes in DataFrame having MatchFactsStats data, and drops the result based columns from the available stats"""
    df = df_mf_stats.copy(deep=True)
    columns = df.columns.tolist()
    columns_to_drop = list(
        filter(
            lambda column: ('WhileWinning' in column) or ('WhileLosing' in column) or ('WhileDrawing' in column),
            columns,
        )
    )
    df.drop(labels=columns_to_drop, axis=1, inplace=True)
    return df


def get_match_facts_stats(data: pd.DataFrame, ignore_result_based_stats: bool) -> pd.DataFrame:
    """Expects MatchFacts DataFrame. Returns DataFrame of MatchFacts related stats by team"""
    df_mf = data.copy(deep=True)
    df_mf_stats = pd.DataFrame()
    teams = utils.get_unique_teams(df_match_facts=df_mf)
    for team in teams:
        df_by_team = filters.filter_by_team(df_match_facts=df_mf, team=team)
        games_played = len(df_by_team)
        df_temp = pd.DataFrame(data={
            'Team': team,
            'GamesPlayed': games_played,
            'AvgPossession': get_avg_possession(data=df_by_team, team=team),
            'AvgShots': get_avg_shots(data=df_by_team, team=team),
            'AvgShotsOnTarget': get_avg_shots_on_target(data=df_by_team, team=team),
            'AvgShotAccuracy': get_avg_shot_accuracy(data=df_by_team, team=team),
            'AvgPassAccuracy': get_avg_pass_accuracy(data=df_by_team, team=team),
            'AvgTackles': get_avg_tackles(data=df_by_team, team=team),
            'AvgFouls': get_avg_fouls(data=df_by_team, team=team),
            'AvgPossessionWhileWinning': get_avg_possession(
                data=filters.filter_by_team_result(data=df_by_team, team=team, result='win'),
                team=team,
            ),
            'AvgPossessionWhileLosing': get_avg_possession(
                data=filters.filter_by_team_result(data=df_by_team, team=team, result='loss'),
                team=team,
            ),
            'AvgPossessionWhileDrawing': get_avg_possession(
                data=filters.filter_by_team_result(data=df_by_team, team=team, result='draw'),
                team=team,
            ),
            'AvgShotsWhileWinning': get_avg_shots(
                data=filters.filter_by_team_result(data=df_by_team, team=team, result='win'),
                team=team,
            ),
            'AvgShotsWhileLosing': get_avg_shots(
                data=filters.filter_by_team_result(data=df_by_team, team=team, result='loss'),
                team=team,
            ),
            'AvgShotsWhileDrawing': get_avg_shots(
                data=filters.filter_by_team_result(data=df_by_team, team=team, result='draw'),
                team=team,
            ),
            'AvgShotsOnTargetWhileWinning': get_avg_shots_on_target(
                data=filters.filter_by_team_result(data=df_by_team, team=team, result='win'),
                team=team,
            ),
            'AvgShotsOnTargetWhileLosing': get_avg_shots_on_target(
                data=filters.filter_by_team_result(data=df_by_team, team=team, result='loss'),
                team=team,
            ),
            'AvgShotsOnTargetWhileDrawing': get_avg_shots_on_target(
                data=filters.filter_by_team_result(data=df_by_team, team=team, result='draw'),
                team=team,
            ),
            'AvgShotAccuracyWhileWinning': get_avg_shot_accuracy(
                data=filters.filter_by_team_result(data=df_by_team, team=team, result='win'),
                team=team,
            ),
            'AvgShotAccuracyWhileLosing': get_avg_shot_accuracy(
                data=filters.filter_by_team_result(data=df_by_team, team=team, result='loss'),
                team=team,
            ),
            'AvgShotAccuracyWhileDrawing': get_avg_shot_accuracy(
                data=filters.filter_by_team_result(data=df_by_team, team=team, result='draw'),
                team=team,
            ),
            'AvgPassAccuracyWhileWinning': get_avg_pass_accuracy(
                data=filters.filter_by_team_result(data=df_by_team, team=team, result='win'),
                team=team,
            ),
            'AvgPassAccuracyWhileLosing': get_avg_pass_accuracy(
                data=filters.filter_by_team_result(data=df_by_team, team=team, result='loss'),
                team=team,
            ),
            'AvgPassAccuracyWhileDrawing': get_avg_pass_accuracy(
                data=filters.filter_by_team_result(data=df_by_team, team=team, result='draw'),
                team=team,
            ),
            'AvgTacklesWhileWinning': get_avg_tackles(
                data=filters.filter_by_team_result(data=df_by_team, team=team, result='win'),
                team=team,
            ),
            'AvgTacklesWhileLosing': get_avg_tackles(
                data=filters.filter_by_team_result(data=df_by_team, team=team, result='loss'),
                team=team,
            ),
            'AvgTacklesWhileDrawing': get_avg_tackles(
                data=filters.filter_by_team_result(data=df_by_team, team=team, result='draw'),
                team=team,
            ),
            'AvgFoulsWhileWinning': get_avg_fouls(
                data=filters.filter_by_team_result(data=df_by_team, team=team, result='win'),
                team=team,
            ),
            'AvgFoulsWhileLosing': get_avg_fouls(
                data=filters.filter_by_team_result(data=df_by_team, team=team, result='loss'),
                team=team,
            ),
            'AvgFoulsWhileDrawing': get_avg_fouls(
                data=filters.filter_by_team_result(data=df_by_team, team=team, result='draw'),
                team=team,
            ),
        }, index=[0])
        df_mf_stats = pd.concat(objs=[df_mf_stats, df_temp], ignore_index=True, sort=False)
    df_mf_stats = df_mf_stats.round(2)
    df_mf_stats.sort_values(by=['Team'], ascending=[True], ignore_index=True, inplace=True)
    if ignore_result_based_stats:
        df_mf_stats = __drop_result_based_columns(df_mf_stats=df_mf_stats)
    return df_mf_stats