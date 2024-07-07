import pandas as pd

def merge_sort(df, column, ascending=True):
    # Base case: if the dataframe has one or no rows, it is already sorted
    if len(df) <= 1:
        return df

    # Split the dataframe into two halves
    middle = len(df) // 2
    left_half = df.iloc[:middle]
    right_half = df.iloc[middle:]

    # Recursively sort each half
    left_sorted = merge_sort(left_half, column, ascending)
    right_sorted = merge_sort(right_half, column, ascending)

    # Merge the two sorted halves
    return merge(left_sorted, right_sorted, column, ascending)

def merge(left, right, column, ascending=True):
    sorted_df = pd.DataFrame()
    left_index, right_index = 0, 0

    # Merge the two sorted dataframes
    while left_index < len(left) and right_index < len(right):
        # Ascending order
        if ascending:
            if left.iloc[left_index][column] <= right.iloc[right_index][column]:
                sorted_df = sorted_df.append(left.iloc[left_index])
                left_index += 1
            else:
                sorted_df = sorted_df.append(right.iloc[right_index])
                right_index += 1
        # Descending Order
        else:
            if left.iloc[left_index][column] >= right.iloc[right_index][column]:
                sorted_df = sorted_df.append(left.iloc[left_index])
                left_index += 1
            else:
                sorted_df = sorted_df.append(right.iloc[right_index])
                right_index += 1

    # Append the remaining rows from the left dataframe, if any
    while left_index < len(left):
        sorted_df = sorted_df.append(left.iloc[left_index])
        left_index += 1

    # Append the remaining rows from the right dataframe, if any
    while right_index < len(right):
        sorted_df = sorted_df.append(right.iloc[right_index])
        right_index += 1

    return sorted_df.reset_index(drop=True)