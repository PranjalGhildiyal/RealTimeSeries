from pmdarima import arima
from pmdarima import model_selection
from pmdarima import pipeline
from pmdarima import preprocessing


class Model:
        
    def __init__(self):
        pass
    
    def fit(self, y, X):
        n_diffs = arima.ndiffs(y, max_d=5)
        date_feat = preprocessing.DateFeaturizer(
                                                    column_name="DATETIME", 
                                                    with_day_of_week=True,
                                                    with_day_of_month=True
                                                )
        self.model = pipeline.Pipeline([
                                    ('DATETIME', date_feat),
                                    ('arima', arima.AutoARIMA(d=n_diffs,
                                                            trace=3,
                                                            stepwise=True,
                                                            suppress_warnings=True,
                                                            seasonal=False))
                                ])
        self.model.fit(y, X)

    
    def predict(self, *args, **kwargs):
        return self.model.predict(*args, **kwargs)
    
    def update(self, *args, **kwargs):
        return self.model.update(*args, **kwargs)
        
