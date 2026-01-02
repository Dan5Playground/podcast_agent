# 🍫 Project Chocolate: Operational Workflow

This document tracks the steps to move from a raw memory to a published podcast.

## 🛠 Step 1: Ingestion (The Journal)
* **Script:** `src/google_docs.py`
* **Action:** Write the new entry in the Google Doc.
* **Logic:** The script fetches the text. It uses the `GOOGLE_DOC_ID` from `.env`.
* **Goal:** Get raw text into the Python environment.

## 🧠 Step 2: Transformation (The Story)
* **Script:** `src/generator.py` (via `generate_story`)
* **Action:** Combine the Raw Journal + `character_bible.txt` + `series_history.txt`.
* **Logic:** Gemini Flash latest processes the text.
* **Goal:** A 300-word whimsical script that maintains character consistency.

## 🎙 Step 3: Synthesis (The Voice)
* **Script:** `src/generator.py` (via `generate_voice`)
* **Action:** Send the story text to ElevenLabs.
* **Logic:** Uses the "Clyde" or "River" voice ID. # <--needs update
* **Goal:** An MP3 file saved in the `/output` folder.

## 📦 Step 4: Archiving & Review
* **Script:** `main.py` (The Orchestrator)
* **Action:** Save a copy of the raw journal to `/journal_archive`. Append the story summary to `series_history.txt`.
* **Goal:** Ensure the agent "remembers" this episode for next week.

## 🚀 Step 5: Distribution (Manual)
* **Action:** Upload the `.mp3` from `/output` to Spotify for Podcasters.
* **Time Check:** Should take less than 5 minutes.

---


## Backlog
1. create a webUI for all the related materials to monitor the generation process 
