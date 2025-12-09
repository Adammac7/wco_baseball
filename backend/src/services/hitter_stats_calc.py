from typing import Any, Dict, List, Optional
from supabase import Client
import numpy as np
import json


class Batter:
    """
    A class representing a baseball player with their pitches and stats.
    name TEXT NOT NULL,

    plate_appearance INTEGER,
    at_bat INTEGER,
    hits INTEGER,
    doubles INTEGER,
    triples INTEGER,
    home_runs INTEGER,
    strikeouts INTEGER,
    walks INTEGER,
    total_bases INTEGER,

    avg NUMERIC,
    obp NUMERIC,
    slg NUMERIC,
    ops NUMERIC,

    k_percent NUMERIC,
    bb_percent NUMERIC,
    bbe INTEGER,

    avg_exit_velocity NUMERIC,
    ev_90th NUMERIC,
    ev_max NUMERIC,

    hhla NUMERIC,
    hh_percent NUMERIC,
    brl_percent NUMERIC,

    gb_percent NUMERIC,
    ld_percent NUMERIC,
    fb_percent NUMERIC,
    pu_percent NUMERIC,

    pitches_seen INTEGER,
    swing_percent NUMERIC,    
    whiff_percent NUMERIC,
    chase_percent NUMERIC,
    iz_swing_percent NUMERIC,
    iz_miss_percent NUMERIC,
    fp_swing_percent NUMERIC,

    bwar NUMERIC,
    fwar NUMERIC,
    ops_plus NUMERIC,
    wrc_plus NUMERIC,
    wobp NUMERIC,
    """
    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.pitches = []  # Array to store pitch objects
        self.pitchers_faced = []

        # basic average stats
        self.avg= 0.0
        self.obp= 0.0
        self.slg= 0.0
        self.ops= 0.0
        self.k_rate= 0.0
        self.bb_rate= 0.0
        self.avg_exit_velocity = 0.0
        self.avg_launch_angle = 0.0
        self.max_exit_velocity = 0.0

        # counting stats
        self.pitches_seen = 0  # addeded 
        self.whiffs= 0.0  # added
        self.swings= 0.0 # added

        self.plate_appearances= 0.0
        self.at_bats= 0
        self.hits= 0.0
        self.doubles= 0.0
        self.triples= 0.0
        self.home_runs= 0.0
        self.walks= 0.0
        self.hdp = 0.0
        self.strikeouts= 0.0
        self.total_bases= 0.0
        self.contacts = 0
        # in zone / out of zone stats
        self.in_zone_misses = 0
        self.in_zone_swings = 0 # contacts = swings - whiffs
        self.in_zone_pitches = 0
        self.chase_swings = 0
        self.chase_misses = 0
        self.out_of_zone_pitches = 0

        self.ground_balls = 0
        self.line_drives = 0
        self.fly_balls = 0
        self.popups = 0
        self.foul_balls = 0
        self.bunts = 0

 
        # uncalculated so far
        self.whiff_rate = 0.0
        self.swing_rate = 0.0
        self.chase_rate = 0.0
        self.chase_whiff_rate = 0.0
        self.hard_hit_rate = 0.0
        self.ground_ball_rate = 0.0
        self.line_drive_rate = 0.0
        self.fly_ball_rate = 0.0
        self.popup_rate = 0.0
        self.barell_percent = 0.0
        self.hard_hit_rate = 0.0
        self.inzone_swing_rate = 0.0
        self.inzone_miss_rate = 0.0
        self.foul_percent = 0.0 # might not be the correct stat
        self.hard_hit_launch_angle = 0.0 # don't know how to calculate

        #advanced stats, not yet calculated
        self.wrc_plus = 0.0
        self.ops_plus = 0.0
        self.bwar = 0.0
        self.fwar = 0.0
        self.wobp= 0.0


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
                return "Strikeout Swinging", True
            elif pitch.pitch_call == "StrikeCalled":
                return "Strikeout Looking", True
            else:
                print("pitch call ", pitch.pitch_call, " for strikeout is not accounted for")
                return "Undefined", True    
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
        # worried this logic may be wrong !!! ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ important +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        self.pitches_seen += 1
        self.pitches.append(p)
        self.pitchers_faced.append(p.pitcher_name)
        # add logic for batter stats vs a pitcher
        # if something happens count as an at bat
        # did something happen on the pitch
        p.outcome,p.action = self.get_outcome(p)
        if p.action:  # if action is true, it means the pitch resulted in an outcome that affects batter stats
            self.plate_appearances += 1
            is_ab = p.outcome not in {"Whiff","Walk", "Hit by Pitch", "Sac Fly", "Sac Bunt", "Called Strike", "Ball", "Intentional Ball", "Ball in Dirt", "Foul ball"}
            if is_ab:
                self.at_bats += 1
            if p.outcome == "Out":
                self.swings += 1
                self.contacts += 1
                self.max_exit_velocity = p.exit_velocity if p.exit_velocity > self.max_exit_velocity else self.max_exit_velocity
                self.avg_exit_velocity += p.exit_velocity if p.exit_velocity != None else self.avg_exit_velocity / self.contacts
                self.avg_launch_angle += p.launch_angle if p.launch_angle != None else self.avg_launch_angle / self.contacts
                if in_zone(p.plateLocSide, p.plateLocHeight,p.zone_width, p.zone_height_low, p.zone_height_high):
                    self.in_zone_swings += 1
                    self.in_zone_misses += 1
                    self.in_zone_pitches += 1
                else:
                    self.chase_swings += 1
                    self.chase_misses += 1
                
            elif p.outcome == "Single":
                self.hits += 1
                self.swings += 1
                self.total_bases += 1
                self.contacts += 1
                self.max_exit_velocity = p.exit_velocity if p.exit_velocity > self.max_exit_velocity else self.max_exit_velocity
                self.avg_exit_velocity += p.exit_velocity if p.exit_velocity != None else self.avg_exit_velocity / self.contacts
                self.avg_launch_angle += p.launch_angle if p.launch_angle != None else self.avg_launch_angle / self.contacts
                if in_zone(p.plateLocSide, p.plateLocHeight,p.zone_width, p.zone_height_low, p.zone_height_high):
                    self.in_zone_swings += 1
                    self.in_zone_misses += 1
                    self.in_zone_pitches += 1
                else:
                    self.chase_swings += 1
                    self.chase_misses += 1
            elif p.outcome == "Double":
                self.hits += 1
                self.swings += 1
                self.doubles += 1
                self.total_bases += 2
                self.contacts += 1
                self.max_exit_velocity = p.exit_velocity if p.exit_velocity > self.max_exit_velocity else self.max_exit_velocity
                self.avg_exit_velocity += p.exit_velocity if p.exit_velocity != None else self.avg_exit_velocity / self.contacts
                self.avg_launch_angle += p.launch_angle if p.launch_angle != None else self.avg_launch_angle / self.contacts
                if in_zone(p.plateLocSide, p.plateLocHeight,p.zone_width, p.zone_height_low, p.zone_height_high):
                    self.in_zone_swings += 1
                    self.in_zone_misses += 1
                    self.in_zone_pitches += 1
                else:
                    self.chase_swings += 1
                    self.chase_misses += 1
            elif p.outcome == "Triple":
                self.hits += 1
                self.swings += 1
                self.triples += 1
                self.total_bases += 3
                self.contacts += 1
                self.max_exit_velocity = p.exit_velocity if p.exit_velocity > self.max_exit_velocity else self.max_exit_velocity
                self.avg_exit_velocity += p.exit_velocity if p.exit_velocity != None else self.avg_exit_velocity / self.contacts
                self.avg_launch_angle += p.launch_angle if p.launch_angle != None else self.avg_launch_angle / self.contacts
                if in_zone(p.plateLocSide, p.plateLocHeight,p.zone_width, p.zone_height_low, p.zone_height_high):
                    self.in_zone_swings += 1
                    self.in_zone_misses += 1
                    self.in_zone_pitches += 1
                else:
                    self.chase_swings += 1
                    self.chase_misses += 1
            elif p.outcome == "HomeRun":
                self.hits += 1
                self.swings += 1
                self.home_runs += 1
                self.total_bases += 4
                self.contacts += 1
                self.max_exit_velocity = p.exit_velocity if p.exit_velocity > self.max_exit_velocity else self.max_exit_velocity
                self.avg_exit_velocity += p.exit_velocity if p.exit_velocity != None else self.avg_exit_velocity
                self.avg_launch_angle += p.launch_angle if p.launch_angle != None else self.avg_launch_angle   # easy fix for missing input data, just add average to
                if in_zone(p.plateLocSide, p.plateLocHeight,p.zone_width, p.zone_height_low, p.zone_height_high):
                    self.in_zone_swings += 1
                    self.in_zone_misses += 1
                    self.in_zone_pitches += 1
                else:
                    self.chase_swings += 1
                    self.chase_misses += 1
            elif p.outcome == "Walk":
                self.walks += 1
                self.out_of_zone_pitches += 1
            elif p.outcome == "Strikeout Swinging":    
                self.strikeouts += 1
                self.swings += 1
                self.whiffs += 1
                if in_zone(p.plateLocSide, p.plateLocHeight,p.zone_width, p.zone_height_low, p.zone_height_high):
                    self.in_zone_swings += 1
                    self.in_zone_misses += 1
                    self.in_zone_pitches += 1
                else:
                    self.chase_swings += 1
                    self.chase_misses += 1
            elif p.outcome == "Strikeout Looking":
                self.strikeouts += 1
                self.in_zone_pitches += 1
            elif p.outcome == "Sac Fly":
                self.contacts += 1
                self.swings += 1
                if in_zone(p.plateLocSide, p.plateLocHeight,p.zone_width, p.zone_height_low, p.zone_height_high):
                    self.in_zone_swings += 1
                    self.in_zone_misses += 1
                    self.in_zone_pitches += 1
                else:
                    self.chase_swings += 1
                    self.chase_misses += 1
            elif p.outcome == "Sac Bunt":
                self.bunts += 1
            elif p.outcome == "Hit by Pitch":
                self.hdp += 1

            #logic for hit type stats

            if p.tagged_result == "GroundBall":
                self.ground_balls += 1
            elif p.tagged_result == "LineDrive":
                self.line_drives += 1
            elif p.tagged_result == "FlyBall":
                self.fly_balls += 1
            elif p.tagged_result == "Popup":
                self.popups += 1
        else:
            # logic for pitches that do not result in an at bat
            if p.outcome == "Whiff":
                self.swings += 1
                self.whiffs += 1
                if in_zone(p.plateLocSide, p.plateLocHeight,p.zone_width, p.zone_height_low, p.zone_height_high):
                    self.in_zone_swings += 1
                    self.in_zone_misses += 1
                    self.in_zone_pitches += 1
                else:
                    self.chase_swings += 1
                    self.chase_misses += 1
            elif p.outcome == "Foul ball":
                self.foul_balls += 1
                self.contacts += 1  # fouls count as contacts
                self.swings += 1  # fouls count as swings
                if in_zone(p.plateLocSide, p.plateLocHeight,p.zone_width, p.zone_height_low, p.zone_height_high):
                    self.in_zone_swings += 1
                    self.in_zone_pitches += 1
                else:
                    self.chase_swings += 1
            elif p.outcome == "Called Strike":
                self.in_zone_pitches += 1   
            elif p.outcome == "Ball" or p.outcome == "Intentional Ball" or p.outcome == "Ball in Dirt":
                self.out_of_zone_pitches += 1

                    
        #logic for the plate zone stats, (switch to dict for optimization)
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
             # Identity
                'name': self.name,
                'role': self.role,

                # Basic counting stats
                'pitches_seen': self.pitches_seen,
                'swings': self.swings,
                'whiffs': self.whiffs,
                'contacts': self.contacts,
                'at_bats': self.at_bats,
                'plate_appearances': self.plate_appearances,
                'hits': self.hits,
                'doubles': self.doubles,
                'triples': self.triples,
                'home_runs': self.home_runs,
                'walks': self.walks,
                'strikeouts': self.strikeouts,
                'total_bases': self.total_bases,

                # Traditional slash-line stats
                'avg': self.avg,
                'obp': self.obp,
                'slg': self.slg,
                'ops': self.ops,
                'wobp': self.wobp,
                'hdp': self.hdp,

                'ground_balls': self.ground_balls,
                'line_drives': self.line_drives,
                'fly_balls': self.fly_balls,
                'popups': self.popups,
                'foul_balls': self.foul_balls,
                'bunts': self.bunts,
                


                # Advanced rate stats
                'k_rate': self.k_rate,
                'bb_rate': self.bb_rate,
                'whiff_rate': self.whiff_rate,
                'swing_rate': self.swing_rate,
                'inzone_swing_rate': self.inzone_swing_rate,
                'inzone_miss_rate': self.inzone_miss_rate,
                'chase_rate': self.chase_rate,
                'chase_whiff_rate': self.chase_whiff_rate,
                'hard_hit_rate': self.hard_hit_rate,
                'ground_ball_rate': self.ground_ball_rate,
                'line_drive_rate': self.line_drive_rate,
                'fly_ball_rate': self.fly_ball_rate,
                'popup_rate': self.popup_rate,
                'foul_percent': self.foul_percent,
                'barrel_percent': self.barell_percent,
                'hard_hit_launch_angle': self.hard_hit_launch_angle,

                # Batted-ball measurements
                'avg_exit_velocity': self.avg_exit_velocity,
                'avg_launch_angle': self.avg_launch_angle,
                'max_exit_velocity': self.max_exit_velocity,

                # Advanced sabermetrics (future)
                'wrc_plus': self.wrc_plus,
                'ops_plus': self.ops_plus,
                'bwar': self.bwar,
                'fwar': self.fwar,

                # Zone-based stats (nested dict)
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
        self.swing_rate = self.swings / self.pitches_seen if self.pitches_seen > 0 else 0.0
        self.whiff_rate = self.whiffs / self.swings if self.swings > 0 else 0.0

        self.inzone_swing_rate = self.in_zone_swings / self.in_zone_pitches if self.in_zone_pitches > 0 else 0.0
        self.inzone_miss_rate = self.in_zone_misses / self.in_zone_swings if self.in_zone_swings > 0 else 0.0
        self.chase_rate = self.chase_swings / self.out_of_zone_pitches if self.out_of_zone_pitches > 0 else 0.0
        self.chase_whiff_rate = self.chase_misses / self.chase_swings if self.chase_swings > 0 else 0.0
        self.hard_hit_rate = 0.0      # to be implemented
        self.ground_ball_rate = self.ground_balls / (self.contacts - self.foul_balls) if (self.contacts - self.foul_balls) > 0 else 0.0
        self.line_drive_rate = self.line_drives / (self.contacts - self.foul_balls) if (self.contacts - self.foul_balls) > 0 else 0.0
        self.fly_ball_rate = self.fly_balls / (self.contacts - self.foul_balls) if (self.contacts - self.foul_balls) > 0 else 0.0
        self.popup_rate = self.popups / (self.contacts - self.foul_balls) if (self.contacts - self.foul_balls) > 0 else 0.0
        self.barell_percent = 0.0     # to be implemented
        self.foul_percent = self.foul_balls / self.contacts if self.contacts > 0 else 0.0   
        self.hard_hit_launch_angle = 0.0 # to be implemented



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
    
