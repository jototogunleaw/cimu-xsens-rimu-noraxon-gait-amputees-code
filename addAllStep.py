"""
addAllStep.py

Description
-----------
Utility function for combining multiple normalized step DataFrames into a
single DataFrame.

For each step:
1. The original column names are renamed by appending a step suffix
   (e.g., '_step1', '_step2', ...)
2. The renamed step DataFrame is concatenated column-wise to the output table

This is useful for preparing a single wide-format DataFrame that contains
all normalized gait-step parameters for subsequent averaging and plotting.

Notes
-----
- The input dictionary is expected to have keys such as:
    "Step_1", "Step_2", ...
- The function preserves the original step-ordering logic from the project.
"""

import pandas as pd


def add_steps(all_parameters, df, step_start=1):
    """
    Append multiple normalized step DataFrames into a single wide-format DataFrame.

    Parameters
    ----------
    all_parameters : pandas.DataFrame
        Existing output DataFrame to which renamed step columns will be added.
        This may be an empty DataFrame on the first call.

    df : dict
        Dictionary of step DataFrames, typically in the format:
        {
            "Step_1": DataFrame,
            "Step_2": DataFrame,
            ...
        }

    step_start : int, optional (default=1)
        Starting index used when assigning step suffixes to the column names.
        For example, if step_start=3, columns will be renamed as:
        parameter_step3, parameter_step4, ...

    Returns
    -------
    pandas.DataFrame
        Combined DataFrame containing all appended step-specific columns.

    Example
    -------
    >>> all_parameters = pd.DataFrame()
    >>> all_parameters = add_steps(all_parameters, normalized_steps, step_start=1)

    Notes
    -----
    - The step number is extracted from keys such as "Step_1".
    - Column names are renamed before concatenation to preserve step identity.
    - A copy of each step DataFrame is used before renaming columns to avoid
      modifying the original input DataFrames in place.
    """
    for k, step_data in df.items():
        # Extract the numeric part from keys such as "Step_1"
        step_num = int(k.split("_")[1])

        # Preserve the original numbering logic from the existing workflow
        step_num = step_num - 1

        # Rename columns to indicate the corresponding step number
        new_columns = [
            f"{col}_step{step_start + step_num}"
            for col in step_data.columns
        ]

        # Use a copy to avoid modifying the original DataFrame in the input dict
        renamed_step_data = step_data.copy()
        renamed_step_data.columns = new_columns

        # Concatenate step-specific columns into the output DataFrame
        all_parameters = pd.concat([all_parameters, renamed_step_data], axis=1)

    return all_parameters