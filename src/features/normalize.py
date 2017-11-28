import pandas as pd
from sklearn.feature_selection import VarianceThreshold
from sklearn.preprocessing import StandardScaler


def select_variance_features(df, threshold=20):
    columns = df.columns
    selector = VarianceThreshold(threshold=threshold)
    selector.fit_transform(df)
    labels = [columns[x] for x in selector.get_support(indices=True) if x]
    return pd.DataFrame(selector.fit_transform(df), columns=labels)


def scale_df(df):
    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df)
    return pd.DataFrame(df_scaled, columns=df.columns)
