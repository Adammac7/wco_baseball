import json
from pathlib import Path
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from pydantic import BaseModel


router = APIRouter()


@router.post("/in_pipeline")
async def in_pipeline():
                                    print("In pipeline started.")  
    #=============================== Need to get csv from google drive ===============================#  works
                                    
                                 
                                    ROOT = Path(__file__).resolve().parents[3]   # go up to project root
                                    csv_file_path = ROOT / "All Intrasquads.csv"  # hard code for now
    #=============================== Process csv into JSON ======Might not need this actually, use pandas instead=====================================#  works
                                    print("Processing CSV to JSON...")
                                    from src.services.csv_to_json import csv_to_json
                                    from src.services.csv_to_json import save_json
                                    json_data = csv_to_json(csv_file_path) # works 
                                    save_json(json_data) # saves to backend\src\data\output.json
                                    print("CSV processed to JSON.")
    #=============================== clean playerIDs ======================================#  works
                                    from src.services.hitter_calc import Hitter_calc
                                    hc = Hitter_calc()
                                    json_data = hc.clean_player_ID(json_data)
                                    save_json(json_data)
                                   
    #=============================== send json to pitches table ======================================#  works
                                    # print("Uploading to pitches table...")
                                    # from src.services.supa_uploader import Supa_uploader
                                    # uploader = Supa_uploader(
                                    #     supabase_client=None,  # use default client inside the class
                                    #     json_file=json_data,  
                                    #     table="pitch_data",
                                    #     chunk_size=200,
                                    #     upsert=True,
                                    #     on_conflict="id"
                                    # )
                                    # uploader.run()
                                    # print("Upload to pitches table completed.")
    #=============================== send json to players table ====================================#  works

                                    # go through json and set player ID based on custom hash function
                                    
                                    
                                    #     dic = player_id : list of counting stats
                                    #     add couting stats from row to dic


                                    # new json = get * where player_id == dic_keys from hitters table

                                    # for row in json:
                                    #     row = row with new calc stats
                                    # supa_uploader(new json)
                                        
                                        

                                    # create json to keep track of new counting stats for each player 
                                    
                                    # add json to hitters table
                                    # pull all counting stats from hitters table per each player and calculate non-counting stats( avg, obp, avg EV... etc)

                                    # 

                                    # players = Supa_uploader.build_players_from_pitches(json_data)

                                    # print("Uploading to players table...")  
                                    # uploader_players = Supa_uploader(
                                    #     supabase_client=None,  # use default client inside the class
                                    #     json_file=players,
                                    #     table="players",
                                    #     chunk_size=100,
                                    #     upsert=True,
                                    #     on_conflict="id"
                                    # )
                                    # uploader_players.run()
                                    # print("Upload to players table completed.")
                                    #check for new players and add to table if needed
                                    
    

    #=============================== claculate stats by querying, output json =========================#
                                    print("Calculating hitter stats...")
                                    from src.services.supabase_client import supabase
                                    from src.services.hitter_stats_calc import HitterStatsCalculator

                                    calculator = HitterStatsCalculator(supabase)  # use default client inside the class
                                    print("Calculating and saving stats for player 1000118742...")

                                                                                                    # change to str, update func accordingly
                                    calculator.compute_and_save_for_player(player_id="6691ce9aee74abbe", season="Fall-2025")
                                             # ====next task==== #
                                            
                                    # need to upate the hitters_table to match to batter.get_stats() output
                                    # need to finish the get hitters function to get all the hitters to add to the stats table and
                                    # loop this compute_and_save_for_player function for each hitter returned from get_hitters
                                    print("Hitter stats calculation completed.")

    #=============================== send json to frontend ============================================#

                        

                                    return {"message": "In pipeline executed successfully."}     


def main():
        in_pipeline()


if __name__ == "__main__":
        main()
    







    
    
    