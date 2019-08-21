import mne
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Organize file/path/channel names
participant_file_name = 'sample_egi_data'
data_file_name = '{0}.nsf'.format(participant_file_name)
events_file_name = '{0}.evt'.format(participant_file_name)
bad_channels_file_name = '{0}.bci'.format(participant_file_name)
egi_montage = mne.channels.read_montage('GSN-HydroCel-257')
egi_eog = ['E18', 'E25', 'E32', 'E37', 'E238', 'E241']

# collate events for this participant
events = pd.read_csv(events_file_name, skiprows=3)
# raw = mne.io.read_raw_egi(data_file_name, montage=egi_montage, eog=egi_eog)
raw = mne.io.read_raw_egi(data_file_name, montage=egi_montage)
raw.plot(annotate=True, block=True)

for channel_index, eog_ch in enumerate(egi_eog):
    if channel_index:
        raw.set_channel_types({egi_eog[channel_index - 1]: 'eeg'})
    raw.set_channel_types({eog_ch: 'eog'})
    # find blinks
    annotated_blink_raw = raw.copy()
    event_id = 998
    eog_events = mne.preprocessing.find_eog_events(raw)
    n_blinks = len(eog_events)

    # Turn blink events into Annotations of 0.5 seconds duration,
    # each centered on the blink event:
    onset = eog_events[:, 0] / raw.info['sfreq'] - 0.25
    duration = np.repeat(0.5, n_blinks)
    description = ['bad blink'] * n_blinks
    annot = mne.Annotations(onset, duration, description,
                            orig_time=raw.info['meas_date'])
    annotated_blink_raw.set_annotations(annot)

    # plot the annotated raw
    annotated_blink_raw.plot(block=True)

    # Read epochs
    picks = mne.pick_types(raw.info, meg=False, eeg=False, stim=False, eog=True,
                           exclude='bads')
    tmin, tmax = -0.2, 0.2
    epochs = mne.Epochs(raw, eog_events, event_id, tmin, tmax, picks=picks)
    data = epochs.get_data()

    plt.plot(1e3 * epochs.times, np.squeeze(data).T)
    plt.xlabel('Times (ms)')
    plt.ylabel('EOG (muV)')
    plt.show()

if __name__ != '__main__':
    layout = raw.plot_sensors(ch_groups='position', to_sphere=True, show=False)
    layout.savefig('layout.png')
