from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd

class SchemeRecommender:
    def __init__(self, scheme_data):
        # Assuming scheme_data is a DataFrame
        self.scheme_data = scheme_data
        self.vectorizer = CountVectorizer(stop_words='english')

    def get_recommendations(self, user_needs, category=None, eligibility=None, location=None, sort_by="relevance"):
        # Filter the scheme data based on user input filters
        filtered_schemes = self.scheme_data
        
        if category:
            filtered_schemes = filtered_schemes[filtered_schemes['category'] == category]
        if eligibility:
            filtered_schemes = filtered_schemes[filtered_schemes['eligibility'].str.contains(eligibility, case=False, na=False)]
        if location:
            filtered_schemes = filtered_schemes[filtered_schemes['location'] == location]

        # Ensure there's meaningful data to vectorize
        if filtered_schemes.empty:
            print("Error: No schemes found after filtering!")
            return []
        
        # Inspect the scheme descriptions before processing
        print("Scheme Descriptions Before Vectorization:")
        print(filtered_schemes[['scheme_name', 'scheme_description']].head())

        # Check if 'scheme_description' column has valid content
        scheme_descriptions = filtered_schemes['scheme_description'].dropna().tolist()
        if not scheme_descriptions:
            print("Error: No valid descriptions to process!")
            return []

        try:
            # Vectorize the descriptions
            scheme_matrix = self.vectorizer.fit_transform(scheme_descriptions)
        except ValueError as e:
            print(f"Error in vectorization: {e}")
            return []

        # Proceed with recommending schemes based on the vectorized data (for now returning filtered schemes)
        recommendations = filtered_schemes.head(5)  # Returning top 5 schemes for simplicity
        return recommendations[['scheme_name', 'scheme_description']].to_dict(orient='records')
