# backend/src/services/supabase_client.py

import os
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client

# Ensure we load the backend/.env when running scripts from repo root
env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)  # loads backend/.env in local dev
print("Loaded env from:", env_path)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("supabase_anon_key")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("Missing SUPABASE_URL or SUPABASE_KEY. Check your .env and remove spaces around '='.")
    raise SystemExit(1)

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
