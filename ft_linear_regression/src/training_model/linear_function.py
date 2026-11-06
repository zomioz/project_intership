import numpy as np


def linear_regression(df, number_of_iteration) -> tuple[float, float]:

    '''
    Function that execute an linear regression on a dataframe
    argument: Dirst: Dataframe (column 0: x, column 1: y). Second: number of iteration for the linear regression
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
