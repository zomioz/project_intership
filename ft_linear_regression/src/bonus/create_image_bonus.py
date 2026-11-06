import matplotlib.pyplot as plt
import pandas as pd
from get_value_bonus import get_value, output_file
from load_bonus import load_period

LABELS = {"day": "date", "week": "week (Monday)", "month": "month"}

# Hours per week of each pace
PACES = {"PACE8": 61, "PACE12": 35, "PACE15": 25, "PACE18": 19, "PACE22": 15, "PACE24": 10}
# Number of weeks in a period: a month is 4 weeks (PACE8 = 61h/week = 244h/month)
WEEKS_PER_PERIOD = {"day": 1 / 7, "week": 1, "month": 4}


def pace_minutes(period: str) -> dict[str, float]:

    '''
    Function that convert the pace (hours per week) in minutes for a day, a week or a month
    Argument: period: "day", "week" or "month"
    Return: a dict pace name -> minutes per period (ex: PACE8 per day: 61 * 60 / 7 = 522.86)
    '''

    return {name: hours * 60 * WEEKS_PER_PERIOD[period] for name, hours in PACES.items()}


def create_image(login, period="week"):

    '''
    Function that create graphics in .png from a .csv and an output linear regresion file
    Argument: login of the student, period: "day", "week" or "month"
    return: None
    '''

    df = load_period("data.csv", period)
    df = df[df["login"] == login]
    T0, T1 = get_value(output_file(period), login)

    days = df['days'].values
    dates = pd.to_datetime(days, unit='D')
    log_time = df['log_time_minutes'].values

    plt.scatter(dates, log_time)
    plt.xlabel(LABELS[period])
    plt.gcf().autofmt_xdate()
    plt.ylabel('log time per ' + period + ' (minutes)')
    plt.title('Log time per ' + period + ' of the student ' + str(login))
    plt.savefig("bonus_regression_scatter.png", dpi=100, bbox_inches="tight", pad_inches=0.3)

    regression_function = T0 + T1 * days

    plt.clf()
    plt.plot(dates, regression_function, color='red')
    plt.xlabel(LABELS[period])
    plt.gcf().autofmt_xdate()
    plt.ylabel('log time per ' + period + ' (minutes)')
    plt.title('Log time per ' + period + ' from linear regression function of the student ' + str(login))
    plt.savefig("bonus_regression_linearfunction.png", dpi=100, bbox_inches="tight", pad_inches=0.3)

    plt.scatter(dates, log_time)
    colors = ["tab:orange", "tab:green", "tab:purple", "tab:brown", "tab:pink", "tab:gray"]
    for i, (name, minutes) in enumerate(pace_minutes(period).items()):
        plt.axhline(minutes, color=colors[i], linestyle="--", linewidth=1,
                    label=name + " (" + "{:.1f}".format(minutes / 60) + "h)")
    plt.legend(title="Pace per " + period, loc="upper left", bbox_to_anchor=(1.02, 1), fontsize=8)
    plt.xlabel(LABELS[period])
    plt.gcf().autofmt_xdate()
    plt.ylabel('log time per ' + period + ' (minutes)')
    plt.title('Log time per ' + period + ' and linear regression function of the student ' + str(login))
    plt.savefig("bonus_regression_all.png", dpi=100, bbox_inches="tight", pad_inches=0.3)
    plt.close("all")
