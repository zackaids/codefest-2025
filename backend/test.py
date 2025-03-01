import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from datetime import datetime

df = pd.read_csv("datatest.txt")

# for i in df["date"]:
#     i = datetime.strptime(i, '%Y-%m-%d %H:%M:%S')



df["date"] = pd.to_datetime(df["date"])
print(df.dtypes)
df_features = df.drop(["Occupancy"], axis=1).values
df_occupancy = df["Occupancy"].values
df_occupancy = df_occupancy / np.max(df_occupancy)


X_train, X_test, y_train, t_test = train_test_split(df_features,
                                                    df_occupancy,
                                                    test_size=0.2,
                                                    random_state=42)

normalizer = StandardScaler()
X_train = normalizer.fit_transform(X_train)
X_test = normalizer.transform(X_test)

lr = LogisticRegression()

lr.fit(X_train, y_train)
print(f"bias is {str(lr.intercept_)}")