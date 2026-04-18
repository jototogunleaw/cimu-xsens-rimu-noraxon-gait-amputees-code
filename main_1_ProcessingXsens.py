"""
main_1_ProcessingXsensData.py

Description
-----------
This script processes raw Xsens CSV files for gait analysis.

Main steps:
1. Load multiple CSV files (trials)
2. Compute joint kinematics (hip, knee, ankle) for both limbs
3. Extract shank acceleration signals
4. Estimate foot contact events from acceleration
5. Export processed results to Excel

Input
-----
- CSV files from Xsens system (pattern-based loading)

Output
------
- One Excel file per trial with processed kinematics and foot contact signals

Notes
-----
- Left limb is labeled as "Amputated"
- Right limb is labeled as "Sound"
- Depends on functions defined in `calculation.py`
"""

# =============================================================================
# Import libraries
# =============================================================================

import glob
import pandas as pd
from pathlib import Path

from calculation import (
    calculate_angle,
    calculate_angle_2,
    calculate_angle_5,
    calculate_z_axis_invert,
    calculate_foot_contact,
)

# =============================================================================
# Configuration (Cross-platform paths)
# =============================================================================

# Root directory of the project (auto-detect current script location)
BASE_DIR = Path(__file__).resolve().parent

# Input directory (modify folder structure as needed)
INPUT_DIR = BASE_DIR / "data" / "raw"

# File pattern (glob style)
INPUT_FILE_PATTERN = str(INPUT_DIR / "S16_T[1-5]_*.csv")

# Output directory
OUTPUT_PATH = BASE_DIR / "data" / "processed"

# Ensure output directory exists
OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

# Label mapping (for output naming)
LEFT_LABEL = "Amputated"
RIGHT_LABEL = "Sound"

# =============================================================================
# Load CSV files
# =============================================================================

file_paths = glob.glob(INPUT_FILE_PATTERN)

# Dictionary to store all loaded trials
trial_data = {}

for file_path in file_paths:
    file_name = file_path.split("\\")[-1].replace(".csv", "")

    try:
        trial_data[file_name] = pd.read_csv(
            file_path,
            delimiter=",",
            on_bad_lines="skip",
            encoding="utf-8",
        )
    except pd.errors.ParserError as error:
        print(f"[ERROR] ParserError in file '{file_name}': {error}")
    except Exception as error:
        print(f"[ERROR] Failed to load '{file_name}': {error}")

# =============================================================================
# Process each trial
# =============================================================================

