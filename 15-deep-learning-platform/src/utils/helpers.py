from pathlib import Path


def create_directory(path):

    Path(path).mkdir(
        parents=True,
        exist_ok=True
    )


def create_output_directories(settings):

    folders = [

        settings.OUTPUTS_DIR,
        settings.FIGURES_DIR,
        settings.METRICS_DIR,
        settings.PREDICTIONS_DIR,
        settings.EXPLAINABILITY_DIR,
        settings.REPORTS_DIR,
        settings.HISTORY_DIR

    ]

    for folder in folders:

        create_directory(folder)