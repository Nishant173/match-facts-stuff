from typing import Dict
import random
import numpy as np
import pandas as pd
import utils


TEAM_NAMES = [
    'Manchester City', 'Manchester Utd', 'Liverpool', 'Chelsea',
    'Bayern', 'Leipzig', 'Gladbach', 'Frankfurt',
    'Real Madrid', 'Barcelona', 'Atletico', 'Sevilla',
    'AC Milan', 'Inter', 'Juventus', 'Roma',
    'PSG', 'Lille', 'Marseille', 'Monaco', 'Reims',
]

PLAYER_NAMES = [
    'Ederson', 'Paul', 'Thiago', 'Kai',
    'Joshua', 'Kevin', 'Florian', 'Andre',
    'Toni', 'Leo', 'Koke', 'Lucas',
    'Zlatan', 'Ivan', 'Cristiano', 'Chris',
    'Kylian', 'Renato',
]


def generate_fake_match_facts(num_records: int) -> Dict[str, int]:
    df_fmf = pd.DataFrame()
    home_players = [random.choice(PLAYER_NAMES) for _ in range(num_records)]
    away_players = [
        utils.get_random_choice_except(choices=PLAYER_NAMES[:], exception=home_player) for home_player in home_players
    ]
    home_teams = [random.choice(TEAM_NAMES) for _ in range(num_records)]
    away_teams = [
        utils.get_random_choice_except(choices=TEAM_NAMES[:], exception=home_team) for home_team in home_teams
    ]
    df_fmf['Timestamp'] = [utils.get_random_timestamp() for _ in range(num_records)]
    df_fmf['HomePlayer'] = home_players
    df_fmf['AwayPlayer'] = away_players
    df_fmf['HomeTeam'] = home_teams
    df_fmf['AwayTeam'] = away_teams
    df_fmf['HomeGoals'] = [random.randint(0, 5) for _ in range(num_records)]
    df_fmf['AwayGoals'] = [random.randint(0, 5) for _ in range(num_records)]
    df_fmf['HomePossession'] = [random.randint(25, 75) for _ in range(num_records)]
    df_fmf['AwayPossession'] = 100 - df_fmf['HomePossession']
    df_fmf['HomeShots'] = df_fmf['HomeGoals'] + random.randint(0, 15)
    df_fmf['AwayShots'] = df_fmf['AwayGoals'] + random.randint(0, 15)
    df_fmf['HomeShotsOnTarget'] = (df_fmf['HomeShots'] * random.randint(20, 80) / 100).apply(np.floor).astype(int)
    df_fmf['AwayShotsOnTarget'] = (df_fmf['AwayShots'] * random.randint(20, 80) / 100).apply(np.floor).astype(int)
    df_fmf['HomeTackles'] = [random.randint(10, 30) for _ in range(num_records)]
    df_fmf['AwayTackles'] = [random.randint(10, 30) for _ in range(num_records)]
    df_fmf['HomeFouls'] = [random.randint(1, 10) for _ in range(num_records)]
    df_fmf['AwayFouls'] = [random.randint(1, 10) for _ in range(num_records)]
    df_fmf['HomeYellowCards'] = [random.randint(1, 4) for _ in range(num_records)]
    df_fmf['AwayYellowCards'] = [random.randint(1, 6) for _ in range(num_records)]
    df_fmf['HomeRedCards'] = [random.randint(0, 1) for _ in range(num_records)]
    df_fmf['AwayRedCards'] = [random.randint(0, 1) for _ in range(num_records)]
    df_fmf['HomeOffsides'] = [random.randint(0, 10) for _ in range(num_records)]
    df_fmf['AwayOffsides'] = [random.randint(0, 10) for _ in range(num_records)]
    df_fmf['HomeCorners'] = [random.randint(0, 20) for _ in range(num_records)]
    df_fmf['AwayCorners'] = [random.randint(0, 20) for _ in range(num_records)]
    df_fmf['HomeShotAccuracy'] = (df_fmf['HomeShotsOnTarget'] * 100 / df_fmf['HomeShots']).apply(round, args=[2])
    df_fmf['AwayShotAccuracy'] = (df_fmf['AwayShotsOnTarget'] * 100 / df_fmf['AwayShots']).apply(round, args=[2])
    df_fmf['HomePassAccuracy'] = [random.randint(55, 91) for _ in range(num_records)]
    df_fmf['AwayPassAccuracy'] = [random.randint(55, 91) for _ in range(num_records)]
    df_fmf.sort_values(by=['Timestamp'], ascending=[True], ignore_index=True, inplace=True)
    return df_fmf


if __name__ == "__main__":
    df_fake_match_facts = generate_fake_match_facts(num_records=2000)    
    timestamp = utils.get_current_timestamp()
    df_fake_match_facts.to_csv(f"FakeMatchFacts {timestamp}.csv", index=False)
    print(f"Saved fake MatchFacts to CSV @ {timestamp}")