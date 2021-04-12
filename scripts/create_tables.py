import os
import sys

import pandas as pd

def table_header(columns):
    """Return table header string with specified columns.

    Parameters
    ==========
    columns : list of str
         List of column names.

    Returns
    =======
    str
         The tabular header with the appropriate number of columns set.
    """
    return \
        f"\\begin{{tabular}}{{{'l' + 'r' * (len(columns) - 1)}}}\n"\
        f"\t\\toprule\n"\
        f"\t{' & '.join(columns)} \\\\\n"\
        f"\t\\midrule\n"


def table_end():
    """Return table end string."""
    return \
        f"\t\\bottomrule\n"\
        f"\\end{{tabular}}\n"


def matplotlib_versions():
    """Write table of matplotlib versions to file."""
    path_table = os.path.join(os.path.dirname(__file__),
                              "../tables/matplotlib_versions.tex")

    path_data = os.path.join(os.path.dirname(__file__),
                              "../data/release_dates.csv")
    data = pd.read_csv(path_data)

    with open(path_table, "w") as table:

        table.write(table_header(["Version", "Date"]))

        # Ensure that the table data is sorted by date
        for _, row in data.sort_values("date").iterrows():

            version = row.version
            date = row.date

            table.write(f"{version} & {date}\\\\\n")

        table.write(table_end())

if __name__ == "__main__":

    # table_name : table_function
    TABLE_FUNCTIONS = {
        "matplotlib_versions": matplotlib_versions,
    }

    if len(sys.argv) < 2:
        print("Provide a table name to compile it. Choose from:")
        print(list(TABLE_FUNCTIONS.keys()))
        sys.exit()

    # Call the figure function
    if not "--all" in sys.argv:
        table_name = sys.argv[1]
        TABLE_FUNCTIONS[table_name]()
    else:
        for table, function in TABLE_FUNCTIONS.items():
            print(f"Compiling {table}..")
            function()
