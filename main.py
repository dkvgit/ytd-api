from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)


# 👇 Вот сюда вставь
@app.route('/')
def root():
    return "Сервер работает!"


@app.route('/get_link', methods=['POST'])
def get_link():
    try:
        data = request.get_json()
        url = data.get("url")
        format_type = data.get("format", "video")

        if not url:
            return jsonify({"error": "URL is required"}), 400

        ydl_opts = {
            'format': 'bestaudio/best' if format_type == "audio" else 'best',
            'quiet': True,
            'noplaylist': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return jsonify({
                "title": info.get("title"),
                "url": info.get("url"),
                "ext": info.get("ext"),
                "duration": info.get("duration")
            })



    except Exception as e:
        return jsonify({"error": str(e)}), 500





if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

