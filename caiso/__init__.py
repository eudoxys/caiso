"""California ISO market operations data

Usage
-----

    caiso {rtm,dam} year [-M|--month MONTH] 
          [--refresh] [--header] [--index] [--notz] 
          [-f|--format {csv,table}] [-o|--output OUTPUT] 
          [-h|--help] [--debug] [--warning] 

Positional arguments
--------------------

  - `dam`: get day-ahead market data

  - `rtm`: get real-time market data

  - `year`: market data year

Optional arguments
------------------

  - `--debug`: enable traceback on exceptions

  - `-f|--format FORMAT`: specify format. Valid formats are `table`(the default)
    to output a human readable data frame format, or `csv` to output in machine
    readable CSV format.

  - `--header`: omit CSV header output

  - `--index`: omit CSV index output

  - `-h|--help`: get online documentation

  - `-M|--month`: specify month

  - `--notz`: convert date/time values to local (US/Pacific) timezone and omit
    timezone specification from timestamps

  - `-o|--output`: specify CSV output filename (default is `/dev/stdout`)

  - `--warning`: enable warning messages

Example
-------

To obtain the real-time market data for August 2020 use the
command

    caiso rtm 2020 -M=8

which outputs the following

                                        MW                                                                                                                                                                                                                                                                                                                                                                                                                                           
    market                             RTM                                                                                                                                                                                                                                                                                                                                                                                                                                           
    zone                      Caiso_Totals                       TAC_AZPS                      TAC_BANCSMUD                     TAC_BCHA                     TAC_ECNTR                     TAC_IPCO                      TAC_NCNTR TAC_NEVP                     TAC_NORTH                       TAC_PAC                       TAC_PGE                     TAC_PSEI                     TAC_SCL                    TAC_SOUTH                     TAC_SRP                     TAC_NCNTR
    schedule                        Export Generation    Import    Export Generation    Import       Export Generation   Import   Export Generation   Import    Export Generation   Import   Export Generation   Import Generation   Export Generation   Import    Export Generation   Import    Export Generation    Import   Export Generation   Import   Export Generation   Import  Export Generation  Import    Export Generation  Import   Export Generation   Import    Import
    timestamp                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
    2020-08-01 00:00:00+00:00      9624.94   38178.01  11481.78  14623.08    8279.19  14543.50       264.76     913.45   971.63  3122.46    9597.00  1560.44   7551.35   17195.76  7427.38   394.63    2865.69   958.94      69.66  1594.65    6020.33  3930.46   1323.38   17174.53  3811.12   7358.67   10244.71   9816.77  2445.97    2883.75  2693.89  1005.77    2175.02  1762.15  219.75     703.25  583.62    750.21    3738.07  243.29  3432.67    5440.14  5923.96       NaN
    2020-08-01 01:00:00+00:00      9451.12   37272.28  12534.51  14886.42    8198.84  14711.33       263.17     941.95   930.50  3201.87    9488.13  1563.05   7107.56   16328.09  7970.24   344.75    2832.58   909.11      47.52  1909.96    5667.27  4316.00   1714.64   17231.37  4411.26   7856.40    9648.16  10254.82  2445.21    2873.77  2760.89   937.24    2183.69  1654.82  315.06     827.84  587.22    628.91    3665.30  153.01  3381.67    5414.87  5789.71       NaN
    2020-08-01 02:00:00+00:00      8908.98   34024.28  13371.24  14565.25    7893.05  14506.14       265.00    1327.41   837.54  3324.43    9310.77  1591.68   6921.64   14286.21  8742.94   394.54    2928.54   960.46      15.25  1594.21    5298.14  4061.82   1461.59   16433.32  4425.64   7186.16    9243.21   9479.25  2447.42    2832.03  2719.27  1056.89    2272.11  1724.10  332.86     884.83  606.15    525.75    3289.49  202.67  3655.08    5378.81  5669.42       NaN
    .
    .
    .
    2020-08-31 21:00:00+00:00      3501.97   26335.30   9268.01  10631.78    7509.10  10040.78       204.05    1178.10   647.47  3344.31    9401.46  1313.31   1601.86    9480.05  5857.13    54.17    2272.28   487.09      68.90   901.05    5021.84  2076.19   1348.41   13812.04  3113.75   4442.01    8852.19   4643.67  2125.67    2126.99  2421.80   589.68    1777.13  1449.14  111.80     255.00  621.67    551.70    2974.31  297.13  2488.17    4209.82  2524.29       NaN
    2020-08-31 22:00:00+00:00      3490.25   27469.15   9462.09  10588.32    7563.48   9962.40       202.30    1190.14   822.37  3263.50    9376.45  1307.53   1520.48   10116.87  5867.38   141.67    2286.59   491.84      65.18  1016.08    5303.50  2202.40   1347.31   14433.60  3257.26   4882.73    9212.04   4991.86  2173.17    2271.87  2624.85   564.57    1776.49  1393.23  118.22     285.43  626.34    622.46    2853.50  337.45  2485.83    4285.68  2627.38       NaN
    2020-08-31 23:00:00+00:00      4185.61   28401.52  10795.80  10842.03    7472.93  10223.28       231.38     857.15   870.67  3088.97    9196.14  1297.72   1873.39   10572.54  6550.48    54.17    2350.54   556.09      66.14  1188.62    5741.29  2380.12   1757.55   15057.01  3983.22   5249.64    9027.83   5385.60  2178.75    2246.86  2463.97   575.39    1848.19  1389.97  122.60     238.79  631.51    554.67    2705.84  262.09  2508.08    4118.18  2622.79       NaN
"""

from caiso.dam import DAM
from caiso.rtm import RTM
from caiso.cli import main
