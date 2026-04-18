"""
main_2_ResultXsens.py

Description
-----------
Post-processing pipeline for Xsens gait data.

This script:
1. Loads processed Xsens trial data (.xlsx)
2. Selects kinematic parameters (Sound / Amputated)
3. Extracts gait steps (manual or automatic)
4. Normalizes each step to 0–100% stance phase
5. Combines all steps into a single dataset
6. Computes average kinematic profiles
7. Generates plots for each parameter
8. Exports results + graphs to Excel

Notes
-----
- Currently uses manual step selection
- Automatic detection functions are available but commented out
"""

# =============================================================================
# Imports
# =============================================================================

import glob
import os
import time as tm
from pathlib import Path

import pandas as pd
from openpyxl.drawing.image import Image

from detection import detect_cycles_xsens, detect_cycles_xsens_select_step
from selected import select_parameters_sound_xsens, select_parameters_amputated_xsens
from divided import divide_step
from normalization import normalize_to_percentage
from addAllStep import add_steps
from calculation import average_step
from plotGraph import plotgraph

# =============================================================================
# Start timer
# =============================================================================

start_time = tm.time()

# =============================================================================
# Configuration (Cross-platform)
# =============================================================================

BASE_DIR = Path(__file__).resolve().parent

NAME_FILE = "S[1][6]_T[5]"

INPUT_DIR = BASE_DIR / "Result_ProcessingXsenx"
OUTPUT_DIR = BASE_DIR
IMAGE_DIR = BASE_DIR / "images_Xsens"

INPUT_FILE_PATTERN = str(INPUT_DIR / f"{NAME_FILE}.xlsx")
OUTPUT_FILE = OUTPUT_DIR / f"Result_Xsens_{NAME_FILE}.xlsx"

IMAGE_DIR.mkdir(parents=True, exist_ok=True)

# =============================================================================
# Processing
# =============================================================================

file_paths = glob.glob(INPUT_FILE_PATTERN)

with pd.ExcelWriter(OUTPUT_FILE, engine="openpyxl") as writer:

    for file_path in file_paths:

        file_name = Path(file_path).stem
        df = pd.read_excel(file_path)

        print(f"[INFO] Processing {file_name}")

        # ---------------------------------------------------------------------
        # Extract foot contact signals
        # ---------------------------------------------------------------------
        foot_contact_sound = df["foot_Sound_contact_0"]
        foot_contact_amputated = df["foot_Amputated_contact_0"]

        # ---------------------------------------------------------------------
        # Step detection (manual / automatic)
        # ---------------------------------------------------------------------
        # Automatic (optional)
        # sound_5step = detect_cycles_xsens_select_step(foot_contact_sound, 50, 5)
        # amputated_5step = detect_cycles_xsens_select_step(foot_contact_amputated, 50, 5)

        # Manual selection (current workflow)
        sound_5step = [[2650, 2756]]
        amputated_5step = [[2700, 2808]]

        # ---------------------------------------------------------------------
        # Select kinematic parameters
        # ---------------------------------------------------------------------
        kinematic_sound = select_parameters_sound_xsens(df)
        kinematic_amputated = select_parameters_amputated_xsens(df)

        # ---------------------------------------------------------------------
        # Divide into steps
        # ---------------------------------------------------------------------
        sound_steps = divide_step(kinematic_sound, sound_5step)
        amputated_steps = divide_step(kinematic_amputated, amputated_5step)

        # ---------------------------------------------------------------------
        # Normalize each step to 100 points (% stance phase)
        # ---------------------------------------------------------------------
        normalized_sound = {
            step: pd.DataFrame({
                col: normalize_to_percentage(step_df[col].values, 100)
                for col in step_df.columns
            })
            for step, step_df in sound_steps.items()
        }

        normalized_amputated = {
            step: pd.DataFrame({
                col: normalize_to_percentage(step_df[col].values, 100)
                for col in step_df.columns
            })
            for step, step_df in amputated_steps.items()
        }

        # ---------------------------------------------------------------------
        # Combine steps
        # ---------------------------------------------------------------------
        all_parameters = add_steps(pd.DataFrame(), normalized_sound)
        all_parameters = add_steps(all_parameters, normalized_amputated)

        # ---------------------------------------------------------------------
        # Average profiles
        # ---------------------------------------------------------------------
        columns_to_average = [
            "hip_Sound_flexion", "hip_Sound_abduction", "hip_Sound_rotation",
            "knee_Sound_flexion", "knee_Sound_abduction", "knee_Sound_rotation",
            "ankle_Sound_flexion", "ankle_Sound_rotation", "ankle_Sound_abduction",
            "hip_Amputated_flexion", "hip_Amputated_abduction", "hip_Amputated_rotation",
            "knee_Amputated_flexion", "knee_Amputated_abduction", "knee_Amputated_rotation",
            "ankle_Amputated_flexion", "ankle_Amputated_rotation", "ankle_Amputated_abduction",
        ]

        for col in columns_to_average:
            all_parameters = average_step(all_parameters, col)

        # ---------------------------------------------------------------------
        # Plot configuration
        # ---------------------------------------------------------------------
        graph_configs = [
            ("hip_Sound_flexion", "(deg)", "#FF9393", "#FF0000"),
            ("knee_Sound_flexion", "(deg)", "#00FF00", "#00B400"),
            ("ankle_Sound_flexion", "(deg)", "#6D6DFF", "#0000FF"),
            ("hip_Amputated_flexion", "(deg)", "#FF9393", "#FF0000"),
            ("knee_Amputated_flexion", "(deg)", "#00FF00", "#00B400"),
            ("ankle_Amputated_flexion", "(deg)", "#6D6DFF", "#0000FF"),
        ]

        # ---------------------------------------------------------------------
        # Plot graphs
        # ---------------------------------------------------------------------
        for param, unit, color_light, color_dark in graph_configs:

            step_col = f"{param}_step"
            avg_col = f"average_{param}"

            image_path = IMAGE_DIR / f"{param}_chart_{file_name}.png"

            plotgraph(
                all_parameters,
                step_col,
                avg_col,
                param,
                "%stance phase",
                unit,
                str(image_path),
                color_light,
                color_dark,
            )

        # ---------------------------------------------------------------------
        # Export data
        # ---------------------------------------------------------------------
        if not all_parameters.empty:
            all_parameters.to_excel(writer, sheet_name=file_name, index=False)

        worksheet = writer.sheets[file_name]

        # ---------------------------------------------------------------------
        # Insert images into Excel
        # ---------------------------------------------------------------------
        image_positions = [
            ("A2", "hip_Sound_flexion"),
            ("A25", "knee_Sound_flexion"),
            ("A48", "ankle_Sound_flexion"),
            ("J2", "hip_Amputated_flexion"),
            ("J25", "knee_Amputated_flexion"),
            ("J48", "ankle_Amputated_flexion"),
        ]

        for cell, param in image_positions:
            img_path = IMAGE_DIR / f"{param}_chart_{file_name}.png"
            if img_path.exists():
                worksheet.add_image(Image(str(img_path)), cell)

        print(f"[DONE] {file_name}")

# =============================================================================
# End timer
# =============================================================================

elapsed_time = tm.time() - start_time
print(f"[INFO] Elapsed time: {elapsed_time:.2f} seconds")