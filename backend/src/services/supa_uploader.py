# backend/scripts/import_json_to_supabase.py

import time
from typing import List, Dict, Any
from src.services.supabase_client import supabase  # uses backend/.env


class Supa_uploader:
    def __init__(
        self,
        supabase_client,
        json_file,      # <-- now this should be actual list/dict data
        table,
        chunk_size=200,
        upsert=False,
        on_conflict="id",
    ):
        self.supabase = supabase_client or supabase
        self.json_data = json_file   # <-- renamed for clarity
        self.table = table
        self.chunk_size = chunk_size
        self.upsert = upsert
        self.on_conflict = on_conflict
        print(table, "uploader initialized.")

    def chunk_array(self, arr):
        return [arr[i:i + self.chunk_size] for i in range(0, len(arr), self.chunk_size)]

    

    def build_players_from_pitches(pitch_rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        players: Dict[str, Dict[str, Any]] = {}

        for row in pitch_rows:
            # Pitcher
            pid = row.get("PitcherId")
            if pid and pid not in players:
                players[pid] = {
                    "id": pid,
                    "name": row.get("Pitcher"),
                    "team": row.get("BatterTeam"),   # or another source if you prefer
                    "bats": None,
                    "throws": row.get("PitcherThrows"),
                }

            # Batter
            bid = row.get("BatterId")
            if bid and bid not in players:
                players[bid] = {
                    "id": bid,
                    "name": row.get("Batter"),
                    "team": row.get("BatterTeam"),
                    "bats": row.get("BatterSide"),
                    "throws": None,
                }

        return list(players.values())

    def run(self):
        try:
            print("Using provided JSON data...")

            all_rows = self.json_data   # <-- directly use the passed-in data

            if not isinstance(all_rows, list):
                raise ValueError("JSON data must be a list of objects")

            total = len(all_rows)
            print("Total records to import:", total)
            if total == 0:
                print("No data to import.")
                return

            rows = [r for r in all_rows]
            chunks = self.chunk_array(rows)

            inserted = 0
            failed = 0

            for i, chunk in enumerate(chunks, start=1):
                print(f"Importing chunk {i}/{len(chunks)} ({len(chunk)} rows)...")

                if self.upsert:
                    res = (
                        self.supabase
                        .table(self.table)
                        .upsert(chunk, on_conflict=self.on_conflict)
                        .execute()
                    )
                else:
                    res = (
                        self.supabase
                        .table(self.table)
                        .insert(chunk)
                        .execute()
                    )

                error = getattr(res, "error", None)

                if error:
                    print("Chunk error:", error)
                    failed += len(chunk)
                else:
                    data = getattr(res, "data", None)
                    count = len(data) if isinstance(data, list) else (1 if data else 0)
                    inserted += count
                    print(f"Chunk success, inserted: {count}")

                time.sleep(0.2)  # avoid rate limits

            print("Import finished. inserted:", inserted, "failed:", failed)

        except Exception as err:
            print("Import failed:", err)
