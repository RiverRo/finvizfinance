"""
.. module:: future
   :synopsis: future.

.. moduleauthor:: Tianning Li <ltianningli@gmail.com>
"""

import json
import re
import pandas as pd
from finvizfinance.util import web_scrap


class Future:
    """Future
    Getting information from the finviz future page.
    """

    def __init__(self):
        """initiate module"""
        pass

    def performance(self, timeframe="D"):
        """Get forex performance table.

        Args:
            timeframe (str): choice of timeframe(D, W, M, Q, HY, Y)

        Returns:
            df(pandas.DataFrame): forex performance table
        """
        timeframe_dict = {"W": 12, "M": 13, "Q": 14, "HY": 15, "Y": 16}
        params = {}
        if timeframe in timeframe_dict:
            params["v"] = timeframe_dict[timeframe]
        elif timeframe != "D":
            raise ValueError("Invalid timeframe '{}'".format(timeframe))

        soup = web_scrap("https://finviz.com/futures_performance.ashx", params)

        # Rows are passed inline: window.FinvizInitFuturesPerformance([...])
        match = re.search(
            r"FinvizInitFuturesPerformance\((\[.*?\])\)", str(soup), re.DOTALL
        )
        if match is None:
            raise ValueError("Futures performance data not found on page")
        data = json.loads(match.group(1))
        df = pd.DataFrame(data)
        return df
