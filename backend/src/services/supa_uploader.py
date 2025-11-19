# backend/scripts/import_json_to_supabase.py

import json
import time
from pathlib import Path

from supabase_client import supabase  # uses backend/.env


class Supa_uploader:
    def __init__(
        self,
        supabase_client,
        json_file,
        table,
        chunk_size=200,
        upsert=False,
        on_conflict="id",
    ):
        self.supabase = supabase_client
        self.json_file = Path(json_file)
        self.table = table
        self.chunk_size = chunk_size
        self.upsert = upsert
        self.on_conflict = on_conflict

    def read_json_file(self):
        if not self.json_file.exists():
            raise FileNotFoundError(f"JSON file not found: {self.json_file}")
        with self.json_file.open("r", encoding="utf-8") as f:
            return json.load(f)

    def chunk_array(self, arr):
        return [arr[i:i + self.chunk_size] for i in range(0, len(arr), self.chunk_size)]

    def transform_row(self, row: dict) -> dict:
        # Optional: customize this to match your table schema.
        # For now, return the row as-is (same as original script).
        return row

    def run(self):
        try:
            print("Reading JSON from", self.json_file)
            all_rows = self.read_json_file()

            if not isinstance(all_rows, list):
                raise ValueError("JSON root must be an array of objects")

            total = len(all_rows)
            print("Total records to import:", total)
            if total == 0:
                print("No data to import.")
                return

            rows = [self.transform_row(r) for r in all_rows]
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

                error = getattr(res, "error", None) if hasattr(res, "error") else None

                if error:
                    print("Chunk error:", error)
                    failed += len(chunk)
                else:
                    data = getattr(res, "data", None)
                    count = len(data) if isinstance(data, list) else (1 if data else 0)
                    inserted += count
                    print(f"Chunk success, inserted: {count}")

                time.sleep(0.2)  # small pause to avoid rate limits (optional)

            print("Import finished. inserted:", inserted, "failed:", failed)

        except Exception as err:
            print("Import failed:", err)


if __name__ == "__main__":
    JSON_FILE = Path(__file__).resolve().parent.parent / "src" / "output_jsons" / "output.json"
    TABLE = "pitch_data"
    CHUNK_SIZE = 100
    UPSERT = False
    ON_CONFLICT = "id"

    uploader = Supa_uploader(
        supabase_client=supabase,
        json_file=JSON_FILE,
        table=TABLE,
        chunk_size=CHUNK_SIZE,
        upsert=UPSERT,
        on_conflict=ON_CONFLICT,
    )
    uploader.run()
