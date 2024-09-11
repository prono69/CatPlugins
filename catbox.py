import os
import requests
from . import catub, eor, eod

plugin_category = "extra"

def upload_to_catbox(file_path):
    url = 'https://catbox.moe/user/api.php'
    data = {
        'reqtype': 'fileupload',
        'userhash': ''
    }

    with open(file_path, 'rb') as f:
        files = {
            'fileToUpload': f
        }
        response = requests.post(url, data=data, files=files)
        
        if response.status_code == 200:
            return response.text
        else:
            return None

@catub.cat_cmd(
    pattern="catb ?(.*)",
    command=("catb", plugin_category),
    info={
        "header": "Convert media to ascii art.",
        "description": "Reply to any media files like pic, gif, sticker, video and it will convert into ascii.",
        "usage": [
            "{tr}catb <reply to a media>",
        ],
    },
)
async def handler(event):
    # Check if there's an attached file to the message
    reply = await event.get_reply_message()
    if event.is_reply and reply.media:
        file_path = await reply.download_media()
        kk = await eor(event, "`Uploading...`")
        
        upload_link = upload_to_catbox(file_path)
        if upload_link:
            await kk.edit(f"✘ **File Uploaded to Catbox!** \n>> __{upload_link}__")
        else:
            await kk.edit("__Failed to upload the file to Catbox.__")
        
        # Optionally delete the downloaded file to clean up
        os.remove(file_path)
    else:
        await eod(event, "__Please send a file along with the command.__")
