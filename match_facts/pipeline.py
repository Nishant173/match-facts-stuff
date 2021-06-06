import pandas as pd

from config import FOLDER_STRUCTURE
from create_folder_structure import create_folder_structure
import excel_formatter
import match_facts_stats_by_team
from metric_fetcher import StatValueFetcher
import plotter
import scoreline_stats_by_team
import validators


def execute_pipeline(src_filepath: str) -> None:
    df_match_facts = pd.read_csv(src_filepath)
    validators.validate_match_facts(df_match_facts=df_match_facts)

    # Create folder structure to store stats
    create_folder_structure()

    # Getting basic tabular stats
    df_scoreline_stats_by_team = scoreline_stats_by_team.get_scoreline_stats(data=df_match_facts)
    df_scoreline_stats_by_team.to_csv(f"{FOLDER_STRUCTURE['tables']}/ScorelineBased - StatsByTeam.csv", index=False)
    
    df_mfs_by_team = match_facts_stats_by_team.get_match_facts_stats(
        data=df_match_facts,
        ignore_result_based_stats=False,
    )
    df_mfs_by_team.to_csv(f"{FOLDER_STRUCTURE['tables']}/MatchFacts - StatsByTeam.csv", index=False)

    # Getting basic tabular stats (Excel formatted)
    df_mfs_by_team_styled = excel_formatter.style_dataframe(
        data=df_mfs_by_team,
        columns_with_desirable_highs=['AvgPossession', 'AvgShots', 'AvgShotsOnTarget', 'AvgShotAccuracy', 'AvgPassAccuracy', 'AvgTackles'],
        columns_with_desirable_lows=['AvgFouls'],
    )
    excel_formatter.save_styled_dataframe(
        filepath_with_ext=f"{FOLDER_STRUCTURE['tables']}/MatchFacts - Calculated Stats (formatted).xlsx",
        sheet_name_to_styler={
            'Team': df_mfs_by_team_styled,
        },
    )

    # DataViz
    svf = StatValueFetcher(df_match_facts=df_match_facts)
    dataframes_by_stat = svf.as_dataframes()
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