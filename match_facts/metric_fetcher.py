from typing import Dict, List, Union
import numpy as np
import pandas as pd
from errors import InvalidMatchFactsError
import utils
from validators import EXPECTED_COLUMNS


class StatValueFetcher:
    """
    Computes stat values by team, given the MatchFacts DataFrame.
    Exposes a dictionary/dataframe having all the stat values by team, in ascending order of timestamp.
    """

    def __init__(self, df_match_facts: pd.DataFrame) -> None:
        self.df_match_facts = df_match_facts.copy(deep=True)
        self.__validate_columns()
        self.stat_options = [
            'goals', 'possession', 'shots', 'shots_on_target', 'shot_accuracy', 'pass_accuracy', 'tackles', 'fouls',
            'goals_conceded', 'possession_conceded', 'shots_conceded', 'shots_on_target_conceded',
            'shot_accuracy_conceded', 'pass_accuracy_conceded', 'tackles_suffered', 'fouls_suffered',
        ]
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
        return None
    
    def __validate_columns(self) -> None:
        """
        Validates match facts DataFrame, and raises an Exception if the validation fails.
        Returns None if the validation is successful.
        """
        columns_available = self.df_match_facts.columns.tolist()
        columns_missing = list(
            set(EXPECTED_COLUMNS[:]).difference(set(columns_available))
        )
        if columns_missing:
            raise InvalidMatchFactsError(
                f"Match facts does not have all the expected columns. Columns missing: {columns_missing}"
            )
        return None
    
    def compute_all_stat_values(self) -> None:
        """Computes all stat values and stores them in the objects initialized in the constructor"""
        df_mf = self.df_match_facts.copy(deep=True)
        df_mf.sort_values(by='Timestamp', ascending=True, ignore_index=True, inplace=True)
        teams = utils.get_unique_teams(df_match_facts=df_mf)

        for team in teams:
            self.goals[team] = []
            self.possession[team] = []
            self.shots[team] = []
            self.shots_on_target[team] = []
            self.shot_accuracy[team] = []
            self.pass_accuracy[team] = []
            self.tackles[team] = []
            self.fouls[team] = []
            self.goals_conceded[team] = []
            self.possession_conceded[team] = []
            self.shots_conceded[team] = []
            self.shots_on_target_conceded[team] = []
            self.shot_accuracy_conceded[team] = []
            self.pass_accuracy_conceded[team] = []
            self.tackles_suffered[team] = []
            self.fouls_suffered[team] = []
        
        for row in df_mf.itertuples():
            home_team = row.HomeTeam
            away_team = row.AwayTeam
            self.goals[home_team].append(row.HomeGoals)
            self.goals[away_team].append(row.AwayGoals)
            self.possession[home_team].append(row.HomePossession)
            self.possession[away_team].append(row.AwayPossession)
            self.shots[home_team].append(row.HomeShots)
            self.shots[away_team].append(row.AwayShots)
            self.shots_on_target[home_team].append(row.HomeShotsOnTarget)
            self.shots_on_target[away_team].append(row.AwayShotsOnTarget)
            self.shot_accuracy[home_team].append(row.HomeShotAccuracy)
            self.shot_accuracy[away_team].append(row.AwayShotAccuracy)
            self.pass_accuracy[home_team].append(row.HomePassAccuracy)
            self.pass_accuracy[away_team].append(row.AwayPassAccuracy)
            self.tackles[home_team].append(row.HomeTackles)
            self.tackles[away_team].append(row.AwayTackles)
            self.fouls[home_team].append(row.HomeFouls)
            self.fouls[away_team].append(row.AwayFouls)

            self.goals_conceded[home_team].append(row.AwayGoals)
            self.goals_conceded[away_team].append(row.HomeGoals)
            self.possession_conceded[home_team].append(row.AwayPossession)
            self.possession_conceded[away_team].append(row.HomePossession)
            self.shots_conceded[home_team].append(row.AwayShots)
            self.shots_conceded[away_team].append(row.HomeShots)
            self.shots_on_target_conceded[home_team].append(row.AwayShotsOnTarget)
            self.shots_on_target_conceded[away_team].append(row.HomeShotsOnTarget)
            self.shot_accuracy_conceded[home_team].append(row.AwayShotAccuracy)
            self.shot_accuracy_conceded[away_team].append(row.HomeShotAccuracy)
            self.pass_accuracy_conceded[home_team].append(row.AwayPassAccuracy)
            self.pass_accuracy_conceded[away_team].append(row.HomePassAccuracy)
            self.tackles_suffered[home_team].append(row.AwayTackles)
            self.tackles_suffered[away_team].append(row.HomeTackles)
            self.fouls_suffered[home_team].append(row.AwayFouls)
            self.fouls_suffered[away_team].append(row.HomeFouls)
        return None
    
    def as_dicts(self) -> Dict[str, Dict[str, List[Union[int, float]]]]:
        """
        Returns dictionary having keys = stat name, and values = dictionary of stat values by team.
        The stat values will be in ascending order of timestamp.
        """
        self.compute_all_stat_values()
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
            dict_obj_with_dataframes[stat] = StatValueFetcher.dict2dataframe(dict_obj=dict_stat_values_by_team)
        return dict_obj_with_dataframes
    
    @staticmethod
    def dict2dataframe(dict_obj: Dict[str, List[Union[int, float]]]) -> pd.DataFrame:
        """
        Converts dictionary having keys = strings, and values = list of numbers into a DataFrame.
        Note: The keys of the dictionary will become the columns of the DataFrame.
        """
        max_length_of_lists = max(
            [len(numbers) for _, numbers in dict_obj.items()]
        )
        dict_obj_new = {}
        for string, numbers in dict_obj.items():
            slots_to_fill = max_length_of_lists - len(numbers)
            dict_obj_new[string] = numbers + [np.nan] * slots_to_fill
        df_obj = pd.DataFrame(data=dict_obj_new)
        return df_obj