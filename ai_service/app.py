import os
import json
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import google.generativeai as genai
from datetime import datetime
import logging
import random # Importing random for Gen Z time-of-day phrases

# Load environment variables from .env file in the ai_service directory
load_dotenv()

app = Flask(__name__)

# --- Setup Logging ---
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# Configure Gemini API
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    logger.info("Gemini API configured successfully.")
else:
    logger.error("CRITICAL: GEMINI_API_KEY not found in environment variables for AI service. AI suggestions will fail.")

# --- Helper function to list models ---
@app.route('/list-models', methods=['GET'])
def list_models_endpoint(): # Renamed function slightly to avoid potential clashes if imported elsewhere
    if not GEMINI_API_KEY:
        logger.error("Gemini API key not available. Cannot list models.")
        return jsonify({"error": "AI service not configured. Missing API key."}), 503
    try:
        logger.info("Listing available Gemini models...")
        models_list_data = []
        for m in genai.list_models():
            # Check if the model supports the 'generateContent' method
            if 'generateContent' in m.supported_generation_methods:
                models_list_data.append({
                    "name": m.name,
                    "display_name": m.display_name,
                    "description": m.description,
                    "version": m.version,
                    "supported_generation_methods": m.supported_generation_methods
                })
        logger.info(f"Found {len(models_list_data)} models supporting 'generateContent'.")
        return jsonify({"available_models_for_generateContent": models_list_data}), 200
    except Exception as e:
        logger.error(f"Error listing Gemini models: {str(e)}", exc_info=True)
        return jsonify({"error": "Failed to list AI models", "details": str(e)}), 500


# --- Helper function to call Gemini ---
def generate_gemini_response(prompt_text, is_json_output=False):
    if not GEMINI_API_KEY:
        logger.error("Gemini API key not available. Cannot generate response.")
        return {"error": "AI service not configured. Missing API key."}, 503

    logger.debug(f"Attempting to generate content with Gemini. JSON output expected: {is_json_output}")
    logger.debug(f"Prompt for Gemini:\n---\n{prompt_text}\n---")

    # List of models to try - you will likely update this based on /list-models output
    # Common model names. The `models/` prefix is often handled by the library.
    models_to_try = ['gemini-1.0-pro', 'gemini-pro', 'gemini-1.5-flash-latest'] 
    
    last_exception = None
    last_model_tried = ""

    for model_name in models_to_try:
        last_model_tried = model_name
        try:
            logger.info(f"Attempting to use Gemini model: {model_name}")
            # Ensure you are using the correct model name format expected by your library version
            # Sometimes it's 'gemini-1.0-pro', sometimes 'models/gemini-1.0-pro'
            # The error "404 models/gemini-pro" suggests the library might be adding "models/"
            # So, we provide the base name here.
            model_instance = genai.GenerativeModel(model_name)
            response = model_instance.generate_content(prompt_text)
            
            logger.debug(f"Raw Gemini API response object from {model_name}: {response}")
            
            if not response.parts: # Check if response.parts is empty
                error_message = f"AI model ({model_name}) did not return content."
                if response.prompt_feedback and response.prompt_feedback.block_reason:
                    error_message = f"Content generation blocked by Gemini ({model_name}): {response.prompt_feedback.block_reason_message}"
                    logger.warning(f"Gemini content generation blocked for {model_name}. Reason: {response.prompt_feedback.block_reason_message}, Safety Ratings: {response.prompt_feedback.safety_ratings}")
                else:
                    logger.warning(f"Gemini response.parts is empty for {model_name}. No content generated or content was filtered.")
                
                # If content is blocked or empty, this is a valid (though not useful) response from this model attempt.
                # We might not want to immediately try the next model unless it's a "model not found" type error.
                # However, for simplicity in this loop, we'll let it fall through to the exception handling if it's critical.
                # If it's just empty parts, we should return that specific error.
                return {"error": error_message, "details": f"The AI model's ({model_name}) response was empty or filtered."}, 500

            generated_text = response.text
            logger.debug(f"Text extracted from Gemini response ({model_name}): {generated_text}")

            if is_json_output:
                try:
                    parsed_json = json.loads(generated_text)
                    logger.info(f"Successfully parsed Gemini JSON output using {model_name}.")
                    return parsed_json, 200
                except json.JSONDecodeError as e:
                    logger.error(f"Gemini API Warning ({model_name}): Expected JSON output but received non-JSON: {generated_text}. Error: {e}")
                    return [s.strip() for s in generated_text.split('\n') if s.strip()], 200 # Fallback
            else:
                logger.info(f"Successfully generated text content from Gemini using {model_name}.")
                return {"text": generated_text}, 200

        except Exception as e:
            last_exception = e
            error_str = str(e).lower()
            logger.error(f"Exception during Gemini API call with {model_name}: {error_str}", exc_info=False) # Set exc_info to False for cleaner logs unless debugging deep
            
            # Check for specific "not found" or "permission" errors to try the next model
            # The error "404 models/... is not found" comes from the client library interpreting a 404 from the service.
            if "not found" in error_str or \
               "permission denied" in error_str or \
               "could not be found" in error_str or \
               "404" in error_str or \
               "invalid_argument" in error_str and "model" in error_str: # More general model error
                logger.warning(f"Model {model_name} failed. Trying next model if available.")
                continue 
            else:
                # For other errors, don't try other models, just fail.
                return {"error": f"Failed to generate AI response with {model_name} due to an API error", "details": str(e)}, 500
    
    # If all models failed
    logger.error(f"All attempted Gemini models ({', '.join(models_to_try)}) failed. Last model tried: {last_model_tried}. Last error: {str(last_exception)}")
    details_message = str(last_exception)
    if "API version v1beta" in details_message:
        details_message += " This might indicate an issue with the model name or your library version targeting an old API. Try updating the 'google-generativeai' library."
    return {"error": "Failed to generate AI response after trying multiple models.", "details": details_message}, 500

