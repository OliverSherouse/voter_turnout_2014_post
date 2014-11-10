#! /usr/bin/env python
# Copyright Oliver Sherouse, http://oliversherouse.com
# Release under CC BY-NC-SA 4.0, available from
# http://creativecommons.org/licenses/by-nc-sa/4.0/
"""
create_plots.py

Create a series of plots on voter turnout in the 2014 general election by type
of voter ID law.
"""
import sys

import pandas as pd
import seaborn as sb
import numpy as np

from pathlib import Path

from matplotlib import pyplot as plt
from matplotlib import ticker as tkr


PROJ_DIR = Path(sys.argv[0]).absolute().parents[0]
DATA_DIR = PROJ_DIR.joinpath("data")
IMG_DIR = PROJ_DIR.joinpath("img")

ATTR = """Source: Michael P. McDonald, http://www.electproject.org/2014g, and
LongDistanceVoter.org, http://www.longdistancevoter.org/2014-voter-id-laws
Visualization by Oliver Sherouse, http://oliversherouse.com"""

sb.set_style("white")


def get_turnout():
    """
    Read in data and merge
    """
    turnout = pd.read_csv(str(DATA_DIR.joinpath("turnout.csv")),
                          skiprows=1, usecols=[0, 2])
    turnout.columns=["state", "turnout"]
    turnout["turnout"] = turnout["turnout"].apply(
        lambda x: float(x.strip("%")) / 100)
    turnout = turnout.merge(pd.read_csv(str(DATA_DIR.joinpath("idlaws.csv"))),
                            how="left")
    turnout["law"] = turnout["law"].map(
        {"photo": "Photo ID", "nonphoto": "Non-Photo ID", np.nan: "No ID"})
    return turnout


def plot(data, title, figpath, set_bounds=True, **kwargs):
    """
    Generic plotting function
    """
    sb.factorplot("law", "turnout", data=data, **kwargs) 
    ax = plt.gca()
    if set_bounds:
        ax.set_ybound(0, .5) # keep bounds the same for comparison
    ax.yaxis.set_major_formatter(
        tkr.FuncFormatter(lambda x, y: "{:.0%}".format(x)))
    plt.title(title, size="large")
    plt.xlabel("")
    plt.text(ax.get_xbound()[-1],
             (lambda x: x[0] - .15 * (x[1] - x[0]))(ax.get_ybound()),
             ATTR, ha="right")
    plt.gcf().set_size_inches(8, 6)
    plt.savefig(str(figpath), bbox_inches="tight")


def main():
    turnout = get_turnout()
    plot(turnout, "Mean 2014 State Turnout by Voter ID Law",
         IMG_DIR.joinpath("mean.png"), kind="bar", ci=0)
    plot(turnout,
         "Mean 2014 State Turnout by Voter ID Law with Confidence Intervals",
         IMG_DIR.joinpath("mean_ci.png"), kind="bar")
    plot(turnout, "Median 2014 State Turnout by Voter ID Law",
         IMG_DIR.joinpath("median.png"), kind="bar", estimator=np.median, ci=0)
    plot(turnout, "2014 State Turnout Distribution by Voter ID Law",
         IMG_DIR.joinpath("box.png"), kind="box", set_bounds=False)    


if __name__ == "__main__":
    main()
