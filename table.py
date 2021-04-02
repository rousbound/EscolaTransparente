from dataPrep import *
import os
import pandas as pd
import numpy as np
import jinja2

# Project specific global variables: paths, URIs, etc.
file_abspath = os.path.abspath(__file__)
file_basename = os.path.basename(file_abspath)
file_dirname = os.path.dirname(file_abspath)


def main():
    """The main function."""
    os.chdir(file_dirname)

    # Create a random dataframe.
    df_cols = list('ABCD')
    row_count = 12
    # df = pd.DataFrame(np.random.randint(0, 100, size=(
        # row_count, len(df_cols))), columns=df_cols)

    # Generate HTML from template.
    template = jinja2.Template("""<!DOCTYPE html>
<html>

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width">
    <title>Demo</title>
    <link href="https://cdn.jsdelivr.net/npm/simple-datatables@latest/dist/style.css" rel="stylesheet" type="text/css">
    <script src="https://cdn.jsdelivr.net/npm/simple-datatables@latest" type="text/javascript"></script>
    </head>

    <body>

        {{ dataframe }}

    </body>

    <script defer type="text/javascript">
        let myTable = new simpleDatatables.DataTable("#myTable");
    </script>

</html>"""
                               )

    output_html = template.render(dataframe=df3201_1T.to_html(table_id="myTable"))

    # Write generated HTML to file.
    with open("demo.htm", "w", encoding="utf-8") as file_obj:
        file_obj.write(output_html)


if __name__ == "__main__":
    main()