# --- Motivation Endpoint ---
@app.route('/motivation', methods=['POST'])
def get_motivation():
    logger.info("Received request for /motivation endpoint.")
    data = request.get_json()
    if not data:
        logger.warning("Missing JSON payload for /motivation.")
        return jsonify({"error": "Missing JSON payload"}), 400
    
    logger.debug(f"Motivation request payload: {data}")

    user_name = data.get('user_name', 'User')
    mood_trend_label = data.get('mood_trend_label', 'neutral')
    recent_mood_texts = data.get('recent_mood_texts', [])
    recent_notes_texts = data.get('recent_notes_texts', [])
    user_age = data.get('user_age', None)

    # Expanded Gen Z, modern time-of-day phrases
    current_hour = datetime.now().hour
    if 5 <= current_hour < 12:
        genz_time = random.choice([
            "chill morning", "vibey morning", "soft sunrise", "slow-mo morning", "cozy morning", "no rush morning", "just-woke-up vibes"
        ])
        mature_time = random.choice([
            "peaceful morning", "productive morning", "early start", "quiet morning"
        ])
    elif 12 <= current_hour < 18:
        genz_time = random.choice([
            "mid afternoon", "pretty chill afternoon", "laid-back afternoon", "solid afternoon", "golden hour", "snack o'clock", "energy dip zone"
        ])
        mature_time = random.choice([
            "afternoon", "busy afternoon", "steady afternoon", "sunny afternoon"
        ])
    else:
        genz_time = random.choice([
            "pretty chill evening", "cool evening", "low-key evening", "mid evening", "comfy night", "Netflix o'clock", "scroll-and-chill time"
        ])
        mature_time = random.choice([
            "relaxing evening", "quiet evening", "peaceful night", "unwind time"
        ])

    # Decide which style to use based on age
    if user_age is not None:
        try:
            age = int(user_age)
        except Exception:
            age = None
    else:
        age = None

    # Default to Gen Z if age is not provided
    if age is not None and age >= 30:
        time_of_day_phrase = mature_time
        style_instructions = (
            "Use a warm, supportive, and mature tone. Avoid slang and keep it professional yet friendly. "
            "No emojis unless it feels natural. Focus on actionable, realistic encouragement."
        )
        prompt_examples = (
            f"- For stress: 'Hi {user_name}, evenings can be a good time to decompress. Consider a short walk or reading to unwind.'\n"
            f"- For positive: 'Glad to hear you're feeling good this {mature_time}. Keep nurturing those positive habits.'\n"
            f"- For neutral: 'It's perfectly fine to have a {mature_time}. Maybe take a moment for yourself or connect with a friend.'\n"
        )
    else:
        time_of_day_phrase = genz_time
        style_instructions = (
            "Use a friendly, modern, Gen Z style—think real words, not clinical or generic. "
            "Sometimes use emojis if it fits naturally (but don't overdo it). "
            "If it fits, use a little humor, meme reference, or pop culture nod (but don't force it)."
        )
        prompt_examples = (
            f"- For anxiety: 'Hey {user_name}, sounds like anxiety's creeping in. Try a quick breathing reset—inhale for 4, hold for 4, exhale for 4. You got this. 💪'\n"
            f"- For positive: 'Yo {user_name}, loving that {mood_trend_label} vibe! Keep the energy up and maybe treat yourself to something fun this {genz_time}. ✨'\n"
            f"- For neutral: 'Sup {user_name}, it's all good to have a {genz_time}. Maybe just chill and recharge for a bit. No pressure, just vibes. 😌'\n"
            f"- For tired: 'Hey {user_name}, if you need a nap, take it. Self-care is not a crime. 💤'\n"
            f"- For stress: 'Hey {user_name}, stress is real. Maybe put your phone down for a sec and take a walk, or just vibe to your favorite song.'\n"
            f"- For low-key: 'Hey {user_name}, it's a low-key {genz_time}. Sometimes that's exactly what you need. Treat yourself to a snack or a meme scroll.'\n"
        )

    prompt_context = f"User: {user_name}. Time of day: {time_of_day_phrase}.\n"
    prompt_context += f"Recent mood trend: {mood_trend_label}.\n"
    if recent_mood_texts:
        prompt_context += f"Recent logged moods: {', '.join(recent_mood_texts)}.\n"
    if recent_notes_texts:
        notes_str = "; ".join(filter(None, recent_notes_texts))
        if notes_str:
            prompt_context += f"Recent notes: \"{notes_str}\".\n"

    has_anxiety = any('anxious' in text.lower() or 'anxiety' in text.lower() for text in recent_mood_texts + recent_notes_texts)
    has_stress = any('stress' in text.lower() for text in recent_notes_texts)

    if has_anxiety:
        prompt_context += "The user has expressed feelings of anxiety.\n"
    if has_stress:
        prompt_context += "The user has mentioned stress.\n"

    prompt = (
        f"{prompt_context}"
        "You are a supportive, relatable, and empathetic AI companion for a mood tracking app. "
        f"{style_instructions} "
        "Based on the user's context, provide a short (2-3 sentences), personalized, and actionable motivational message. "
        "If anxiety or stress is indicated, gently offer a brief, practical coping strategy. "
        "Keep it positive and encouraging, but avoid platitudes or toxic positivity. "
        "Make it sound like a caring friend offering support, not a robot. Do not refer to yourself as an AI. "
        "Examples:\n"
        f"{prompt_examples}"
        "Focus on the provided context and use the time-of-day phrase for a natural, relatable touch."
    )

    result, status_code = generate_gemini_response(prompt)
    logger.info(f"Sending response for /motivation. Status: {status_code}, Result: {result}")
    return jsonify(result), status_code

