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
                                    json_data = csv_to_json(csv_file_path) # works 
                                    import os
                                    os.makedirs("src/data", exist_ok=True)
                                    with open("src/data/output.json", "w", encoding="utf-8") as f:
                                        json.dump(json_data, f, indent=2)
                                    print("CSV processed to JSON.")
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
                                    # print("Calculating hitter stats...")
                                    # from src.services.supabase_client import supabase
                                    # from src.services.hitter_stats_calc import HitterStatsCalculator

                                    # calculator = HitterStatsCalculator(supabase)  # use default client inside the class
                                    # print("Calculating and saving stats for player 1000118742...")


                                    # calculator.compute_and_save_for_player(player_id="1000118742", season=2025)

    #=============================== send josn to frontend ============================================#

                        

                                    return {"message": "In pipeline executed successfully."}     


def main():
        in_pipeline()


if __name__ == "__main__":
        main()
    







    
    
    