import os
import google.generativeai as genai
from elevenlabs.client import ElevenLabs
from elevenlabs import save

def generate_story(journal_text):
    # Load your config files
    with open('config/character_bible.txt', 'r') as f:
        bible = f.read()

    with open('config/prompt_template.txt', 'r') as f:
        template = f.read()
    
    # Load the summary log
    with open('config/series_history.txt', 'r') as f:
        past_episodes = f.read()

    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel('models/gemini-3-flash-preview')
    
    # We combine the bible and template into one powerful instruction
    system_instruction = f"{template}\n\nCHARACTER BIBLE:\n{bible}"
    #print("system_instruction", system_instruction)
    prompt = f"""
    {system_instruction}\n\n
    SERIES HISTORY:
    {past_episodes}

    NEW JOURNAL NOTES:
    {journal_text}

    Task: Write a new 2-minute story for the podcast.
    """
    response = model.generate_content(prompt)
    return response.text

def generate_story_and_summary(journal_text):
    # Initialize model inside this function or at the top of this file
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel('models/gemini-3-flash-preview')
    
    # 1. Load your config files
    with open('config/character_bible.txt', 'r') as f:
        bible = f.read()
    with open('config/prompt_template.txt', 'r') as f:
        template = f.read()
    with open('config/series_history.txt', 'r') as f:
        history = f.read()

    # 2. Generate the Story
    full_prompt = f"{template}\n\nHISTORY:\n{history}\n\nBIBLE:\n{bible}\n\nJOURNAL:\n{journal_text}"
    story_response = model.generate_content(full_prompt)
    story_text = story_response.text

    # 3. Generate the Summary (The "Memory")
    summary_prompt = f"Summarize this story in one short sentence for a history log. Focus on the main event: {story_text}"
    summary_response = model.generate_content(summary_prompt)
    summary_text = summary_response.text

    return story_text, summary_text

def generate_voice(text, output_path):
    client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
    
    print(f"Generating audio for: {text[:30]}...")
    
    # In the new SDK, we use text_to_speech.convert
    audio_generator = client.text_to_speech.convert(
        text=text,
        voice_id="qlnUbSLa6XkXV9pK52QP", # This is the ID for 'Clyde'
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )
    
    # The result is a generator, so we collect the chunks and save
    with open(output_path, "wb") as f:
        for chunk in audio_generator:
            if chunk:
                f.write(chunk)
                
    print(f"✅ Audio saved to {output_path}")

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv('api_key.env')
    test_journal = "Today the kid tried to use a banana as a telephone and got frustrated when it didn't ring."
    story = generate_story(test_journal)
    print("--- GENERATED STORY ---")
    print(story)
    generate_voice(story, "test_audio.mp3")
    print("Audio generated as test_audio.mp3")