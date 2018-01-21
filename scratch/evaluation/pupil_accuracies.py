import numpy as np
import pandas as pd

DATASETS = ('pexels.csv', 'BioID.csv')
METHODS = ('gaze', 'eyelike')
SIDES = ('left', 'right')
METRICS = {'min': min, 'max': max, 'mean': lambda x, y: (x + y) / 2}
OUTPATH = '../../assets/gen_files'


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


def write_computation_times(dataset, allcomp, smallcomp, bigcomp):
    comptable = f"""
Table: Comparison of computation times between `EyeLike` and
`PupilLocalization`. Data measured on the {dataset} dataset. \\label{{tab:comptimes-{dataset}}}

Computation times [\\si{{\milli\second}}] Eye size  `PupilLocalization`  `EyeLike`
-------------------------------------- -------- -------------------- ----------
\\multirow{{3}}{{*}}{{Median}}                $\le 50$   {smallcomp['gaze/median']:>4.0f}               {smallcomp['eyelike/median']:>4.0f}
                                       $> 50$     {bigcomp['gaze/median']:>4.0f}               {bigcomp['eyelike/median']:>4.0f}
                                       all        {allcomp['gaze/median']:>4.0f}               {allcomp['eyelike/median']:>4.0f}
\\midrule\\multirow{{3}}{{*}}{{Min}}           $\le 50$   {smallcomp['gaze/min']:>4.0f}               {smallcomp['eyelike/min']:>4.0f}
                                       $> 50$     {bigcomp['gaze/min']:>4.0f}               {bigcomp['eyelike/min']:>4.0f}
                                       all        {allcomp['gaze/min']:>4.0f}               {allcomp['eyelike/min']:>4.0f}
\\midrule\\multirow{{3}}{{*}}{{Mean}}          $\le 50$   {smallcomp['gaze/mean']:>4.0f}               {smallcomp['eyelike/mean']:>4.0f}
                                       $> 50$     {bigcomp['gaze/mean']:>4.0f}               {bigcomp['eyelike/mean']:>4.0f}
                                       all        {allcomp['gaze/mean']:>4.0f}               {allcomp['eyelike/mean']:>4.0f}
\\midrule\\multirow{{3}}{{*}}{{Max}}           $\le 50$   {smallcomp['gaze/max']:>4.0f}               {smallcomp['eyelike/max']:>4.0f}
                                       $> 50$     {bigcomp['gaze/max']:>4.0f}               {bigcomp['eyelike/max']:>4.0f}
                                       all        {allcomp['gaze/max']:>4.0f}               {allcomp['eyelike/max']:>4.0f}
"""
    with open(f'{OUTPATH}/table-comptimes-{dataset}.md', 'w') as f:
        print(comptable, file=f)


def write_relative_errors(dataset, result):
    pass


def store_accuracy_vs_error(dataset, result):
    timm11 = np.empty(26)
    timm11.fill(np.nan)
    timm11[(0, 5, 10, 15, 20, 25), ] = np.array((0, 0.825, 0.934, 0.952, 0.964, 0.98))
    result['Timm2011'] = timm11
    result.to_csv(f'{OUTPATH}/{dataset}_accuracy_vs_error.csv', index_label='error')

'''
Table: Different relative error accuracies on the BioID dataset. \label{tab:bioid_accuracies}

                            0.00   0.05   0.10   0.15   0.20   0.25
-------------------------- ------ ------ ------ ------ ------ ------
max `EyeLike`
max `PupilLocalization`
max @Timm2011
mean `EyeLike`
mean `PupilLocalization`
mean @Timm2011
min `EyeLike`
min `PupilLocalization`
min @Timm2011
'''

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
        if all(f'{dataset[:-4]}/{condition}/comptimes' in results.keys() for condition in conditions):
            write_computation_times(dataset[:-4],
                results[f'{dataset[:-4]}/all/comptimes'],
                results[f'{dataset[:-4]}/eyes<=50/comptimes'],
                results[f'{dataset[:-4]}/eyes>50/comptimes'])

    store_accuracy_vs_error(dataset[:-4], results[f'{dataset[:-4]}/all/accuracy'].copy())

