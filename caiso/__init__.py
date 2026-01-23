"""California ISO market operations data

Usage
-----

    caiso [OPTIONS ...] {dam,rtm} YEAR

Positional arguments
--------------------

  - `dam`: get day-ahead market data

  - `rtm`: get real-time market data

Optional arguments
------------------

  - `--debug`: enable traceback on exceptions

  - `-f|--format FORMAT`: specify format. Valid formats are `table`(the default)
    to output a human readable data frame format, or `csv` to output in machine
    readable CSV format.

  - `--header`: disable CSV header output

  - `-h|--help`: get online documentation

  - `--index`: disable CSV index output

  - `-o|--output`: specify CSV output filename (default is `/dev/stdout`)

  - `--warning`: enable warning messages

  - `-M|--month`: specify month
"""

from caiso.dam import DAM
from caiso.rtm import RTM
from caiso.cli import main
