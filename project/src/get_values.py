import pandas as pd

#Dataframe is set-up as USER_ID | SECTION | ROW | FIELD | VALUE

def get_value_users(df, user_id):

    '''
    Read all values from the DataFrame built by to_long_dataframe for a specific USER_ID.
    Argument: Dataframe build by to_long_dataframe, an user_id
    Return: the user_id specific section
    '''

    try:
        return df.loc[user_id]
    except KeyError:
        return "Get_value_users : No match for USER_ID"

def get_value_section(df, user_id, section):

    '''
    Read all ROW from a SECTION for an USER_ID.
    Argument: Dataframe build by to_long_dataframe, an user_id, a section
    Return: the row from a section for an USER_ID
    '''

    try:
        return df.loc[(user_id, section)]
    except KeyError:
        return "Get_value_section: No match for SECTION"

def get_value_row(df, user_id, section, row):

    '''
    Read all FIELD from a ROW from a SECTION for an USER_ID.
    Argument: Dataframe build by to_long_dataframe, an user_id, a section
    Return: the FIELD from a ROW from a SECTION for an USER_ID
    '''

    try:
        return df.loc[(user_id, section, row)]
    except KeyError:
        return "Get_value_row: No match for ROW"

def get_value_field(df, user_id, section, row, field):

    '''
    Read the VALUE from a FIELD from a ROW from a SECTION for an USER_ID.
    Argument: Dataframe build by to_long_dataframe, an user_id, a section
    Return: the VALUE from a FIELD from a ROW from a SECTION for an USER_ID
    '''

    try:
        return df.loc[(user_id, section, row, field), "value"]
    except KeyError:
        return "Get_value_row: No match for FIELD"

def _as_list(x):
    return list(x) if isinstance(x, (list, tuple, set, pd.Index)) else [x]


def _row_mask(df, user_id=None, section=None, row=None, field=None, value=None):

    '''
    Boolean mask of the rows matching every given criterion (None = no criterion).
    '''

    mask = pd.Series(True, index=df.index)
    for level, wanted in (("user_id", user_id), ("section", section),
                          ("row", row), ("field", field)):
        if wanted is not None:
            mask &= df.index.get_level_values(level).isin(_as_list(wanted))
    if value is not None:
        mask &= df["value"].astype(str).isin([str(v) for v in _as_list(value)])
    return mask


def search(df, user_id=None, section=None, row=None, field=None, value=None,
           where=None, filters=None):

    '''
    Generic filter on the DataFrame built by to_long_dataframe.
    Every argument is optional: None means "all". Each one accepts a single
    element or a list/set/Index of elements (ex: field=["login", "pool_month"]).

    - user_id, section, row, field, value: which ROWS to return.
    - filters: shortcut {field: value(s)}. The user must match EVERY field (AND),
      and any of the values listed for a field (OR).
      ex: filters={"pool_year": 2025, "pool_month": ["august", "july"]}
    - where: same idea with full control. A dict, or a list of dicts (all must be
      true, AND). Each dict accepts section, row, field, value.
      ex: where=[{"field": "pool_month", "value": "august"},
                 {"section": "campus", "field": "id", "value": 31}]

    Return: the matching rows (same USER_ID | SECTION | ROW | FIELD | VALUE layout)
    '''

    mask = _row_mask(df, user_id, section, row, field, value)

    conditions = [] if where is None else _as_list(where)
    for filter_field, filter_value in (filters or {}).items():
        conditions.append({"field": filter_field, "value": filter_value})

    users = None
    for condition in conditions:
        matching = df.index[_row_mask(df, **condition)].get_level_values("user_id")
        users = set(matching) if users is None else users & set(matching)
    if users is not None:
        mask &= df.index.get_level_values("user_id").isin(list(users))

    return df[mask]

