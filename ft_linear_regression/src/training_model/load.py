import pandas as pd
from pandas import DataFrame as DataFrame


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
    days = (dates - pd.Timestamp("1970-01-01")).dt.total_seconds() / 86400

    df = pd.DataFrame({"login": raw["login"].astype(str), "days": days, "log_time_minutes": minutes}).dropna().reset_index(drop=True)
    if len(df) < 2:
        print("Error: not enough valid rows in the csv file")
        return None

    print("Loading DataFrame of dimension : " + "(",
          df.shape[0], ",", df.shape[1], ")", "for", df["login"].nunique(), "students")
    return df
