import pandas as pd

def launch_algorithm(log_time, promo_2026, df):
    with pd.option_context("display.max_rows", None,
                   "display.max_columns", None,
                   "display.max_colwidth", None,
                   "display.width", None):
        print(log_time)
        #print(promo_2026)
        #print(df)