import pandas as pd

OUTPATH = '../../assets/gen_files'
SI_PREFIX = r'\micro'

STEPS = {
    'FaceLandmarks': 'landmarks_time',
    'HeadPoseEstimation': 'headpose_time',
    'PupilLocalization': 'gaze_time',
    'EyeLike': 'eyelike_time',
    'GazePointCalculation': 'gazepoint_time',
    'GazeCapture': 'gazecapture_time',
}

PIPELINES = {
    'Default (FHPG)': ['FaceLandmarks', 'HeadPoseEstimation', 'PupilLocalization', 'GazePointCalculation'],
    'EyeLike (FHEG)': ['FaceLandmarks', 'HeadPoseEstimation', 'EyeLike', 'GazePointCalculation'],
    'iTracker (FC)': ['FaceLandmarks', 'GazeCapture'],
}


def write_pipeline_times(df):
    metrics = [r'Median', 'Max', 'Mean', 'Min']

    first_col_width = max(len(i) for i in PIPELINES.keys()) + 1  # + space
    metrics_width = 15

    first_col_fmt = f' <{first_col_width}'
    time_fmt = f'{metrics_width-6}.0f'  # minus   \num{}

    header = f'{{:{first_col_fmt}}}'.format('Pipeline')
    header += ' '.join([f'{{:>{metrics_width}}}'] * len(metrics)).format(*metrics)

    dashes = ' '.join(['-' * (first_col_width - 1)] + ['-' * metrics_width] * len(metrics))
    lines = []
    for pipeline, steps in PIPELINES.items():
        line = f'{{:{first_col_fmt}}}'.format(f'{pipeline}')
        acc = df[[STEPS[step] for step in steps]].sum(axis=1)
        times = [acc.median(), acc.max(), acc.mean(), acc.min()]

        pre, post = r'\num{', '}'
        times = ' '.join(pre + f'{{:{time_fmt}}}'.format(time) + post for time in times)
        lines.append(line + times)
    table_caption = r"""
Table: Accumulated computation times per pipeline configuration.;;Accumulated computation times per pipeline configuration, measured on
the pexels dataset. The `SourceCapture` step is excluded. The other steps are
`FaceLandmarks` (F), `HeadPoseEstimation` (H), `PupilLocalization` (P),
`EyeLike` (E), `GazePointCalculation` (G), and `GazeCapture` (C). All values
are in \si{""" + SI_PREFIX + r"""\second}. \label{tab:pipeline-times}
"""
    table = '\n'.join([table_caption, header, dashes] + lines)
    with open(OUTPATH + '/table-pipeline-times.md', 'w') as f:
        print(table, file=f)


def write_pipeline_step_times(df):
    steps = ['FaceLandmarks', 'HeadPoseEstimation', 'PupilLocalization', 'GazePointCalculation', 'EyeLike', 'GazeCapture']
    metrics = [r'Median', 'Max', 'Mean', 'Min']

    first_col_width = max(len(i) for i in steps) + 3  # + `` and space
    metrics_width = 15

    first_col_fmt = f' <{first_col_width}'
    time_fmt = f'>{metrics_width - 6}.0f'

    header = f'{{:{first_col_fmt}}}'.format('Pipeline step')
    header += ' '.join([f'{{:>{metrics_width}}}'] * len(metrics)).format(*metrics)

    dashes = ' '.join(['-' * (first_col_width - 1)] + ['-' * metrics_width] * len(metrics))
    pre, post = r'\num{', '}'
    lines = []
    for step in steps:
        line = f'{{:{first_col_fmt}}}'.format(f'`{step}`')
        times = [df[STEPS[step]].median(), df[STEPS[step]].max(), df[STEPS[step]].mean(), df[STEPS[step]].min()]
        times = ' '.join(pre + f'{{:{time_fmt}}}'.format(time) + post for time in times)
        lines.append(line + times)
    table_caption = r"""
Table: Computation times per pipeline step.;;The different computation times per pipeline step, measured on the pexels
dataset. All values are in \si{""" + SI_PREFIX + r"""\second}.
Note that all pipeline steps except for the source capture are included,
even though the default pipeline only uses the first four.
\label{tab:pipeline-step-times}
"""
    table = '\n'.join([table_caption, header, dashes] + lines)
    with open(OUTPATH + '/table-pipeline-step-times.md', 'w') as f:
        print(table, file=f)


if __name__ == '__main__':
    df = pd.read_csv('pexels.csv')
    write_pipeline_times(df)
    write_pipeline_step_times(df)