# --- Habit Suggestion Endpoint ---
@app.route('/habits', methods=['POST'])
def get_habit_suggestions():
    logger.info("Received request for /habits endpoint.")
    data = request.get_json()
    if not data:
        logger.warning("Missing JSON payload for /habits.")
        return jsonify({"error": "Missing JSON payload"}), 400

    logger.debug(f"Habit suggestion request payload: {data}")
    
    user_name = data.get('user_name', 'User')
    low_mood_activities = data.get('low_mood_activities', [])
    high_mood_activities = data.get('high_mood_activities', [])

    prompt_context = f"User: {user_name}.\n"
    if low_mood_activities:
        prompt_context += f"Activities sometimes linked to their lower moods: {', '.join(low_mood_activities)}.\n"
    if high_mood_activities:
        prompt_context += f"Activities sometimes linked to their better moods: {', '.join(high_mood_activities)}.\n"
    
    if not low_mood_activities and not high_mood_activities:
         prompt_context += "No specific activities strongly correlated with high or low moods were found in the recent data.\n"

    prompt = (
        f"{prompt_context}"
        "You are an AI assistant for a mood tracking app, providing habit suggestions. "
        "Based on the user's context, provide 2-3 concise, actionable, and empathetic habit suggestions. "
        "If specific activities are mentioned, try to incorporate them. "
        "One suggestion could be about mindfully approaching or reducing an activity linked to lower moods, and another about encouraging an activity linked to better moods. "
        "If no specific activities are strongly correlated, offer general well-being habits. "
        "Frame suggestions gently and constructively. Do not refer to yourself as an AI. "
        "Example for correlated activities: 'It seems like \"{low_activity}\" sometimes coincides with lower moods for you, {user_name}. Perhaps explore how that activity makes you feel, or try a mindful alternative. On the other hand, \"{high_activity}\" often appears with better moods - maybe find more ways to weave that into your week?' "
        "Example for general: '{user_name}, consider setting a small, achievable goal for today, like a 10-minute walk or dedicating time to a hobby you enjoy. Consistent small actions can make a big difference.' "
        "Output should be a list of strings, where each string is a suggestion. Format as a JSON list of strings. For example: [\"Suggestion 1\", \"Suggestion 2\"]"
    )
    
    result, status_code = generate_gemini_response(prompt, is_json_output=True)
    
    if status_code == 200 and not isinstance(result, list):
        logger.warning(f"Habit suggestions from AI was not a list as expected. Received: {type(result)}, Data: {result}. Attempting to reformat.")
        if isinstance(result, dict) and "text" in result: 
            result = [s.strip() for s in result["text"].split('\n') if s.strip()]
        elif isinstance(result, str): 
             result = [s.strip() for s in result.split('\n') if s.strip()]
        else: 
            result = ["Consider what small step you can take for your wellbeing today."]
            logger.warning("Could not reformat AI habit suggestions into a list. Using default.")


    if status_code == 200:
        logger.info(f"Sending response for /habits. Status: {status_code}, Suggestions: {result}")
        return jsonify({"suggestions": result}), status_code
    else:
        logger.info(f"Sending error response for /habits. Status: {status_code}, Error: {result}")
        return jsonify(result), status_code


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5001))
    # Ensure debug is True for development to see detailed errors and auto-reload
    app.run(debug=True, host='0.0.0.0', port=port)
    logger.info(f"Flask AI service stopped.")
