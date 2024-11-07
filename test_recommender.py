# test_recommender.py
from vectorizer import SchemeRecommender  # Import your recommender class

# Specify the path to the schemes.json file
scheme_file = 'jsondb/schemes.json'  # Adjust to the correct path of your JSON file

# Initialize the recommender with the schemes data
recommender = SchemeRecommender(scheme_file)

# Example: Get recommendations based on user needs and filter by category
recommendations = recommender.get_recommendations(
    user_needs="financial support", 
    category="child support", 
    sort_by="relevance"
)

# Print the filtered and sorted recommendations
print("Recommendations:", recommendations)
