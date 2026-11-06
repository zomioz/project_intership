import sys
from load import load
from linear_function import linear_regression

def train_student(df, number_of_iteration) -> tuple[float, float] | None:

    '''
    Function that normalize the data of ONE student and execute the linear regression on it
    argument: Dataframe with the columns "days" and "log_time_minutes" of one student. Number of iteration
    return: The two real θ (log time = θ0 + θ1 * days), None if the student has less than two different dates
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


def main() -> None:

    '''
    Main function it load the data file and execute one linear regression per student
    (x = date in days, y = log time in minutes)
    argument : optional path of the csv file (default: data.csv)
    return : None
    '''

    path = sys.argv[1] if len(sys.argv) > 1 else "data.csv"
    df = load(path)
    if df is None:
        return

    number_of_iteration = 1000
    results = []
    for login, df_student in df.groupby("login", sort=True):
        thetas = train_student(df_student, number_of_iteration)
        if thetas is None:
            print("Skipped student", login, ": needs at least two different dates")
            continue
        results.append((login, thetas[0], thetas[1]))
        print("student", login, "->", len(df_student), "days : θ0 =", "{:.4f}".format(thetas[0]), "θ1 =", "{:.4f}".format(thetas[1]))

    if not results:
        print("Error: no student could be trained")
        return

    with open("output.csv", "w") as f:
        print("login,theta0,theta1", file=f)
        for login, T0, T1 in results:
            print(login, float(T0), float(T1), sep=",", file=f)

    print("After the linear regression:", len(results), "students saved in output.csv")


if __name__ == "__main__":
    main()
