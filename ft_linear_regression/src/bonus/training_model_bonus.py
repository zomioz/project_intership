from load_bonus import load_period
from get_value_bonus import output_file

def linear_regression(df, number_of_iteration) -> tuple[float, float]:

    '''
    Function that execute an linear regression on a dataframe
    argument: Dirst: Dataframe. Second: number of iteration for the linear regression
    return: The two θ for the prediction
    '''

    learningRate = 0.1
    x = df.iloc[:, 0].to_numpy(dtype=float)
    y = df.iloc[:, 1].to_numpy(dtype=float)
    m = len(df)
    T0 = 0.0
    T1 = 0.0

    for _ in range(number_of_iteration):

        error = (T0 + (T1 * x)) - y
        TmpT0 = error.sum()
        TmpT1 = (error * x).sum()

        T0 = T0 - learningRate * (1 / m) * TmpT0
        T1 = T1 - learningRate * (1 / m) * TmpT1

    return T0, T1

def train_student(df, number_of_iteration) -> tuple[float, float] | None:

    '''
    Function that normalize the data of ONE student and execute the linear regression on it
    argument: Dataframe with the columns "days" (first day of the period) and "log_time_minutes" (total of the period) of one student. Number of iteration
    return: The two real θ (log time of the period = θ0 + θ1 * days), None if the student has less than two different periods
    '''

    df_normalized = df[["days", "log_time_minutes"]].astype(float)

    days_min = df_normalized.iloc[:, 0].min()
    days_range = df_normalized.iloc[:, 0].max() - days_min
    if days_range == 0:
        return None
    df_normalized.iloc[:, 0] = (df_normalized.iloc[:, 0] - days_min) / days_range

    time_min = df_normalized.iloc[:, 1].min()
    time_range = df_normalized.iloc[:, 1].max() - time_min
    if time_range == 0:
        time_range = 1.0
    df_normalized.iloc[:, 1] = (df_normalized.iloc[:, 1] - time_min) / time_range

    T0, T1 = linear_regression(df_normalized, number_of_iteration)

    T1_real = T1 * (time_range / days_range)
    T0_real = time_min + (time_range * T0) - (T1_real * days_min)
    return T0_real, T1_real

def training_model(period="week"):

    '''
    Main function it load the data file and execute one linear regression per student on his log time by day, week or month
    argument : period: "day", "week" or "month"
    return : False if the training is impossible, True otherwise
    '''

    df = load_period("data.csv", period)
    if df is None:
        return False

    number_of_iteration = 1000
    results = []
    for login, df_student in df.groupby("login", sort=True):
        thetas = train_student(df_student, number_of_iteration)
        if thetas is not None:
            results.append((login, float(thetas[0]), float(thetas[1])))

    if not results:
        return False

    with open(output_file(period), "w") as f:
        print("login,theta0,theta1", file=f)
        for login, T0, T1 in results:
            print(login, T0, T1, sep=",", file=f)

    return True
