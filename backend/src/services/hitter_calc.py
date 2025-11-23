import hashlib

class Hitter_calc:

    out_json: list[dict] = []

    @staticmethod
    def player_hash(full_name: str, team: str, side: str, position: str, season: str) -> str:
        identity = f"{full_name}|{team}|{side}|{position}{season}"
        h = hashlib.sha256(identity.encode("utf-8")).hexdigest()
        return h[:16]   # first 16 hex chars → stable, short ID
    

    # trackman csv playerIDs are not consistant so we make our own, this works unless two players have the exact same name, team, and they throw and bat from the same side
    
    def clean_player_ID(self, data: list[dict]) -> list[dict]:
        for row in data:
            batterID = self.player_hash(
                full_name=row.get("Batter", ""),
                team=row.get("BatterTeam", ""),
                side=row.get("BatterSide", ""),
                position= "batter",
                season= row.get("Season", "")
            )
            pitcherID = self.player_hash(
                full_name=row.get("Pitcher", ""),
                team=row.get("PitcherTeam", ""),
                side=row.get("PitcherThrows", ""),
                position= "pitcher",
                season= row.get("Season", "")
            )
           
            row["BatterId"] = batterID
            row["PitcherId"] = pitcherID

        return data
    
    def get_all_seasons_for_player(self, player_id: str) -> list[str]:
        #this function would find out all other seasons the player has played and will return a list of the player IDs for those seasons
        # right now the hash includes season as a input so each player gets a new hash each season
        # player id give player json and one field holds the id of the stats from that season
        return []
    
    def get_hitters(self, data: list[dict]) -> dict[dict]:
        num_hitters = []
        for row in data:
            id = row["BatterID"]
            if id not in num_hitters:
                num_hitters[id] = {"Name": row["Batter"],
                                   "ID": row["BatterID"],
                                   "Team": row["BatterTeam"],
                                   "Bats": row["BatterSide"],
                                #    "Seasons": get_all_seasons_for_player(id)
                }

        return num_hitters
    
    
    
    def count_stats(self, data: list[dict]) -> list[dict]:
        for row in data:
            if row.get("PlayerID") not in Hitter_calc.out_json:
                Hitter_calc.out_json.append({
                    "PlayerID": row.get("PlayerID"),

                    "AtBats": self.data.get("AtBats"),
                    "PlateAppearances": 0,
                    "BBE": 0,
                    "GBs": 0,
                    "FBs": 0,
                    "LDs": 0,
                    "PUs":0,
                    "HH":0,
                    "Bar":0,

                    "Hits": 0,
                    "Singles": 0,
                    "Doubles": 0,
                    "Triples": 0,
                    "HomeRuns": 0,

                    "RBIs": 0,
                    "BB": 0,
                    "K": 0,

                    "TotalBases": 0,
                    "TotalEV": 0,
                    "TotalLA": 0,
                    "MaxEV": 0,

                    "plate_zones_avg": {
                        0: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # plate appearances, at bats, contacts, whiffs, hits, total bases, walks, strikeouts, tot exit velocity
                        1: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # plate appearances, at bats, contacts, whiffs, hits, total bases, walks, strikeouts, tot exit velocity
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
                    },


                    # add more counting stats as needed
                })
