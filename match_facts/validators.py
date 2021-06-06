import pandas as pd
from errors import InvalidMatchFactsError

EXPECTED_COLUMNS_WITH_DATATYPE = {
    'Timestamp': 'integer',
    'HomePlayer': 'string',
    'AwayPlayer': 'string',
    'HomeTeam': 'string',
    'AwayTeam': 'string',
    'HomeGoals': 'integer',
    'AwayGoals': 'integer',
    'HomePossession': 'integer',
    'AwayPossession': 'integer',
    'HomeShots': 'integer',
    'AwayShots': 'integer',
    'HomeShotsOnTarget': 'integer',
    'AwayShotsOnTarget': 'integer',
    'HomeTackles': 'integer',
    'AwayTackles': 'integer',
    'HomeFouls': 'integer',
    'AwayFouls': 'integer',
    'HomeYellowCards': 'integer',
    'AwayYellowCards': 'integer',
    'HomeRedCards': 'integer',
    'AwayRedCards': 'integer',
    'HomeOffsides': 'integer',
    'AwayOffsides': 'integer',
    'HomeCorners': 'integer',
    'AwayCorners': 'integer',
    'HomeShotAccuracy': 'float',
    'AwayShotAccuracy': 'float',
    'HomePassAccuracy': 'integer',
    'AwayPassAccuracy': 'integer',
}

EXPECTED_COLUMNS = list(EXPECTED_COLUMNS_WITH_DATATYPE.keys())
EXPECTED_STRING_COLUMNS = [
    column for column, datatype in EXPECTED_COLUMNS_WITH_DATATYPE.items() if datatype == 'string'
]
EXPECTED_INTEGER_COLUMNS = [
    column for column, datatype in EXPECTED_COLUMNS_WITH_DATATYPE.items() if datatype == 'integer'
]
EXPECTED_FLOAT_COLUMNS = [
    column for column, datatype in EXPECTED_COLUMNS_WITH_DATATYPE.items() if datatype == 'float'
]


def __has_no_missing_values(df_match_facts: pd.DataFrame) -> None:
    has_no_missing_values = (df_match_facts.isnull().sum().sum() == 0)
    if not has_no_missing_values:
        raise InvalidMatchFactsError("Match facts has missing data")
    return None


def __has_all_expected_columns(df_match_facts: pd.DataFrame) -> None:
    has_expected_columns = (sorted(df_match_facts.columns.tolist()) == sorted(EXPECTED_COLUMNS))
    if not has_expected_columns:
        raise InvalidMatchFactsError("Match facts does not have all the expected columns")
    return None


def __has_appropriate_object_columns(df_match_facts: pd.DataFrame) -> None:
    df_mf_subset = df_match_facts.select_dtypes(include='object')
    columns = df_mf_subset.columns.tolist()
    has_appropriate_object_columns = (sorted(columns) == sorted(EXPECTED_STRING_COLUMNS))
    if not has_appropriate_object_columns:
        raise InvalidMatchFactsError("Match facts does not have all the expected string columns")
    return None


def __has_no_blanks_in_object_columns(df_match_facts: pd.DataFrame) -> None:
    df_mf_subset = df_match_facts.select_dtypes(include='object')
    columns = df_mf_subset.columns.tolist()
    for column in columns:
        series_lengths = df_mf_subset[column].apply(len)
        num_blank_values = (series_lengths == 0).sum()
        if num_blank_values > 0:
            raise InvalidMatchFactsError(f"Match facts has blank values in the string column: '{column}'")
    return None


def __has_appropriate_float_columns(df_match_facts: pd.DataFrame) -> None:
    df_mf_subset = df_match_facts.select_dtypes(include='float64')
    columns = df_mf_subset.columns.tolist()
    has_appropriate_float_columns = (sorted(columns) == sorted(EXPECTED_FLOAT_COLUMNS))
    if not has_appropriate_float_columns:
        raise InvalidMatchFactsError("Match facts does not have all the expected float columns")
    return None


def __has_appropriate_integer_columns(df_match_facts: pd.DataFrame) -> None:
    df_mf_subset = df_match_facts.select_dtypes(include='int64')
    columns = df_mf_subset.columns.tolist()
    has_appropriate_integer_columns = (sorted(columns) == sorted(EXPECTED_INTEGER_COLUMNS))
    if not has_appropriate_integer_columns:
        raise InvalidMatchFactsError("Match facts does not have all the expected integer columns")
    return None


def __has_matchups_between_unique_teams(df_match_facts: pd.DataFrame) -> None:
    has_matchups_between_unique_teams = (
        (df_match_facts['HomeTeam'] == df_match_facts['AwayTeam']).sum() == 0
    )
    if not has_matchups_between_unique_teams:
        raise InvalidMatchFactsError("Match facts contains matches that are between the same HomeTeam and AwayTeam")
    return None


def __has_matchups_between_unique_players(df_match_facts: pd.DataFrame) -> None:
    has_matchups_between_unique_players = (
        (df_match_facts['HomePlayer'] == df_match_facts['AwayPlayer']).sum() == 0
    )
    if not has_matchups_between_unique_players:
        raise InvalidMatchFactsError("Match facts contains matches that are between the same HomePlayer and AwayPlayer")
    return None


def validate_match_facts(df_match_facts: pd.DataFrame) -> None:
    """
    Validates match facts DataFrame, and raises an Exception if the validation fails.
    Returns None if the validation is successful.
    """
    __has_no_missing_values(df_match_facts=df_match_facts)
    __has_all_expected_columns(df_match_facts=df_match_facts)
    __has_appropriate_object_columns(df_match_facts=df_match_facts)
    __has_appropriate_float_columns(df_match_facts=df_match_facts)
    __has_appropriate_integer_columns(df_match_facts=df_match_facts)
    __has_no_blanks_in_object_columns(df_match_facts=df_match_facts)
    __has_matchups_between_unique_teams(df_match_facts=df_match_facts)
    __has_matchups_between_unique_players(df_match_facts=df_match_facts)
    return None


if __name__ == "__main__":
    filepath = "FakeMatchFacts 20210606190918.csv"
    df_match_facts = pd.read_csv(filepath)

    print(f"Validating MatchFacts located at '{filepath}'...")
    validate_match_facts(df_match_facts=df_match_facts)
    print("Validation done successfully!")