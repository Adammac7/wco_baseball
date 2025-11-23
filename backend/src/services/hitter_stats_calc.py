from typing import Any, Dict, List, Optional
from supabase import Client
import numpy as np
import json


class Batter:
    """
    A class representing a baseball player with their pitches and stats.
    """
    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.pitches = []  # Array to store pitch objects
        self.pitchers_faced = []
        self.at_bats= 0
        self.avg= 0.0
        self.obp= 0.0
        self.slg= 0.0
        self.ops= 0.0
        self.wobp= 0.0
        self.k_rate= 0.0
        self.bb_rate= 0.0

        self.hits= 0.0
        self.walks= 0.0
        self.strikeouts= 0.0
        self.total_bases= 0.0
        self.plate_appearances= 0.0
        self.avg_exit_velocity = 0.0
        self.avg_launch_angle = 0.0
        self.max_exit_velocity = 0.0
        self.contacts = 0

       # 4x4 grid of plate zones, z1 = avg, z2 = slg, z3 = avg exit velocity
        self.plate_zones_avg = {
            0: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # plate appearances, at bats, contacts, whiffs, hits, total bases, walks, strikeouts, avg exit velocity
            1: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # plate appearances, at bats, contacts, whiffs, hits, total bases, walks, strikeouts, avg exit velocity
            2: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            3: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            4: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
            5: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            6: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            7: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            8: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            9: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            10: [0, 0, 0, 0, 0, 0, 0, 0, 0,0],
            11: [0, 0, 0, 0, 0, 0, 0, 0, 0,0],
            12: [0, 0, 0, 0, 0, 0, 0, 0, 0,0],
            13: [0, 0, 0, 0, 0, 0, 0, 0, 0,0],
            14: [0, 0, 0, 0, 0, 0, 0, 0, 0,0],
            15: [0, 0, 0, 0, 0, 0, 0, 0, 0,0],
            16: [0, 0, 0, 0, 0, 0, 0, 0, 0,0],           
        }
                 # avg, slg, avg exit velocity, whiff rate
        self.plate_zone_stats = {
            0: [0, 0, 0, 0],
            1: [0, 0, 0, 0],
            2: [0, 0, 0, 0], 
            3: [0, 0, 0, 0],
            4: [0, 0, 0, 0],
            5: [0, 0, 0, 0],
            6: [0, 0, 0, 0],
            7: [0, 0, 0, 0],
            8: [0, 0, 0, 0],
            9: [0, 0, 0, 0],
            10: [0, 0, 0, 0],
            11: [0, 0, 0, 0],
            12: [0, 0, 0, 0],
            13: [0, 0, 0, 0],
            14: [0, 0, 0, 0],
            15: [0, 0, 0, 0],
            16: [0, 0, 0, 0]
        }
           
        # wOBA weights
        self.a = .69
        self.b = .89
        self.c = 1.27
        self.d = 1.62
        self.e = 2.10


    def get_outcome(self, pitch):   
        # print("pitch call ", pitch.pitch_call)
        # print("play result ", pitch.play_result)
        if pitch.pitch_call == "InPlay":
            if pitch.play_result == "Single":
                return "Single", True
            elif pitch.play_result == "Double":
                return "Double", True
            elif pitch.play_result == "Triple":
                return "Triple", True
            elif pitch.play_result == "HomeRun":
                return "HomeRun", True
            elif pitch.play_result == "Out":
                return "Out", True
            elif pitch.play_result == "Sacrifice":
                if pitch.tagged_result == "FlyBall":
                    return "Sac Fly", True
                elif pitch.tagged_result == "Bunt":
                    return "Sac Bunt", True
                else:
                    print("Tagged result ", pitch.tagged_result, " is not accounted for")
                    return "Undefined", True
        elif pitch.KorBB == "Strikeout":
            if pitch.pitch_call == "StrikeSwinging":
                return "Strikeout Swing", True
            elif pitch.pitch_call == "StrikeCalled":
                return "Strikeout Looking", True
            else:
                return "Strikeout", True
        elif pitch.KorBB == "Walk":
            return "Walk", True
        elif pitch.pitch_call == "StrikeSwinging":
            return "Whiff", False
        elif pitch.pitch_call == "StrikeCalled":
            return "Called Strike", False
        elif pitch.pitch_call == "BallCalled":
            return "Ball", False
        elif pitch.pitch_call == "BallIntentional":
            return "Intentional Ball", False
        elif pitch.pitch_call == "FoulBallNotFieldable" or pitch.pitch_call == "FoulBallFieldable":
            return "Foul ball", False
        elif pitch.pitch_call == "HitByPitch":
            return "Hit by Pitch", True
        elif pitch.pitch_call == "BallinDirt":
            return "Ball in Dirt", False
        else:
            print("play_call ", pitch.pitch_call, " is not accounted for")
            return "Undefined", False
             

    
    def add_pitch(self, p):
        self.pitches.append(p)
        self.pitchers_faced.append(p.pitcher_name)
        # add logic for batter stats vs a pitcher
        # if something happens count as an at bat
        if p.play_result == "Out":
            self.at_bats += 1
            self.plate_appearances += 1
            self.contacts += 1
            self.max_exit_velocity = p.exit_velocity if p.exit_velocity > self.max_exit_velocity else self.max_exit_velocity
            self.avg_exit_velocity += p.exit_velocity if p.exit_velocity != None else self.avg_exit_velocity
            self.avg_launch_angle += p.launch_angle if p.launch_angle != None else self.avg_launch_angle
            p.outcome,p.action = self.get_outcome(p)
        elif p.play_result != "Undefined" or p.KorBB != "Undefined":
            self.at_bats += 1
            self.plate_appearances += 1
            if p.play_result == "Single":
                self.hits += 1
                self.total_bases += 1
                self.contacts += 1
                self.max_exit_velocity = p.exit_velocity if p.exit_velocity > self.max_exit_velocity else self.max_exit_velocity
                self.avg_exit_velocity += p.exit_velocity if p.exit_velocity != None else self.avg_exit_velocity
                self.avg_launch_angle += p.launch_angle if p.launch_angle != None else self.avg_launch_angle
            elif p.play_result == "Double":
                self.hits += 1
                self.total_bases += 2
                self.contacts += 1
                self.max_exit_velocity = p.exit_velocity if p.exit_velocity > self.max_exit_velocity else self.max_exit_velocity
                self.avg_exit_velocity += p.exit_velocity if p.exit_velocity != None else self.avg_exit_velocity
                self.avg_launch_angle += p.launch_angle if p.launch_angle != None else self.avg_launch_angle
            elif p.play_result == "Triple":
                self.hits += 1
                self.total_bases += 3
                self.contacts += 1
                self.max_exit_velocity = p.exit_velocity if p.exit_velocity > self.max_exit_velocity else self.max_exit_velocity
                self.avg_exit_velocity += p.exit_velocity if p.exit_velocity != None else self.avg_exit_velocity
                self.avg_launch_angle += p.launch_angle if p.launch_angle != None else self.avg_launch_angle
            elif p.play_result == "HomeRun":
                self.hits += 1
                self.total_bases += 4
                self.contacts += 1
                self.max_exit_velocity = p.exit_velocity if p.exit_velocity > self.max_exit_velocity else self.max_exit_velocity
                self.avg_exit_velocity += p.exit_velocity if p.exit_velocity != None else self.avg_exit_velocity
                self.avg_launch_angle += p.launch_angle if p.launch_angle != None else self.avg_launch_angle   # easy fix for missing input data, just add average to
            elif p.KorBB == "Walk":
                self.walks += 1
                self.at_bats -= 1
            elif p.KorBB == "Strikeout":
                self.strikeouts += 1
        else:
            # print("Error entering batter stats during add pitch")
            pass
        p.outcome,p.action = self.get_outcome(p)
        if p.plateLocSide != None and p.plateLocHeight != None:
            p.zone = get_zone_number(p.plateLocSide, p.plateLocHeight,p.zone_width, p.zone_height_low, p.zone_height_high)
        else:
            p.zone = -1
        # print("pzone ", p.zone)

        if p.zone in self.plate_zones_avg:
            if p.outcome == "Strikeout Swing":
                self.plate_zones_avg[p.zone][0] += 1 #pa
                self.plate_zones_avg[p.zone][1] += 1 #atbat
                self.plate_zones_avg[p.zone][3] += 1 #whiffs
                self.plate_zones_avg[p.zone][7] += 1 #strikeouts
            elif p.outcome == "Strikeout Looking":
                self.plate_zones_avg[p.zone][0] += 1 #pa
                self.plate_zones_avg[p.zone][1] += 1 #atbat
                self.plate_zones_avg[p.zone][7] += 1 #strikeouts 
            elif p.outcome == "Out":
                self.plate_zones_avg[p.zone][0] += 1 #pa
                self.plate_zones_avg[p.zone][1] += 1 #atbat
                self.plate_zones_avg[p.zone][2] += 1 #contacts
                self.plate_zones_avg[p.zone][8] += p.exit_velocity #avg exit velocity
                self.plate_zones_avg[p.zone][9] += 1 #in play
            elif p.outcome == "Single":
                self.plate_zones_avg[p.zone][0] += 1 #pa
                self.plate_zones_avg[p.zone][1] += 1 #atbat
                self.plate_zones_avg[p.zone][2] += 1 #contacts
                self.plate_zones_avg[p.zone][4] += 1 #hits
                self.plate_zones_avg[p.zone][5] += 1 #total bases
                self.plate_zones_avg[p.zone][8] += p.exit_velocity #avg exit velocity
                self.plate_zones_avg[p.zone][9] += 1 #in play
            elif p.outcome == "Double":
                self.plate_zones_avg[p.zone][0] += 1 #pa
                self.plate_zones_avg[p.zone][1] += 1 #atbat
                self.plate_zones_avg[p.zone][2] += 1 #contacts
                self.plate_zones_avg[p.zone][4] += 1 #hits
                self.plate_zones_avg[p.zone][5] += 2 #total bases
                self.plate_zones_avg[p.zone][8] += p.exit_velocity #avg exit velocity
                self.plate_zones_avg[p.zone][9] += 1 #in play
            elif p.outcome == "Triple":
                self.plate_zones_avg[p.zone][0] += 1 #pa
                self.plate_zones_avg[p.zone][1] += 1 #atbat
                self.plate_zones_avg[p.zone][2] += 1 #contacts
                self.plate_zones_avg[p.zone][4] += 1 #hits
                self.plate_zones_avg[p.zone][5] += 3 #total bases
                self.plate_zones_avg[p.zone][8] += p.exit_velocity #avg exit velocity
                self.plate_zones_avg[p.zone][9] += 1 #in play
            elif p.outcome == "HomeRun":
                self.plate_zones_avg[p.zone][0] += 1 #pa
                self.plate_zones_avg[p.zone][1] += 1 #atbat
                self.plate_zones_avg[p.zone][2] += 1 #contacts
                self.plate_zones_avg[p.zone][4] += 1 #hits
                self.plate_zones_avg[p.zone][5] += 4 #total bases
                self.plate_zones_avg[p.zone][8] += p.exit_velocity #avg exit velocity
                self.plate_zones_avg[p.zone][9] += 1 #in play
            elif p.outcome == "Walk" or p.outcome == "Hit by Pitch":
                self.plate_zones_avg[p.zone][0] += 1 #pa
                self.plate_zones_avg[p.zone][6] += 1 #walks
            elif p.outcome == "Foul ball":
                self.plate_zones_avg[p.zone][2] += 1 #contacts
            elif p.outcome == "Whiff":
                self.plate_zones_avg[p.zone][3] += 1 #Whiffs
            
    def filter_pitches(self, data):
        for row in data:
            pitch = Pitch(
                batter_name=row['Batter'],
                pitcher_name=row['Pitcher'],
                outcome="Undefined",
                action="Undefined",
                tagged_pitch_type=row['TaggedPitchType'],
                pitch_call=row['PitchCall'],
                rel_speed=row['RelSpeed'],
                spin_rate=row['SpinRate'],
                IVB=row['InducedVertBreak'],
                launch_angle=row['Angle'],
                exit_velocity=row['ExitSpeed'],
                tagged_result=row['TaggedHitType'],
                play_result=row['PlayResult'],
                KorBB=row['KorBB'],
                plateLocHeight=row['PlateLocHeight'],
                plateLocSide=row['PlateLocSide']
            )
            try:
                self.add_pitch(pitch)   
            except Exception as e:
                print("Error adding pitch for play ", self.get_outcome(pitch), ": ", e)
                continue

    def get_stats(self):
        #returns field variables as a dictionary
        data = {
            'name': self.name,
            'role': self.role,
            'hits': self.hits,
            'walks': self.walks,
            'strikeouts': self.strikeouts,
            'total bases': self.total_bases,
            'plate appearences': self.plate_appearances,
            'avg': self.avg,
            'obp': self.obp,
            'slg': self.slg,
            'ops': self.ops,
            'wobp': self.wobp,
            'k_rate': self.k_rate,
            'bb_rate': self.bb_rate,
            'avg_exit_velocity': self.avg_exit_velocity,
            'avg_launch_angle': self.avg_launch_angle,
            'max_exit_velocity': self.max_exit_velocity,    
            'plate_zone_stats': self.plate_zone_stats,
        }
        return data
                
    def calculate_stats(self):
        self.avg = self.hits / self.at_bats if self.at_bats > 0 else 0.0
        self.obp = (self.hits + self.walks) / self.plate_appearances if self.plate_appearances > 0 else 0.0
        self.slg = self.total_bases / self.at_bats if self.at_bats > 0 else 0.0
        self.ops = self.obp + self.slg 
        # wOBA is nonsense at the moment, fomula is wrong and weights are arbitray 
        self.wobp = (self.a * self.walks + self.b * self.hits + self.c * self.hits + self.d * self.hits + self.e * self.hits) / self.at_bats  if self.at_bats > 0 else 0.0
        self.k_rate = self.strikeouts / self.at_bats if self.at_bats > 0 else 0.0
        self.bb_rate = self.walks / self.plate_appearances if self.plate_appearances > 0 else 0.0

        self.avg_exit_velocity = self.avg_exit_velocity / self.contacts if self.contacts > 0 else 0.0
        self.avg_launch_angle = self.avg_launch_angle / self.contacts if self.contacts > 0 else 0.0
        
        # Calculate the average for each plate zone
        # AVG, SLG, AVG Exit Velocity, Whiff Rate
        # plate apearances, at bats, contacts, whiffs, hits, total bases, walks, strikeouts, summed exit velo,in play 
        print("Calculating batter stats...")
       
        for i in range(len(self.plate_zones_avg)):
            # if i == 1:
            #     print(self.plate_zones_avg[i][0] > 0)
            # print("plate zone ", i, " exit velo ", self.plate_zones_avg[i][8]," in play ", self.plate_zones_avg[i][9])
            # if self.plate_zones_avg[i][0] > 0:
                self.plate_zone_stats[i][0] = self.plate_zones_avg[i][4] / self.plate_zones_avg[i][1] if self.plate_zones_avg[i][1] > 0 else 0  # AVG = hits / at bats
                self.plate_zone_stats[i][1] = self.plate_zones_avg[i][5] / self.plate_zones_avg[i][1] if self.plate_zones_avg[i][1] > 0 else 0  # SLG = total bases / at bats
                self.plate_zone_stats[i][2] = self.plate_zones_avg[i][8] / self.plate_zones_avg[i][9] if self.plate_zones_avg[i][9] > 0 else 0  # AVG Exit Velocity = avg exit velocity / contacts
                self.plate_zone_stats[i][3] = self.plate_zones_avg[i][3] / (self.plate_zones_avg[i][3] + self.plate_zones_avg[i][2]) if (self.plate_zones_avg[i][3] + self.plate_zones_avg[i][2]) > 0 else 0
                # print("plate zone ", i, " whiffs ", self.plate_zones_avg[i][3], "  swings ", self.plate_zones_avg[i][2] + self.plate_zones_avg[i][3])
               
        
        print("Batter stats calculated.")



