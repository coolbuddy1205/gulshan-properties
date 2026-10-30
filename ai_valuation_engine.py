import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables from your root .env file
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl4eGJiY2RpdXJxb2ZnamVvdnd2Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc5MzAxMzg3MywiZXhwIjoyMTA4NTg5ODczfQ.3cBBkSp0BDz9xz7fQ9gP_gifVEpP4H6xLRQN10n4aNI"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
def calculate_ai_property_valuations():
    print("Fetching properties from Supabase for AI valuation analysis...")
    
    # Fetch all properties
    response = supabase.table("properties").select("*").execute()
    properties = response.data
    
    if not properties:
        print("No properties found in the database.")
        return

    for prop in properties:
        prop_id = prop["id"]
        price = prop["price"]
        size = prop["size_sqft"]
        location = prop["location"]
        
        # Simple AI baseline heuristic model (can be replaced with an ML model or LLM API call)
        # Calculates expected market valuation score based on local factors
        base_rate_sqft = 12000  # Default Delhi NCR baseline per sqft
        if location.lower() in ["south delhi", "gurugram"]:
            base_rate_sqft = 18000
        
        estimated_fair_value = size * base_rate_sqft if size else price
        valuation_score = round(min(max((price / estimated_fair_value) * 100, 50), 150), 2)
        
        print(f"Property: {prop['title']} | Location: {location} | AI Valuation Score: {valuation_score}")
        
        # Update the property record with the AI valuation score
        supabase.table("properties").update({
            "ai_valuation_score": valuation_score
        }).eq("id", prop_id).execute()

    print("AI Property Valuations successfully updated across all listings!")

if __name__ == "__main__":
    calculate_ai_property_valuations()