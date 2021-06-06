from typing import Any, Dict, List, Optional
import pandas as pd


def style_dataframe(
        data: pd.DataFrame,
        columns_with_desirable_highs: Optional[List[str]] = None,
        columns_with_desirable_lows: Optional[List[str]] = None,
    ) -> Any:
    """Styles DataFrame and returns Styler object"""
    if not columns_with_desirable_highs and not columns_with_desirable_lows:
        raise ValueError(
            "Expects `columns_with_desirable_highs` and/or `columns_with_desirable_lows` in order to style said columns"
        )
    df = data.copy(deep=True)
    # Color mapping options: ['bwr', 'Greens', 'Blues', 'RdYlGn', 'summer']
    df = df.style\
        .background_gradient(subset=columns_with_desirable_highs, cmap='Greens')\
        .background_gradient(subset=columns_with_desirable_lows, cmap='Blues')
    return df


def save_styled_dataframe(
        filepath_with_ext: str,
        sheet_name_to_styler: Dict[str, Any],
    ) -> None:
    """Saves Pandas Styler object/s to an Excel file, which could have multiple sheets"""
    with pd.ExcelWriter(filepath_with_ext) as excel_writer:
        for sheet_name, styler_obj in sheet_name_to_styler.items():
            styler_obj.to_excel(
                excel_writer=excel_writer,
                sheet_name=sheet_name,
                index=False,
                engine='xlsxwriter',
            )
    return None