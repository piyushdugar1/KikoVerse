import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

def connect_to_youtube():
    # Connect to YouTube using our secret keys — like showing an ID card at the door
    credentials = Credentials(
        token=None,
        refresh_token=os.environ['YT_REFRESH_TOKEN'],
        client_id=os.environ['YT_CLIENT_ID'],
        client_secret=os.environ['YT_CLIENT_SECRET'],
        token_uri='https://oauth2.googleapis.com/token',
        scopes=['https://www.googleapis.com/auth/youtube.upload'],
    )
    return build('youtube', 'v3', credentials=credentials)

def post_to_youtube(video_file, script, topic):
    youtube = connect_to_youtube()

    # Fill in the video details — like filling in a form before posting a letter
    video_details = {
        'snippet': {
            'title':       script['title'][:100],
            'description': f'{script["title"]}\n\n#GappuVerse #KidsFacts #Shorts',
            'tags':        ['GappuVerse', 'kids facts', 'fun facts', 'Shorts', 'Gappu', topic],
            'categoryId':  '27',  # 27 = Education on YouTube
        },
        'status': {
            'privacyStatus': 'public',
            'madeForKids':   True,
        },
    }

    # Load the video file and get it ready to send
    media = MediaFileUpload(video_file, mimetype='video/mp4', resumable=True)

    # Actually send everything to YouTube — like clicking the Upload button!
    request  = youtube.videos().insert(part='snippet,status',
                                       body=video_details, media_body=media)
    response = request.execute()

    video_id = response['id']
    print(f'Posted! Watch at: https://youtube.com/shorts/{video_id}')
    return video_id
