from flask import Flask, request, jsonify
from googleapiclient.discovery import build
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def format_number(number):
    if number >= 1_000_000:
        return f"{number/1_000_000:.2f}M"
    elif number >= 1_000:
        return f"{number/1_000:.2f}K"
    else:
        return str(number)

def get_channel_details(api_key, channel_name):
    youtube = build('youtube', 'v3', developerKey=api_key)

    # Search for the channel
    search_response = youtube.search().list(
        part='snippet',
        q=channel_name,
        type='channel',
        maxResults=1
    ).execute()

    if not search_response['items']:
        return jsonify({"error": f"No channel found with name: {channel_name}"}), 404

    channel_id = search_response['items'][0]['id']['channelId']

    channels_response = youtube.channels().list(
        part='snippet,brandingSettings,contentDetails,statistics,topicDetails,status',
        id=channel_id
    ).execute()

    if not channels_response['items']:
        return jsonify({"error": f"No channel details found for ID: {channel_id}"}), 404
    channel_details = channels_response['items'][0]
    snippet = channel_details.get('snippet', {})
    branding_settings = channel_details.get('brandingSettings', {})
    statistics = channel_details.get('statistics', {})
    content_details = channel_details.get('contentDetails', {})
    topic_details = channel_details.get('topicDetails', {})
    status = channel_details.get('status', {})
    uploads_playlist_id = content_details.get('relatedPlaylists', {}).get('uploads', 'Not available')
    videos_response = youtube.playlistItems().list(
        part='snippet,contentDetails',
        playlistId=uploads_playlist_id,
        maxResults=800
    ).execute()

    top_videos = []
    for item in videos_response.get('items', []):
        video_snippet = item.get('snippet', {})
        video_content_details = item.get('contentDetails', {})
        video_statistics = youtube.videos().list(
        part='statistics',
        id=video_content_details.get('videoId', 'Not available'),
        ).execute()
        views = int(video_statistics['items'][0]['statistics'].get('viewCount', 0))
        
        video = {
            "title": video_snippet.get('title', 'Unknown'),
            "video_id": video_content_details.get('videoId', 'Not available'),
            "published_date": video_snippet.get('publishedAt', 'Not available'),
            "views": format_number(views)
        }
        top_videos.append(video)

    result = {
        "title": snippet.get('title', 'Unknown'),
        "channel_id": channel_id,
        "subscribers": format_number(int(statistics.get('subscriberCount', 0))),
        "total_views": format_number(int(statistics.get('viewCount', 0))),
        "total_videos": format_number(int(statistics.get('videoCount', 0))),
        "description": snippet.get('description', 'Not available'),
        "published_date": snippet.get('publishedAt', 'Not available'),
        "country": snippet.get('country', 'Not available'),
        "default_language": branding_settings.get('channel', {}).get('defaultLanguage', 'Not available'),
        "channel_keywords": branding_settings.get('channel', {}).get('keywords', 'Not available'),
        "uploads_playlist_id": uploads_playlist_id,
        "top_videos": top_videos,
        "topic_categories": topic_details.get('topicCategories', 'Not available'),
        "privacy_status": status.get('privacyStatus', 'Not available'),
        "upload_status": status.get('uploadStatus', 'Not available')
    }

    return jsonify(result)

@app.route('/get_channel_details', methods=['GET'])
def api_get_channel_details():
    api_key = 'AIzaSyA3yqAaeAM2uUyCBdUD2uwjMnqminDtzcY'  # Replace with your actual API key
    channel_name = request.args.get('channel_name')
    if not channel_name:
        return jsonify({"error": "Channel name is required"}), 400

    return get_channel_details(api_key, channel_name)
if __name__ == '__main__':
    app.run(debug=True)
