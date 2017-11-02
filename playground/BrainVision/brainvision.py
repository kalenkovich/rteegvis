from mne.io import read_raw_brainvision
import mne.io.brainvision.brainvision as brainvision

bobe_header = 'BrainVision Data Exchange Header File Version 1.0'

brainvision._check_mrk_version_original = brainvision._check_mrk_version
brainvision._check_hdr_version_original = brainvision._check_hdr_version


def _check_mrk_version(header):
    if header == bobe_header:
        return True
    else:
        return brainvision._check_mrk_version_original(header)


def _check_hdr_version(header):
    if header == bobe_header:
        return True
    else:
        return brainvision._check_hdr_version_original(header)


brainvision._check_hdr_version = _check_hdr_version
brainvision._check_mrk_version = _check_mrk_version