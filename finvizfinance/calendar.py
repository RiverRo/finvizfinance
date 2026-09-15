"""
.. module:: calendar
   :synopsis: calendar.

.. moduleauthor:: Tianning Li <ltianningli@gmail.com>
"""

import json
import pandas as pd
from finvizfinance.util import web_scrap


class Calendar:
    """Calendar
    Getting information from the finviz calendar page.
    """

    def __init__(self):
        """initiate module"""
        pass

    def calendar(self):
        """Get economic calendar table.

        Returns:
            df(pandas.DataFrame): economic calendar table
        """
        soup = web_scrap("https://finviz.com/calendar/economic")
        # Events are embedded as JSON rather than rendered as tables.
        script = soup.find("script", id="route-init-data")
        if script is None:
            raise ValueError("Economic calendar data not found on page")
        entries = json.loads(script.string)["data"]["entries"]

        impact_dict = {1: "low", 2: "medium", 3: "high"}
        frame = []
        for entry in entries:
            info_dict = {
                "Datetime": entry["date"],
                "Release": entry["event"],
                "Impact": impact_dict.get(entry["importance"], entry["importance"]),
                "For": entry["reference"],
                "Actual": entry["actual"],
                "Expected": entry["forecast"],
                "Prior": entry["previous"],
            }
            frame.append(info_dict)
        return pd.DataFrame(frame)
