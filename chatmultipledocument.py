import streamlit as st
import os
import requests
from dotenv import load_dotenv
from PIL import Image

# Load environment variables (Cohere API key)
load_dotenv()

# Retrieve the API key from the environment variable
cohere_api_key = os.getenv("cohere_api_key ")  # Replace with your actual API key

# Streamlit UI setup
st.set_page_config(page_title="Conversational Q&A Chatbot")
st.header("Gemini Image and Text Demo")

# Input and upload image setup
input = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

image = ""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

# Function to send a request to Cohere API and get a response
def get_cohere_response(input_text):
    # Define the Cohere API endpoint
    url = "https://api.cohere.ai/v1/generate"

    # Headers for authentication and content-type
    headers = {
        "Authorization": f"Bearer {cohere_api_key}",
        "Content-Type": "application/json"
    }

    # Define the prompt with the user input and image description (optional)
    prompt = f"""
    You are an expert in nutrition, and based on the uploaded food image, you need to provide a detailed breakdown of the food items and their respective calorie values. Use the following format:

    1. Item 1 - no of calories
    2. Item 2 - no of calories
    ----
    ----
    """

    # API payload
    payload = {
        "prompt": prompt + "\n" + input_text,
        "max_tokens": 150,
        "temperature": 0.7
    }

    # Make the POST request to Cohere API
    response = requests.post(url, headers=headers, json=payload)

    # Handle API response
    if response.status_code == 200:
        result = response.json()
        return result['generations'][0]['text'].strip()
    else:
        return f"Error: {response.status_code} - {response.text}"

# Submit button functionality
submit = st.button("Tell me about the image")

if submit:
    if uploaded_file is not None and input:
        # Get the response from Cohere API
        response_text = get_cohere_response(input)
        st.subheader("The Response is")
        st.write(response_text)
    else:
        st.error("Please provide both a prompt and upload an image.")
