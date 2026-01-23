"""CAISO day-ahead market data accessor

Example
-------

To obtain the day-ahead market data for August 2020 run the commands

    from caiso import DAM
    print(DAM(2018,8))

which outputs 

                                        MW                                                                                                                                                                          
    market                             DAM                                                                                                                                                                          
    zone                      Caiso_Totals                              NONTAC TAC_ECNTR                               TAC_NCNTR         TAC_NORTH                              TAC_SOUTH                           
    schedule                        Export Generation  Import      Load   Load    Export Generation  Import      Load Generation    Load    Export Generation  Import      Load    Export Generation Import     Load
    timestamp                                                                                                                                                                                                       
    2018-08-01 00:00:00+00:00       2699.0   37874.06  7941.0  42937.80   0.00    1106.0   13312.68  4915.0  21878.62       3.83  116.77    1236.0   20510.28  2870.0  17012.00     357.0    4047.27  156.0  3930.41
    2018-08-01 01:00:00+00:00       2580.0   36089.90  8569.0  42116.20   0.00    1055.0   12108.83  5275.0  21106.89       1.41  112.06    1168.0   20247.32  3250.0  17075.42     357.0    3732.34   44.0  3821.83
    2018-08-01 02:00:00+00:00       2290.0   33720.27  9113.0  40573.06   0.25     906.0   10315.54  5670.0  19822.61       0.15  104.03    1027.0   19876.30  3439.0  16926.21     357.0    3528.28    4.0  3719.96
    2018-08-01 03:00:00+00:00       1802.0   31787.92  9670.0  39429.83   0.76     553.0    9474.66  6573.0  19243.55       0.00   95.29     892.0   19346.29  3097.0  16426.39     357.0    2966.97    0.0  3663.84
    2018-08-01 04:00:00+00:00       1490.0   28732.65  9116.0  37471.02   0.65     356.0    8642.88  6342.0  18294.71       0.00   86.16     777.0   17971.53  2774.0  15619.41     357.0    2118.24    0.0  3470.09
    ...                                ...        ...     ...       ...    ...       ...        ...     ...       ...        ...     ...       ...        ...     ...       ...       ...        ...    ...      ...
    2018-08-31 19:00:00+00:00       1427.0   22788.60  8712.0  31184.28   0.00     501.0    9922.90  5566.0  16655.21      11.64   94.20     621.0   10658.08  2934.0  11532.16     305.0    2195.98  212.0  2902.71
    2018-08-31 20:00:00+00:00       1444.0   23818.38  8858.0  32678.13   0.00     452.0   10096.30  5753.0  17679.48      11.55   97.52     641.0   11311.82  2894.0  11835.36     351.0    2398.71  211.0  3065.77
    2018-08-31 21:00:00+00:00       1583.0   25600.75  9059.0  34176.18   0.00     445.0   10355.65  5866.0  18416.70      11.56  101.73     761.0   12764.58  2985.0  12461.68     377.0    2468.96  208.0  3196.07
    2018-08-31 22:00:00+00:00       1633.0   26490.75  9640.0  35206.38   0.00     478.0   10712.38  6460.0  18879.33      10.03  104.12     761.0   13517.83  2975.0  12872.73     394.0    2250.51  205.0  3350.20
    2018-08-31 23:00:00+00:00       1569.0   27788.52  9440.0  36020.65   0.00     414.0   11983.71  6231.0  19144.67       7.44  104.28     761.0   13815.23  3044.0  13279.85     394.0    1982.14  165.0  3491.85

    [744 rows x 19 columns]
"""

import datetime as dt
from time import sleep
from zipfile import ZipFile
from io import BytesIO, StringIO
from xml.etree import ElementTree as XML
import logging

import pandas as pd
import pytz
import requests

from cache import Cache

_logger = logging.getLogger(__file__)

