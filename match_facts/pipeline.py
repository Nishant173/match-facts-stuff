import pandas as pd

from config import FOLDER_STRUCTURE
from create_folder_structure import create_folder_structure
import excel_formatter
from match_facts_stats import (
    get_match_facts_stats_by_player,
    get_match_facts_stats_by_player_and_team_combo,
    get_match_facts_stats_by_team,
)
import plotter
from scoreline_stats import (
    get_scoreline_stats_by_player,
    get_scoreline_stats_by_player_and_team_combo,
    get_scoreline_stats_by_team,
)
from stat_value_fetcher import StatValueFetcher
from validators import validate_match_facts


def execute_pipeline(src_filepath: str) -> None:
    df_match_facts = pd.read_csv(src_filepath)
    validate_match_facts(df_match_facts=df_match_facts)

    # Create folder structure to store the tables/visualizations
    create_folder_structure()

    # Table - Scoreline stats
    df_scoreline_stats_by_team = get_scoreline_stats_by_team(data=df_match_facts)
    df_scoreline_stats_by_player = get_scoreline_stats_by_player(data=df_match_facts)
    df_scoreline_stats_by_player_and_team_combo = get_scoreline_stats_by_player_and_team_combo(data=df_match_facts)
    df_scoreline_stats_by_team.to_csv(f"{FOLDER_STRUCTURE['tables']}/ScorelineStats - Team.csv", index=False)
    df_scoreline_stats_by_player.to_csv(f"{FOLDER_STRUCTURE['tables']}/ScorelineStats - Player.csv", index=False)
    df_scoreline_stats_by_player_and_team_combo.to_csv(f"{FOLDER_STRUCTURE['tables']}/ScorelineStats - PlayerAndTeam.csv", index=False)
    
    # Table - MatchFacts stats
    df_mfs_by_team = get_match_facts_stats_by_team(data=df_match_facts)
    df_mfs_by_player = get_match_facts_stats_by_player(data=df_match_facts)
    df_mfs_by_player_and_team_combo = get_match_facts_stats_by_player_and_team_combo(data=df_match_facts)
    df_mfs_by_team.to_csv(f"{FOLDER_STRUCTURE['tables']}/MatchFactsStats - Team.csv", index=False)
    df_mfs_by_player.to_csv(f"{FOLDER_STRUCTURE['tables']}/MatchFactsStats - Player.csv", index=False)
    df_mfs_by_player_and_team_combo.to_csv(f"{FOLDER_STRUCTURE['tables']}/MatchFactsStats - PlayerAndTeam.csv", index=False)

    # Table - MatchFacts stats (Excel formatted)
    df_mfs_by_team_styled = excel_formatter.style_dataframe(
        data=df_mfs_by_team,
        columns_with_desirable_highs=['AvgPossession', 'AvgShots', 'AvgShotsOnTarget', 'AvgShotAccuracy', 'AvgPassAccuracy', 'AvgTackles'],
        columns_with_desirable_lows=['AvgFouls'],
    )
    df_mfs_by_player_styled = excel_formatter.style_dataframe(
        data=df_mfs_by_player,
        columns_with_desirable_highs=['AvgPossession', 'AvgShots', 'AvgShotsOnTarget', 'AvgShotAccuracy', 'AvgPassAccuracy', 'AvgTackles'],
        columns_with_desirable_lows=['AvgFouls'],
    )
    df_mfs_by_player_and_team_combo_styled = excel_formatter.style_dataframe(
        data=df_mfs_by_player_and_team_combo,
        columns_with_desirable_highs=['AvgPossession', 'AvgShots', 'AvgShotsOnTarget', 'AvgShotAccuracy', 'AvgPassAccuracy', 'AvgTackles'],
        columns_with_desirable_lows=['AvgFouls'],
    )
    excel_formatter.save_styled_dataframe(
        filepath_with_ext=f"{FOLDER_STRUCTURE['tables']}/MatchFactsStats - All (Excel formatted).xlsx",
        sheet_name_to_styler={
            'Team': df_mfs_by_team_styled,
            'Player': df_mfs_by_player_styled,
            'PlayerAndTeam': df_mfs_by_player_and_team_combo_styled,
        },
    )

    # DataViz
    svf_teams = StatValueFetcher(
        df_match_facts=df_match_facts,
        participant_type='teams',
    )
    dataframes_by_stat = svf_teams.as_dataframes()
    plotter.plot_match_facts_distributions(
        dataframes_by_stat=dataframes_by_stat,
        folder_to_store=FOLDER_STRUCTURE['viz-distributions'],
    )
    plotter.plot_match_facts_bar_charts(
        dataframes_by_stat=dataframes_by_stat,
        folder_to_store=FOLDER_STRUCTURE['viz-bar'],
    )
    plotter.plot_match_facts_timeseries(
        dataframes_by_stat=dataframes_by_stat,
        folder_to_store=FOLDER_STRUCTURE['viz-timeseries'],
    )
    plotter.plot_match_facts_radar(
        df_match_facts_stats=df_mfs_by_team,
        folder_to_store=FOLDER_STRUCTURE['viz-radar'],
    )
    return None


if __name__ == "__main__":
    execute_pipeline(src_filepath="FakeMatchFacts 20210606190918.csv")
    print("Done!")