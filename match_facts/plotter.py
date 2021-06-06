from typing import Dict
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from casing import sc2ucc
from plotter_helpers import (
    add_plot_skeleton,
    plot_bar,
    plot_radar,
)
import utils

plt.rcParams.update({'figure.max_open_warning': 0})


def plot_match_facts_distributions(
        dataframes_by_stat: Dict[str, pd.DataFrame],
        folder_to_store: str,
    ) -> None:
    """Saves MatchFacts related distribution plots to PNG file/s"""
    for stat, df_obj in dataframes_by_stat.items():
        stat_cleaned = sc2ucc(string=stat)
        title = f"Distribution of {stat_cleaned} by team"
        add_plot_skeleton(title=title, x_label=stat_cleaned, y_label='Team', fig_size=(30, 16))
        sns.boxplot(data=df_obj, orient='h', dodge=False, palette='Set2')
        plt.savefig(f"{folder_to_store}/{title}.png")
    return None


def plot_match_facts_bar_charts(
        dataframes_by_stat: Dict[str, pd.DataFrame],
        folder_to_store: str,
    ) -> None:
    """Saves MatchFacts related bar-charts to PNG file/s"""
    for stat, df_obj in dataframes_by_stat.items():
        stat_cleaned = f"Average {sc2ucc(string=stat)}"
        dict_averages_by_team = df_obj.mean().sort_values(ascending=True).apply(round, args=[2]).to_dict()
        
        title = f"{stat_cleaned} by team"
        bar_labels = list(dict_averages_by_team.keys())
        bar_values = list(dict_averages_by_team.values())
        plot_bar(
            title=title, x_label=stat_cleaned, y_label='Team', horizontal=True, fig_size=(30, 16),
            colors=[utils.generate_random_hex_code()], bar_labels=bar_labels, bar_values=bar_values,
            annotate=True, symmetrical=False, save_at=f"{folder_to_store}/{title}.png",
        )
    return None


def plot_match_facts_timeseries(
        dataframes_by_stat: Dict[str, pd.DataFrame],
        folder_to_store: str,
    ) -> None:
    """Saves MatchFacts related timeseries charts to PNG file/s"""
    for stat, df_obj in dataframes_by_stat.items():
        stat_cleaned = sc2ucc(string=stat)
        title = f"{stat_cleaned} over time"
        teams = sorted(df_obj.columns.tolist())
        matchdays = list(range(1, len(df_obj) + 1))
        max_teams_per_plot = 6
        sections_of_teams = [
            teams[idx : idx + max_teams_per_plot] for idx in range(0, len(teams), max_teams_per_plot)
        ]
        for section_of_teams in sections_of_teams:
            section_name = "".join(list(map(lambda team: team[0], section_of_teams)))
            plt.figure(figsize=(16, 10), dpi=300, clear=True)
            subplot_counter = 910
            for team in section_of_teams:
                subplot_counter += 1
                if subplot_counter > 919:
                    raise Exception("Please decrease the number of teams in each plot. Keep it atmost 9 teams per plot")
                ax = plt.subplot(subplot_counter)
                ax.set_title(f"{title} - {team}", size=15, weight='bold')
                plt.plot(matchdays, df_obj[team], linewidth=3)
                plt.setp(ax.get_xticklabels(), visible=False)
                plt.tight_layout()
            plt.savefig(f"{folder_to_store}/{title} ({section_name}).png")
    return None


def plot_match_facts_radar(
        df_match_facts_stats: pd.DataFrame,
        folder_to_store: str,
    ) -> None:
    """Saves MatchFacts related radar charts to PNG file/s"""
    df_mfs = df_match_facts_stats.copy(deep=True)
    dict_stats_by_type = {
        'Overall': ['AvgPossession', 'AvgShots', 'AvgShotsOnTarget', 'AvgShotAccuracy', 'AvgPassAccuracy', 'AvgTackles', 'AvgFouls'],
        'WhileWinning': [
            'AvgPossessionWhileWinning', 'AvgShotsWhileWinning', 'AvgShotsOnTargetWhileWinning', 'AvgShotAccuracyWhileWinning',
            'AvgPassAccuracyWhileWinning', 'AvgTacklesWhileWinning', 'AvgFoulsWhileWinning',
        ],
        'WhileLosing': [
            'AvgPossessionWhileLosing', 'AvgShotsWhileLosing', 'AvgShotsOnTargetWhileLosing', 'AvgShotAccuracyWhileLosing',
            'AvgPassAccuracyWhileLosing', 'AvgTacklesWhileLosing', 'AvgFoulsWhileLosing',
        ],
        'WhileDrawing': [
            'AvgPossessionWhileDrawing', 'AvgShotsWhileDrawing', 'AvgShotsOnTargetWhileDrawing', 'AvgShotAccuracyWhileDrawing',
            'AvgPassAccuracyWhileDrawing', 'AvgTacklesWhileDrawing', 'AvgFoulsWhileDrawing',
        ],
    }
    for stat_type, stat_columns_by_type in dict_stats_by_type.items():
        columns_subset = ['Team'] + stat_columns_by_type
        df_mfs_subset = df_mfs.loc[:, columns_subset]
        df_mfs_norm = utils.normalize_numerical_columns(
            data=df_mfs_subset,
            columns=stat_columns_by_type,
        )
        columns_to_flip = list(
            filter(lambda string: 'AvgFouls' in string, stat_columns_by_type)
        )
        for column_to_flip in columns_to_flip:
            df_mfs_norm[column_to_flip] = df_mfs_norm[column_to_flip].apply(lambda number: abs(number - 100))
        teams = df_mfs_norm['Team'].tolist()
        for team in teams:
            title = f"Performance Radar by percentile ({stat_type}) - {team}"
            dict_stats = df_mfs_norm[df_mfs_norm['Team'] == team].drop(labels='Team', axis=1).iloc[0].to_dict()
            labels = list(dict_stats.keys())
            values = list(dict_stats.values())
            labels = list(
                map(
                    lambda label: str(label).replace('Avg', '').replace('WhileWinning', '').replace('WhileLosing', '').replace('WhileDrawing', ''),
                    labels,
                )
            )
            plot_radar(
                title=title, labels=labels, values=values, fig_size=(15, 9), color=None,
                ticks=[], tick_limit=(0, 100), save_at=f"{folder_to_store}/{title}.png",
            )
    return None