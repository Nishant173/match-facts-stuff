from typing import List
import pandas as pd


def filter_by_team(df_match_facts: pd.DataFrame, team: str) -> pd.DataFrame:
    df_mf = df_match_facts.copy(deep=True)
    team_is_playing = (df_mf['HomeTeam'] == team) | (df_mf['AwayTeam'] == team)
    df_by_team = df_mf[team_is_playing]
    return df_by_team


def filter_by_player(df_match_facts: pd.DataFrame, player: str) -> pd.DataFrame:
    df_mf = df_match_facts.copy(deep=True)
    player_is_playing = (df_mf['HomePlayer'] == player) | (df_mf['AwayPlayer'] == player)
    df_by_player = df_mf[player_is_playing]
    return df_by_player


def filter_by_team_result(
        data: pd.DataFrame,
        team: str,
        result: str,
    ) -> pd.DataFrame:
    """
    Filters DataFrame having MatchFacts data (based on result obtained by the team).
    Options for `result`: ['win', 'loss', 'draw']
    """
    if result not in ['win', 'loss', 'draw']:
        raise ValueError(f"Expected one of ['win', 'loss', 'draw'] for `result`, but got {result}")
    df_by_team = filter_by_team(df_match_facts=data, team=team)
    if result == 'win':
        home_win = ((df_by_team['HomeTeam'] == team) & (df_by_team['HomeGoals'] > df_by_team['AwayGoals']))
        away_win = ((df_by_team['AwayTeam'] == team) & (df_by_team['AwayGoals'] > df_by_team['HomeGoals']))
        df_by_team = df_by_team.loc[(home_win | away_win), :]
    elif result == 'loss':
        home_loss = ((df_by_team['HomeTeam'] == team) & (df_by_team['HomeGoals'] < df_by_team['AwayGoals']))
        away_loss = ((df_by_team['AwayTeam'] == team) & (df_by_team['AwayGoals'] < df_by_team['HomeGoals']))
        df_by_team = df_by_team.loc[(home_loss | away_loss), :]
    elif result == 'draw':
        df_by_team = df_by_team.loc[(df_by_team['HomeGoals'] == df_by_team['AwayGoals']), :]
    return df_by_team


def filter_by_player_result(
        data: pd.DataFrame,
        player: str,
        result: str,
    ) -> pd.DataFrame:
    """
    Filters DataFrame having MatchFacts data (based on result obtained by the player).
    Options for `result`: ['win', 'loss', 'draw']
    """
    if result not in ['win', 'loss', 'draw']:
        raise ValueError(f"Expected one of ['win', 'loss', 'draw'] for `result`, but got {result}")
    df_by_player = filter_by_player(df_match_facts=data, player=player)
    if result == 'win':
        home_win = ((df_by_player['HomePlayer'] == player) & (df_by_player['HomeGoals'] > df_by_player['AwayGoals']))
        away_win = ((df_by_player['AwayPlayer'] == player) & (df_by_player['AwayGoals'] > df_by_player['HomeGoals']))
        df_by_player = df_by_player.loc[(home_win | away_win), :]
    elif result == 'loss':
        home_loss = ((df_by_player['HomePlayer'] == player) & (df_by_player['HomeGoals'] < df_by_player['AwayGoals']))
        away_loss = ((df_by_player['AwayPlayer'] == player) & (df_by_player['AwayGoals'] < df_by_player['HomeGoals']))
        df_by_player = df_by_player.loc[(home_loss | away_loss), :]
    elif result == 'draw':
        df_by_player = df_by_player.loc[(df_by_player['HomeGoals'] == df_by_player['AwayGoals']), :]
    return df_by_player


def filter_by_team_matchup(
        df_match_facts: pd.DataFrame,
        matchup: List[str],
    ) -> pd.DataFrame:
    if len(matchup) != 2:
        raise ValueError(f"Expected list of length 2, but got length {len(matchup)}")
    team1, team2 = matchup
    df_mf = df_match_facts.copy(deep=True)
    team1_is_home = (df_mf['HomeTeam'] == team1) & (df_mf['AwayTeam'] == team2)
    team2_is_home = (df_mf['HomeTeam'] == team2) & (df_mf['AwayTeam'] == team1)
    df_by_matchup = df_mf[team1_is_home | team2_is_home]
    return df_by_matchup


def filter_by_player_matchup(
        df_match_facts: pd.DataFrame,
        matchup: List[str],
    ) -> pd.DataFrame:
    if len(matchup) != 2:
        raise ValueError(f"Expected list of length 2, but got length {len(matchup)}")
    player1, player2 = matchup
    df_mf = df_match_facts.copy(deep=True)
    player1_is_home = (df_mf['HomePlayer'] == player1) & (df_mf['AwayPlayer'] == player2)
    player2_is_home = (df_mf['HomePlayer'] == player2) & (df_mf['AwayPlayer'] == player1)
    df_by_matchup = df_mf[player1_is_home | player2_is_home]
    return df_by_matchup