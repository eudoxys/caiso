"""California ISO market data accessor"""

import sys
import argparse
import pathlib
import warnings
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

def main(*args:list[str]) -> int:
    """California ISO market data accessor main command line processor

    Arguments
    ---------

      - `*args`: command line arguments (`None` is `sys.argv`)

    Returns
    -------

      - `int`: return/exit code (see `E_*` codes)
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
            choices=["rtm","dam","help"],
            help="specify the market dataset")
        parser.add_argument("year",
            type=int,
            help="specify the year")
        parser.add_argument("-m","--month",
            type=int,
            help="specify the month")

        parser.add_argument("--debug",
            action="store_true",
            help="enable debug traceback on exceptions",
            )
        parser.add_argument("-f","--format",
            choices={"table","csv"},
            default="table",
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

        # handle help request
        if args.dataset == "help":
            print(__doc__)
            return E_OK

        # get locale data
        match args.dataset:
            case "rtm":
                result = RTM(args.year,args.month).resample("1h").mean()
            case "dam":
                result = DAY(args.year,args.month)
            case "_":
                raise ValueError(f"{args.dataset=} is invalid")

        # print result using format
        match args.format:
            case "table":
                print(result)
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

        raise
        if hasattr(args,"debug") and getattr(args,"debug"):
            raise

        print(f"ERROR [caiso]: {err}")
        return E_FAILED

if __name__ == '__main__':

    pd.options.display.width = None
    pd.options.display.max_columns = None
    pd.options.display.max_rows = None
    
    main("rtm",2018,"-M=8","--debug")
