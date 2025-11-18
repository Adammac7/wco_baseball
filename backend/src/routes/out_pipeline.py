from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from pydantic import BaseModel

router = APIRouter(prefix="/out_pipeline", tags=["out_pipeline"])


@router.post("out_pipeline")
async def out_pipeline():
                                    
    #=============================== Need to get csv from google drive ===============================#
                                    # hard code for now
                                    csv_file_path = 'All Intrasquads.csv'
    #=============================== Process csv into JSON ===========================================#
                                    from src.services.csv_to_json import csv_to_json
                                    json_data = csv_to_json(csv_file_path) # works
    #=============================== send json to supabase (pitches table is updated) ================#

    #=============================== Need to calculate total stats ( stats table )  ============================================#

    #=============================== get all pitches from table and turn table into json ============================================#
    
    #=============================== claculate stats ============================================#

    #=============================== update stats table ============================================#

                         #====this should tigger front end to update stats display ====#

                                    return {"message": "Out pipeline executed successfully."}                           
    







    
    
    