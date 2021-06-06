from typing import Dict
import pandas as pd
import config
import filters
import utils


def get_win_count(data: pd.DataFrame, team: str) -> int:
    """Get count of wins by team (Expects DataFrame having MatchFacts data)"""
    team_is_home = (data['HomeTeam'] == team)
    team_is_away = (data['AwayTeam'] == team)
    df_home_wins = data[team_is_home & (data['HomeGoals'] > data['AwayGoals'])]
    df_away_wins = data[team_is_away & (data['AwayGoals'] > data['HomeGoals'])]
    win_count = len(df_home_wins) + len(df_away_wins)
    return win_count


def get_loss_count(data: pd.DataFrame, team: str) -> int:
    """Get count of losses by team (Expects DataFrame having MatchFacts data)"""
    team_is_home = (data['HomeTeam'] == team)
    team_is_away = (data['AwayTeam'] == team)
    df_home_losses = data[team_is_home & (data['HomeGoals'] < data['AwayGoals'])]
    df_away_losses = data[team_is_away & (data['AwayGoals'] < data['HomeGoals'])]
    loss_count = len(df_home_losses) + len(df_away_losses)
    return loss_count


def get_draw_count(data: pd.DataFrame, team: str) -> int:
    """Get count of draws by team (Expects DataFrame having MatchFacts data)"""
    team_is_playing = (data['HomeTeam'] == team) | (data['AwayTeam'] == team)
    is_drawn = (data['HomeGoals'] == data['AwayGoals'])
    draw_count = len(data[team_is_playing & is_drawn])
    return draw_count


def get_goals_scored(data: pd.DataFrame, team: str) -> int:
    """Get count of goals scored by team (Expects DataFrame having MatchFacts data)"""
    home_goals_scored = data[data['HomeTeam'] == team]['HomeGoals'].sum()
    away_goals_scored = data[data['AwayTeam'] == team]['AwayGoals'].sum()
    goals_scored = home_goals_scored + away_goals_scored
    return goals_scored


def get_goals_allowed(data: pd.DataFrame, team: str) -> int:
    """Get count of goals allowed by team (Expects DataFrame having MatchFacts data)"""
    home_goals_allowed = data[data['HomeTeam'] == team]['AwayGoals'].sum()
    away_goals_allowed = data[data['AwayTeam'] == team]['HomeGoals'].sum()
    goals_allowed = home_goals_allowed + away_goals_allowed
    return goals_allowed


def get_clean_sheet_count(data: pd.DataFrame, team: str) -> int:
    """Get count of clean sheets kept by team (Expects DataFrame having MatchFacts data)"""
    team_is_home = (data['HomeTeam'] == team)
    team_is_away = (data['AwayTeam'] == team)
    df_cs_away = data[team_is_away & (data['HomeGoals'] == 0)]
    df_cs_home = data[team_is_home & (data['AwayGoals'] == 0)]
    number_of_clean_sheets = len(df_cs_away) + len(df_cs_home)
    return number_of_clean_sheets


def get_clean_sheets_against_count(data: pd.DataFrame, team: str) -> int:
    """Get count of clean sheets kept against given team (Expects DataFrame having MatchFacts data)"""
    team_is_home = (data['HomeTeam'] == team)
    team_is_away = (data['AwayTeam'] == team)
    df_cs_against_away = data[team_is_away & (data['AwayGoals'] == 0)]
    df_cs_against_home = data[team_is_home & (data['HomeGoals'] == 0)]
    number_of_clean_sheets_against = len(df_cs_against_away) + len(df_cs_against_home)
    return number_of_clean_sheets_against


def get_rout_count(data: pd.DataFrame, team: str, goal_margin: int) -> int:
    """Get count of wins by team that are by margin >= `goal_margin` (Expects DataFrame having MatchFacts data)"""
    df_altered = data.copy(deep=True)
    df_altered['goal_margin'] = (df_altered['HomeGoals'] - df_altered['AwayGoals']).abs()
    df_rout_subset = df_altered[df_altered['goal_margin'] >= goal_margin]
    team_is_home = (df_rout_subset['HomeTeam'] == team)
    team_is_away = (df_rout_subset['AwayTeam'] == team)
    df_rout_home = df_rout_subset[team_is_home & (df_rout_subset['HomeGoals'] > df_rout_subset['AwayGoals'])]
    df_rout_away = df_rout_subset[team_is_away & (df_rout_subset['AwayGoals'] > df_rout_subset['HomeGoals'])]
    total_routs = len(df_rout_home) + len(df_rout_away)
    return total_routs


