import gradio as gr
import requests

# Gradio Inputs
categories = ["Agriculture", "Healthcare", "Education", "Employment", "Financial Inclusion", "Social Security", "Technology", "Urban Development", "Women Empowerment", "Business Support"]
eligibility_options = ["Children", "Low-Income Families", "Farmers", "Senior Citizens", "Unorganized Sector Workers", "Urban Poor", "Rural Poor", "Women"]
locations = ["Nationwide", "Urban", "Rural", "State-Specific"]
sort_options = ["Relevance", "Benefits", "Most Recent"]

# Function to call the FastAPI backend for recommendations
def gradio_recommend_schemes(user_needs, category, eligibility, location, sort_by):
    # Prepare the data to send to FastAPI
    data = {
        "user_needs": user_needs,
        "category": category,
        "eligibility": eligibility,
        "location": location,
        "sort_by": sort_by
    }
    
    # Send the input data to FastAPI backend
    try:
        response = requests.post("http://127.0.0.1:8000/recommend_schemes/", json=data)
        if response.status_code == 200:
            return response.json()  # Return the recommendations
        else:
            return {"error": "No relevant schemes found or error in the backend"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Error communicating with the backend: {str(e)}"}

# Gradio Interface
gradio_interface = gr.Interface(
    fn=gradio_recommend_schemes,
    inputs=[
        gr.Textbox(label="User Needs"),
        gr.Dropdown(choices=categories, label="Category", value=""),
        gr.Dropdown(choices=eligibility_options, label="Eligibility", value=""),
        gr.Dropdown(choices=locations, label="Location", value=""),
        gr.Dropdown(choices=sort_options, label="Sort By", value="Relevance")
    ],
    outputs="json"
)

# Launch Gradio Interface
if __name__ == "__main__":
    gradio_interface.launch(share=True)
