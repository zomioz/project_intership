import pandas as pd
from get_value import get_value


def main() -> None:

    '''
    main function that calculate the log time (in minutes) of a student on a given day based on his linear regression model
    argument: None
    return: None
    '''

    try:
        print("Welcome to the prediction program. Enter the login of the student :")
        login = input().strip()
        print("Enter a date (YYYY-MM-DD) :")
        date = pd.to_datetime(input().strip(), format="%Y-%m-%d")
    except (ValueError, TypeError, KeyboardInterrupt, EOFError) as err:
        print("Error: thanks to enter a valid login and a valid date (YYYY-MM-DD)\n", err)
        return

    thetas = get_value("output.csv", login)
    if thetas is None:
        return
    T0, T1 = thetas

    days = (date - pd.Timestamp("1970-01-01")).total_seconds() / 86400
    minutes = T0 + (T1 * days)
    minutes_formatted = "{:.2f}".format(minutes)
    if minutes < 0:
        return print("Error: the log time should be :", minutes_formatted, "minutes, a log time cannot be negative")
    hours, rest = divmod(int(round(minutes)), 60)
    print("The log time of the student", login, "on", date.strftime("%Y-%m-%d"), "will be :", minutes_formatted, "minutes (" + str(hours) + "h" + "{:02d}".format(rest) + ")")

if __name__ == "__main__":
    main()
