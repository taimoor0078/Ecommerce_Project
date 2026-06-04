
from sklearn.preprocessing import StandardScaler, MinMaxScaler
class Scaler:
    def __init__(self, method="standard"):
        if method == "standard":
            self.scaler = StandardScaler()
        elif method == "minmax":
            self.scaler = MinMaxScaler()
        else:
            raise ValueError("method must be 'standard' or 'minmax'")

        self.columns = None

    def fit_transform(self, df, columns):
        df = df.copy()
        self.columns = columns
        df[columns] = self.scaler.fit_transform(df[columns])
        return df

    def transform(self, df):
        df = df.copy()
        df[self.columns] = self.scaler.transform(df[self.columns])
        return df
