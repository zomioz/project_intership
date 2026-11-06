import pandas as pd


def output_file(period: str) -> str:

    '''
    fuction that give the name of the file where the models of a period (day, week or month) are saved
    argument: period
    return: the name of the file
    '''

    return "output_bonus_" + period + ".csv"


def get_students(path: str) -> list[str]:

    '''
    fuction that list the students having a trained model
    argument: path of the file (login,theta0,theta1)
    return: a list of login, empty if the file is not found
    '''

    try:
        df = pd.read_csv(path, dtype={"login": str})
    except (FileNotFoundError, PermissionError, IsADirectoryError, pd.errors.EmptyDataError):
        return []

    return list(df["login"])


def get_value(path: str, login: str) -> tuple[float, float]:

    '''
    fuction that gather linear regression output of one student from a file
    argument: path of the file, login of the student
    return: a Tuple that contain both θ, (0, 0) if the file or the student is not found
    '''

    try:
        df = pd.read_csv(path, dtype={"login": str})
    except (FileNotFoundError, PermissionError, IsADirectoryError, pd.errors.EmptyDataError):
        return 0, 0

    row = df[df["login"] == login]
    if row.empty:
        return 0, 0

    return float(row["theta0"].iloc[0]), float(row["theta1"].iloc[0])
