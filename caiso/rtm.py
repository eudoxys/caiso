"""CAISO real-time market data accessor

Example
-------

To obtain the real-time market data for August 2020 run the commands

    from caiso import RTM
    print(RTM(2018,8).resample("1h").mean())

which outputs

                                        MW                                                                                                                                                                                                                                                                                                                                    
    market                             RTM                                                                                                                                                                                                                                                                                                                                    
    zone                      Caiso_Totals                      TAC_AZPS                     TAC_BCHA                     TAC_ECNTR                     TAC_IPCO                     TAC_NCNTR TAC_NEVP                     TAC_NORTH                      TAC_PAC                       TAC_PGE                     TAC_PSEI                     TAC_SOUTH                   
    schedule                        Export Generation    Import   Export Generation   Import   Export Generation   Import    Export Generation   Import   Export Generation  Import Generation   Export Generation   Import    Export Generation   Import   Export Generation    Import   Export Generation   Import   Export Generation   Import    Export Generation  Import
    timestamp                                                                                                                                                                                                                                                                                                                                                                 
    2018-08-01 00:00:00+00:00      3948.25   37083.35  10011.57  6741.24    7709.72  5961.18  3975.14   10470.34  2388.94   1559.18   13372.45  6391.67   541.96    2807.05  963.71       3.10  1339.18    5893.02  3234.61   1675.18   19557.42  3429.30  8810.58    9919.51  11850.73  2526.51    3024.30  3360.43   670.01    2221.76  1292.51    713.89    4150.37  190.60
    2018-08-01 01:00:00+00:00      3840.54   35694.34  10649.08  6642.20    7519.56  5935.16  3837.72   10190.16  2327.67   1701.97   12293.77  6812.48   528.35    2757.45  947.42       1.51  1238.32    5797.08  3162.71   1466.11   19544.36  3775.78  8780.37    9655.59  11796.08  2592.80    3082.49  3257.97   729.59    2239.59  1409.67    672.46    3854.70   60.81
    2018-08-01 02:00:00+00:00      3554.54   33097.78  11223.36  6778.78    7346.66  6057.92  3983.40   10097.76  2354.60   1534.98   10812.52  7205.53   410.88    2741.31  851.37       0.14  1332.97    5517.49  3220.71   1292.66   18717.40  3901.76  8842.57    9663.69  11795.20  2748.98    3092.25  3276.03   700.59    2220.38  1411.18    726.89    3567.73  116.07
    2018-08-01 03:00:00+00:00      3108.76   31256.09  11278.09  6746.36    7397.68  6325.32  3573.75    9541.00  2293.70   1118.94    9738.94  7552.22   169.83    2771.46  731.15       0.00  1321.60    5633.13  2839.01   1259.67   18579.36  3649.88  7857.93    9745.66  10174.21  2565.96    3084.50  2740.93   681.73    2126.11  1256.48    730.16    2937.80   75.99
    2018-08-01 04:00:00+00:00      3264.80   29100.48  11037.90  6955.58    7356.47  6462.00  2366.46    8126.26  2187.21   1297.26    9116.40  7576.77   145.04    2724.72  689.92       0.00  1169.05    5704.07  2141.04   1221.07   17608.17  3326.79  7639.88    9753.48   9694.31  2701.42    3007.67  2749.10   886.94    2057.32  1283.10    746.47    2375.91  134.33
    ...                                ...        ...       ...      ...        ...      ...      ...        ...      ...       ...        ...      ...      ...        ...     ...        ...      ...        ...      ...       ...        ...      ...      ...        ...       ...      ...        ...      ...      ...        ...      ...       ...        ...     ...
    2018-08-31 19:00:00+00:00      3152.33   23876.99   9974.18  7325.43    6909.04  5207.33   429.03    7102.88   460.32   1632.89   10414.64  6487.56   503.21    2094.85  645.09      13.54   560.04    4169.38  1682.92    891.52   10949.95  3152.67  6658.23    9018.34   7374.86  2162.55    2205.89  2405.55   658.42    1678.48  1775.51    627.92    2498.86  333.95
    2018-08-31 20:00:00+00:00      3075.73   24540.02  10007.65  7315.20    7005.58  5510.42   504.11    7078.20   545.77   1551.19   10627.50  6654.30   460.42    2058.63  603.09      13.51   575.06    4306.81  1708.53    841.17   11380.35  3047.48  6822.72    9828.09   7446.76  2138.21    2219.52  2385.34   563.88    1721.25  1677.21    683.38    2518.66  305.86
    2018-08-31 21:00:00+00:00      3264.14   26084.44  10276.52  7365.21    7029.16  5638.46   533.67    6734.04   873.42   1606.08   11287.63  6854.59   426.08    2049.12  562.42      11.80   606.21    4525.01  1843.45    950.72   12271.63  3110.57  6983.46   10116.65   7695.50  2164.13    2214.64  2405.76   567.13    1709.50  1613.72    707.34    2513.38  311.37
    2018-08-31 22:00:00+00:00      3416.12   26993.59  11126.93  7399.09    7374.78  5842.99  1149.87    7072.71   976.00   1566.53   11992.15  7557.32   511.08    2185.98  648.67       9.32   726.94    4655.33  1988.08   1118.42   12586.75  3263.39  7263.93    9797.46   8025.40  2187.55    2178.47  2421.66   634.14    1777.38  1712.60    731.17    2405.37  306.22
    2018-08-31 23:00:00+00:00      3204.74   28402.03  10828.21  7407.51    7544.22  5825.71   993.84    6428.77  1514.22   1668.43   12360.49  7488.61   259.63    2217.04  411.75       8.12   743.44    4636.10  2047.88    828.10   13589.41  3096.92  7227.98   10260.62   7927.65  2055.59    2251.69  2227.26   590.50    1938.30  1489.37    708.21    2444.02  242.69

    [744 rows x 34 columns]

References
----------

  - https://developer.caiso.com/Artifacts/OASIS/Report-URLs-for-OASIS.docx
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

class RTM(pd.DataFrame):
    """Real-time market data frame"""
    
    SOURCE = "https://oasis.caiso.com/oasisapi/SingleZip?resultformat=6&queryname=ENE_SLRS&version=1&market_run_id=RTM&tac_zone_name=ALL&schedule=ALL&startdatetime={start}&enddatetime={end}"
    """OASIS data source"""

    CACHEDIR = None
    """Cache data folder"""

    PRECISION = 2
    """Data rounding precision"""

    def __init__(self,
        year:int,
        month:int|None=None,
        freq:str|None="1h",
        raw:bool=False,
        refresh:bool=False,
        ):
        """Construct a real-time market data frame

        Arguments
        ---------

          - `year`: year for which data is collected

          - `month`: month for which data is collected, default is entire year

          - `raw`: flag to return raw OASIS data instead of structured RTM data

          - `refresh`: force refresh of local data cache
        """
        data = []
        for month in range(1,13) if month is None else [month]:
            cache = Cache(package="oasis",version=0,path=["caiso","RTM",f"{year}_{month:02d}.csv.gz"])
            if cache.exists() and not refresh:
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
                result.to_csv(cache.pathname,
                    index=False,
                    header=True,
                    compression="gzip" if cache.pathname.endswith(".gz") else None,
                    )
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
            if isinstance(freq,str):
                data = data.resample(freq).mean()

        super().__init__(data.round(self.PRECISION))

if __name__ == "__main__":

    # pd.options.display.max_rows = None
    pd.options.display.max_columns = None
    pd.options.display.max_colwidth = None
    pd.options.display.width = None

    logging.basicConfig(level=logging.DEBUG)
    result = RTM(2018,8)
    print(result)
