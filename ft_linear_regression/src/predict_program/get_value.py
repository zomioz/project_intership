import pandas as pd


def get_value(path: str, login: str) -> tuple[float, float] | None:

    '''
    fuction that gather linear regression output of one student from a file
    argument: path of the file (login,theta0,theta1), login of the student
    return: a Tuple that contain both θ, None if the file or the student is not found
    '''

    try:
        df = pd.read_csv(path, dtype={"login": str})
    except (FileNotFoundError, PermissionError, IsADirectoryError, pd.errors.EmptyDataError):
        print("Error: unable to load the variable file. Launch the training first")
        return None

    if not {"login", "theta0", "theta1"}.issubset(df.columns):
        print("Error: invalid variable file. Launch the training first")
        return None

    row = df[df["login"] == login]
    if row.empty:
        print("Error: no trained model for the student", login)
        return None

    return float(row["theta0"].iloc[0]), float(row["theta1"].iloc[0])