def in_zone(plateLocSide, plateLocHeight, zone_width, zone_height_low, zone_height_high):
    try:
        left = -zone_width / 2
        right = zone_width / 2

        in_horizontal = left <= plateLocSide <= right
        in_vertical = zone_height_low <= plateLocHeight <= zone_height_high
        return in_horizontal and in_vertical
    except Exception as e:
        print(f"Error in in_zone function, Bad data: {e}")
        return False

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


    

    def normalize_hitter_stats_payload(payload: dict) -> dict:
        INT_FIELDS = [
        "pitches_seen", "swings", "whiffs", "contacts",
        "at_bats", "plate_appearances", "hits", "doubles",
        "triples", "home_runs", "walks", "strikeouts",
        "total_bases", "hdp", "ground_balls", "line_drives",
        "fly_balls", "popups", "foul_balls", "bunts",
    ]
        # Ensure counting stats are proper integers or None
        for field in INT_FIELDS:
            val = payload.get(field)
            if val is None:
                continue
            # some might be "0.0", 0.0, "12", etc.
            try:
                payload[field] = int(float(val))
            except (ValueError, TypeError):
                # if it's truly garbage, set to None or handle as you like
                payload[field] = None
        return payload

    # ---------- Public API ----------

    def compute_and_save_for_player(self, player_id: str, season: str) -> None:
        """
        Fetch pitch_data for this batter + season, compute all stats,
        and upsert one row into hitter_stats.
        """
        pitch_rows = self._fetch_pitches_for_season(player_id, season)
        try:
            batter_name = pitch_rows[0].get("Batter")
        except IndexError:
            print(f"No pitch data found for player {player_id} in season {season}")
            return
        batter  = Batter(batter_name, "general")

        
        # Create a Pitch object from the first row
        # Iterate through each row in the DataFrame
        batter.filter_pitches(pitch_rows)
        batter.calculate_stats()
        stats = batter.get_stats()
        stats['batter_id'] = player_id
        stats['season'] = season
        payload = HitterStatsCalculator.normalize_hitter_stats_payload(stats)
        # for k, v in stats.items():
        #     print(f"{k}: {v}")

        # self._compute_all_stats(batter, season, pitch_rows)
        self._upsert_hitter_stats(payload)

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
            .upsert(stats, on_conflict=["batter_id","season"])
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
    from supabase_client import supabase
    calculator = HitterStatsCalculator(supabase)
    calculator.compute_and_save_for_player(player_id="32cc658426150550", season="Fall-2025")
    