class Pitch:
    def __init__(self, batter_name, pitcher_name, outcome, action, tagged_pitch_type, pitch_call, 
                 rel_speed, spin_rate, IVB, launch_angle, exit_velocity, 
                 tagged_result, play_result, KorBB,plateLocHeight,plateLocSide):
        self.batter_name = batter_name
        self.pitcher_name = pitcher_name
        self.outcome = outcome
        self.action = action
        self.pitch_type = tagged_pitch_type
        self.pitch_call = pitch_call
        self.rel_speed = rel_speed
        self.spin_rate = spin_rate
        self.IVB = IVB
        self.launch_angle = launch_angle
        self.exit_velocity = exit_velocity
        self.tagged_result = tagged_result 
        self.play_result = play_result
        self.KorBB = KorBB
        self.plateLocHeight = plateLocHeight
        self.plateLocSide = plateLocSide

         # srikezone constants
        self.zone_width = 17 * 0.0833  # 17 inches converted to feet
        self.zone_height_low = 1.5     # Approximately knee height
        self.zone_height_high = 3.5    # Approximately mid-chest height
        
        if str(launch_angle).strip() in ["Undefined", ""]:
            print("launch angle is undefined")

    def __repr__(self):
        return f"Pitch({self.batter_name}, {self.pitcher_name},{self.outcome},{self.action},{self.pitch_type}, {self.rel_speed},{self.exit_velocity},{self.launch_angle})"
    


