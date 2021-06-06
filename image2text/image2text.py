from typing import Dict, Union
import re

import pandas as pd
from PIL import Image
import pyocr
from pyocr import builders


# Constants
TOOLS = pyocr.get_available_tools()
if len(TOOLS) == 0:
    raise Exception("Error with PyOCR - No tools available")
TOOL = TOOLS[0]

LANGUAGES = TOOL.get_available_languages()
if 'eng' not in LANGUAGES:
    raise Exception("Error with PyOCR - Cannot handle the English language")



def get_raw_text_from_image(filepath_to_image: str) -> str:
    raw_text = TOOL.image_to_string(
        image=Image.open(filepath_to_image),
        lang='eng',
        builder=builders.TextBuilder(),
    )
    return raw_text


def keep_alpha_numerical_chars(string: str) -> str:
    return re.sub(pattern='[^A-Za-z0-9]+', repl='', string=string)


def keep_alphabets(string: str) -> str:
    return re.sub(pattern='[^A-Za-z]+', repl='', string=string)


def integerify_if_possible(number: Union[int, float]) -> Union[int, float]:
    if int(number) == number:
        return int(number)
    return number


def get_stat_dictionary_from_raw_text(raw_text: str) -> Dict[str, Union[int, float]]:
    dict_stat = {}
    lines = raw_text.split('\n')
    for line in lines:
        if line != '':
            stat_name_and_reading = keep_alpha_numerical_chars(string=line)
            stat_name = keep_alphabets(string=stat_name_and_reading)
            stat_value_home, stat_value_away = stat_name_and_reading.split(stat_name)
            stat_name_cleaned = 'ShotsOnTarget' if stat_name == 'ShotsonTarget' else stat_name # Changing casing
            obj = {
                f"Home{stat_name_cleaned}": integerify_if_possible(number=float(stat_value_home)),
                f"Away{stat_name_cleaned}": integerify_if_possible(number=float(stat_value_away)),
            }
            dict_stat.update(obj)
    return dict_stat


if __name__ == "__main__":
    filepath_to_image = "20210529_214354 (small).png"
    filename_without_ext = filepath_to_image.split('.')[0]

    raw_text = get_raw_text_from_image(filepath_to_image=filepath_to_image)
    dict_stat = get_stat_dictionary_from_raw_text(raw_text=raw_text)
    df_stat = pd.DataFrame(data=dict_stat, index=[0])
    df_stat = df_stat.T.reset_index().rename({'index': 'stat', 0: 'value'}, axis=1)
    df_stat.to_csv(f"{filename_without_ext}.csv", index=False)
    print("Saved to CSV")