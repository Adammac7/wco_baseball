from typing import Any, Dict, List, Optional
from supabase import Client


class HitterStatsCalculator:
    """
    Computes per-season hitting stats for a single player from pitch_data
    and writes them into the hitter_stats table.
    """

    def __init__(self, supabase: Client):
        self.supabase = supabase

    # ---------- Public API ----------

    def compute_and_save_for_player(self, player_id: str, season: int) -> None:
        """
        Fetch pitch_data for this batter + season, compute all stats,
        and upsert one row into hitter_stats.
        """
        pitch_rows = self._fetch_pitches_for_season(player_id, season)

        if not pitch_rows:
            print(f"No pitch data found for player {player_id} in season {season}")
            return

        stats = self._compute_all_stats(player_id, season, pitch_rows)
        self._upsert_hitter_stats(stats)

    # ---------- Data Fetching ----------


    def _fetch_pitches_for_season(
        self,
        player_id: str,
        season: int,
    ) -> List[Dict[str, Any]]:
        """
        Fetch all pitch_data rows for this batter and season.
        Adjust filters to match your schema and season definition.
        """
        # Example: filter by BatterId and year(Date) in SQL via RPC or a view.
        # For now, we fetch by BatterId only – you can later add a season filter.
        # You might eventually create a dedicated view or endpoint for this.
        res = (
            self.supabase
            .table("pitch_data")
            .select("*")
            .eq("BatterId", player_id)
            # .gte("Date", f"{season}-01-01")
            # .lte("Date", f"{season}-12-31")
            .execute()
        )

        data = getattr(res, "data", None)
        if not isinstance(data, list):
            return []
        return data

    # ---------- Master Stat Computation ----------

    def _compute_all_stats(
        self,
        player_id: str,
        season: int,
        rows: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Orchestrates calculation of all hitter_stats fields.
        """
        name = self._infer_player_name(rows)

        plate_appearance = self._calc_plate_appearances(rows)
        at_bat = self._calc_at_bats(rows)
        hits = self._calc_hits(rows)
        doubles = self._calc_doubles(rows)
        triples = self._calc_triples(rows)
        home_runs = self._calc_home_runs(rows)
        strikeouts = self._calc_strikeouts(rows)
        walks = self._calc_walks(rows)
        total_bases = self._calc_total_bases(rows)

        avg = self._calc_avg(hits, at_bat)
        obp = self._calc_obp(plate_appearance, hits, walks)
        slg = self._calc_slg(total_bases, at_bat)
        ops = self._calc_ops(obp, slg)

        k_percent = self._calc_k_percent(strikeouts, plate_appearance)
        bb_percent = self._calc_bb_percent(walks, plate_appearance)
        bbe = self._calc_bbe(rows)

        ev = self._calc_ev(rows)
        ev_90th = self._calc_ev_90th(rows)
        ev_max = self._calc_ev_max(rows)

        hhla = self._calc_hhla(rows)
        hh_percent = self._calc_hh_percent(rows)
        brl_percent = self._calc_brl_percent(rows)

        gb_percent = self._calc_gb_percent(rows)
        ld_percent = self._calc_ld_percent(rows)
        fb_percent = self._calc_fb_percent(rows)
        pu_percent = self._calc_pu_percent(rows)

        pitches_seen = self._calc_pitches_seen(rows)
        swing_percent = self._calc_swing_percent(rows)
        whiff_percent = self._calc_whiff_percent(rows)
        chase_percent = self._calc_chase_percent(rows)
        iz_swing_percent = self._calc_iz_swing_percent(rows)
        iz_miss_percent = self._calc_iz_miss_percent(rows)
        fp_swing_percent = self._calc_fp_swing_percent(rows)

        bwar = self._calc_bwar(rows)
        fwar = self._calc_fwar(rows)
        ops_plus = self._calc_ops_plus(ops, season)
        wrc_plus = self._calc_wrc_plus(rows, season)
        wobp = self._calc_wobp(rows)

        return {
            "player_id": player_id,
            "season": season,
            "name": name,
            "plate_appearance": plate_appearance,
            "at_bat": at_bat,
            "hits": hits,
            "doubles": doubles,
            "triples": triples,
            "home_runs": home_runs,
            "strikeouts": strikeouts,
            "walks": walks,
            "total_bases": total_bases,
            "avg": avg,
            "obp": obp,
            "slg": slg,
            "ops": ops,
            "k_percent": k_percent,
            "bb_percent": bb_percent,
            "bbe": bbe,
            "ev": ev,
            "ev_90th": ev_90th,
            "ev_max": ev_max,
            "hhla": hhla,
            "hh_percent": hh_percent,
            "brl_percent": brl_percent,
            "gb_percent": gb_percent,
            "ld_percent": ld_percent,
            "fb_percent": fb_percent,
            "pu_percent": pu_percent,
            "pitches_seen": pitches_seen,
            "swing_percent": swing_percent,
            "whiff_percent": whiff_percent,
            "chase_percent": chase_percent,
            "iz_swing_percent": iz_swing_percent,
            "iz_miss_percent": iz_miss_percent,
            "fp_swing_percent": fp_swing_percent,
            "bwar": bwar,
            "fwar": fwar,
            "ops_plus": ops_plus,
            "wrc_plus": wrc_plus,
            "wobp": wobp,
        }

    # ---------- DB Write ----------

    def _upsert_hitter_stats(self, stats: Dict[str, Any]) -> None:
        """
        Upsert the computed stats row into hitter_stats.
        Assumes PRIMARY KEY (player_id, season).
        """
        res = (
            self.supabase
            .table("hitter_stats")
            .upsert(stats, on_conflict="player_id,season")
            .execute()
        )
        error = getattr(res, "error", None)
        if error:
            print("Error upserting hitter_stats:", error)

    # ---------- Helper / individual stat methods (math left empty) ----------

    def _infer_player_name(self, rows: List[Dict[str, Any]]) -> str:
        """
        Infer the hitter's name from pitch rows (e.g., first non-null Batter).
        """
        # TODO: implement logic to extract name
        return ""

    def _calc_plate_appearances(self, rows: List[Dict[str, Any]]) -> int:
        """
        Calculate plate appearances (PA) from pitch result / play data.
        """
        return 0

    def _calc_at_bats(self, rows: List[Dict[str, Any]]) -> int:
        return 0

    def _calc_hits(self, rows: List[Dict[str, Any]]) -> int:
        return 0

    def _calc_doubles(self, rows: List[Dict[str, Any]]) -> int:
        return 0

    def _calc_triples(self, rows: List[Dict[str, Any]]) -> int:
        return 0

    def _calc_home_runs(self, rows: List[Dict[str, Any]]) -> int:
        return 0

    def _calc_strikeouts(self, rows: List[Dict[str, Any]]) -> int:
        return 0

    def _calc_walks(self, rows: List[Dict[str, Any]]) -> int:
        return 0

    def _calc_total_bases(self, rows: List[Dict[str, Any]]) -> int:
        return 0

    def _calc_avg(self, hits: int, at_bat: int) -> Optional[float]:
        return None

    def _calc_obp(
        self,
        plate_appearance: int,
        hits: int,
        walks: int,
    ) -> Optional[float]:
        return None

    def _calc_slg(self, total_bases: int, at_bat: int) -> Optional[float]:
        return None

    def _calc_ops(self, obp: Optional[float], slg: Optional[float]) -> Optional[float]:
        return None

    def _calc_k_percent(self, strikeouts: int, plate_appearance: int) -> Optional[float]:
        return None

    def _calc_bb_percent(self, walks: int, plate_appearance: int) -> Optional[float]:
        return None

    def _calc_bbe(self, rows: List[Dict[str, Any]]) -> int:
        return 0

    def _calc_ev(self, rows: List[Dict[str, Any]]) -> Optional[float]:
        return None

    def _calc_ev_90th(self, rows: List[Dict[str, Any]]) -> Optional[float]:
        return None

    def _calc_ev_max(self, rows: List[Dict[str, Any]]) -> Optional[float]:
        return None

    def _calc_hhla(self, rows: List[Dict[str, Any]]) -> Optional[float]:
        return None

    def _calc_hh_percent(self, rows: List[Dict[str, Any]]) -> Optional[float]:
        return None

    def _calc_brl_percent(self, rows: List[Dict[str, Any]]) -> Optional[float]:
        return None

    def _calc_gb_percent(self, rows: List[Dict[str, Any]]) -> Optional[float]:
        return None

    def _calc_ld_percent(self, rows: List[Dict[str, Any]]) -> Optional[float]:
        return None

    def _calc_fb_percent(self, rows: List[Dict[str, Any]]) -> Optional[float]:
        return None

    def _calc_pu_percent(self, rows: List[Dict[str, Any]]) -> Optional[float]:
        return None

    def _calc_pitches_seen(self, rows: List[Dict[str, Any]]) -> int:
        return 0

    def _calc_swing_percent(self, rows: List[Dict[str, Any]]) -> Optional[float]:
        return None

    def _calc_whiff_percent(self, rows: List[Dict[str, Any]]) -> Optional[float]:
        return None

    def _calc_chase_percent(self, rows: List[Dict[str, Any]]) -> Optional[float]:
        return None

    def _calc_iz_swing_percent(self, rows: List[Dict[str, Any]]) -> Optional[float]:
        return None

    def _calc_iz_miss_percent(self, rows: List[Dict[str, Any]]) -> Optional[float]:
        return None

    def _calc_fp_swing_percent(self, rows: List[Dict[str, Any]]) -> Optional[float]:
        return None

    def _calc_bwar(self, rows: List[Dict[str, Any]]) -> Optional[float]:
        return None

    def _calc_fwar(self, rows: List[Dict[str, Any]]) -> Optional[float]:
        return None

    def _calc_ops_plus(self, ops: Optional[float], season: int) -> Optional[float]:
        return None

    def _calc_wrc_plus(self, rows: List[Dict[str, Any]], season: int) -> Optional[float]:
        return None

    def _calc_wobp(self, rows: List[Dict[str, Any]]) -> Optional[float]:
        return None
    


def get_hitter_players() -> List[Dict[str, Any]]:
    """
    Fetch all players that should have hitter stats calculated.
    (role = 'hitter' or 'two-way')
    """
    res = (
        supabase
        .table("players")
        .select("id, name, role")
        .in_("role", ["hitter", "two-way"])
        .execute()
    )

    data = getattr(res, "data", None)
    if not isinstance(data, list):
        return []
    return data

def rebuild_all_hitter_stats_for_season(season: int) -> None:
    """
    Iterate over all hitter-type players and compute/update their hitter_stats
    for the given season.
    """
    players = get_hitter_players()
    print(f"Found {len(players)} hitter players to process for season {season}")

    calculator = HitterStatsCalculator(supabase)

    for p in players:
        player_id = p["id"]
        name = p.get("name", "")
        print(f"Computing hitter stats for {player_id} ({name}) season {season}...")

    calculator.compute_and_save_for_player(player_id, season)