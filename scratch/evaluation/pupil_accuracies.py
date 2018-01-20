import numpy as np
import pandas as pd

DATASETS = ('pexels.csv', 'bioid.csv')
METHODS = ('gaze', 'eyelike')
SIDES = ('left', 'right')
METRICS = {'min': min, 'max': max, 'mean': lambda x, y: (x + y) / 2}


def add_eye_vecs(df):
    """Adds eye vectors to the dataframe."""
    for method in METHODS + ('target', ):
        for side in SIDES:
            ms = f'{method}_{side}'
            df[f'{ms}_eye'] = df[[f'{ms}_x', f'{ms}_y']].apply(tuple, axis=1)


def add_normalized_errors(df):
    """Adds normalized errors to the dataframe."""
    def eucl(x, y):
        """euclidean distance between two 2D values"""
        return ((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2) ** .5

    def normalized_error(rt, r, lt, l, metric):
        """Calculates the normalized error over a metric."""
        return metric(eucl(lt, l), eucl(rt, r)) / eucl(lt, rt)

    for method in METHODS:
        for metric, func in METRICS.items():
            k = f'{method}_{metric}_normalized_error'
            rtk = 'target_right_eye'
            rk = f'{method}_right_eye'
            ltk = 'target_left_eye'
            lk = f'{method}_left_eye'
            df[k] = df[[rtk, rk, ltk, lk]].apply(lambda row: normalized_error(*row, func), axis=1)


def create_accuracy_error_curves(df):
    accuracies = {}
    x = np.arange(0, 0.26, 0.01)
    for method in METHODS:
        for metric in METRICS.keys():
            k = f'{method}_{metric}_normalized_error'
            accuracy = np.vectorize(lambda theta: (df[k] < theta).sum() / df[k].count())
            accuracies[k] = accuracy(x)
    return pd.DataFrame(accuracies, index=x)


def computation_times(df):
    times = {}
    for method in METHODS:
        k = f'{method}_time'
        times[f'{method}/median'] = df[k].median()
        times[f'{method}/mean'] = df[k].mean()
        times[f'{method}/min'] = df[k].min()
        times[f'{method}/max'] = df[k].max()
    return times


if __name__ == '__main__':
    conditions = {'all': lambda df: df,
                  'eyes<=50': lambda df: df[(df['eye_right_width'] <= 50)
                                            & (df['eye_left_width'] <= 50)],
                  'eyes>50': lambda df: df[(df['eye_right_width'] > 50)
                                           & (df['eye_right_width'] > 50)]}
    results = {}
    for dataset in DATASETS:
        for condition, select in conditions.items():
            df = pd.read_csv(dataset)
            df = select(df)
            add_eye_vecs(df)
            add_normalized_errors(df)
            results[f'{dataset[:-4]}/{condition}/accuracy'] = create_accuracy_error_curves(df)
            if all(f'{method}_time' in list(df) for method in METHODS):
                results[f'{dataset[:-4]}/{condition}/comptimes'] = computation_times(df)

    # Although this script calculates all accuracies, I only need to compare
    # accuracy for BioID with Timm2011 and Hume2012, so I will only write that
    # to a csv
    bioid_result = results['bioid/all/accuracy'].copy()
    timm11 = np.empty(26)
    timm11.fill(np.nan)
    timm11[(0, 5, 10, 15, 20, 25), ] = np.array((0, 0.825, 0.934, 0.952, 0.964, 0.98))
    bioid_result['Timm2011'] = timm11
    #bioid_result.to_csv('../../assets/gen_files/bioid_accuracy_vs_error.csv', index_label='error')

    # The computation times are still interesting
    comp = results['pexels/all/comptimes']
    # TODO(shoeffner): print tables for appendix!
