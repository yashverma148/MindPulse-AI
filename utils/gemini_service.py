import os
import json
import time
from google import genai
from google.genai import types

def get_gemini_client():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return None
    api_key = api_key.strip('"\'')
    return genai.Client(api_key=api_key)

def generate_insights(data, is_roast_mode=False):
    client = get_gemini_client()
    if not client:
        return {
            "summary": "AI API Key not configured.",
            "suggestions": ["Add GEMINI_API_KEY to your .env file."],
            "behavioral_analysis": "Cannot analyze without API key.",
            "roast": "Too broke for an API key? Expected." if is_roast_mode else ""
        }
        
    prompt = f"""
    Analyze the following daily productivity data for a user:
    - Study Hours: {data.get('study_hours')}
    - Work Hours: {data.get('work_hours')}
    - Screen Time: {data.get('screen_time')}
    - Distraction Time: {data.get('distraction_time')}
    - Sleep Hours: {data.get('sleep_hours')}
    - Productivity Score: {data.get('productivity_score'):.1f}/100

    Provide the response strictly in this JSON format:
    {{
        "summary": "A brief 2-sentence summary of their day.",
        "suggestions": ["Suggestion 1", "Suggestion 2", "Suggestion 3"],
        "behavioral_analysis": "A short paragraph analyzing their behavioral pattern.",
        "roast": "{'A fun, sarcastic, but non-offensive roast about their stats.' if is_roast_mode else 'None'}"
    }}
    """
    
    # Try multiple models in order of preference (each has separate quota)
    models_to_try = ['gemini-2.0-flash-lite', 'gemini-2.0-flash', 'gemini-2.5-flash']
    
    for model_name in models_to_try:
        for attempt in range(2):  # 2 attempts per model
            try:
                print(f"Trying model: {model_name} (attempt {attempt + 1})")
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        temperature=0.7
                    )
                )
                text = response.text.strip()
                if text.startswith('```json'):
                    text = text[7:]
                if text.startswith('```'):
                    text = text[3:]
                if text.endswith('```'):
                    text = text[:-3]
                result = json.loads(text.strip())
                print(f"Success with model: {model_name}")
                return result
            except Exception as e:
                error_str = str(e)
                print(f"Error with {model_name}: {error_str[:100]}")
                if 'RESOURCE_EXHAUSTED' in error_str or '429' in error_str:
                    if attempt == 0:
                        print(f"Rate limited on {model_name}, waiting 10s before retry...")
                        time.sleep(10)
                        continue
                    else:
                        print(f"Quota exhausted for {model_name}, trying next model...")
                        break
                elif '404' in error_str or 'NOT_FOUND' in error_str:
                    print(f"Model {model_name} not available, trying next...")
                    break
                else:
                    break
    
    return {
        "summary": "All AI model quotas are temporarily exhausted.",
        "suggestions": [
            "Wait 1-2 minutes and try again (free tier resets per minute).",
            "Or generate a new API key from https://aistudio.google.com/apikey",
            "Your productivity score was still calculated by the ML model above."
        ],
        "behavioral_analysis": "The AI analysis is temporarily unavailable due to API rate limits on the free tier. This is normal — just wait a minute and try again.",
        "roast": "You clicked so many times even Google said 'chill bro'! 😂" if is_roast_mode else ""
    }
