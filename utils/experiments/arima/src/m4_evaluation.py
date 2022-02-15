from itertools import product

import numpy as np
import pandas as pd
from neuralforecast.data.datasets.m4 import M4Evaluation, M4Info

from src.data import get_data


def evaluate(lib: str, group: str):
    if lib != 'arima-r':
        forecast = pd.read_csv(f'data/{lib}-forecasts-M4-{group}.csv')
        horizon = M4Info[group].horizon
        if lib == 'statsforecast':
            col = 'auto_arima_nixtla'
        else:
            col = 'auto_arima_pmdarima'
        forecast = forecast[col].values.reshape(-1, horizon)
    else:
        forecast = np.loadtxt(f'data/{lib}-forecasts-M4-{group}.txt')
    evals = M4Evaluation.evaluate('data', group, forecast)
    times = pd.read_csv(f'data/{lib}-time-M4-{group}.csv')
    evals = evals.rename_axis('dataset').reset_index()
    evals = pd.concat([evals, times], axis=1)

    return evals


if __name__ == '__main__':
    groups = ['Monthly', 'Quarterly', 'Yearly', 'Hourly', 'Weekly', 'Daily']
    groups = ['Weekly', 'Hourly']
    lib = ['statsforecast', 'arima-r']#, 'pmdarima']
    evaluation = [evaluate(lib, group) for lib, group in product(lib, groups)]
    evaluation = pd.concat(evaluation).sort_values(['dataset', 'model']).reset_index(drop=True)

    evaluation.to_csv('data/m4-evaluation.csv')
    print(evaluation.to_markdown())
