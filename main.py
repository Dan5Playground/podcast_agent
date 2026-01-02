import os
from dotenv import load_dotenv
from src.google_docs import get_google_doc_text, extract_latest_entry
from src.generator import generate_story, generate_voice, generate_story_and_summary
from datetime import datetime

# Load keys and IDs
load_dotenv('api_key.env')
DOC_ID = os.getenv("GOOGLE_DOC_ID")

def run_pipeline():
    print("🚀 Starting the Agent...")
    
    # 1. Fetch
    print("✅ Journal fetched from Google Docs.")
    raw_text = get_google_doc_text(DOC_ID)
    journal_for_today = extract_latest_entry(raw_text)
    
    # Safety Check: If the entry is just the date and no text
    if len(journal_for_today) < 20: 
        print("⚠️ The latest entry seems too short. Did you forget to write the journal?")
        return
        
    print(f"📖 Found Journal Entry:\n{journal_for_today[:100]}...")
    
    # 2. Archive
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    with open(f"journal_archive/journal_{timestamp}.txt", "w") as f:
        f.write(raw_text)
    
    # 3. Rewrite
    story, summary = generate_story_and_summary(journal_for_today)
    print(f"✅ Story and Summary generated.")

    # 2. Save the full script for your archive
    with open(f"output/script_{timestamp}.txt", "w") as f:
        f.write(story)

    # 3. Append the summary to your long-term memory
    with open('config/series_history.txt', 'a') as f:
        f.write(f"\n{timestamp}: {summary}")
    print("✅ Memory updated in series_history.txt")

    # 4. Generate Voice
    audio_file = f"output/podcast_{timestamp}.mp3"
    generate_voice(story, audio_file)
    print(f"🎧 Audio saved to {audio_file}")

if __name__ == "__main__":
    run_pipeline()