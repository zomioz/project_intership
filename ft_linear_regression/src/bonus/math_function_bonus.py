from load_bonus import load_period
from get_value_bonus import get_value, output_file

def calculate_precision(login, period="week"):

    '''
    Function that calculate the precision of an linear regression model using RMSE, MSE and R2
    Argument: login of the student, period: "day", "week" or "month"
    Return: 3 values : MSE, RMSE, R2
    '''

    df = load_period("data.csv", period)
    df = df[df["login"] == login].reset_index(drop=True)
    T0, T1 = get_value(output_file(period), login)

    true_price = df["log_time_minutes"]
    predicted_price = T0 + T1 * df["days"]

    mse = calculate_mse(true_price, predicted_price)
    rmse = mse ** 0.5
    r2 = calculate_r2(true_price, predicted_price)
    return mse, rmse, r2


def calculate_mse(true_price, predicted_price):

    '''
    Function that calculate MSE value : Mean squared error
    Argument: True Prices from .csv and Predicted_price from linear regression function
    Return: MSE value
    '''

    total = 0
    n = len(true_price)

    for i in range(n):
        error = true_price[i] - predicted_price[i]
        total += error * error

    return total / n


def calculate_r2(true_price, predicted_price):

    '''
    Function that calculate R2 value : 
    Argument : True Prices from .csv and Predicted_price from linear regression function
    Return: R2 Value
    '''

    n = len(true_price)

    total = 0
    for i in range(n):
        total += true_price[i]
    mean_true = total / n

    ss_res = 0
    ss_tot = 0
    for i in range(n):
        error = true_price[i] - predicted_price[i]
        ss_res += error * error

        diff = true_price[i] - mean_true
        ss_tot += diff * diff

    if ss_tot == 0:
        return 0

    return 1 - (ss_res / ss_tot)