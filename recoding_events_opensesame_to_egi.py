import os
from os.path import join

import pandas as pd

event_folder = 'Flanker_event_files'
data_folder = 'Flanker_data_files'
update_folder = 'Flanker_event_files-Updated'


def egi_events_to_df(file_path):
    df = pd.read_csv(file_path, skiprows=2, header=None, sep='\n')
    df = df[0].str.split('\t', expand=True)
    headers = df.iloc[0]
    # df = pd.DataFrame(df.values[1:], columns=headers)
    df = pd.read_csv(file_path, skiprows=3, names=headers)
    return df


def update_flags(df_path, task_df_path):
    # df = pd.read_csv('101_eeg_flanker_1.evt', skiprows=3,
    #  header=None, sep='\n')
    df_file_path = join(event_folder, df_path)
    # df = pd.read_csv(df_file_path, header=None, sep='\n')
    # df = df[0].str.split('\t', expand=True)
    df = egi_events_to_df(df_file_path)
    task_df = pd.read_csv(task_df_path)
    task_df.index += 1
    flanker_stim_mask = (df[0] == 'stim') & (df[12] != 'rcj ')
    df.loc[flanker_stim_mask, 'trial_id'] = \
        df.loc[flanker_stim_mask, 13].reset_index().index.values + 1
    df = df.set_index('trial_id')
    trial_mask = df.index.notna()
    df.loc[trial_mask, 0] = 'stm1'
    df.loc[trial_mask, 12] = 'resp'
    df.loc[trial_mask, 13] = task_df['response_new_srbox']
    df.loc[trial_mask, 14] = 'corr'
    df.loc[trial_mask, 15] = task_df['correct_new_srbox']
    df.to_csv(join('.', update_folder, 'revised_{0}' \
                   .format(df_path)), index=False, sep='\t')
    # print(df_path)


for file in os.listdir(join('.', event_folder)):
    splitter = len(file.split('_'))
    if splitter == 4:
        participant_id, imaging, task, tail = file.split('_')
    else:
        participant_id, imaging, task, __, tail = file.split('_')
        tail = "_".join((__, tail))
    if task == 'gonogo':
        continue
    task_number, extension = tail.split('.')
    data_file = "{0}_{1}_{2}_{3}.csv" \
        .format(participant_id, imaging, task, task_number)
    data_file_path = join(data_folder, participant_id, data_file)
    update_flags(file, data_file_path)
