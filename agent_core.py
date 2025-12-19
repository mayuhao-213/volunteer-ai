import os
import json
import base64
import mimetypes
from zhipuai import ZhipuAI
from dotenv import load_dotenv

# --- Configuration Initialization ---
load_dotenv()
ZHIPU_API_KEY = os.getenv("ZHIPU_API_KEY")

if not ZHIPU_API_KEY:
    raise ValueError("ZHIPU_API_KEY is not configured in the .env file! Please check.")
client = ZhipuAI(api_key=ZHIPU_API_KEY)


# ----------------------------------------------------
# A. Core Utility: File Pre-processing
# ----------------------------------------------------

def file_to_base64(file_path: str) -> str | None:
    """Convert local file to Base64 encoding with Data URI Scheme (for Multimodal API)"""
    try:
        mime_type, _ = mimetypes.guess_type(file_path)
        if not mime_type:
            return None
        
        with open(file_path, "rb") as file:
            encoded_content = base64.b64encode(file.read()).decode('utf-8')
            return f"data:{mime_type};base64,{encoded_content}"
            
    except FileNotFoundError:
        print(f"Agent Core Error: File not found: {file_path}")
        return None
    except Exception as e:
        print(f"Agent Core Error: Base64 conversion failed: {e}")
        return None

# ----------------------------------------------------
# B. Multimodal Analysis Functions (Step-by-step implementation)
# ----------------------------------------------------

def analyze_audio_to_text(audio_path: str) -> str:
    """
    TODO: ASR Core Logic
    Currently returns None, waiting for Whisper or other ASR integration.
    """
    # Future integration: audio_text = asr_service.transcribe(audio_path)
    return None 

def analyze_image_for_context(image_path: str) -> str:
    """
    Image Scenario/Emotion Analysis Core Logic
    Currently returns None, waiting for GLM-4V integration.
    """
    # Future integration: image_summary = get_image_summary(image_path)
    return None 

# ----------------------------------------------------
# C. Final Agent for Report Generation
# ----------------------------------------------------

def generate_student_report(
    student_name: str,
    teacher_description: str,
    image_analysis_result: str | None,
    audio_transcription: str | None
) -> dict:
    """
    Core Agent: Integrates all multimodal inputs and calls GLM-4 to generate a structured report.
    """
    # 1. Construct unified input text
    image_text = f"[Image Analysis Result]: {image_analysis_result}" if image_analysis_result else "[Image Analysis Result]: None (Not provided or analyzed)"
    audio_text = f"[Audio Transcription]: {audio_transcription}" if audio_transcription else "[Audio Transcription]: None (Not provided or analyzed)"
    
    # Define English JSON Format
    JSON_FORMAT = f"""
        {{
            "user_name": "{student_name}",
            "summary_intro": "One-sentence deep summary, e.g., '{student_name} is a keen observer with great talent in logic and art, but needs support in building psychological safety.'",
            "personality": "Markdown formatted long text. Write in paragraphs. **Bold key traits**. Analyze specific details from input (e.g., 'drawing' or 'math solving').",
            "learning_advice": "Markdown formatted long text. DO NOT use simple lists. Use **bullet points with bold headers** (e.g., **1. Build Safety Zone**: ...). Must include at least 3 specific, actionable suggestions. Separate points with double newlines (\\n\\n).",
            "hobbies_analysis": "Markdown formatted text. Deeply analyze the psychological drivers and potential behind their interests.",
            "scores": {{
                "innovation": Score 10-100, 
                "communication": Score 10-100, 
                "stability": Score 10-100,
                "drive": Score 10-100,
                "empathy": Score 10-100
            }},
            "key_takeaways": [
                "First key takeaway",
                "Second key takeaway",
                "Third key takeaway"
            ]
        }}
        """
    
    # Define English Prompt
    PROMPT_TEXT = f"""
        You are a senior **Child Educational Psychologist** with 20 years of experience. You look beyond surface behaviors to understand deep psychological motivations.
        Please read the multimodal data for student [{student_name}] and generate a **profound, human-centric, and professional** growth analysis report in **ENGLISH**.
        
        【Input Data】
        1. **Teacher Observation**: {teacher_description}
        2. **Image Analysis**: {image_text}
        3. **Audio Transcription**: {audio_text}
        
        【Analysis Principles】
        1. **No Generic Advice**: Do not write generic phrases like "study hard". Every sentence must be based on specific details from the input (e.g., "Because she used graphical methods to solve math problems, it indicates...").
        2. **Markdown Formatting**: 
            - **learning_advice** field must use standard Markdown list format.
            - Separate each suggestion point (e.g., 1. xxx) with **double newlines (\\n\\n)** to ensure they appear as separate paragraphs on the web page.
            - Use **Bold** to emphasize core concepts.
        3. **Format Correction**: 'learning_advice' must return a **single long string containing newlines**, not a list object.
        4. **Scoring Criteria (0-100)**:
        - innovation: Creativity and novel problem-solving.
        - communication: Willingness and ability to express (introverts might score lower here, be realistic).
        - stability: Emotional stability and resilience.
        - drive: Inner drive to explore the unknown.
        - empathy: Ability to perceive others' emotions.
        
        Please strictly output ONLY a valid JSON object following this structure:
        {JSON_FORMAT}
        """
    try:
        response = client.chat.completions.create(
            model="glm-4", # Use stable GLM-4 text model for JSON output stability
            messages=[
                {"role": "user", "content": PROMPT_TEXT}
            ],
            response_format={"type": "json_object"} 
        )
        
        json_string = response.choices[0].message.content
        return json.loads(json_string)
    
    except Exception as e:
        print(f"❌ GLM-4 Agent Call Failed: {e}")
        # Return a fallback report with error info
        return {
            "user_name": student_name,
            "personality": f"AI Report Generation Failed. Error: {e}",
            "learning_advice": "Please check API Key, network connection, or Agent Prompt.",
            "hobbies_analysis": "No analysis result.",
            "scores": {"innovation": 50, "communication": 50, "stability": 50, "drive": 50, "empathy": 50},
            "summary_intro": "Error generating report.",
            "key_takeaways": ["System Error"]
        }