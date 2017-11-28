import pandas as pd

from ..config import SMALL_SET_PATH, BIG_SET_META_PATH, BIG_SET_PATH


def get_small_dataset_content():
    df = pd.read_csv(SMALL_SET_PATH)
    old_columns = df.columns.values
    old_columns[0] = "sample_id"
    df.columns = old_columns
    df = df.set_index('sample_id')
    return df


def get_big_dataset_content():
    big_df_meta = pd.read_csv(BIG_SET_META_PATH)
    big_df = pd.read_csv(BIG_SET_PATH)
    old_columns = big_df.columns.values
    old_columns[0] = "sample_id"
    big_df.columns = old_columns
    big_df = big_df.set_index('sample_id')

    # Retrieve the cancer types for each record in the big DataFrame
    big_df.dropna(axis=(0, 1), inplace=True)
    labels_true = []
    for sample_id in big_df.index:
        cancer_type = big_df_meta[sample_id][0]
        if "TCGA" in str(cancer_type):
            labels_true.append(cancer_type)
        else:
            # Remove measurement from big_df that has no valid cancer type
            big_df.drop(index=sample_id, inplace=True)

    return big_df, labels_true
