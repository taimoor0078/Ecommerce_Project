from sklearn.model_selection import cross_val_score
class CrossValidation:
 def __init__(self, model, X, y):
        self.model = model
        self.X = X
        self.y = y
    def FiveFold(self):
        scores = cross_val_score(self.model, self.X, self.y, cv=5)
        return scores
    def TenFold(self):
        scores = cross_val_score(self.model, self.X, self.y, cv=10)
        return scores
    def CustomFold(self, folds):
        scores = cross_val_score(self.model, self.X, self.y, cv=folds)
        return scores