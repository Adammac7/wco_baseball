import json
from pathlib import Path
from src.services import supa_uploader
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from pydantic import BaseModel


router = APIRouter()

# to optimize calculuating player stats, switch from list to dict to store the stats per zone box

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
    json_data = csv_to_json(csv_file_path) # adds season tag to each entry
    save_json(json_data) # saves to backend\src\data\output.json
    print("CSV processed to JSON.")
    #=============================== check for season mismatch ======================================#  
    season = json_data[0]['Season']
    for entry in json_data:
        if entry['Season'] != season:
            raise HTTPException(status_code=400, detail=f"CSV contained data from multiple seasons. Condense to one season. Season mismatch found: {entry['Season']}. Expected: {season}")
    #=============================== clean playerIDs ======================================#  works
    from src.services.hitter_calc import Hitter_calc
    hc = Hitter_calc()
    json_data = hc.clean_player_ID(json_data)
    save_json(json_data)

    #=============================== send json to pitches table ======================================#  works
    print("Uploading to pitches table...")
    from src.services.supa_uploader import Supa_uploader
    uploader = Supa_uploader(
        supabase_client=None,  # use default client inside the class
        json_file=json_data,
        table="pitch_data",
        chunk_size=200,
        upsert=True,
        on_conflict="id"
    )
    uploader.run()
    print("Upload to pitches table completed.")
    #=============================== send json to players table ====================================#  works
    # 1. Go through the pitch JSON and assign each row a player_id
    #    (using your custom hash or mapping function)

    #    Build a dictionary:
    #        stats_dict[player_id] = list_of_counting_stats
    #
    #    As you loop through each pitch in the JSON:
    #        - compute counting stats for that pitch
    #        - accumulate into stats_dict[player_id]

    # -------------------------------------------------------

    # 2. Pull existing players from hitters table (ONLY once)
    #    new_json = SELECT * FROM hitters WHERE id IN stats_dict.keys()

    # 3. Update each player row with newly calculated stats
    #    for row in new_json:
    #        row = row_with_updated_counting_stats
    #
    #    After updating counting stats, recompute derived stats:
    #        - AVG
    #        - OBP
    #        - SLG
    #        - OPS
    #        - wOBA
    #        - Avg EV, Avg LA, etc.

    # -------------------------------------------------------

    

    # -------------------------------------------------------

    # 5. Build Player objects from pitch JSON (your existing method)
    players = Supa_uploader.build_players_from_pitches(json_data)

    print("Uploading to players table...")
    uploader_players = Supa_uploader(
        supabase_client=None,   # use default client inside the class
        json_file=players,
        table="players",
        chunk_size=100,
        upsert=True,
        on_conflict="id"
    )
    uploader_players.run()
    print("Upload to players table completed.")

    # -------------------------------------------------------

    # 6. Check for new players and add them to the table if needed
    # need to get all player IDs from the json_data
    new_batter_ids = set()
    for pitch in json_data:
        new_batter_ids.add(pitch['BatterId'])

    #=============================== claculate stats by querying, output json =========================#
    print("Calculating hitter stats...")
    from src.services.supabase_client import supabase
    from src.services.hitter_stats_calc import HitterStatsCalculator

    calculator = HitterStatsCalculator(supabase)  # use default client inside the class
#     print("Calculating and saving stats for player 6691ce9aee74abbe...")
#     player_id = "6691ce9aee74abbe"


#+++++++++++++++++++++++++++++++++ add check for multiple seasons in one csv, fail upload if there are multiple seasons ++++++++++++++++++++++++++++++#
    # change to str, update func accordingly
    season = "Fall-2025" # hard code for now, need to get season from csv file name or data
    for batter_id in new_batter_ids:
        print(f"Calculating and saving stats for player {batter_id}...")
        calculator.compute_and_save_for_player(batter_id, season=season)
    # ====next task==== #

    # need to update the hitters_table to match to batter.get_stats() output
    # need to finish the get hitters function to get all the hitters to add to the stats table and
    # loop this compute_and_save_for_player function for each hitter returned from get_hitters
    print("Hitter stats calculation completed.")

    #=============================== send json to frontend ============================================#

    return {"message": "In pipeline executed successfully."}

#++++++++++++++++ full pipeline upload went through successfully,
#++++++++++++++++ need to check for correctness
#++++++++++++++++ need to try and send data to the frontend
#++++++++++++++++ start on pitcher stats calc next

def main():
    in_pipeline()


if __name__ == "__main__":
    main()










