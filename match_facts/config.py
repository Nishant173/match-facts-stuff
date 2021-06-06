import os

BIG_RESULT_GOAL_MARGIN = 3

FOLDER_NAMES = {
    'root-results': "MatchFacts - Results",
    'tables': 'Tables',
    'viz': 'Visualizations',
    'viz-bar': 'Bar charts',
    'viz-distributions': 'Distribution charts',
    'viz-radar': 'Radar charts',
    'viz-timeseries': 'Timeseries charts',
}

FOLDER_STRUCTURE = {
    'root-results': FOLDER_NAMES['root-results'],
    'tables': os.path.join(
        FOLDER_NAMES['root-results'], FOLDER_NAMES['tables'],
    ),
    'viz': os.path.join(
        FOLDER_NAMES['root-results'], FOLDER_NAMES['viz'],
    ),
    'viz-bar': os.path.join(
        FOLDER_NAMES['root-results'], FOLDER_NAMES['viz'], FOLDER_NAMES['viz-bar'],
    ),
    'viz-distributions': os.path.join(
        FOLDER_NAMES['root-results'], FOLDER_NAMES['viz'], FOLDER_NAMES['viz-distributions'],
    ),
    'viz-radar': os.path.join(
        FOLDER_NAMES['root-results'], FOLDER_NAMES['viz'], FOLDER_NAMES['viz-radar'],
    ),
    'viz-timeseries': os.path.join(
        FOLDER_NAMES['root-results'], FOLDER_NAMES['viz'], FOLDER_NAMES['viz-timeseries'],
    ),
}