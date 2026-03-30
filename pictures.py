import requests
import time
import os
from urllib.parse import quote

# Gappu's description — NEVER change this so he always looks the same!
# Think of it like Gappu's ID card.
GAPPU_LOOKS = (
    'cute chubby round-faced Indian cartoon boy named Gappu age 8 '
    'yellow kurta with star patterns big brown eyes short black hair '
    'with small cowlick missing front tooth friendly smile '
    '2D flat animation style vibrant pastel background child-friendly '
    'wholesome Pixar-inspired colorful'
)

def draw_one_picture(scene_description, picture_number):
    # Combine Gappu's ID card description with the scene we want
    full_description = f'{GAPPU_LOOKS}, {scene_description}'

    # Make the description safe to put in a web link
    safe_text = quote(full_description)

    # Build the web address for our free picture
    # seed=42 keeps Gappu looking the same every time (consistency trick!)
    picture_url = (
        f'https://image.pollinations.ai/prompt/{safe_text}'
        f'?width=1080&height=1920'
        f'&seed=42'
        f'&model=flux'
        f'&nologo=true'
    )

    # Try up to 3 times in case the internet is slow
    for try_number in range(3):
        try:
            response = requests.get(picture_url, timeout=60)

            # 200 = success!
            if response.status_code == 200:
                save_path = f'temp/pic_{picture_number:02d}.jpg'
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                print(f'  Picture {picture_number} drawn and saved!')
                return save_path
        except Exception as error:
            print(f'  Try {try_number+1} failed: {error}. Trying again...')
            time.sleep(5)

    raise Exception(f'Could not draw picture number {picture_number}')

def draw_all_pictures(scene_list):
    # Draw ALL 5 pictures, one by one
    os.makedirs('temp', exist_ok=True)
    picture_paths = []

    for i, scene in enumerate(scene_list):
        print(f'Drawing picture {i+1} of {len(scene_list)}...')
        path = draw_one_picture(scene, i)
        picture_paths.append(path)
        time.sleep(2)  # wait 2 seconds between each request to be polite

    return picture_paths
