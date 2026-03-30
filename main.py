import shutil

# Call all our other files — like calling teammates onto the field
from brain    import pick_topic, write_script
from voice    import make_all_audio
from pictures import draw_all_pictures
from video    import build_video
from upload   import post_to_youtube

def run_everything():
    print('Good morning! GappuVerse robot is starting...')

    # STEP 1: Pick today's topic
    topic = pick_topic()

    # STEP 2: Write a script about that topic
    script = write_script(topic)

    # STEP 3: Gather all the lines that will be spoken aloud
    all_lines = [script['hook']] + script['lines'] + [script['outro']]

    # STEP 4: Record all the voice lines
    print("Recording Gappu's voice...")
    audio_files = make_all_audio(script)

    # STEP 5: Draw all 5 pictures
    print('Drawing pictures...')
    picture_files = draw_all_pictures(script['images'])

    # STEP 6: Put everything together into a video
    print('Assembling the video...')
    video_path = build_video(picture_files, audio_files, all_lines)

    # STEP 7: Post the video to YouTube
    print('Posting to YouTube...')
    post_to_youtube(video_path, script, topic)

    # STEP 8: Save today's topic so we never repeat it
    with open('used_topics.txt', 'a') as f:
        f.write(topic + '\n')

    # STEP 9: Delete the temp folder — we don't need those files anymore
    shutil.rmtree('temp', ignore_errors=True)

    print('ALL DONE! Gappu posted a new video today!')

# This line starts everything — like pressing the Play button
if __name__ == '__main__':
    run_everything()
