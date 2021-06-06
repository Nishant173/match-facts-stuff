from typing import Dict, List, Union
import datetime
import random
import numpy as np
import pandas as pd
from randomtimestamp import randomtimestamp


def normalize_array(array: List[Union[int, float]]) -> List[Union[int, float]]:
    """
    Normalizes values in array to range of [0, 1].
    Ignores and removes all NaNs.
    """
    array = np.array(array)
    array = array[~np.isnan(array)]
    normalized_array = (array - np.min(array)) / np.ptp(array)
    return list(normalized_array)


def normalize_numerical_columns(data: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """
    Takes in DataFrame and list of numerical columns to normalize.
    Normalizes the given columns between [0-100].
    Note: Does not work with NaN values.
    """
    df = data.copy(deep=True)
    for column in columns:
        values = df[column].tolist()
        df[column] = normalize_array(array=values)
        df[column] = df[column].mul(100).round(2)
    return df


def get_timetaken_dictionary(num_seconds: Union[int, float]) -> Dict[str, Union[int, float]]:
    hrs, mins, secs = 0, 0, 0
    decimal_after_secs = None
    if int(num_seconds) == num_seconds:
        num_seconds = int(num_seconds)
    else:
        decimal_after_secs = num_seconds - np.floor(num_seconds)
        num_seconds = int(np.floor(num_seconds))
    if num_seconds < 60:
        secs = num_seconds
    elif 60 <= num_seconds < 3600:
        mins, secs = divmod(num_seconds, 60)
    else:
        hrs, secs_remainder = divmod(num_seconds, 3600)
        mins, secs = divmod(secs_remainder, 60)
    dictionary_timetaken = {
        "hrs": hrs,
        "mins": mins,
        "secs": secs + decimal_after_secs if decimal_after_secs else secs,
    }
    dictionary_timetaken = {key: value for key, value in dictionary_timetaken.items() if value > 0}
    return dictionary_timetaken


def get_timetaken_fstring(num_seconds: Union[int, float]) -> str:
    dict_timetaken = get_timetaken_dictionary(num_seconds=num_seconds)
    timetaken_components = [f"{value} {unit}" for unit, value in dict_timetaken.items()]
    return " ".join(timetaken_components).strip()


def has_negative_number(array: List[Union[int, float]]) -> bool:
    for number in array:
        if number < 0:
            return True
    return False


def has_positive_number(array: List[Union[int, float]]) -> bool:
    for number in array:
        if number > 0:
            return True
    return False


def get_max_of_abs_values(array: List[Union[int, float]]) -> Union[int, float]:
    """Finds maximum of absolute values of numbers in an array"""
    array_abs = list(map(abs, array))
    return max(array_abs)


def get_min_of_abs_values(array: List[Union[int, float]]) -> Union[int, float]:
    """Finds minimum of absolute values of numbers in an array"""
    array_abs = list(map(abs, array))
    return min(array_abs)


def generate_random_hex_code() -> str:
    """Generates random 6-digit hexadecimal code"""
    choices = '0123456789ABCDEF'
    random_hex_code = '#'
    for _ in range(6):
        random_hex_code += random.choice(choices)
    return random_hex_code


def generate_random_hex_codes(how_many: int) -> List[str]:
    """Returns list of random 6-digit hexadecimal codes"""
    random_hex_codes = [generate_random_hex_code() for _ in range(how_many)]
    return random_hex_codes


def get_random_timestamp() -> int:
    ts_random = randomtimestamp(
        start_year=2000,
        end_year=2020,
        pattern="%Y%m%d%H%M%S",
    )
    return int(ts_random)


def get_current_timestamp() -> int:
    ts_now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    return int(ts_now)


def timestamp_to_datetime(timestamp: int) -> datetime.datetime:
    dt_obj = datetime.datetime.strptime(str(timestamp), "%Y%m%d%H%M%S")
    return dt_obj


def get_random_choice_except(choices: List[str], exception: str) -> str:
    if exception not in choices:
        raise ValueError("The `exception` is not available in the given `choices`")
    choices_available = list(set(choices).difference(set([exception])))
    if not choices_available:
        raise Exception("No choices available")
    return random.choice(choices_available)


def round_off_columns(data: pd.DataFrame,
                      columns: List[str],
                      round_by: int) -> pd.DataFrame:
    """
    Rounds off specified numerical (float) columns in DataFrame.
    >>> round_off_columns(data=data, columns=['column1', 'column3', 'column5'], round_by=2)
    """
    data_altered = data.copy(deep=True)
    for column in columns:
        data_altered[column] = data_altered[column].apply(round, args=[int(round_by)])
    return data_altered


def get_unique_teams(df_match_facts: pd.DataFrame) -> List[str]:
    df_mf = df_match_facts.copy(deep=True)
    all_teams = pd.concat(
        objs=[df_mf['HomeTeam'], df_mf['AwayTeam']]
    ).dropna().sort_values(ascending=True).unique().tolist()
    return all_teams


def get_unique_players(df_match_facts: pd.DataFrame) -> List[str]:
    df_mf = df_match_facts.copy(deep=True)
    all_players = pd.concat(
        objs=[df_mf['HomePlayer'], df_mf['AwayPlayer']]
    ).dropna().sort_values(ascending=True).unique().tolist()
    return all_players


def add_ranking_column(
        data: pd.DataFrame,
        rank_column_name: str,
        rank_by: List[str],
        ascending: List[bool],
    ) -> pd.DataFrame:
    """Adds ranking column based on `rank_by` column/s to DataFrame"""
    if len(rank_by) != len(ascending):
        raise ValueError(
            "Expected `rank_by` and `ascending` to be of same length,"
            f" but got lengths {len(rank_by)} and {len(ascending)} respectively"
        )
    df_ranked = data.sort_values(by=rank_by, ascending=ascending, ignore_index=True)
    rankings = np.arange(start=1, stop=len(df_ranked) + 1, step=1)
    df_ranked[rank_column_name] = rankings
    column_order = [rank_column_name] + df_ranked.drop(labels=[rank_column_name], axis=1).columns.tolist()
    df_ranked = df_ranked.loc[:, column_order]
    return df_ranked