import google.generativeai as genai
import json
import os

# This line uses your secret Gemini key stored safely in GitHub
genai.configure(api_key=os.environ['GEMINI_API_KEY'])

# This picks the free AI model — 'flash' is fast AND free
model = genai.GenerativeModel('gemini-1.5-flash')

def pick_topic():
    # Read the list of topics we already used so we never repeat
    used = []
    if os.path.exists('used_topics.txt'):
        with open('used_topics.txt') as f:
            used = f.read().splitlines()

    # Build the question we ask the AI — like writing a note to a teacher
    question = f'''
    You are helping a kids YouTube channel called GappuVerse.
    Pick ONE fun and surprising fact for children aged 5 to 12.
    Do NOT use these topics that we already made videos about: {used}
    Reply with ONLY the topic name. Nothing else.
    Example: Why starfish have no brain
    '''

    # Send the question to Gemini AI and wait for the answer
    answer = model.generate_content(question)

    # Take just the text from the answer
    topic = answer.text.strip()

    print(f'Today Gappu will talk about: {topic}')
    return topic

def write_script(topic):
    # Ask the AI to write a full video script
    prompt = f'''
    Write a 60-second YouTube Shorts script for GappuVerse kids channel.
    Topic: {topic}
    Main character: Gappu — a curious 8-year-old Indian boy.
    Keep language simple — a 7-year-old must understand every word.
    Output ONLY as JSON with these parts:
    {{
      "title": "video title (max 60 letters)",
      "hook":  "first sentence to grab attention",
      "lines": ["line1", "line2", "line3", "line4", "line5"],
      "outro": "ending — ask viewers to like and subscribe",
      "images": ["describe scene 1", "describe scene 2", "describe scene 3", "describe scene 4", "describe scene 5"]
    }}
    '''

    # Send the writing job to Gemini and get the script back
    result = model.generate_content(prompt)

    # Clean up the text (removes ```json fences if AI added them)
    raw = result.text.strip().replace('```json', '').replace('```', '')

    # Turn the text into a Python dictionary (like a labelled box)
    script = json.loads(raw)

    print(f'Script ready! Title: {script["title"]}')
    return script
