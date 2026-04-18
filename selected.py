"""
selected.py

Description
-----------
Helper functions for selecting predefined kinematic parameter columns
from processed gait-analysis DataFrames.

This module provides separate selection functions for:
1. Xsens data - Sound limb
2. Xsens data - Amputated limb
3. Noraxon data - Sound limb
4. Noraxon data - Amputated limb

Notes
-----
- Each function returns a new DataFrame containing only the required columns.
- Column names are kept exactly as defined in the source datasets.
- The logic is intentionally simple and preserved for reproducibility.
"""


def select_parameters_sound_xsens(df):
    """
    Select Sound-limb kinematic parameters from an Xsens processed DataFrame.

    Parameters
    ----------
    df : pandas.DataFrame
        Input DataFrame containing processed Xsens kinematic variables.

    Returns
    -------
    pandas.DataFrame
        DataFrame containing only the selected Sound-limb Xsens parameters.
    """
    selected_df = df[
        [
            "hip_Sound_flexion",
            "hip_Sound_abduction",
            "hip_Sound_rotation",
            "knee_Sound_flexion",
            "knee_Sound_abduction",
            "knee_Sound_rotation",
            "ankle_Sound_flexion",
            "ankle_Sound_rotation",
            "ankle_Sound_abduction",
        ]
    ]

    return selected_df


def select_parameters_amputated_xsens(df):
    """
    Select Amputated-limb kinematic parameters from an Xsens processed DataFrame.

    Parameters
    ----------
    df : pandas.DataFrame
        Input DataFrame containing processed Xsens kinematic variables.

    Returns
    -------
    pandas.DataFrame
        DataFrame containing only the selected Amputated-limb Xsens parameters.
    """
    selected_df = df[
        [
            "hip_Amputated_flexion",
            "hip_Amputated_abduction",
            "hip_Amputated_rotation",
            "knee_Amputated_flexion",
            "knee_Amputated_abduction",
            "knee_Amputated_rotation",
            "ankle_Amputated_flexion",
            "ankle_Amputated_rotation",
            "ankle_Amputated_abduction",
        ]
    ]

    return selected_df


def select_parameters_sound_naroxon(df):
    """
    Select Sound-limb kinematic parameters from a Noraxon processed DataFrame.

    Parameters
    ----------
    df : pandas.DataFrame
        Input DataFrame containing processed Noraxon kinematic variables.

    Returns
    -------
    pandas.DataFrame
        DataFrame containing only the selected Sound-limb Noraxon parameters.
    """
    selected_df = df[
        [
            "Sound Hip Flexion (deg)",
            "Sound Hip Abduction (deg)",
            "Sound Hip Rotation Ext (deg)",
            "Sound Knee Flexion (deg)",
            "Sound Knee Abduction (deg)",
            "Sound Knee Rotation Ext (deg)",
            "Sound Ankle Dorsiflexion (deg)",
            "Sound Ankle Abduction (deg)",
            "Sound Ankle Inversion (deg)",
        ]
    ]

    return selected_df


def select_parameters_amputated_naroxon(df):
    """
    Select Amputated-limb kinematic parameters from a Noraxon processed DataFrame.

    Parameters
    ----------
    df : pandas.DataFrame
        Input DataFrame containing processed Noraxon kinematic variables.

    Returns
    -------
    pandas.DataFrame
        DataFrame containing only the selected Amputated-limb Noraxon parameters.
    """
    selected_df = df[
        [
            "Amputated Hip Flexion (deg)",
            "Amputated Hip Abduction (deg)",
            "Amputated Hip Rotation Ext (deg)",
            "Amputated Knee Flexion (deg)",
            "Amputated Knee Abduction (deg)",
            "Amputated Knee Rotation Ext (deg)",
            "Amputated Ankle Dorsiflexion (deg)",
            "Amputated Ankle Abduction (deg)",
            "Amputated Ankle Inversion (deg)",
        ]
    ]

    return selected_df