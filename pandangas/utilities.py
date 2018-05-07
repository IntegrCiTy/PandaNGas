def get_index(value, df, col="name"):
    """
    Return the index of an element in a DataFrame bus given a value and the name of the column to search for.
    Return a new index if the element doesn't exist yet

    :param value: the value to look for
    :param df: the DataFrame to search in
    :param col: the name of the column
    :return:
    """
    if value in df[col].unique():
        idx = df.index[df[col] == value].tolist()[0]

    else:
        idx = len(df)

    return idx
