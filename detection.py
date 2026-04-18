"""
detection.py

Description
-----------
Utility functions for detecting gait-step ranges from binary or discrete
foot-contact signals.

This module supports two data formats:
1. Xsens   -> contact state encoded as 10
2. Noraxon -> contact state encoded as 1000

Main workflow
-------------
1. Find all indices where the contact signal equals the target contact value
2. Group consecutive indices into continuous contact segments
3. Convert those segments into step ranges
4. Filter short steps using a minimum-length threshold
5. Either:
   - select the first N steps after a chosen starting step, or
   - select user-specified step indices

Notes
-----
- The output step ranges are returned as:
    [[start_1, end_1], [start_2, end_2], ...]
- Output indices are converted to float to preserve compatibility with the
  original project workflow.
"""

import numpy as np


def detect_cycles_xsens(leg_data, min_points, num_steps, start_step):
    """
    Detect gait-step ranges from an Xsens foot-contact signal.

    Parameters
    ----------
    leg_data : array-like
        Foot-contact signal in which contact is encoded as 10.
    min_points : int
        Minimum number of points required for a step to be retained.
    num_steps : int
        Maximum number of steps to return.
    start_step : int
        Step number to start selection from (1-based index).

    Returns
    -------
    list of list of float
        Detected step ranges in the format:
        [[start_1, end_1], [start_2, end_2], ...]
    """
    result_steps = []
    array_leg = []

    # Find indices where the Xsens contact signal equals 10
    indices_10 = np.where(leg_data == 10)[0]

    # Group consecutive contact indices into continuous segments
    for indices in np.split(indices_10, np.where(np.diff(indices_10) != 1)[0] + 1):
        first_idx = indices[0]
        last_idx = indices[-1]
        array_leg.append([first_idx, last_idx])

    # Convert contact segments into step ranges
    for i in range(len(array_leg)):
        first_value = array_leg[i][0]
        if i + 1 < len(array_leg):
            second_value = array_leg[i + 1][0]
        else:
            second_value = array_leg[i][1]
        result_steps.append([first_value, second_value])

    result_steps = np.array(result_steps)

    # Filter out short steps
    filtered_steps = [
        step for step in result_steps
        if (step[1] - step[0] + 1) >= min_points
    ]

    # Start from the user-defined step index (1-based)
    if len(filtered_steps) >= start_step:
        filtered_steps = filtered_steps[start_step - 1:]

    # Keep only the requested number of steps
    if len(filtered_steps) > num_steps:
        selected_steps = filtered_steps[:num_steps]
    else:
        selected_steps = filtered_steps

    # Convert output to float to preserve original workflow compatibility
    result_steps = [[float(step[0]), float(step[1])] for step in selected_steps]

    return result_steps


def detect_cycles_xsens_select_step(leg_data, min_points, *steps):
    """
    Detect gait-step ranges from an Xsens foot-contact signal and return only
    the user-specified step numbers.

    Parameters
    ----------
    leg_data : array-like
        Foot-contact signal in which contact is encoded as 10.
    min_points : int
        Minimum number of points required for a step to be retained.
    *steps : int
        Variable number of 1-based step indices to extract.

    Returns
    -------
    list of list of float
        Selected step ranges in the format:
        [[start_1, end_1], [start_2, end_2], ...]
    """
    result_steps = []
    array_leg = []

    # Find indices where the Xsens contact signal equals 10
    indices_10 = np.where(leg_data == 10)[0]

    # Group consecutive indices where contact is present
    for indices in np.split(indices_10, np.where(np.diff(indices_10) != 1)[0] + 1):
        first_idx = indices[0]
        last_idx = indices[-1]
        array_leg.append([first_idx, last_idx])

    # Convert contact segments into step ranges
    for i in range(len(array_leg)):
        first_value = array_leg[i][0]
        if i + 1 < len(array_leg):
            second_value = array_leg[i + 1][0]
        else:
            second_value = array_leg[i][1]
        result_steps.append([first_value, second_value])

    result_steps = np.array(result_steps)

    # Filter out short steps
    filtered_steps = [
        step for step in result_steps
        if (step[1] - step[0] + 1) >= min_points
    ]

    # Select only user-requested step numbers
    selected_steps = []
    for step_idx in steps:
        if step_idx - 1 < len(filtered_steps):
            selected_steps.append(filtered_steps[step_idx - 1])

    # Convert output to float to preserve original workflow compatibility
    result_steps = [[float(step[0]), float(step[1])] for step in selected_steps]

    return result_steps


