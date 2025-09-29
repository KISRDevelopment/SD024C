import numpy as np
import pandas as pd
from typing import Optional, Dict
from .percentile_table import GRADE_TABLES

def _pick_round_up_row(data_table: pd.DataFrame, raw_value: Optional[int], raw_col: str) -> int:
    """
    Round-up (CEIL) selection:
      - If raw_value is exactly in the table, pick that row.
      - Else choose the next higher available raw threshold.
      - If raw_value > max threshold → clamp to last row.
      - If raw_value < min threshold → pick first row.
    """
    ordered_column = data_table[[raw_col]].dropna().copy().sort_values(raw_col, ascending=True)
    vals = ordered_column[raw_col].to_numpy()

    if raw_value is None:
        return int(ordered_column.index[0])  # first row index in original data_table

    pos = np.searchsorted(vals, raw_value, side="left")  # CEIL position
    if pos >= len(vals):
        pos = len(vals) - 1  # clamp to last

    # map back to original data_table index
    return int(ordered_column.index[pos])

def lookup_scores_primary(grade: str,test1_raw: Optional[int], test2_raw: Optional[int], test3_raw: Optional[int],test4_raw: Optional[int], test5_raw: Optional[int], test6_raw: Optional[int],
) -> Dict[str, Dict[str, Optional[int]]]:
    """
    Uses ROUND-UP rule per client guideline stated in Chapter 4 of the booklet
    Returns a dict:
      {'test1': {'letter': str, 'percentile': int, 'std': int}, ...}
    """
    data_table = GRADE_TABLES[str(grade)]
    subtests_config = [
        ("test1_Raw_score","test1_Modified_standard", test1_raw),
        ("test2_Raw_score","test2_Modified_standard", test2_raw),
        ("test3_Raw_score","test3_Modified_standard", test3_raw),
        ("test4_Raw_score","test4_Modified_standard", test4_raw),
        ("test5_Raw_score","test5_Modified_standard", test5_raw),
        ("test6_Raw_score","test6_Modified_standard", test6_raw),
    ]

    out: Dict[str, Dict[str, Optional[int]]] = {}
    for i, (raw_col, std_col, raw_val) in enumerate(subtests_config, start=1):
        if raw_col not in data_table.columns or std_col not in data_table.columns:
            out[f"test{i}"] = {"letter": None, "percentile": None, "std": None}
            continue

        row = data_table.loc[_pick_round_up_row(data_table, raw_val, raw_col)]
        out[f"test{i}"] = {
            "letter":     str(row["Percentile_Letter"]),
            "percentile": int(row["Percentile_Number"]),
            "std":        int(row[std_col]),
        }
    return out

def lookup_scores_secondary(grade: str,test1_raw: Optional[int], test2_raw: Optional[int], test3_raw: Optional[int],test4_raw: Optional[int],
) -> Dict[str, Dict[str, Optional[int]]]:
    """
    Uses ROUND-UP rule per client guideline stated in Chapter 4 of the booklet
    Returns a dict:
      {'test1': {'letter': str, 'percentile': int, 'std': int}, ...}
    """
    data_table = GRADE_TABLES[str(grade)]
    subtests_config = [
        ("test1_Raw_score","test1_Modified_standard", test1_raw),
        ("test2_Raw_score","test2_Modified_standard", test2_raw),
        ("test3_Raw_score","test3_Modified_standard", test3_raw),
        ("test4_Raw_score","test4_Modified_standard", test4_raw),
    ]

    out: Dict[str, Dict[str, Optional[int]]] = {}
    for i, (raw_col, std_col, raw_val) in enumerate(subtests_config, start=1):
        if raw_col not in data_table.columns or std_col not in data_table.columns:
            out[f"test{i}"] = {"letter": None, "percentile": None, "std": None}
            continue

        row = data_table.loc[_pick_round_up_row(data_table, raw_val, raw_col)]
        out[f"test{i}"] = {
            "letter":     str(row["Percentile_Letter"]),
            "percentile": int(row["Percentile_Number"]),
            "std":        int(row[std_col]),
        }
    return out
