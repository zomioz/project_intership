import pandas as pd

def to_long_dataframe(data):

    '''
    Convert one user (dict) or several users (list of dicts) into ONE DataFrame
    indexed by (user_id, section, row, field) with a single column "value".
    - section: the API key ("campus", "projects_users", ...), "user" for simple fields
    - row: position inside the section (0 for a dict, 0..n for a list)
    - field: the flattened field name ("id", "project.name", ...)
    Return: a sorted DataFrame, ex: df.loc[(166888, "campus", 0, "id"), "value"]
    '''

    users = data if isinstance(data, list) else [data]
    records = []

    for user in users:
        user_id = user["id"]
        for section, content in user.items():
            if isinstance(content, dict):
                content = [content]
            if not isinstance(content, list):
                records.append((user_id, "user", 0, section, content))
                continue
            for row, item in enumerate(content):
                if not isinstance(item, dict):
                    records.append((user_id, section, row, "value", item))
                    continue
                for field, value in pd.json_normalize(item).iloc[0].items():
                    records.append((user_id, section, row, field, value))

    df = pd.DataFrame(records, columns=["user_id", "section", "row", "field", "value"])
    return df.set_index(["user_id", "section", "row", "field"]).sort_index()