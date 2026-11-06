import time
import pandas as pd
from pathlib import Path
from api import load_or_scrap, create_token, scrap_from_api, scrap_log_time, add_log_time_minutes
from get_values import get_value_users, get_value_section, get_value_row, get_value_field, search
from creation_dataframe import to_long_dataframe
from handle_dataframe_values import add_log_time_minutes, replace_id_by_login, create_login_log_time_csv
from algo import launch_algorithm

def print_informations(df):

    with pd.option_context("display.max_rows", None,
                           "display.max_columns", None,
                           "display.max_colwidth", None,
                           "display.width", None):

        login_df = search(df, section="user")
        print(login_df)

def main():

    try:
        df = load_or_scrap("all_users_campusid_2025.csv", "campus/31/users?filter[pool_year]=2025")
    except Exception as e:
        print(e)
        return

    promo_2026 = search(df, field=["login", "pool_year", "pool_month", "active?"],
                             filters={"active?": "True",
                                      "pool_year": 2025,
                                      "pool_month": ["august", "july", "september"]})

    ids = promo_2026.index.get_level_values("user_id").unique()

    try:
        user_log_time = scrap_log_time(ids, csv_name="log_time.csv", per_page=100, requests_per_second=2)
        add_log_time_minutes("log_time.csv")
        create_login_log_time_csv(promo_2026, "log_time.csv", "login_log_time.csv")
        user_log_time = replace_id_by_login(user_log_time, promo_2026)
    except Exception as e:
        print(e)
        return

        print(user_log_time)

    launch_algorithm(user_log_time, promo_2026, df)

if __name__ == "__main__":  
    main()