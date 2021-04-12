import os
import sys

import pandas as pd

def write_variables_to_file(stats):
    """Write the variables to the aux/stats.tex file.

    Parameters
    ==========
    stats : dict
        Dictionary containing variable names as keys and their value and filetype as values.
        The LaTeX variable name cannot contain underscores.
    """
    PATH_STATS = os.path.join(os.path.dirname(__file__), "../aux/stats.tex")

    with open(PATH_STATS, "w") as file_:

        for name, value in stats.items():

            if "_" in name:
                print(f"'_' is not a valid character in TeX variable names. "
                    f"Removing them from {name}.")

            name = name.replace("_", "")

            value, type_ = value

            if type_ is int:
                file_.write(f'\\def\\{name}{{{value:,}\\xspace}}\n')
            elif type_ is float:
                file_.write(f'\\def\\{name}{{{value:.2f}\\xspace}}\n')
            elif type_ is str:
                file_.write(f'\\def\\{name}{{{value}\\xspace}}\n')

if __name__ == "__main__":

    # Directories and data
    PATH_DATA = os.path.join(os.path.dirname(__file__), "../data/")
    data = pd.read_csv(os.path.join(PATH_DATA, "release_dates.csv"))

    # Dictionary storing the variable : (value, type) pairs
    STATS = {}

    # Add the number of matplotlib versions
    STATS["NVersions"] = (len(data), int)

    # Get the earliest and latest version
    STATS["VersionEarliest"] = (data.version.min(), str) 
    STATS["VersionLatest"] = (data.version.max(), str) 
    STATS["VersionEarliestDate"] = (data.loc[
         data.version == data.version.min(), "date"
         ].values[0], str)
    STATS["VersionLatestDate"] = (data.loc[
         data.version == data.version.min(), "date"
         ].values[0], str)

    # And write to file
    write_variables_to_file(STATS)