def get_zone_number(x, y, zone_width, zone_height_low, zone_height_high):
        x_sections = np.linspace(-zone_width/2, zone_width/2, 5)
        y_sections = np.linspace(zone_height_high, zone_height_low, 5)
        
        zone_num = 0
        
        for row in range(4):
            for col in range(4):
                x_min, x_max = x_sections[col], x_sections[col+1]
                y_max, y_min = y_sections[row], y_sections[row+1]
                if (x_min <= x <= x_max) and (y_min <= y <= y_max):
                    zone_num = row * 4 + col + 1
                    break
        return zone_num
         
            

class HitterStatsCalculator:
    """
    Computes per-season hitting stats for a single player from pitch_data
    and writes them into the hitter_stats table.
    """

    def __init__(self, supabase: Client):
        self.supabase = supabase

    # ---------- Public API ----------

    def compute_and_save_for_player(self, player_id: str, season: str) -> None:
        """
        Fetch pitch_data for this batter + season, compute all stats,
        and upsert one row into hitter_stats.
        """
        pitch_rows = self._fetch_pitches_for_season(player_id, season)
        batter_name = pitch_rows[0].get("Batter")
        batter  = Batter(batter_name, "general")

        if not pitch_rows:
            print(f"No pitch data found for player {player_id} in season {season}")
            return

        
        # Create a Pitch object from the first row
        # Iterate through each row in the DataFrame
        batter.filter_pitches(pitch_rows)
        batter.calculate_stats()

        # self._compute_all_stats(batter, season, pitch_rows)
        self._upsert_hitter_stats(batter.get_stats())

    # ---------- Data Fetching ----------


    def _fetch_pitches_for_season(
        self,
        playerID: str,
        season: str,
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
            .eq("BatterId", playerID)
            .eq("Season", season)
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
        player_name: str,
        season: int,
        rows: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Orchestrates calculation of all hitter_stats fields.
        This method is inefficient. we need to add the pitch data to a player object for each iteration of going through pitch_rows
        """
        #player_id = self.get_player_id  # trackman makes new player IDs for each game we need to create our own hash function to create unique player IDs
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
            "name": player_name,
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

if __name__ == "__main__":
    # Example usage:
    print("Running main function...")

    from pathlib import Path
    d = Path(__file__).resolve().parents[1] / "data" / "output.json"
    with d.open("r", encoding = "utf-8") as f:
        data = json.load(f)

    Battername = "Justice, Zach"  # edit player name here, this sets the filter of who we are looking for


    player = Batter(Battername, "gerneral") # general is for basic analysis, recomend changing general to a different role to distinguish filter paramters

    # Create a Pitch object from the first row
    # Iterate through each row in the DataFrame
    player.filter_pitches(data)
    player.calculate_stats()
    print(player.get_stats())