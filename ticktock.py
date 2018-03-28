import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.interpolate import spline
import datetime as dt
import calendar
import re
import warnings

def convert_columns(df):
    """
    Return df with columns converted to proper datatypes (Event to string, times to datetime).
    Params:
        df: dataframe with columns 'Event', 'Start_time', and 'End_time'.
    """
    df['Event'] = df['Event'].astype(str)
    df['Start_time'] = pd.to_datetime(df['Start_time'])
    df['End_time'] = pd.to_datetime(df['End_time'])
    return df


def filter_by_date(pd, date_start, date_end):
    """
    Return dataframe with rows where 'Start_time' is between date_start and date_end.
    Params:
        pd: dataframe with 'Start_time' column
        date_start: string with start date in MM/DD/YYYY format
        date_end: string with end date in MM/DD/YYYY format
    """
    start = dt.datetime.strptime(date_start, "%m/%d/%Y")
    end = dt.datetime.strptime(date_end, "%m/%d/%Y")
    return pd[(pd['Start_time'] > start) & (pd['End_time'] < end)]


def total_time(x):
    """
    Return total length, in hours, of an event.
    Params:
        x: dataframe row with 'Start_time' and 'End_time' columns
    """
    return (x['End_time'] - x['Start_time']).total_seconds() / 3600


def is_studying(event, subject):
    """
    Return True if event is about studying the subject, False otherwise.
    Params:
        event: string with event summary
        subject: string
    """
    regex_str = r"study.*{}".format(subject)
    if re.search(regex_str, event, re.IGNORECASE):
        return True
    return False


def create_plot(figsize=(15,6), title="", xlabel="", ylabel=""):
    """
    Create matplotlib plot with provided parameters. Returns fig, ax.
    """
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    return fig, ax


def group_by_week(df, quarter_start, function="size"):
    """
    Return dataframe with total time grouped by week, using the function provided.
    By default, the function is 'size' to compute the number of events that week.
    Params:
        df: dataframe with date index and 'total time' column
        quarter start: string containing quarter start date in "%m/%d/%Y" format
    """
    week_0 = dt.datetime.strptime(quarter_start, "%m/%d/%Y").isocalendar()[1] 
    if function == "sum":
        by_week = df.groupby(lambda x: x.isocalendar()[1] - week_0, as_index=True).sum()
    elif function == "mean":
        by_week = df.groupby(lambda x: x.isocalendar()[1] - week_0, as_index=True).mean()
    elif function == "size":
        by_week = df.groupby(lambda x: x.isocalendar()[1] - week_0, as_index=True).size()
    return by_week


def group_by_weekday(df, function="size"):
    """
    Return dataframe with data grouped by weekday using function.
    Params:
        df: Series with dates as index.
    """
    if function == "mean":
        result = df.groupby(lambda x: calendar.day_name[x.weekday()], as_index=True).mean()
    elif function == "size":
        result = df.groupby(lambda x: calendar.day_name[x.weekday()], as_index=True).size()
    return result


def is_workout(event, workout_type):
    """
    Return True if event is of a certain workout type (e.g. run, swim), False otherwise.
    Params:
        event: string with event summary
        workout_type: string
    """
    regex_str = r".*{}.*".format(workout_type)
    if re.search(regex_str, event, re.IGNORECASE):
        return True
    return False


def run_length(event):
    """
    Return the length of a run, in miles, if the event is a run. Otherwise, return 0.
    Params:
        event: string with event description
    """
    regex_str = r"(\d+.?\d*).*run"
    mo = re.search(regex_str, event, re.IGNORECASE)
    if mo:
        return float(mo.group(1))
    else:
        return 0


def is_mock_related(event):
    """
    Return True if an event is mock trial related, False otherwise.
    Params:
        event: string holding event description
    """
    regex_str = r".*(Mock|MT|Invitational|Tournament|Regionals|ORCS|Direct|Equal).*"
    mo = re.search(regex_str, event, re.IGNORECASE)
    if mo:
        return True
    return False


def is_tournament(event):
    """
    Return True if an event is a tournament related, False otherwise.
    Params:
        event: string holding event description
    """
    regex_str = r".*(Invitational|Tournament|Regionals|ORCS).*"
    mo = re.search(regex_str, event, re.IGNORECASE)
    if mo:
        return True
    return False
    