def detect_cycles_naroxon(leg_data, min_points, num_steps, start_step):
    """
    Detect gait-step ranges from a Noraxon foot-contact signal.

    Parameters
    ----------
    leg_data : array-like
        Foot-contact signal in which contact is encoded as 1000.
    min_points : int
        Minimum number of points required for a step to be retained.
    num_steps : int
        Maximum number of steps to return.
    start_step : int
        Step number to start selection from (1-based index).

    Returns
    -------
    list of list of float
        Detected step ranges in the format:
        [[start_1, end_1], [start_2, end_2], ...]
    """
    result_steps = []
    array_leg = []

    # Find indices where the Noraxon contact signal equals 1000
    indices_1000 = np.where(leg_data == 1000)[0]

    # Group consecutive contact indices into continuous segments
    for indices in np.split(indices_1000, np.where(np.diff(indices_1000) != 1)[0] + 1):
        first_idx = indices[0]
        last_idx = indices[-1]
        array_leg.append([first_idx, last_idx])

    # Convert contact segments into step ranges
    for i in range(len(array_leg)):
        first_value = array_leg[i][0]
        if i + 1 < len(array_leg):
            second_value = array_leg[i + 1][0]
        else:
            second_value = array_leg[i][1]
        result_steps.append([first_value, second_value])

    result_steps = np.array(result_steps)

    # Filter out short steps
    filtered_steps = [
        step for step in result_steps
        if (step[1] - step[0] + 1) >= min_points
    ]

    # Start from the user-defined step index (1-based)
    if len(filtered_steps) >= start_step:
        filtered_steps = filtered_steps[start_step - 1:]

    # Keep only the requested number of steps
    if len(filtered_steps) > num_steps:
        selected_steps = filtered_steps[:num_steps]
    else:
        selected_steps = filtered_steps

    # Convert output to float to preserve original workflow compatibility
    result_steps = [[float(step[0]), float(step[1])] for step in selected_steps]

    return result_steps


def detect_cycles_naroxon_select_step(leg_data, min_points, *steps):
    """
    Detect gait-step ranges from a Noraxon foot-contact signal and return only
    the user-specified step numbers.

    Parameters
    ----------
    leg_data : array-like
        Foot-contact signal in which contact is encoded as 1000.
    min_points : int
        Minimum number of points required for a step to be retained.
    *steps : int
        Variable number of 1-based step indices to extract.

    Returns
    -------
    list of list of float
        Selected step ranges in the format:
        [[start_1, end_1], [start_2, end_2], ...]
    """
    result_steps = []
    array_leg = []

    # Find indices where the Noraxon contact signal equals 1000
    indices_1000 = np.where(leg_data == 1000)[0]

    # Group consecutive indices where contact is present
    for indices in np.split(indices_1000, np.where(np.diff(indices_1000) != 1)[0] + 1):
        first_idx = indices[0]
        last_idx = indices[-1]
        array_leg.append([first_idx, last_idx])

    # Convert contact segments into step ranges
    for i in range(len(array_leg)):
        first_value = array_leg[i][0]
        if i + 1 < len(array_leg):
            second_value = array_leg[i + 1][0]
        else:
            second_value = array_leg[i][1]
        result_steps.append([first_value, second_value])

    result_steps = np.array(result_steps)

    # Filter out short steps
    filtered_steps = [
        step for step in result_steps
        if (step[1] - step[0] + 1) >= min_points
    ]

    # Select only user-requested step numbers
    selected_steps = []
    for step_idx in steps:
        if step_idx - 1 < len(filtered_steps):
            selected_steps.append(filtered_steps[step_idx - 1])

    # Convert output to float to preserve original workflow compatibility
    result_steps = [[float(step[0]), float(step[1])] for step in selected_steps]

    return result_steps