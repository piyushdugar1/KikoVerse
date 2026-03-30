from moviepy.editor import *
import os

# These numbers set the size of the video — phone screen size (9:16 tall)
VIDEO_WIDTH  = 1080
VIDEO_HEIGHT = 1920
FRAMES_PER_SECOND = 30

def add_subtitle(text, duration):
    # Create the white words shown at the bottom of the screen
    return (
        TextClip(
            text,
            fontsize=50,
            color='white',
            font='DejaVu-Sans-Bold',
            stroke_color='black',  # black outline so text is readable on any background
            stroke_width=3,
            method='caption',
            size=(900, None),      # max width before wrapping to next line
            align='center'
        )
        .set_duration(duration)
        .set_position(('center', 0.75), relative=True)  # puts text near the bottom
    )

def build_video(picture_paths, audio_paths, script_lines):
    # Assemble all pieces into one video — like cutting and gluing a scrapbook
    os.makedirs('output', exist_ok=True)

    scenes = []  # empty storyboard

    for i, (pic, audio_file, narration) in enumerate(zip(picture_paths, audio_paths, script_lines)):

        # Load audio and find out how long it is
        audio = AudioFileClip(audio_file)
        scene_length = audio.duration + 0.4  # tiny pause at the end

        # Load picture and resize it to fill the phone screen
        image = ImageClip(pic).resize(height=VIDEO_HEIGHT)
        if image.w < VIDEO_WIDTH:
            image = image.resize(width=VIDEO_WIDTH)

        # Crop to exactly the right size — like trimming a photo to fit a frame
        image = image.crop(
            x_center=image.w/2, y_center=image.h/2,
            width=VIDEO_WIDTH, height=VIDEO_HEIGHT
        )
        image = image.set_duration(scene_length)

        # Slow zoom effect — makes the video feel more alive
        zoom_effect = lambda t: 1 + 0.025*(t/scene_length)
        image = image.resize(zoom_effect)

        # Create the subtitle for this scene
        subtitle = add_subtitle(narration, scene_length)

        # Combine picture + subtitle into one scene, then add audio
        combined = CompositeVideoClip([image, subtitle]).set_audio(audio)
        scenes.append(combined)

    # Stick all scenes together end-to-end
    full_video = concatenate_videoclips(scenes, method='compose')

    output_path = 'output/gappu_short.mp4'
    full_video.write_videofile(
        output_path,
        fps=FRAMES_PER_SECOND,
        codec='libx264',       # best video format for YouTube
        audio_codec='aac',     # best audio format for YouTube
        logger=None
    )
    print(f'Video saved to: {output_path}')
    return output_path
