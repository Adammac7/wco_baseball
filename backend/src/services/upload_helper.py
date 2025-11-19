import csv
import json
import os
from typing import Iterable, Dict, List, Any


class upload_helper:
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

    def _is_blank(self, val: Any) -> bool:
        if val is None:
            return True
        s = str(val).strip().lower()
        return s in self.BLANK_STRINGS

    def to_int_or_null(self, v: Any):
        if self._is_blank(v):
            return None
        try:
            # handle strings like "12.0" by casting to float then int
            n = float(self, str(v).strip())
            return int(n)
        except Exception:
            return None

    def to_float_or_null(self, v: Any):
        if self._is_blank(v):
            return None
        try:
            return float(str(v).strip())
        except Exception:
            return None
    
    def to_text_or_null(self, v: Any):
        if v is None:
            return None
        s = str(v).strip()
        return s if s != "" else None

    def clean_row(self, row: Dict[str, Any]) -> Dict[str, Any]:
        cleaned: Dict[str, Any] = {}
        for col in self.COLUMNS:
            raw = row.get(col, None)
            if col in self.INT_FIELDS:
                cleaned[col] = self.to_int_or_null(raw)
            elif col in self.FLOAT_FIELDS:
                cleaned[col] = self.to_float_or_null(raw)
            else:
                cleaned[col] = self.to_text_or_null(raw)
        return cleaned

    def csv_to_json(self, # works
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
                extracted.append(self.clean_row(subset))

        return extracted

    stat_cols = [
    "Name",
    "PA",
    "AB",
    "H",
    "2B",
    "3B",
    "HR",
    "K",
    "BB",
    "AVG",
    "OBP",
    "SLG",
    "OPS",
    "K%",
    "BB%",
    "BBE",
    "EV",
    "90thEV",
    "MAXEV",
    "HHLA",
    "HH%",
    "BRL%",
    "GB%",
    "LD%",
    "FB%",
    "PU%",
    "P",
    "SWING%",
    "WHIFF%",
    "CHASE%",
    "IZ SWING%",
    "IZ MISS%",
    "FPSWING%",
    "bWar",
    "fWar",
    "OPS+",
    "WRC+",
    "wOBP"
]


    def calc_new_stats(self, new_data: json) -> json:
                
            
            pass

    if __name__ == "__main__":
        # Example usage
        csv_file_path = 'All Intrasquads.csv'
        print(csv_to_json(csv_file_path))
        print("Done.")
        