for file_path in file_paths:

    # Extract trial name (e.g., S16_T1)
    parts = file_path.split("\\")[-1].split("_")
    trial_name = f"{parts[0]}_{parts[1]}"

    print(f"[INFO] Processing {trial_name}")

    # -------------------------------------------------------------------------
    # RIGHT limb (Sound side)
    # -------------------------------------------------------------------------
    hip_R_flexion = calculate_angle(trial_data, trial_name, 'pelvis', 'Euler_X', 'right_thigh', 'Euler_Y') * (-1)
    hip_R_abduction = calculate_angle(trial_data, trial_name, 'pelvis', 'Euler_Y', 'right_thigh', 'Euler_X')
    hip_R_rotation = calculate_angle(trial_data, trial_name, 'pelvis', 'Euler_Z', 'right_thigh', 'Euler_Z')

    knee_R_flexion = calculate_angle(trial_data, trial_name, 'right_thigh', 'Euler_Y', 'right_calf', 'Euler_Y')
    knee_R_abduction = calculate_angle_2(trial_data, trial_name, 'right_thigh', 'Euler_X', 'right_calf', 'Euler_X')
    knee_R_rotation = calculate_angle(trial_data, trial_name, 'right_thigh', 'Euler_Z', 'right_calf', 'Euler_Z')

    ankle_R_flexion = calculate_angle(trial_data, trial_name, 'right_calf', 'Euler_Y', 'right_foot', 'Euler_X')
    ankle_R_abduction = calculate_angle(trial_data, trial_name, 'right_calf', 'Euler_Z', 'right_foot', 'Euler_Z')
    ankle_R_rotation = calculate_angle(trial_data, trial_name, 'right_calf', 'Euler_X', 'right_foot', 'Euler_Y')
    ankle_R_abduction = calculate_z_axis_invert(ankle_R_abduction)

    shank_R_acc_x = trial_data[f'{trial_name}_right_calf']['Acc_X']
    shank_R_acc_y = trial_data[f'{trial_name}_right_calf']['Acc_Y']
    shank_R_acc_z = trial_data[f'{trial_name}_right_calf']['Acc_Z']

    # -------------------------------------------------------------------------
    # LEFT limb (Amputated side)
    # -------------------------------------------------------------------------
    hip_L_flexion = calculate_angle(trial_data, trial_name, 'pelvis', 'Euler_X', 'left_thigh', 'Euler_Y')
    hip_L_abduction = calculate_angle(trial_data, trial_name, 'pelvis', 'Euler_Y', 'left_thigh', 'Euler_X')
    hip_L_rotation = calculate_angle_2(trial_data, trial_name, 'pelvis', 'Euler_Z', 'left_thigh', 'Euler_Z')

    knee_L_flexion = calculate_angle(trial_data, trial_name, 'left_thigh', 'Euler_Y', 'left_calf', 'Euler_Y')
    knee_L_abduction = calculate_angle_2(trial_data, trial_name, 'left_thigh', 'Euler_X', 'left_calf', 'Euler_X')
    knee_L_rotation = calculate_angle(trial_data, trial_name, 'left_thigh', 'Euler_Z', 'left_calf', 'Euler_Z')

    ankle_L_flexion = calculate_angle_5(trial_data, trial_name, 'left_calf', 'Euler_Y', 'left_foot', 'Euler_X')
    ankle_L_abduction = calculate_angle(trial_data, trial_name, 'left_calf', 'Euler_Z', 'left_foot', 'Euler_Z')
    ankle_L_rotation = calculate_angle(trial_data, trial_name, 'left_calf', 'Euler_X', 'left_foot', 'Euler_Y')
    ankle_L_abduction = calculate_z_axis_invert(ankle_L_abduction)

    shank_L_acc_x = trial_data[f'{trial_name}_left_calf']['Acc_X']
    shank_L_acc_y = trial_data[f'{trial_name}_left_calf']['Acc_Y']
    shank_L_acc_z = trial_data[f'{trial_name}_left_calf']['Acc_Z']

    # -------------------------------------------------------------------------
    # Combine all features into a single DataFrame
    # -------------------------------------------------------------------------
    column_names = [
        f'hip_{RIGHT_LABEL}_flexion', f'hip_{RIGHT_LABEL}_abduction', f'hip_{RIGHT_LABEL}_rotation',
        f'knee_{RIGHT_LABEL}_flexion', f'knee_{RIGHT_LABEL}_abduction', f'knee_{RIGHT_LABEL}_rotation',
        f'ankle_{RIGHT_LABEL}_flexion', f'ankle_{RIGHT_LABEL}_rotation', f'ankle_{RIGHT_LABEL}_abduction',
        f'shank_{RIGHT_LABEL}_acc_x', f'shank_{RIGHT_LABEL}_acc_y', f'shank_{RIGHT_LABEL}_acc_z',

        f'hip_{LEFT_LABEL}_flexion', f'hip_{LEFT_LABEL}_abduction', f'hip_{LEFT_LABEL}_rotation',
        f'knee_{LEFT_LABEL}_flexion', f'knee_{LEFT_LABEL}_abduction', f'knee_{LEFT_LABEL}_rotation',
        f'ankle_{LEFT_LABEL}_flexion', f'ankle_{LEFT_LABEL}_rotation', f'ankle_{LEFT_LABEL}_abduction',
        f'shank_{LEFT_LABEL}_acc_x', f'shank_{LEFT_LABEL}_acc_y', f'shank_{LEFT_LABEL}_acc_z'
    ]

    combined_df = pd.concat([
        hip_R_flexion, hip_R_abduction, hip_R_rotation,
        knee_R_flexion, knee_R_abduction, knee_R_rotation,
        ankle_R_flexion, ankle_R_rotation, ankle_R_abduction,
        shank_R_acc_x, shank_R_acc_y, shank_R_acc_z,

        hip_L_flexion, hip_L_abduction, hip_L_rotation,
        knee_L_flexion, knee_L_abduction, knee_L_rotation,
        ankle_L_flexion, ankle_L_rotation, ankle_L_abduction,
        shank_L_acc_x, shank_L_acc_y, shank_L_acc_z
    ], axis=1)

    combined_df.columns = column_names

    # Remove rows with missing values
    combined_df = combined_df.dropna()

    # -------------------------------------------------------------------------
    # Foot contact detection
    # -------------------------------------------------------------------------
    combined_df = calculate_foot_contact(
        combined_df,
        f'shank_{LEFT_LABEL}_acc_x', f'shank_{LEFT_LABEL}_acc_y', f'shank_{LEFT_LABEL}_acc_z',
        f'foot_{LEFT_LABEL}_contact_10',
        height=10, distance=50, prominence=1, initial_value=10
    )

    combined_df = calculate_foot_contact(
        combined_df,
        f'shank_{LEFT_LABEL}_acc_x', f'shank_{LEFT_LABEL}_acc_y', f'shank_{LEFT_LABEL}_acc_z',
        f'foot_{LEFT_LABEL}_contact_0',
        height=10, distance=50, prominence=1, initial_value=0
    )

    combined_df = calculate_foot_contact(
        combined_df,
        f'shank_{RIGHT_LABEL}_acc_x', f'shank_{RIGHT_LABEL}_acc_y', f'shank_{RIGHT_LABEL}_acc_z',
        f'foot_{RIGHT_LABEL}_contact_10',
        height=10, distance=50, prominence=1, initial_value=10
    )

    combined_df = calculate_foot_contact(
        combined_df,
        f'shank_{RIGHT_LABEL}_acc_x', f'shank_{RIGHT_LABEL}_acc_y', f'shank_{RIGHT_LABEL}_acc_z',
        f'foot_{RIGHT_LABEL}_contact_0',
        height=10, distance=50, prominence=1, initial_value=0
    )

    # -------------------------------------------------------------------------
    # Export results
    # -------------------------------------------------------------------------
    output_file = fr'{OUTPUT_PATH}\{trial_name}.xlsx'
    combined_df.to_excel(output_file, index=False)

    print(f"[DONE] Saved: {output_file}")