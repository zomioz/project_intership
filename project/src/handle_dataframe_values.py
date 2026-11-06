import pandas as pd
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).resolve().parent.parent / '.env', override=True)

def add_log_time_minutes(csv_name="log_time.csv"):

    '''
    Add a log_time_minutes column to the csv: 02:00:00 -> 120.0 (rounded to 0.01).
    The original log_time column is kept, so scrap_log_time still reads the file.
    Safe to run several times.
    '''

    csv_path = Path(__file__).resolve().parent.parent / csv_name
    df = pd.read_csv(csv_path)
    df["log_time_minutes"] = (pd.to_timedelta(df["log_time"]).dt.total_seconds() / 60).round(2)
    df.to_csv(csv_path, index=False)
    return df

def replace_id_by_login(df_log, df_users):

    '''
    Replace the user_id of df_log (index level "user_id") by the user login.
    Argument: df_log indexed by user_id (ex: from scrap_log_time),
              df_users in the long format USER_ID | SECTION | ROW | FIELD | VALUE
              containing the "login" field (ex: promo_2026)
    Return: a copy of df_log where user_id is the login (unknown ids are kept as is)
    '''

    logins = df_users.xs("login", level="field")["value"].droplevel(["section", "row"])
    return df_log.rename(index=logins.to_dict(), level="user_id").rename_axis(index={"user_id": "login"})


def create_login_log_time_csv(df_users, csv_name="log_time.csv", output_name="login_log_time.csv"):

    '''
    Create a csv from log_time.csv where the user_id column is replaced by a login column.
    Argument: df_users in the long format USER_ID | SECTION | ROW | FIELD | VALUE
              containing the "login" field (ex: promo_2026),
              name of the source csv, name of the csv to create
    Return: the DataFrame written in output_name (unknown ids are kept as is)
    '''

    base_path = Path(__file__).resolve().parent.parent
    df = pd.read_csv(base_path / csv_name)

    logins = df_users.xs("login", level="field")["value"].droplevel(["section", "row"])
    logins = logins[~logins.index.duplicated()].to_dict()
    df["user_id"] = df["user_id"].map(lambda user_id: logins.get(user_id, user_id))
    df = df.rename(columns={"user_id": "login"})

    df.to_csv(base_path / output_name, index=False)
    return df
