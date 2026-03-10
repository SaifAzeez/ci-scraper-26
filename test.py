import os
from supabase import create_client, Client

# Load from environment variables if you set a .env
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Fetch all donors (or limit to 10)
response = supabase.table("donors").select("*").order("scraped_at", desc=True).limit(10).execute()

if response.data:
    print("Latest donors:")
    for donor in response.data:
        print(donor)
else:
    print("No donor records found.")