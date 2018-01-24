import numpy as np
import pandas as pd

DATASETS = ('pexels', 'BioID')
METHODS = ('gaze', 'eyelike')
SIDES = ('left', 'right')
METRICS = {'min': min, 'max': max, 'mean': lambda x, y: (x + y) / 2}
OUTPATH = '../../assets/gen_files'
SI_PREFIX = r'\micro'


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

Computation times [\\si{{{SI_PREFIX}\\second}}] Eye size        `PupilLocalization`        `EyeLike`
-------------------------------------- -------- -------------------------- ----------------
\\multirow{{3}}{{*}}{{Median}}                $\le 50$   \\num{{{smallcomp['gaze/median']:>8.0f}}}            \\num{{{smallcomp['eyelike/median']:>8.0f}}}
                                       $> 50$     \\num{{{bigcomp['gaze/median']:>8.0f}}}            \\num{{{bigcomp['eyelike/median']:>8.0f}}}
                                       all        \\num{{{allcomp['gaze/median']:>8.0f}}}            \\num{{{allcomp['eyelike/median']:>8.0f}}}
\\midrule\\multirow{{3}}{{*}}{{Min}}           $\le 50$   \\num{{{smallcomp['gaze/min']:>8.0f}}}            \\num{{{smallcomp['eyelike/min']:>8.0f}}}
                                       $> 50$     \\num{{{bigcomp['gaze/min']:>8.0f}}}            \\num{{{bigcomp['eyelike/min']:>8.0f}}}
                                       all        \\num{{{allcomp['gaze/min']:>8.0f}}}            \\num{{{allcomp['eyelike/min']:>8.0f}}}
\\midrule\\multirow{{3}}{{*}}{{Mean}}          $\le 50$   \\num{{{smallcomp['gaze/mean']:>8.0f}}}            \\num{{{smallcomp['eyelike/mean']:>8.0f}}}
                                       $> 50$     \\num{{{bigcomp['gaze/mean']:>8.0f}}}            \\num{{{bigcomp['eyelike/mean']:>8.0f}}}
                                       all        \\num{{{allcomp['gaze/mean']:>8.0f}}}            \\num{{{allcomp['eyelike/mean']:>8.0f}}}
\\midrule\\multirow{{3}}{{*}}{{Max}}           $\le 50$   \\num{{{smallcomp['gaze/max']:>8.0f}}}            \\num{{{smallcomp['eyelike/max']:>8.0f}}}
                                       $> 50$     \\num{{{bigcomp['gaze/max']:>8.0f}}}            \\num{{{bigcomp['eyelike/max']:>8.0f}}}
                                       all        \\num{{{allcomp['gaze/max']:>8.0f}}}            \\num{{{allcomp['eyelike/max']:>8.0f}}}
"""
    with open(f'{OUTPATH}/table-comptimes-{dataset}.md', 'w') as f:
        print(comptable, file=f)
    for k, v in [('gaze', 'PupilLocalization'), ('eyelike', 'EyeLike')]:
        for metric in ['median', 'min', 'max', 'mean']:
            with open(f'{OUTPATH}/comptimes/{dataset}-all-{v}-{metric}.si', 'w') as f:
                val = allcomp[f'{k}/{metric}']
                print(r'\SI{' + f'{val/1000:.3f}' + r'}{\milli\second}', file=f)


def write_relative_errors(dataset, result):
    r = result[f'{dataset}/all/accuracy']
    max_timm11 = np.array((0.825, 0.934, 0.952, 0.964, 0.98))
    indices = [0.05, 0.1, 0.15, 0.2, 0.25]
    max_eyelike = r['eyelike_max_normalized_error'][indices].values
    max_gaze = r['gaze_max_normalized_error'][indices].values
    mean_eyelike = r['eyelike_mean_normalized_error'][indices].values
    mean_gaze = r['gaze_mean_normalized_error'][indices].values
    min_eyelike = r['eyelike_min_normalized_error'][indices].values
    min_gaze = r['gaze_min_normalized_error'][indices].values
    mr = 3 if dataset == 'BioID' else 2  # special case for Timm2011
    comptable = f"""
