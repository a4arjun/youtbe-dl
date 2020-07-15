from flask import Flask, render_template, request, send_file
import youtube_dl
import sys


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    def_value = '0'
    data = ''
    data = request.args.get('url', def_value)
    file_name = 'download'
    try:
        with youtube_dl.YoutubeDL({}) as prep:
            info = prep.extract_info(data, download=False)


        params = {
            'format': 'bestaudio/best',
            'outtmpl': 'dwl/' + info['title'].replace('|', '_').replace(' ', '_') + '.%(ext)s',
            'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
        }

        with youtube_dl.YoutubeDL(params) as ydl:
            download = ydl.extract_info(data)

        return send_file('dwl/' + info['title'].replace('|', '_').replace(' ', '_') + '.mp3', as_attachment=True, attachment_filename=info['title'].replace('|', '_') + '.mp3', )

    except youtube_dl.utils.DownloadError:
        return render_template('index.html')



if __name__ == '__main__':
    app.debug = True
    app.run()