import mne
from mne.datasets import sample
from mne.minimum_norm import apply_inverse_raw, read_inverse_operator

data_path = sample.data_path()
fname_inv = data_path + '/MEG/sample/sample_audvis-meg-oct-6-meg-inv.fif'
fname_raw = data_path + '/MEG/sample/sample_audvis_raw.fif'
label_name = 'Aud-lh'
fname_label = data_path + '/MEG/sample/labels/%s.label' % label_name

snr = 1.0  # use smaller SNR for raw data
lambda2 = 1.0 / snr ** 2
method = "MNE"  # use sLORETA method (could also be MNE or dSPM)

# Load data
raw = mne.io.read_raw_fif(fname_raw)
inverse_operator = read_inverse_operator(fname_inv)
label = mne.read_label(fname_label)

raw.set_eeg_reference()  # set average reference.
start, stop = raw.time_as_index([0, 15])  # read the first 15s of data

# Compute inverse solution
stc = apply_inverse_raw(raw, inverse_operator, lambda2, method, label=None,
                        start=start, stop=stop, pick_ori=None)

# Plot
subjects_dir = data_path + '/subjects'
stc.plot(subject='sample', hemi='both', surface='inflated', subjects_dir=subjects_dir)