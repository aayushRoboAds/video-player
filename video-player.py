from flask import Flask, send_from_directory, render_template_string, request, jsonify
import os

app = Flask(__name__)

VIDEO_PATH = 'D:/SanyalTest-main/backend/video/media'
current_video = {'filename': 'Marina-exterior-video.mp4'}  # Default video


@app.route('/')
def home():
    video_file = current_video['filename']
    return render_template_string(f"""
    <html>
    <head>
        <title>Fullscreen Video</title>
        <style>
            html, body {{
                margin: 0;
                padding: 0;
                height: 100%;
                background-color: black;
            }}
            video {{
                width: 100vw;
                height: 100vh;
                object-fit: cover;
            }}
        </style>
    </head>
    <body>
        <video id="videoPlayer" autoplay loop muted playsinline oncanplay="this.requestFullscreen();">
            <source src="/video/{video_file}" type="video/mp4">
            Your browser does not support the video tag.
        </video>

        <script>
            let lastVideo = "{video_file}";
            setInterval(async () => {{
                const res = await fetch("/status");
                const data = await res.json();
                if (data.filename !== lastVideo) {{
                    location.reload();  // Reload page when video changes
                }}
            }}, 1000);  // Poll every 3 seconds
        </script>
    </body>
    </html>
    """)


@app.route('/video/<filename>')
def serve_video(filename):
    return send_from_directory(VIDEO_PATH, filename)


@app.route('/play', methods=['POST'])
def play():
    video_name = request.args.get('filename')
    full_path = os.path.join(VIDEO_PATH, video_name)
    if not os.path.isfile(full_path):
        return jsonify({'error': 'File not found'}), 404
    current_video['filename'] = video_name
    return jsonify({'status': 'OK', 'playing': video_name})


@app.route('/status')
def status():
    return jsonify(current_video)


if __name__ == '__main__':
    app.run(host='localhost', port=5000)
