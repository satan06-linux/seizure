"""
EDF Reader Utility for EEG data
"""
import mne
import numpy as np


def read_edf_file(edf_path):
    """Read EDF file and extract EEG data"""
    try:
        raw = mne.io.read_raw_edf(edf_path, preload=True, verbose=False)
        data = raw.get_data()
        sfreq = raw.info['sfreq']
        channels = raw.ch_names
        
        return {
            'data': data,
            'sampling_rate': sfreq,
            'channels': channels,
            'duration': len(data[0]) / sfreq
        }
    except Exception as e:
        raise Exception(f"Error reading EDF: {str(e)}")
