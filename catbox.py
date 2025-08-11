import os
import requests
from userbot import catub
from catbox import CatboxUploader
from userbot.core.managers import edit_delete, edit_or_reply
from userbot.sql_helper.globals import addgvar, gvarstatus

plugin_category = "extra"

userhash = gvarstatus("CATBOX") if gvarstatus("CATBOX") else None
cat_uploader = CatboxUploader(userhash=userhash)

def upload_to_envs(file_path):
    url = 'https://envs.sh'
    with open(file_path, 'rb') as f:
        files = {
            'file': f
        }
        response = requests.post(url, files=files)
        if response.status_code == 200:
            response_text = response.text
            url_ = response_text.split(' ')[-1]
            return url_
        else:
            return f"Error: {response.status_code} - {response.text}"
            
@catub.cat_cmd(
    pattern="catb ?(.*)$",
    command=("catb", plugin_category),
    info={
        "header": "Catbox Image Uploader",
        "description": "Upload any image to catbox or envs",
        "usage": [
            "{tr}catb <reply to a media>",
            "{tr}catb e <reply to a media> - To upload in envs",
        ],
    },
)
async def catbox(event):
    reply = await event.get_reply_message()
    flag = event.pattern_match.group(1)
    if event.is_reply and reply.media:
        kk = await edit_or_reply(event, "`Uploading...`")
        file_path = await reply.download_media()
        
        if flag == "e":
            upload_link = upload_to_envs(file_path)
            server = "Envs"
        else:
            upload_link = cat_uploader.upload_file(file_path)
            server = "Catbox"
        
        if upload_link and not upload_link.startswith("Error"):
            await kk.edit(f"✘ **File Uploaded to {server}!** \n>> __{upload_link}__")
        else:
            await kk.edit(f"__Failed to upload the file: {upload_link}__")
        
        os.remove(file_path)  # Clean up
    else:
        await edit_delete(event, "__Please send a file along with the command.__")