def get_capitulation_count(data: pd.DataFrame, team: str, goal_margin: int) -> int:
    """Get count of losses by team that are by margin >= `goal_margin` (Expects DataFrame having MatchFacts data)"""
    df_altered = data.copy(deep=True)
    df_altered['goal_margin'] = (df_altered['HomeGoals'] - df_altered['AwayGoals']).abs()
    df_capitulation_subset = df_altered[df_altered['goal_margin'] >= goal_margin]
    team_is_home = (df_capitulation_subset['HomeTeam'] == team)
    team_is_away = (df_capitulation_subset['AwayTeam'] == team)
    home_capitulation = (df_capitulation_subset['HomeGoals'] < df_capitulation_subset['AwayGoals'])
    away_capitulation = (df_capitulation_subset['AwayGoals'] < df_capitulation_subset['HomeGoals'])
    df_capitulation_home = df_capitulation_subset[team_is_home & home_capitulation]
    df_capitulation_away = df_capitulation_subset[team_is_away & away_capitulation]
    total_capitulations = len(df_capitulation_home) + len(df_capitulation_away)
    return total_capitulations


def get_results_string(data: pd.DataFrame) -> Dict[str, str]:
    """
    Gets results-string for games of all teams in MatchFacts DataFrame.
    Each results-string will be in ascending order of 'Timestamp' column.
    Returns dictionary having keys = team names, and values = results-string for said team.
    Example output: {
        "Bayern Munich": "WDLWDLLWWW",
        "Leipzig": "WDDWDWLWLD",
        "Leverkusen": "DLLWWWLLWW",
    }
    """
    df_altered = data.copy(deep=True)
    dictionary_results = {}
    df_altered.sort_values(by='Timestamp', ascending=True, ignore_index=True, inplace=True)
    teams = utils.get_unique_teams(df_match_facts=df_altered)

    for team in teams:
        dictionary_results[team] = ""
    
    for row in df_altered.itertuples():
        home_team = row.HomeTeam
        away_team = row.AwayTeam
        home_goals = row.HomeGoals
        away_goals = row.AwayGoals
        if home_goals > away_goals:
            dictionary_results[home_team] += 'W'
            dictionary_results[away_team] += 'L'
        elif away_goals > home_goals:
            dictionary_results[home_team] += 'L'
            dictionary_results[away_team] += 'W'
        elif home_goals == away_goals:
            dictionary_results[home_team] += 'D'
            dictionary_results[away_team] += 'D'
    return dictionary_results


def get_scoreline_stats(data: pd.DataFrame) -> pd.DataFrame:
    """Expects MatchFacts DataFrame. Returns DataFrame of scoreline related stats by team"""
    df_mf = data.copy(deep=True)
    df_scoreline_stats = pd.DataFrame()
    dict_results_string = get_results_string(data=df_mf)
    teams = utils.get_unique_teams(df_match_facts=df_mf)
    for team in teams:
        df_by_team = filters.filter_by_team(df_match_facts=df_mf, team=team)
        games_played = len(df_by_team)
        wins = get_win_count(data=df_by_team, team=team)
        losses = get_loss_count(data=df_by_team, team=team)
        draws = get_draw_count(data=df_by_team, team=team)
        gs = get_goals_scored(data=df_by_team, team=team)
        ga = get_goals_allowed(data=df_by_team, team=team)
        cs = get_clean_sheet_count(data=df_by_team, team=team)
        csa = get_clean_sheets_against_count(data=df_by_team, team=team)
        routs = get_rout_count(data=df_by_team, team=team, goal_margin=config.BIG_RESULT_GOAL_MARGIN)
        capitulations = get_capitulation_count(data=df_by_team, team=team, goal_margin=config.BIG_RESULT_GOAL_MARGIN)
        df_temp = pd.DataFrame(data={
            'Team': team,
            'GamesPlayed': games_played,
            'Points': 3 * wins + draws,
            'GoalDifference': gs - ga,
            'Wins': wins,
            'Losses': losses,
            'Draws': draws,
            'GoalsScored': gs,
            'GoalsAllowed': ga,
            'CleanSheets': cs,
            'CleanSheetsAgainst': csa,
            'BigWins': routs,
            'BigLosses': capitulations,
            'ResultsString': dict_results_string[team],
        }, index=[0])
        df_scoreline_stats = pd.concat(objs=[df_scoreline_stats, df_temp], ignore_index=True, sort=False)
    df_scoreline_stats['PPG'] = df_scoreline_stats['Points'] / df_scoreline_stats['GamesPlayed']
    df_scoreline_stats['GDPG'] = df_scoreline_stats['GoalDifference'] / df_scoreline_stats['GamesPlayed']
    df_scoreline_stats = utils.add_ranking_column(
        data=df_scoreline_stats,
        rank_column_name='Rank',
        rank_by=['PPG', 'GDPG'],
        ascending=[False, False],
    )
    df_scoreline_stats.drop(labels=['PPG', 'GDPG'], axis=1, inplace=True)
    return df_scoreline_stats