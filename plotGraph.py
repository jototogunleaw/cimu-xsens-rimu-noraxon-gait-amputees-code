"""
plotGraph.py

Description
-----------
Utility functions for visualizing gait-analysis results.

This module provides:
1. plotgraph()
   - Plot multiple step profiles together with their average profile

2. plot_parameters()
   - Compare mean ± standard deviation profiles between Xsens and Noraxon

Notes
-----
- The plotting logic is intentionally kept close to the original implementation
  to preserve the current workflow and output style.
- The functions save figures directly to image files.
"""

import os

import matplotlib.pyplot as plt
import numpy as np


def plotgraph(
    df,
    column_pattern,
    column_average,
    title,
    xlabel,
    ylabel,
    filename,
    color_step,
    color_average,
):
    """
    Plot all step-specific columns matching a given pattern together with
    the corresponding average column.

    Parameters
    ----------
    df : pandas.DataFrame
        Input DataFrame containing step-wise and averaged parameters.

    column_pattern : str
        Pattern used to identify step-specific columns
        (e.g., 'hip_Sound_flexion_step').

    column_average : str
        Exact column name of the average profile
        (e.g., 'average_hip_Sound_flexion').

    title : str
        Figure title.

    xlabel : str
        X-axis label.

    ylabel : str
        Y-axis label.

    filename : str
        Output image file path.

    color_step : str
        Color used for individual step profiles.

    color_average : str
        Color used for the average profile.

    Returns
    -------
    None
        The figure is saved directly to disk.
    """
    # Find all step-specific columns matching the requested pattern
    columns_to_plot = [col for col in df.columns if column_pattern in col]

    plt.figure()

    # Plot each detected step profile
    step_count = 1
    for col in columns_to_plot:
        plt.plot(
            df.index,
            df[col],
            label=f"step{step_count}",
            color=color_step,
            linestyle="--",
        )
        step_count += 1

    # Plot the average profile if available
    if column_average in df.columns:
        plt.plot(
            df.index,
            df[column_average],
            label="average",
            color=color_average,
        )
    else:
        print(f"Warning: '{column_average}' not found in DataFrame columns.")

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend(title="Overall")
    plt.savefig(filename, bbox_inches="tight")
    plt.close()


def plot_parameters(df1, df2, columns_parameters, path_images, filename):
    """
    Compare mean ± standard deviation profiles between Xsens and Noraxon.

    Parameters
    ----------
    df1 : pandas.DataFrame
        DataFrame containing Xsens summary statistics.

    df2 : pandas.DataFrame
        DataFrame containing Noraxon summary statistics.

    columns_parameters : list of str
        List of base parameter names to plot.

    path_images : str or path-like
        Directory where output images will be saved.

    filename : str
        Reserved parameter from the original workflow.
        Currently not used inside the function, but kept for backward
        compatibility to avoid breaking existing calls.

    Returns
    -------
    None
        Comparison plots are saved directly to disk.
    """
    for param in columns_parameters:
        col_mean_1 = f"{param}_mean_sound_xsens"
        col_std_1 = f"{param}_std_sound_xsens"
        col_mean_2 = f"{param}_mean_sound_naroxon"
        col_std_2 = f"{param}_std_sound_naroxon"

        # Ensure all required summary-statistic columns are available
        if all(col in df1.columns for col in [col_mean_1, col_std_1]) and all(
            col in df2.columns for col in [col_mean_2, col_std_2]
        ):
            y_mean_1 = df1[col_mean_1]
            y_std_1 = df1[col_std_1]
            y_mean_2 = df2[col_mean_2]
            y_std_2 = df2[col_std_2]

            # Normalize x-axis to 0-100% gait cycle
            x = np.linspace(0, 100, len(y_mean_1))

            plt.figure()

            # Plot Noraxon mean ± standard deviation
            plt.plot(x, y_mean_2, label="Noraxon", color="g")
            plt.fill_between(
                x,
                y_mean_2 - y_std_2,
                y_mean_2 + y_std_2,
                color="g",
                alpha=0.3,
            )

            # Plot Xsens mean ± standard deviation
            plt.plot(x, y_mean_1, label="Xsens", color="b", linestyle="--")
            plt.fill_between(
                x,
                y_mean_1 - y_std_1,
                y_mean_1 + y_std_1,
                color="b",
                alpha=0.3,
            )

            plt.xlabel("Gait Cycle (%)")
            plt.ylabel("Angle (deg)")
            plt.title(f"sound_{param} Mean ± Std")
            plt.legend()
            plt.grid(True)

            output_path = os.path.join(path_images, f"sound_{param}.png")
            plt.savefig(output_path, bbox_inches="tight")
            plt.close()