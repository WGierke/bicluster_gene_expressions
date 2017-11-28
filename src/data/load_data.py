import pandas as pd
import json

from ..config import SMALL_SET_PATH, BIG_SET_META_PATH, BIG_SET_PATH, BIG_SET_PROCESSED_PATH, BIG_SET_PROCESSED_LABELS_PATH


def get_small_dataset_content():
    df = pd.read_csv(SMALL_SET_PATH)
    old_columns = df.columns.values
    old_columns[0] = "sample_id"
    df.columns = old_columns
    df = df.set_index('sample_id')
    return df


def get_big_dataset_content(cached=True):
    def fix_columns_and_index(df):
        old_columns = df.columns.values
        old_columns[0] = "sample_id"
        df.columns = old_columns
        return df.set_index('sample_id')

    if cached:
        df = pd.read_csv(BIG_SET_PROCESSED_PATH)
        with open(BIG_SET_PROCESSED_LABELS_PATH) as f:
            labels = json.loads(f.read())
        df = fix_columns_and_index(df)
    else:
        big_df_meta = pd.read_csv(BIG_SET_META_PATH)
        df = pd.read_csv(BIG_SET_PATH)
        df = fix_columns_and_index()

        # Retrieve the cancer types for each record in the big DataFrame
        df.dropna(axis=(0, 1), inplace=True)
        labels = []
        for sample_id in df.index:
            cancer_type = big_df_meta[sample_id][0]
            if "TCGA" in str(cancer_type):
                labels.append(cancer_type)
            else:
                # Remove measurement from big_df that has no valid cancer type
                df.drop(index=sample_id, inplace=True)

    return df, labels
