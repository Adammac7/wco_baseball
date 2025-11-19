from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from pydantic import BaseModel

router = APIRouter(prefix="/in_pipeline", tags=["in_pipeline"])


@router.post("in_pipeline")
async def in_pipeline():
                                    
    #=============================== Need to get csv from google drive ===============================#
                                    
                                    csv_file_path = 'All Intrasquads.csv'   # hard code for now
    #=============================== Process csv into JSON ===========================================#
                                    from src.services.csv_to_json import csv_to_json
                                    json_data = csv_to_json(csv_file_path) # works

    #=============================== send json to supabase (pitches table is updated) ================#
                                    from src.services.supa_uploader import Supa_uploader
                                    uploader = Supa_uploader(
                                        supabase_client=None,  # use default client inside the class
                                        json_file=json_data,  
                                        table="pitch_data",
                                        chunk_size=100,
                                        upsert=True,
                                        on_conflict="id"
                                    )
                                    uploader.run()

    #=============================== claculate stats by querying, output json =========================#
                            

    #=============================== send josn to frontend ============================================#

                        

                                    return {"message": "In pipeline executed successfully."}                           
    







    
    
    