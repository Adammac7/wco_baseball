import csv
import json
import os
from typing import Iterable, Dict, List, Any

# Columns to keep (in this exact order)
COLUMNS: List[str] = [
    "Date",
    "GameUID",
    "Pitcher",
    "PitcherThrows",
    "Batter",
    "BatterSide",
    "BatterTeam",
    "Inning",
    "Outs",
    "Balls",
    "Strikes",
    "TaggedPitchType",
    "PitchCall",
    "KorBB",
    "TaggedHitType",
    "PlayResult",
    "OutsOnPlay",
    "RunScored",
    "RelSpeed",
    "VertRelAngle",
    "SpinRate",
    "SpinAxis",
    "RelHeight",
    "RelSide",
    "Extension",
    "InducedVertBreak",
    "HorzBreak",
    "PlateLocHeight",
    "PlateLocSide",
    "VertApprAngle",
    "HorzApprAngle",
    "ExitSpeed",
    "Angle",
    "Direction",
    "HitSpinRate",
    "Distance",
    "Catcher",
    "SpeedDrop",
    "ThrowSpeed",
    "PopTime",
    "ExchangeTime",
    "TimeToBase",
    "BasePositionX",
    "BasePositionY",
    "BasePositionZ",
    "PitchReleaseConfidence",
    "PitchLocationConfidence",
    "PitchMovementConfidence",
    "HitLaunchConfidence",
    "HitLandingConfidence",
    "CatcherThrowReleaseConfidence",
    "CatcherThrowLocationCondience",
]

# Which columns should be integers vs floats
INT_FIELDS = {
    "Inning","Outs","Balls","Strikes","OutsOnPlay","RunScored"
}

FLOAT_FIELDS = {
    "RelSpeed","VertRelAngle","SpinRate","SpinAxis","RelHeight","RelSide","Extension",
    "InducedVertBreak","HorzBreak","PlateLocHeight","PlateLocSide","VertApprAngle",
    "HorzApprAngle","ExitSpeed","Angle","Direction","HitSpinRate","Distance",
    "SpeedDrop","ThrowSpeed","PopTime","ExchangeTime","TimeToBase",
    "BasePositionX","BasePositionY","BasePositionZ",
    "PitchReleaseConfidence","PitchLocationConfidence","PitchMovementConfidence",
    "HitLaunchConfidence","HitLandingConfidence","CatcherThrowReleaseConfidence",
    "CatcherThrowLocationCondience"
}

BLANK_STRINGS = {"", "na", "n/a", "nan", "null", "none", "-"}

def _is_blank(val: Any) -> bool:
    if val is None:
        return True
    s = str(val).strip().lower()
    return s in BLANK_STRINGS

def to_int_or_null(v: Any):
    if _is_blank(v):
        return None
    try:
        # handle strings like "12.0" by casting to float then int
        n = float(str(v).strip())
        return int(n)
    except Exception:
        return None

def to_float_or_null(v: Any):
    if _is_blank(v):
        return None
    try:
        return float(str(v).strip())
    except Exception:
        return None

def to_text_or_null(v: Any):
    if v is None:
        return None
    s = str(v).strip()
    return s if s != "" else None

def clean_row(row: Dict[str, Any]) -> Dict[str, Any]:
    cleaned: Dict[str, Any] = {}
    for col in COLUMNS:
        raw = row.get(col, None)
        if col in INT_FIELDS:
            cleaned[col] = to_int_or_null(raw)
        elif col in FLOAT_FIELDS:
            cleaned[col] = to_float_or_null(raw)
        else:
            cleaned[col] = to_text_or_null(raw)
    return cleaned

def csv_to_json( # works
    csv_file_path: str,
    columns: Iterable[str] = COLUMNS
) -> json:
    """
    Read csv_file_path, keep only `columns`, CLEAN values, and write to json_file_path.
    - Empty strings / NA-like tokens -> null
    - Integer/float columns cast to numbers (or null on failure)
    - Text trimmed; blank -> null
    """


    extracted: List[Dict[str, Any]] = []

    # newline='' avoids extra blank lines on Windows; utf-8-sig handles BOM if present
    with open(csv_file_path, mode='r', newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        # Normalize fieldnames by trimming whitespace to avoid header surprises
        if reader.fieldnames:
            reader.fieldnames = [fn.strip() if fn else fn for fn in reader.fieldnames]
        for row in reader:
            # Build a sub-dict and clean it
            subset = {col: row.get(col, None) for col in columns}
            extracted.append(clean_row(subset))

    return extracted

if __name__ == "__main__":
    # Example usage
    csv_file_path = 'All Intrasquads.csv'
    print(csv_to_json(csv_file_path))
    print("Done.")
    