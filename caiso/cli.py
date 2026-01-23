"""California ISO market data accessor"""

import sys
import argparse
import pathlib
import warnings
import logging

import pandas as pd
# pylint: disable=unused-import
from caiso.rtm import RTM
from caiso.dam import DAM

E_OK = 0
"""Exit code for success"""

E_FAILED = 1
"""Exit code for failure"""

E_SYNTAX = 2
"""Exit code for syntax error"""

_logger = logging.getLogger(__file__)

def main(*args:list[str]) -> int:
    """California ISO market data accessor main command line processor

    Arguments
    ---------

      - `*args`: command line arguments (`None` is `sys.argv`)

    Returns
    -------

      - `int`: return/exit code (see `E_*` codes)

    Caveat
    ------

    - The `notz` convert timestamp to local time but does not account to
      summer time (daylight savings time).
    """
    # pylint: disable=too-many-return-statements
    try:

        # support direct call to main
        if args:
            sys.argv = [__file__] + list(args)

        # setup command line parser
        parser = argparse.ArgumentParser(
            prog="caiso",
            description="California ISO data accessor",
            epilog="See https://www.eudoxys.com/caiso for documentation. ",
            )
        parser.add_argument("dataset",
            choices=["rtm","dam"],
            help="specify the market dataset")
        parser.add_argument("year",
            type=int,
            help="specify the year")
        parser.add_argument("-M","--month",
            type=int,
            help="specify the month")
        parser.add_argument("--refresh",
            action="store_true",
            help="force refresh of local data cache")

        parser.add_argument("--debug",
            action="store_true",
            help="enable debug traceback on exceptions",
            )
        parser.add_argument("-f","--format",
            choices={"table","csv"},
            help="specify the output format",
            )
        parser.add_argument("--header",
            action="store_false",
            help="disable CSV header output",
            )
        parser.add_argument("--index",
            action="store_false",
            help="disable CSV index output",
            )
        parser.add_argument("--notz",
            action="store_true",
            help="discard timezone information")
        parser.add_argument("-o","--output",
            type=pathlib.Path,
            default=None,
            metavar="OUTPUT",
            help="specify the CSV output filename",
            )
        parser.add_argument("--warning",
            action="store_false",
            help="disable warning messages from python",
            )

        # parse arguments
        args = parser.parse_args()

        # setup warning handling
        if args.warning:
            warnings.showwarning = lambda *x:print(
                f"WARNING [{__package__}]:",
                x[0],
                flush=True,
                file=sys.stderr,
                )
        else:
            warnings.showwarning = lambda *x:None

        # debug setting
        if args.debug:
            logging.basicConfig(level=logging.DEBUG)

        # get locale data
        match args.dataset:
            case "rtm":
                result = RTM(args.year,args.month,refresh=args.refresh)
            case "dam":
                result = DAM(args.year,args.month,refresh=args.refresh)
            case "_":
                raise ValueError(f"{args.dataset=} is invalid")
        # automatic format
        if args.format is None:
            args.format = "csv" if str(args.output).endswith(".csv") else "table"

        if args.notz:
            result.index = result.index.tz_convert("US/Pacific").tz_localize(None)

        # print result using format
        match args.format:
            case "table":
                pd.options.display.width = None
                pd.options.display.max_columns = None
                pd.options.display.max_rows = None
                print(result,
                    file=open(args.output,"w") if args.output else sys.stdout,
                    )
            case "csv":
                result.to_csv(
                    args.output if args.output else sys.stdout,
                    index=args.index,
                    header=args.header,
                    )
            case "_":
                raise ValueError(f"{args.format} is invalid")
                return E_SYNTAX

        return E_OK

    # pylint: disable=broad-exception-caught
    except Exception as err:

        if hasattr(args,"debug") and getattr(args,"debug"):
            _logger.exception(f"ERROR [caiso]: {err}")
        else:
            _logger.error(f"ERROR [caiso]: {err}")
        return E_FAILED

if __name__ == '__main__':

    pd.options.display.width = None
    pd.options.display.max_columns = None
    pd.options.display.max_rows = None
    
    main("rtm","2018","-M=08","--debug","--notz")
