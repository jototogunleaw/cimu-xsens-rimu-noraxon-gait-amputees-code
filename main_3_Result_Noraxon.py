"""
main_3_ResultNaroxon.py

Description
-----------
Post-processing pipeline for Noraxon gait data.

This script:
1. Loads Noraxon trial data (.csv)
2. Detects gait steps from foot-contact signals
3. Selects kinematic parameters (Sound / Amputated)
4. Divides the continuous signals into step segments
5. Normalizes each step to 0-100% stance phase
6. Combines normalized steps into a single DataFrame
7. Computes average kinematic profiles across steps
8. Generates plots for each parameter
9. Exports results and graph images to an Excel workbook

Notes
-----
- The current workflow uses automatic step detection for both limbs.
- Optional manual step selection functions are retained in comments for
  future use.
- The original logic is preserved as closely as possible for reproducibility.
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

from detection import detect_cycles_naroxon, detect_cycles_naroxon_select_step
from selected import (
    select_parameters_sound_naroxon,
    select_parameters_amputated_naroxon,
)
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

NAME_FILE = "S01T[1]"

INPUT_DIR = BASE_DIR / "Dataset_Naroxon"
OUTPUT_DIR = BASE_DIR
IMAGE_DIR = BASE_DIR / "images_Naroxon"

INPUT_FILE_PATTERN = str(INPUT_DIR / f"{NAME_FILE}.csv")
OUTPUT_FILE = OUTPUT_DIR / f"Result_Naroxon{NAME_FILE}_test.xlsx"

IMAGE_DIR.mkdir(parents=True, exist_ok=True)

# =============================================================================
# Processing
# =============================================================================

file_paths = glob.glob(INPUT_FILE_PATTERN)

with pd.ExcelWriter(OUTPUT_FILE, engine="openpyxl") as writer:
    for file_path in file_paths:
        file_name = Path(file_path).stem
        df = pd.read_csv(file_path, low_memory=False)

        print(f"[INFO] Processing {file_name}")

        # ---------------------------------------------------------------------
        # Extract foot-contact signals
        # ---------------------------------------------------------------------
        foot_contact_sound = df["Noraxon MyoMotion-Segments-Foot Sound-Contact"]
        foot_contact_amputated = df["Noraxon MyoMotion-Segments-Foot Amputated-Contact"]

        # ---------------------------------------------------------------------
        # Detect gait steps
        # ---------------------------------------------------------------------
        # Automatic step detection (current workflow)
        sound_5step = detect_cycles_naroxon(
            foot_contact_sound,
            min_points=100,
            num_steps=5,
            start_step=5,
        )
        amputated_5step = detect_cycles_naroxon(
            foot_contact_amputated,
            min_points=100,
            num_steps=5,
            start_step=5,
        )

        # Optional manual / specific step selection
        # sound_5step = detect_cycles_naroxon_select_step(
        #     foot_contact_sound, 100, 5
        # )
        # amputated_5step = detect_cycles_naroxon_select_step(
        #     foot_contact_amputated, 100, 3
        # )

        print("sound event: ", sound_5step)
        print("amputated event: ", amputated_5step)

        # ---------------------------------------------------------------------
        # Select kinematic parameters
        # ---------------------------------------------------------------------
        kinematic_sound = select_parameters_sound_naroxon(df)
        kinematic_amputated = select_parameters_amputated_naroxon(df)

        # ---------------------------------------------------------------------
        # Divide continuous data into step segments
        # ---------------------------------------------------------------------
        sound_steps = divide_step(kinematic_sound, sound_5step)
        amputated_steps = divide_step(kinematic_amputated, amputated_5step)

        # ---------------------------------------------------------------------
        # Normalize each step to 100 points (% stance phase)
        # ---------------------------------------------------------------------
        normalized_sound = {
            step: pd.DataFrame(
                {
                    col: normalize_to_percentage(step_df[col].values, target_points=100)
                    for col in step_df.columns
                }
            )
            for step, step_df in sound_steps.items()
        }

        normalized_amputated = {
            step: pd.DataFrame(
                {
                    col: normalize_to_percentage(step_df[col].values, target_points=100)
                    for col in step_df.columns
                }
            )
            for step, step_df in amputated_steps.items()
        }

        # ---------------------------------------------------------------------
        # Combine all normalized steps into one DataFrame
        # ---------------------------------------------------------------------
        all_parameters = add_steps(pd.DataFrame(), normalized_sound)
        all_parameters = add_steps(all_parameters, normalized_amputated)

        # ---------------------------------------------------------------------
        # Compute average profiles across steps
        # ---------------------------------------------------------------------
        columns_to_average = [
            "Sound Hip Flexion (deg)",
            "Sound Hip Abduction (deg)",
            "Sound Hip Rotation Ext (deg)",
            "Sound Knee Flexion (deg)",
            "Sound Knee Abduction (deg)",
            "Sound Knee Rotation Ext (deg)",
            "Sound Ankle Dorsiflexion (deg)",
            "Sound Ankle Abduction (deg)",
            "Sound Ankle Inversion (deg)",
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

        for col in columns_to_average:
            all_parameters = average_step(all_parameters, col)

        # ---------------------------------------------------------------------
        # Plot configuration
        # ---------------------------------------------------------------------
        graph_configs = [
            ("Sound Hip Flexion (deg)", "(deg)", "#FF9393", "#FF0000"),
            ("Sound Hip Abduction (deg)", "(deg)", "#FF9393", "#FF0000"),
            ("Sound Hip Rotation Ext (deg)", "(deg)", "#FF9393", "#FF0000"),
            ("Sound Knee Flexion (deg)", "(deg)", "#00FF00", "#00B400"),
            ("Sound Knee Abduction (deg)", "(deg)", "#00FF00", "#00B400"),
            ("Sound Knee Rotation Ext (deg)", "(deg)", "#00FF00", "#00B400"),
            ("Sound Ankle Dorsiflexion (deg)", "(deg)", "#6D6DFF", "#0000FF"),
            ("Sound Ankle Abduction (deg)", "(deg)", "#6D6DFF", "#0000FF"),
            ("Sound Ankle Inversion (deg)", "(deg)", "#6D6DFF", "#0000FF"),
            ("Amputated Hip Flexion (deg)", "(deg)", "#FF9393", "#FF0000"),
            ("Amputated Hip Abduction (deg)", "(deg)", "#FF9393", "#FF0000"),
            ("Amputated Hip Rotation Ext (deg)", "(deg)", "#FF9393", "#FF0000"),
            ("Amputated Knee Flexion (deg)", "(deg)", "#00FF00", "#00B400"),
            ("Amputated Knee Abduction (deg)", "(deg)", "#00FF00", "#00B400"),
            ("Amputated Knee Rotation Ext (deg)", "(deg)", "#00FF00", "#00B400"),
            ("Amputated Ankle Dorsiflexion (deg)", "(deg)", "#6D6DFF", "#0000FF"),
            ("Amputated Ankle Abduction (deg)", "(deg)", "#6D6DFF", "#0000FF"),
            ("Amputated Ankle Inversion (deg)", "(deg)", "#6D6DFF", "#0000FF"),
        ]

        # ---------------------------------------------------------------------
        # Generate graphs
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
        # Export tabular results to Excel
        # ---------------------------------------------------------------------
        if not all_parameters.empty:
            all_parameters.to_excel(writer, sheet_name=file_name, index=False)
        else:
            print(f"[WARNING] No data to write for {file_name}")
            writer.book.create_sheet(title=file_name)

        worksheet = writer.sheets[file_name]

        # ---------------------------------------------------------------------
        # Export detected time-event table
        # ---------------------------------------------------------------------
        time_event_df = pd.DataFrame(
            {
                "Sound_IC1": [s[0] for s in sound_5step],
                "Sound_IC2": [s[1] for s in sound_5step],
                "Amputated_IC1": [a[0] for a in amputated_5step],
                "Amputated_IC2": [a[1] for a in amputated_5step],
            }
        )
        time_event_df.to_excel(writer, sheet_name="time_event", index=False)

        # ---------------------------------------------------------------------
        # Insert graph images into Excel
        # ---------------------------------------------------------------------
        images = [
            ("A2", f"Sound Hip Flexion (deg)_chart_{file_name}.png"),
            ("S2", f"Sound Hip Abduction (deg)_chart_{file_name}.png"),
            ("AK2", f"Sound Hip Rotation Ext (deg)_chart_{file_name}.png"),
            ("A25", f"Sound Knee Flexion (deg)_chart_{file_name}.png"),
            ("S25", f"Sound Knee Abduction (deg)_chart_{file_name}.png"),
            ("AK25", f"Sound Knee Rotation Ext (deg)_chart_{file_name}.png"),
            ("A48", f"Sound Ankle Dorsiflexion (deg)_chart_{file_name}.png"),
            ("S48", f"Sound Ankle Abduction (deg)_chart_{file_name}.png"),
            ("AK48", f"Sound Ankle Inversion (deg)_chart_{file_name}.png"),
            ("J2", f"Amputated Hip Flexion (deg)_chart_{file_name}.png"),
            ("AB2", f"Amputated Hip Abduction (deg)_chart_{file_name}.png"),
            ("AT2", f"Amputated Hip Rotation Ext (deg)_chart_{file_name}.png"),
            ("J25", f"Amputated Knee Flexion (deg)_chart_{file_name}.png"),
            ("AB25", f"Amputated Knee Abduction (deg)_chart_{file_name}.png"),
            ("AT25", f"Amputated Knee Rotation Ext (deg)_chart_{file_name}.png"),
            ("J48", f"Amputated Ankle Dorsiflexion (deg)_chart_{file_name}.png"),
            ("AB48", f"Amputated Ankle Abduction (deg)_chart_{file_name}.png"),
            ("AT48", f"Amputated Ankle Inversion (deg)_chart_{file_name}.png"),
        ]

        for cell, image_name in images:
            image_path = os.path.join(IMAGE_DIR, image_name)
            if os.path.exists(image_path):
                img = Image(image_path)
                worksheet.add_image(img, cell)
            else:
                print(f"[WARNING] Image not found: {image_path}")

        print(f"[DONE] {file_name} processed successfully.")

# =============================================================================
# End timer
# =============================================================================

elapsed_time = tm.time() - start_time
print(f"[INFO] Elapsed time: {elapsed_time:.2f} seconds")
