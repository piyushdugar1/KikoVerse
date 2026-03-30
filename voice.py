import asyncio
import edge_tts
import os

# This is the voice we chose — a young Indian-English boy voice (totally free!)
GAPPU_VOICE = 'en-IN-PrabhatNeural'
# Other free options you can try:
# 'en-US-GuyNeural'  — American boy voice
# 'en-GB-RyanNeural' — British boy voice

async def speak_line(text, filename):
    # Set up the voice with our chosen sound and a slightly faster speed
    talker = edge_tts.Communicate(text, GAPPU_VOICE, rate='+8%')
    # Record the voice and save it as an audio file
    await talker.save(filename)
    print(f'  Voice saved: {filename}')

def make_all_audio(script):
    # Turn every line of the script into an audio recording
    os.makedirs('temp', exist_ok=True)

    audio_files = []  # empty list — like an empty backpack

    # Record the hook (opening line)
    asyncio.run(speak_line(script['hook'], 'temp/line_00.mp3'))
    audio_files.append('temp/line_00.mp3')

    # Go through each of the 5 main lines and record them one by one
    for i, line in enumerate(script['lines']):
        filename = f'temp/line_{i+1:02d}.mp3'
        asyncio.run(speak_line(line, filename))
        audio_files.append(filename)

    # Record the outro (the goodbye/subscribe message)
    asyncio.run(speak_line(script['outro'], 'temp/line_99.mp3'))
    audio_files.append('temp/line_99.mp3')

    return audio_files
