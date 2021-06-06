from typing import Dict, Optional, List, Tuple, Union
import matplotlib.pyplot as plt
import numpy as np
import utils


def get_calibrated_plot_fonts(fig_size: Tuple[int, int]) -> Dict[str, float]:
    """
    Takes in figure-size (tuple having [width, height]), and returns dictionary containing fontsizes for all other aspects
    of the plot (calculated and set appropriately, based on the figure-size).
    The fontsizes dictionary will have the following keys: `['title_size', 'label_size', 'tick_size', 'legend_label_size', 'annotation_size']`
    """
    if isinstance(fig_size, tuple):
        if len(fig_size) == 2:
            width = int(fig_size[0])
        else:
            raise ValueError (f"Invalid value for `fig_size`. Expected tuple of length 2, but got tuple of length {len(fig_size)}")
    else:
        raise TypeError(f"Invalid type for `fig_size`. Expected 'tuple' but got '{type(fig_size)}'")
    title_to_width_ratio = round((40 / 24), 3)
    labels_to_width_ratio = round((25 / 24), 3)
    ticks_to_width_ratio = round((20 / 24), 3)
    legend_labels_to_width_ratio = round((24 / 24), 3)
    annotation_to_width_ratio = round((18 / 24), 3)
    dictionary_calibrated_plot_fonts = {
        'title_size': width * title_to_width_ratio,
        'label_size': width * labels_to_width_ratio,
        'tick_size': width * ticks_to_width_ratio,
        'legend_label_size': width * legend_labels_to_width_ratio,
        'annotation_size': width * annotation_to_width_ratio,
    }
    return dictionary_calibrated_plot_fonts


def add_plot_skeleton(
        title: str,
        x_label: str,
        y_label: str,
        fig_size: Tuple[int, int],
        include_labels: Optional[bool] = True,
        include_ticks: Optional[bool] = True,
    ):
    """Returns matplotlib plot object, containing skeleton of basic aspects of a plot"""
    dict_plot_fonts = get_calibrated_plot_fonts(fig_size=fig_size)
    obj = plt.figure(figsize=fig_size)
    obj = plt.title(title, fontsize=dict_plot_fonts['title_size'])
    if include_labels:
        obj = plt.xlabel(x_label, fontsize=dict_plot_fonts['label_size'])
        obj = plt.ylabel(y_label, fontsize=dict_plot_fonts['label_size'])
    if include_ticks:
        obj = plt.xticks(fontsize=dict_plot_fonts['tick_size'])
        obj = plt.yticks(fontsize=dict_plot_fonts['tick_size'])
    return obj


def plot_bar(title: str,
             x_label: str,
             y_label: str,
             horizontal: bool,
             bar_labels: List[str],
             bar_values: List[Union[int, float]],
             fig_size: Optional[Tuple[int, int]] = (12, 5),
             colors: Optional[Union[List[str], List]] = [],
             annotate: Optional[bool] = True,
             symmetrical: Optional[bool] = True,
             save_at: Optional[str] = None,
             show: Optional[bool] = False) -> None:
    add_plot_skeleton(title=title,
                      x_label=x_label,
                      y_label=y_label,
                      fig_size=fig_size,
                      include_labels=True,
                      include_ticks=True)
    if not colors:
        colors = utils.generate_random_hex_codes(how_many=len(bar_labels))
    if horizontal:
        plt.barh(y=bar_labels, width=bar_values, color=colors)
    else:
        plt.bar(x=bar_labels, height=bar_values, color=colors)
    if annotate:
        dict_plot_fonts = get_calibrated_plot_fonts(fig_size=fig_size)
        annotation_size = dict_plot_fonts['annotation_size']
    if annotate and horizontal:
        for idx, value in enumerate(bar_values):
            plt.text(x = value * 1.01,
                     y = idx,
                     s = str(value),
                     fontweight='bold',
                     fontsize=annotation_size,
                     color='black')
    if annotate and not horizontal:
        for idx, value in enumerate(bar_values):
            plt.text(x = idx,
                     y = value * 1.01,
                     s = str(value),
                     fontweight='bold',
                     fontsize=annotation_size,
                     color='black')
    if symmetrical:
        if utils.has_negative_number(array=bar_values) and utils.has_positive_number(array=bar_values):
            axis_limit = utils.get_max_of_abs_values(array=bar_values) * 1.05
            if horizontal:
                plt.xlim(-axis_limit, axis_limit)
            else:
                plt.ylim(-axis_limit, axis_limit)
    if save_at:
        plt.savefig(save_at)
    if show:
        plt.show()
    plt.close()
    return None


def plot_radar(
        title: str,
        labels: List[str],
        values: List[Union[int, float]],
        ticks: Optional[List[Union[int, float]]] = None,
        tick_limit: Optional[Tuple[Union[int, float], Union[int, float]]] = None,
        fig_size: Optional[Tuple[int, int]] = (15, 9),
        color: Optional[str] = None,
        save_at: Optional[str] = None,
        show: Optional[bool] = False,
    ) -> None:
    dict_calibrated_plot_fonts = get_calibrated_plot_fonts(fig_size=fig_size)
    angles = np.linspace(start=0, stop=2*np.pi, num=len(labels), endpoint=False)
    values = np.concatenate((values, [values[0]]))
    labels = np.concatenate((labels, [labels[0]]))
    angles = np.concatenate((angles, [angles[0]]))
    
    fig = plt.figure(figsize=fig_size)
    ax = fig.add_subplot(111, polar=True)
    ax.plot(angles, values, 'o-', linewidth=2.5, c=color)
    ax.fill(angles, values, alpha=0.35, c=color)
    ax.set_thetagrids(angles * 180 / np.pi, labels, size=dict_calibrated_plot_fonts['label_size'])
    ax.grid(True)
    if ticks:
        plt.yticks(ticks, size=dict_calibrated_plot_fonts['tick_size'])
    else:
        plt.yticks([])
    if tick_limit:
        plt.ylim(tick_limit)
    plt.title(title, size=dict_calibrated_plot_fonts['title_size'])
    if save_at:
        plt.savefig(save_at)
    if show:
        plt.show()
    plt.close()
    return None