class DAM(pd.DataFrame):
    """Day-ahead market data frame"""

    SOURCE = "https://oasis.caiso.com/oasisapi/SingleZip?resultformat=6&queryname=ENE_SLRS&version=1&market_run_id=DAM&tac_zone_name=ALL&schedule=ALL&startdatetime={start}&enddatetime={end}"
    """OASIS data source"""

    CACHEDIR = None
    """Cache data folder"""

    def __init__(self,
        year:int,
        month:int|None=None,
        raw:bool=False,
        ):
        """Construct a day-ahead market data frame

        Arguments
        ---------

          - `year`: year for which data is collected

          - `month`: month for which data is collected, default is entire year

          - `raw`: flag to return raw OASIS data instead of structured RTM data
        """
        data = []
        for month in range(1,13) if month is None else [month]:
            cache = Cache(package="oasis",version=0,path=["caiso","DAM",f"{year}_{month:02d}.csv"])
            if cache.exists():
                try:
                    result = pd.read_csv(cache.pathname)
                    _logger.debug(f"{cache=} ok")
                except:
                    cache.remove()
                    result = None
                    _logger.debug(f"{cache=} error, deleted {cache.pathname=}")
            else:
                result = None
                _logger.debug(f"{cache=} (re)generation required")
            if result is None:
                start = dt.datetime(year,month,1,0,0,0,0,pytz.UTC).strftime("%Y%m%dT%H:%M-0000")
                cut = dt.datetime(year,month,15,0,0,0,0,pytz.UTC).strftime("%Y%m%dT%H:%M-0000")
                end = dt.datetime(year+1 if month == 12 else year,month+1 if month < 12 else 1,1,0,0,0,0,pytz.UTC).strftime("%Y%m%dT%H:%M-0000")
                url0 = self.SOURCE.format(start=start,end=cut)
                url1 = self.SOURCE.format(start=cut,end=end)
                result = []
                for url in [url0,url1]:
                    req = None
                    while req is None or req.status_code == 429:
                        _logger.debug(f"downloading {url=}")
                        req = requests.get(url,headers={'Connection':'close'})
                        if req.status_code == 200:
                            content = ZipFile(BytesIO(req.content))
                            for file in content.namelist():
                                with content.open(file,"r") as fh:
                                    try:
                                        text = fh.read().decode("utf-8")
                                        if text.startswith("<?xml"):
                                            xml = XML.fromstring(text.replace("m:",""))
                                            err = xml[1][0][2][1].text
                                            raise RuntimeError(err)
                                        partial = pd.read_csv(
                                            StringIO(text),
                                            parse_dates=[0],
                                            )
                                        partial = partial.sort_values(partial.columns[0])
                                        result.append(partial)
                                    except Exception as err:
                                        _logger.exception(f"{url=} failed with {err=}")
                                        raise
                        elif req.status_code == 429:
                            sleep(1)
                        else:
                            _logger.error(f"{url=} failed with HTML Error {req.status_code}")
                result = pd.concat(result)
                result.to_csv(cache.pathname,index=False,header=True)
                _logger.debug(f"{cache=} updated")
            data.append(result)

        data = pd.concat(data)    

        if not raw:

            columns = {
                'INTERVALSTARTTIME_GMT':"timestamp", 
                'INTERVALENDTIME_GMT':None,
                'SLRS_TYPE': None, 
                'OPR_DT': None,
                'OPR_HR': None,
                'OPR_INTERVAL': None,
                'MARKET_RUN_ID': "market",
                'TAC_ZONE_NAME': "zone",
                'SCHEDULE': "schedule",
                'XML_DATA_ITEM': None,
                'POS': None,
                'MW': "MW",
                'GROUP': None,
                }

            data.drop([x for x,y in columns.items() if y is None],inplace=True,axis=1)
            data.rename({x:y for x,y in columns.items() if y is not None},inplace=True,axis=1)
            data.timestamp = pd.DatetimeIndex(data.timestamp)
            data.set_index(["timestamp","market","zone","schedule"],inplace=True)
            data.sort_index(inplace=True)
            data = data.unstack(level=[1,2,3])

        super().__init__(data)

if __name__ == "__main__":

    # pd.options.display.max_rows = None
    pd.options.display.max_columns = None
    pd.options.display.max_colwidth = None
    pd.options.display.width = None

    logging.basicConfig(level=logging.DEBUG)
    result = DAM(2018,8,raw=False)
    print(result)
