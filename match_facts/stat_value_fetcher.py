from typing import Dict, List, Union
import numpy as np
import pandas as pd
from errors import InvalidMatchFactsError
from validators import EXPECTED_COLUMNS


class StatValueFetcher:

    def __init__(
            self,
            df_match_facts: pd.DataFrame,
            participant_type: str,
        ) -> None:
        """
        Fetches stat values from the MatchFacts DataFrame.
        Exposes a dictionary/DataFrame having all the stat values in ascending order of timestamp.
        
        Parameters:
            - df_match_facts (DataFrame): DataFrame having MatchFacts
            - participant_type (str): Type of participant. Options: ['teams', 'players', 'team_and_player_combos']
        
        Stats retrieved: ['goals', 'possession', 'shots', 'shots_on_target', 'shot_accuracy', 'pass_accuracy',
        'tackles', 'fouls', 'goals_conceded', 'possession_conceded', 'shots_conceded',
        'shots_on_target_conceded', 'shot_accuracy_conceded', 'pass_accuracy_conceded',
        'tackles_suffered', 'fouls_suffered']
        """
        self.df_match_facts = df_match_facts.copy(deep=True)
        self.participant_type = participant_type
        self.__validate_columns()
        self.__validate_participant_type()
        self.df_match_facts = self.__add_participant_columns(
            df_match_facts=self.df_match_facts,
            participant_type=self.participant_type,
        )
        self.games_played = {}
        self.max_games_played_by_single_team = 0 # Maximum number of games played by one team/player/team-player-combo
        self.goals = {}
        self.possession = {}
        self.shots = {}
        self.shots_on_target = {}
        self.shot_accuracy = {}
        self.pass_accuracy = {}
        self.tackles = {}
        self.fouls = {}
        self.goals_conceded = {}
        self.possession_conceded = {}
        self.shots_conceded = {}
        self.shots_on_target_conceded = {}
        self.shot_accuracy_conceded = {}
        self.pass_accuracy_conceded = {}
        self.tackles_suffered = {}
        self.fouls_suffered = {}
        self.__compute_all_stat_values()
        return None
    
    def __validate_columns(self) -> None:
        """
        Validates MatchFacts DataFrame, and raises an Exception if the validation fails.
        Returns None if the validation is successful.
        """
        columns_available = self.df_match_facts.columns.tolist()
        columns_missing = list(
            set(EXPECTED_COLUMNS[:]).difference(set(columns_available))
        )
        if columns_missing:
            raise InvalidMatchFactsError(
                f"MatchFacts does not have all the expected columns. Columns missing: {columns_missing}"
            )
        return None
    
    def __validate_participant_type(self) -> None:
        """
        Validates `participant_type`, and raises an Exception if the validation fails.
        Returns None if the validation is successful.
        """
        valid_participant_types = ['teams', 'players', 'team_and_player_combos']
        if self.participant_type not in valid_participant_types:
            raise ValueError(
                f"Expected `participant_type` to be in {valid_participant_types}, but got '{self.participant_type}'"
            )
        return None
    
    def __add_participant_columns(
            self,
            df_match_facts: pd.DataFrame,
            participant_type: str,
        ) -> pd.DataFrame:
        """
        Adds two columns ['HomeParticipant', 'AwayParticipant'] to the `df_match_facts` DataFrame, depending
        on the `participant_type`
        """
        df_mf = df_match_facts.copy(deep=True)
        if participant_type == 'teams':
            df_mf['HomeParticipant'] = df_mf['HomeTeam'].tolist()
            df_mf['AwayParticipant'] = df_mf['AwayTeam'].tolist()
        elif participant_type == 'players':
            df_mf['HomeParticipant'] = df_mf['HomePlayer'].tolist()
            df_mf['AwayParticipant'] = df_mf['AwayPlayer'].tolist()
        elif participant_type == 'team_and_player_combos':
            df_mf['HomeParticipant'] = df_mf['HomePlayer'] + '|' + df_mf['HomeTeam']
            df_mf['AwayParticipant'] = df_mf['AwayPlayer'] + '|' + df_mf['AwayTeam']
        return df_mf
    
    def get_unique_participants(self) -> List[str]:
        """Returns list of all unique participants from the MatchFacts DataFrame i.e; from the columns ['HomeParticipant', 'AwayParticipant']"""
        all_participants = pd.concat(
            objs=[self.df_match_facts['HomeParticipant'], self.df_match_facts['AwayParticipant']]
        ).dropna().sort_values(ascending=True).unique().tolist()
        return all_participants
    
    def __compute_all_stat_values(self) -> None:
        """Fetches all stat values and stores them in the objects initialized in the constructor"""
        df_mf = self.df_match_facts.copy(deep=True)
        df_mf.sort_values(by='Timestamp', ascending=True, ignore_index=True, inplace=True)
        participants = self.get_unique_participants()

        for participant in participants:
            self.games_played[participant] = 0
            self.goals[participant] = []
            self.possession[participant] = []
            self.shots[participant] = []
            self.shots_on_target[participant] = []
            self.shot_accuracy[participant] = []
            self.pass_accuracy[participant] = []
            self.tackles[participant] = []
            self.fouls[participant] = []
            self.goals_conceded[participant] = []
            self.possession_conceded[participant] = []
            self.shots_conceded[participant] = []
            self.shots_on_target_conceded[participant] = []
            self.shot_accuracy_conceded[participant] = []
            self.pass_accuracy_conceded[participant] = []
            self.tackles_suffered[participant] = []
            self.fouls_suffered[participant] = []
        
        for row in df_mf.itertuples():
            home_participant = row.HomeParticipant
            away_participant = row.AwayParticipant
            self.games_played[home_participant] += 1
            self.games_played[away_participant] += 1
            self.goals[home_participant].append(row.HomeGoals)
            self.goals[away_participant].append(row.AwayGoals)
            self.possession[home_participant].append(row.HomePossession)
            self.possession[away_participant].append(row.AwayPossession)
            self.shots[home_participant].append(row.HomeShots)
            self.shots[away_participant].append(row.AwayShots)
            self.shots_on_target[home_participant].append(row.HomeShotsOnTarget)
            self.shots_on_target[away_participant].append(row.AwayShotsOnTarget)
            self.shot_accuracy[home_participant].append(row.HomeShotAccuracy)
            self.shot_accuracy[away_participant].append(row.AwayShotAccuracy)
            self.pass_accuracy[home_participant].append(row.HomePassAccuracy)
            self.pass_accuracy[away_participant].append(row.AwayPassAccuracy)
            self.tackles[home_participant].append(row.HomeTackles)
            self.tackles[away_participant].append(row.AwayTackles)
            self.fouls[home_participant].append(row.HomeFouls)
            self.fouls[away_participant].append(row.AwayFouls)

            self.goals_conceded[home_participant].append(row.AwayGoals)
            self.goals_conceded[away_participant].append(row.HomeGoals)
            self.possession_conceded[home_participant].append(row.AwayPossession)
            self.possession_conceded[away_participant].append(row.HomePossession)
            self.shots_conceded[home_participant].append(row.AwayShots)
            self.shots_conceded[away_participant].append(row.HomeShots)
            self.shots_on_target_conceded[home_participant].append(row.AwayShotsOnTarget)
            self.shots_on_target_conceded[away_participant].append(row.HomeShotsOnTarget)
            self.shot_accuracy_conceded[home_participant].append(row.AwayShotAccuracy)
            self.shot_accuracy_conceded[away_participant].append(row.HomeShotAccuracy)
            self.pass_accuracy_conceded[home_participant].append(row.AwayPassAccuracy)
            self.pass_accuracy_conceded[away_participant].append(row.HomePassAccuracy)
            self.tackles_suffered[home_participant].append(row.AwayTackles)
            self.tackles_suffered[away_participant].append(row.HomeTackles)
            self.fouls_suffered[home_participant].append(row.AwayFouls)
            self.fouls_suffered[away_participant].append(row.HomeFouls)
        
        self.max_games_played_by_single_team = max(
            list(self.games_played.values())
        )
        return None
    
    def as_dicts(self) -> Dict[str, Dict[str, List[Union[int, float]]]]:
        """
        Returns dictionary having keys = stat name, and values = dictionary of stat values by team.
        The stat values will be in ascending order of timestamp.
        """
        dict_obj = {
            'goals': self.goals,
            'possession': self.possession,
            'shots': self.shots,
            'shots_on_target': self.shots_on_target,
            'shot_accuracy': self.shot_accuracy,
            'pass_accuracy': self.pass_accuracy,
            'tackles': self.tackles,
            'fouls': self.fouls,
            'goals_conceded': self.goals_conceded,
            'possession_conceded': self.possession_conceded,
            'shots_conceded': self.shots_conceded,
            'shots_on_target_conceded': self.shots_on_target_conceded,
            'shot_accuracy_conceded': self.shot_accuracy_conceded,
            'pass_accuracy_conceded': self.pass_accuracy_conceded,
            'tackles_suffered': self.tackles_suffered,
            'fouls_suffered': self.fouls_suffered,
        }
        return dict_obj
    
    def as_dataframes(self) -> Dict[str, pd.DataFrame]:
        """
        Returns dictionary having keys = stat name, and values = DataFrame of stat values by team.
        The stat values will be in ascending order of timestamp. The columns in each DataFrame will be the team names.
        """
        dict_obj = self.as_dicts()
        dict_obj_with_dataframes = {}
        for stat, dict_stat_values_by_team in dict_obj.items():
            dict_obj_with_dataframes[stat] = self.__stat_dict_to_dataframe(dict_obj=dict_stat_values_by_team)
        return dict_obj_with_dataframes
    
    def __stat_dict_to_dataframe(
            self,
            dict_obj: Dict[str, List[Union[int, float]]],
        ) -> pd.DataFrame:
        dict_obj_new = {}
        for team, stat_values in dict_obj.items():
            num_slots_to_fill = self.max_games_played_by_single_team - self.games_played[team]
            dict_obj_new[team] = stat_values + [np.nan] * num_slots_to_fill
        df_obj = pd.DataFrame(data=dict_obj_new)
        return df_obj