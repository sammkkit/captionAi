import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={GEMINI_API_KEY}"

def stylize_caption(caption: str, style: str = "cool and Gen Z"):
    """
    Generates styled caption options using the Gemini API.

    Args:
        caption (str): The base caption to be stylized.
        style (str): The desired style for the new captions.

    Returns:
        list[str]: A list of styled captions, or a list with an error message.
    """
    prompt = f"""
    You are a creative instgram worthy caption generator.
    Your task is to rewrite a base caption in a "{style}" style.
    You should try to use atleast one emoji.
    Generate 4 creative options.

    Your output MUST be a valid JSON object with a single key "captions"
    which contains an array of 4 strings. Do not add any other text or explanations.

    Example output format:
    {{
      "captions": ["caption 1", "caption 2", "caption 3", "caption 4"]
    }}

    Base caption: "{caption}"
    """

    body = {
        "contents": [
            {
                "parts": [
                    { "text": prompt }
                ]
            }
        ],
        "generationConfig": {
            "response_mime_type": "application/json"
        }
    }

    try:
        response = requests.post(API_URL, json=body, timeout=30)
        response.raise_for_status()

        response_data = response.json()

        # Validate 'candidates' structure
        if not response_data.get("candidates"):
            return [f"Error: API returned no candidates. Check safety ratings: {response_data.get('promptFeedback')}"]

        raw_text = response_data["candidates"][0]["content"]["parts"][0]["text"]

        # Parse the stringified JSON from Gemini
        parsed = json.loads(raw_text)

        return parsed.get("captions", ["Error: 'captions' key not found in response."])

    except requests.exceptions.RequestException as e:
        return [f"Error: Network or API request failed. {str(e)}"]
    except json.JSONDecodeError:
        return [f"Error: Failed to decode JSON from API response."]
    except KeyError as e:
        return [f"Error: Unexpected API response format. Missing key: {e}"]
    except Exception as e:
        return [f"An unexpected error occurred: {str(e)}"]
