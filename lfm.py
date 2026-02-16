from userbot import catub
import pylast
from userbot.helpers.utils import reply_id
from userbot.sql_helper.globals import gvarstatus
from urllib.parse import quote_plus

API_KEY = gvarstatus("LASTFM_API_KEY")
API_SECRET = gvarstatus("LASTFM_API_SECRET")
USERNAME = gvarstatus("LASTFM_USERNAME")

def get_network():
    if not (API_KEY and API_SECRET and USERNAME):
        return None
    return pylast.LastFMNetwork(
        api_key=API_KEY,
        api_secret=API_SECRET,
        username=USERNAME,
    )

@catub.cat_cmd(
    pattern="np$",
    command=("np", "tools"),
    info={
        "header": "Show currently playing song from Last.fm",
        "usage": "{tr}np",
    },
)
async def now_playing(event):
    reply_to_id = await reply_id(event)
    await event.eor("🎧 **Fetching your current song...**")

    network = get_network()
    if not network:
        return await event.eod(
            "❌ **Last.fm is not configured!**\n\nSet:\n`LASTFM_API_KEY`\n`LASTFM_API_SECRET`\n`LASTFM_USERNAME`",
            5,
        )

    try:
        user = network.get_user(USERNAME)
        track = user.get_now_playing()

        if not track:
            recent = user.get_recent_tracks(limit=1)
            if not recent:
                return await event.eod("😶 **No listening history found!**", 5)

            track = recent[0].track
            status = "⏹ **Last Played**"
        else:
            status = "▶️ **Now Playing**"

        title = track.title
        artist = track.artist
        album_obj = track.get_album()
        album = album_obj.title if album_obj else "Unknown"

        track_url = track.get_url()
        artist_url = track.artist.get_url()

        # Spotify search link (auto opens the song in Spotify app)
        query = quote_plus(f"{title} {artist}")
        spotify_url = f"https://open.spotify.com/search/results/{query}"

        # Try to fetch album art
        cover_url = None
        try:
            if album_obj:
                cover_url = album_obj.get_cover_image()
        except Exception:
            cover_url = None

        caption = f"""
🎵 **Last.fm Status**

{status}

**Track:** __[{title}]__({track_url})
**Artist:** __[{artist}]__({artist_url})
**Album:** `{album}`

🎧 [Listen on Spotify]({spotify_url})

💿 Powered by Last.fm
"""

        if cover_url:
            await event.client.send_file(
                event.chat_id,
                cover_url,
                caption=caption,
                reply_to=reply_to_id,
                link_preview=False,
            )
            await event.delete()
        else:
            await event.eor(caption, link_preview=True)

    except Exception as e:
        await event.eod(f"⚠️ **Error:** `{e}`", 5)


@catub.cat_cmd(
    pattern="lfm$",
    command=("lfm", "tools"),
    info={
        "header": "Show Last.fm profile",
        "usage": "{tr}lastfm",
    },
)
async def lastfm_profile(event):
    reply_to_id = await reply_id(event)
    await event.eor("🔍 **Fetching Last.fm profile...**")

    network = get_network()
    if not network:
        return await event.eod("❌ **Last.fm is not configured!**", 5)

    try:
        user = network.get_user(USERNAME)

        playcount = user.get_playcount()
        profile_url = f"https://www.last.fm/user/{USERNAME}"

        # Try to get profile picture
        avatar_url = None
        try:
            avatar_url = user.get_image()
        except Exception:
            avatar_url = None

        caption = f"""
👤 **Last.fm Profile**

**User:** `{USERNAME}`
**Total Scrobbles:** `{playcount}`

🔗 {profile_url}
"""

        if avatar_url:
            await event.client.send_file(
                event.chat_id,
                avatar_url,
                caption=caption,
                reply_to=reply_to_id,
                link_preview=False,
            )
            await event.delete()
        else:
            await event.eor(caption, link_preview=True)

    except Exception as e:
        await event.eod(f"⚠️ **Error:** `{e}`", 5)