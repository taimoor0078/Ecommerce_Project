from imblearn.over_sampling import SMOTE
import pandas as pd
from sklearn.utils import resample
class Balancing_Data:
    def __init__(self, X, y):
        self.X = X
        self.y = y
        self.data = pd.concat([X, y], axis=1)
        self.target_name = y.name
    # ---------------------------------
    # Oversampling WITH Random State
    # ---------------------------------
    def Oversampling_with_RandomState(self, random_state):
        majority = self.data[self.data[self.target_name] == 0]
        minority = self.data[self.data[self.target_name] == 1]
        minority_upsampled = resample(
            minority,
            replace=True,
            n_samples=len(majority),
            random_state=random_state
        )
        balanced = pd.concat([majority, minority_upsampled])
        return balanced.drop(columns=[self.target_name]), balanced[self.target_name]
    # ---------------------------------
    # Oversampling WITHOUT Random State
    # ---------------------------------
    def Oversampling_without_RandomState(self):
        majority = self.data[self.data[self.target_name] == 0]
        minority = self.data[self.data[self.target_name] == 1]
        minority_upsampled = resample(
            minority,
            replace=True,
            n_samples=len(majority)
        )
        balanced = pd.concat([majority, minority_upsampled])
        return balanced.drop(columns=[self.target_name]), balanced[self.target_name]
    # ---------------------------------
    # Undersampling WITH Random State
    # ---------------------------------
    def Undersampling_with_RandomState(self, random_state):
        majority = self.data[self.data[self.target_name] == 0]
        minority = self.data[self.data[self.target_name] == 1]
        majority_downsampled = resample(
            majority,
            replace=False,
            n_samples=len(minority),
            random_state=random_state
        )
        balanced = pd.concat([majority_downsampled, minority])
        return balanced.drop(columns=[self.target_name]), balanced[self.target_name]
    # ---------------------------------
    # Undersampling WITHOUT Random State
    # ---------------------------------
    def Undersampling_without_RandomState(self):
        majority = self.data[self.data[self.target_name] == 0]
        minority = self.data[self.data[self.target_name] == 1]
        majority_downsampled = resample(
            majority,
            replace=False,
            n_samples=len(minority)
        )
        balanced = pd.concat([majority_downsampled, minority])
        return balanced.drop(columns=[self.target_name]), balanced[self.target_name]
    # ---------------------------------
    # SMOTE WITH Random State
    # ---------------------------------
    def SMOTE_with_RandomState(self, random_state):
        smote = SMOTE(random_state=random_state)
        X_resampled, y_resampled = smote.fit_resample(self.X, self.y)
        return X_resampled, y_resampled
    # ---------------------------------
    # SMOTE WITHOUT Random State
    # ---------------------------------
    def SMOTE_without_RandomState(self):
        smote = SMOTE()
        X_resampled, y_resampled = smote.fit_resample(self.X, self.y)
        return X_resampled, y_resampled
