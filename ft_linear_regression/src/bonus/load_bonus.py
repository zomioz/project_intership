import numpy as np
import pandas as pd
from pandas import DataFrame as DataFrame

PERIODS = ("day", "week", "month")
EPOCH = pd.Timestamp("1970-01-01")


def load(path: str) -> DataFrame | None:

    '''
    Function to load a log_time .csv file (login,date,log_time,log_time_minutes)
    Argument: The path of .csv file
    Return: None on fail, a DataFrame on succes with the columns:
            "login", "days" (days since 1970-01-01) and "log_time_minutes"
    '''

    try:
        raw = pd.read_csv(path)
    except (FileNotFoundError, PermissionError, IsADirectoryError):
        print("Error: unable to load csv file")
        return None
    except (pd.errors.EmptyDataError, pd.errors.ParserError, UnicodeDecodeError) as err:
        print("Error: invalid csv file\n", err)
        return None

    if "login" not in raw.columns and "user_id" in raw.columns:
        raw = raw.rename(columns={"user_id": "login"})
    if "date" not in raw.columns or "login" not in raw.columns:
        print("Error: the csv file needs a 'login' (or 'user_id') and a 'date' column")
        return None
    if "log_time_minutes" in raw.columns:
        minutes = pd.to_numeric(raw["log_time_minutes"], errors="coerce")
    elif "log_time" in raw.columns:
        minutes = pd.to_timedelta(raw["log_time"], errors="coerce").dt.total_seconds() / 60
    else:
        print("Error: the csv file needs a 'log_time_minutes' or a 'log_time' column")
        return None

    dates = pd.to_datetime(raw["date"], errors="coerce")
    days = (dates - EPOCH).dt.total_seconds() / 86400

    df = pd.DataFrame({"login": raw["login"].astype(str), "days": days, "log_time_minutes": minutes}).dropna().reset_index(drop=True)
    if len(df) < 2:
        print("Error: not enough valid rows in the csv file")
        return None

    return df


def get_buckets(df: DataFrame, period: str) -> tuple[pd.Series, np.ndarray]:

    '''
    Function that give, for each row, the first day of its week or month, and the first day of
    all the complete periods covered by the file (the first and last periods are often cut)
    Argument: DataFrame from load(), period: "week" (Monday to Sunday) or "month" (calendar month)
    Return: a Series of the first day of the period of each row, the sorted array of the first days
            of the complete periods (days since 1970-01-01)
    '''

    first, last = df["days"].min(), df["days"].max()

    if period == "week":
        bucket = df["days"] - (df["days"] + 3) % 7
        first_start = first - (first + 3) % 7
        if first_start < first:
            first_start += 7
        return bucket, np.arange(first_start, last - 6 + 1, 7)

    dates = pd.to_datetime(df["days"], unit="D")
    bucket = (dates.dt.to_period("M").dt.to_timestamp() - EPOCH).dt.total_seconds() / 86400

    first_date = EPOCH + pd.Timedelta(days=first)
    last_date = EPOCH + pd.Timedelta(days=last)
    first_month = first_date.to_period("M")
    if first_month.start_time < first_date:
        first_month += 1
    last_month = last_date.to_period("M")
    if (last_date + pd.Timedelta(days=1)).month == last_date.month:
        last_month -= 1

    if first_month > last_month:
        return bucket, np.array([])
    starts = pd.period_range(first_month, last_month, freq="M").start_time
    return bucket, ((starts - EPOCH).total_seconds() / 86400).to_numpy()


def to_period(df: DataFrame, period: str) -> DataFrame:

    '''
    Function that sum the log time of each student by week (10080 minutes max) or by month
    Argument: DataFrame from load(), period: "week" or "month"
    Return: DataFrame with the columns "login", "days" (first day of the period, days since 1970-01-01)
            and "log_time_minutes" (total of the period). Only the complete periods of the file are kept,
            a period without any row counts as 0 minutes, except before the first period of presence
            of the student (he was not there yet).
    '''

    bucket, starts = get_buckets(df, period)
    if len(starts) == 0:
        return DataFrame(columns=["login", "days", "log_time_minutes"])

    totals = df.assign(period=bucket).groupby(["login", "period"])["log_time_minutes"].sum().unstack(fill_value=0)
    totals = totals.reindex(columns=starts, fill_value=0)

    result = totals.reset_index().melt(id_vars="login", var_name="days", value_name="log_time_minutes")
    result = result.sort_values(["login", "days"])
    result["days"] = result["days"].astype(float)
    result["log_time_minutes"] = result["log_time_minutes"].astype(float)

    started = result.groupby("login")["log_time_minutes"].cumsum() > 0
    return result[started].reset_index(drop=True)


def load_period(path: str, period: str = "week") -> DataFrame | None:

    '''
    Function to load a log_time .csv file with the log time of each student by day, week or month
    Argument: The path of .csv file, period: "day", "week" or "month"
    Return: None on fail (or less than two complete periods), a DataFrame on succes with the columns
            "login", "days" (first day of the period) and "log_time_minutes" (total of the period)
    '''

    df = load(path)
    if df is None or period == "day":
        return df

    result = to_period(df, period)
    if result["days"].nunique() < 2:
        print("Error: the csv file needs at least two complete " + period + "s")
        return None

    return result
