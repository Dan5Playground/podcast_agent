# 🦦 Chocolate the River Tinkerer: Podcast Agent
An automated AI pipeline that transforms personal journal entries into whimsical, first-person audio stories for children.

## 🌟 Overview
This agent acts as a "Creative Memory Machine." It fetches recent notes from a Google Doc, uses **Gemini 3 Flash** to rewrite them into a story from the perspective of **Chocolate**, and generates high-quality narration using **ElevenLabs**.

## 🏗️ Project Structure
```text
/podcast-agent
├── main.py                 # The Orchestrator (Run this to start)
├── api_key.env             # Private API keys (Hidden by .gitignore)
├── requirements.txt        # Python dependencies
│
├── config/                 # THE BRAIN
│   ├── character_bible.txt # Chocolate's personality & traits
│   ├── prompt_template.txt # System instructions & audio rules
│   └── series_history.txt  # Persistent memory of past episodes
│
├── src/                    # THE ENGINE
│   ├── google_docs.py      # Google Docs API integration
│   └── generator.py        # Gemini & ElevenLabs logic
│
└── output/                 # THE PRODUCT
    └── (Generated MP3s and Scripts)
```

## Todo List
1. create a webUI to review created stories
2. add auto publishing 