Table: Different accuracies per relative error thresholds on the {dataset}
dataset. """
    if dataset == 'BioID': comptable += f"""While @Timm2011 provide a graph of their results, only their $\\max$
values are reported. """
    comptable += f"""\\label{{tab:{dataset}-pupil-detection-accuracies}}

Error type                       Method               0.05  0.10  0.15  0.20  0.25
-------------------------------- ------------------- ----- ----- ----- ----- -----
\\multirow{{{mr}}}{{*}}{{$\\max$}}          `EyeLike`           {max_eyelike[0]:4.3f} {max_eyelike[1]:4.3f} {max_eyelike[2]:4.3f} {max_eyelike[3]:4.3f} {max_eyelike[4]:4.3f}
                                 `PupilLocalization` {max_gaze[0]:4.3f} {max_gaze[1]:4.3f} {max_gaze[2]:4.3f} {max_gaze[3]:4.3f} {max_gaze[4]:4.3f}"""
    if dataset == 'BioID': comptable += f"""
                                 [@Timm2011]         {max_timm11[0]:4.3f} {max_timm11[1]:4.3f} {max_timm11[2]:4.3f} {max_timm11[3]:4.3f} {max_timm11[4]:4.3f}"""
    comptable += f"""
\\midrule\\multirow{{2}}{{*}}{{$\\mean$}} `EyeLike`           {mean_eyelike[0]:4.3f} {mean_eyelike[1]:4.3f} {mean_eyelike[2]:4.3f} {mean_eyelike[3]:4.3f} {mean_eyelike[4]:4.3f}
                                 `PupilLocalization` {mean_gaze[0]:4.3f} {mean_gaze[1]:4.3f} {mean_gaze[2]:4.3f} {mean_gaze[3]:4.3f} {mean_gaze[4]:4.3f}
\\midrule\\multirow{{2}}{{*}}{{$\\min$}}  `EyeLike`           {min_eyelike[0]:4.3f} {min_eyelike[1]:4.3f} {min_eyelike[2]:4.3f} {min_eyelike[3]:4.3f} {min_eyelike[4]:4.3f}
                                 `PupilLocalization` {min_gaze[0]:4.3f} {min_gaze[1]:4.3f} {min_gaze[2]:4.3f} {min_gaze[3]:4.3f} {min_gaze[4]:4.3f}
"""
    with open(f'{OUTPATH}/table-relative-errors-{dataset}.md', 'w') as f:
        print(comptable, file=f)

def store_accuracy_vs_error(dataset, result):
    timm11 = np.empty(26)
    timm11.fill(np.nan)
    timm11[(0, 5, 10, 15, 20, 25), ] = np.array((0, 0.825, 0.934, 0.952, 0.964, 0.98))
    result['Timm2011'] = timm11
    result.to_csv(f'{OUTPATH}/{dataset}_accuracy_vs_error.csv', index_label='error')


if __name__ == '__main__':
    conditions = {'all': lambda df: df,
                  'eyes<=50': lambda df: df[(df['eye_right_width'] <= 50)
                                            & (df['eye_left_width'] <= 50)],
                  'eyes>50': lambda df: df[(df['eye_right_width'] > 50)
                                           & (df['eye_right_width'] > 50)]}
    results = {}
    for dataset in DATASETS:
        for condition, select in conditions.items():
            df = pd.read_csv(dataset + '.csv')
            df = select(df)
            add_eye_vecs(df)
            add_normalized_errors(df)
            results[f'{dataset}/{condition}/accuracy'] = create_accuracy_error_curves(df)
            if all(f'{method}_time' in list(df) for method in METHODS):
                results[f'{dataset}/{condition}/comptimes'] = computation_times(df)
        if all(f'{dataset}/{condition}/comptimes' in results.keys() for condition in conditions):
            write_computation_times(dataset,
                                    results[f'{dataset}/all/comptimes'],
                                    results[f'{dataset}/eyes<=50/comptimes'],
                                    results[f'{dataset}/eyes>50/comptimes'])

        store_accuracy_vs_error(dataset, results[f'{dataset}/all/accuracy'].copy())
        write_relative_errors(dataset, results)
