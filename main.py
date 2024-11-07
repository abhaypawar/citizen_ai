from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from database import get_scheme_data
from vectorizer import SchemeRecommender

app = FastAPI()

# FastAPI Models
class UserInput(BaseModel):
    user_needs: str
    category: str = None  # Optional category filter
    eligibility: str = None  # Optional eligibility filter
    location: str = None  # Optional location filter
    sort_by: str = "relevance"  # Default sort by relevance

@app.on_event("startup")
def load_recommender():
    # Initialize recommender with scheme data at app startup
    global recommender
    scheme_data = get_scheme_data()  # Fetch scheme data from the database
    recommender = SchemeRecommender(scheme_data=scheme_data)

# Helper function to parse filters
def get_filters(user_input: UserInput):
    return {
        "category": user_input.category,
        "eligibility": user_input.eligibility,
        "location": user_input.location,
        "sort_by": user_input.sort_by
    }

@app.post("/recommend_schemes/")
async def recommend_schemes(user_input: UserInput, filters: dict = Depends(get_filters)):
    # Clean the filters to ensure None values are removed
    filters = {key: value for key, value in filters.items() if value is not None}
    
    # Generate recommendations with the cleaned filter values
    recommendations = recommender.get_recommendations(user_input.user_needs, **filters)
    
    # If no recommendations are found, raise an HTTPException
    if not recommendations:
        raise HTTPException(status_code=404, detail="No relevant schemes found")

    return {"recommendations": recommendations}
