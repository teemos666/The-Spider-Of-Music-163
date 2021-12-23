from flask import Flask, render_template, request, url_for, redirect, flash, session, Response
from flask_cors import *

app = Flask(__name__)
fuck = 'what are you fucking doing'
# --------------------------------------------------
# --------------------------------------------------
# --------------------------------------------------

# 音乐搜索
song_name = ''
song_id = ''

@app.route('/search', methods=['GET', 'POST'])
@cross_origin()
def search():
    global song_name
    if request.method == 'POST':
        song = request.form.get('song')
        song_name = song
    return fuck

@app.route('/search_result', methods=['GET', 'POST'])
@cross_origin()
def search_result():
    from utils.MySong import get_song
    return get_song(song_name)

@app.route('/comments', methods=['GET', 'POST'])
@cross_origin()
def comments():
    global song_id
    from utils.MySong import get_comments
    if request.method == 'POST':
        print(request.form)
        id = request.form.get('id')
        song_id = id
        get_comments(id)
    return fuck

@app.route('/comments_result', methods=['GET', 'POST'])
@cross_origin()
def comments_result():
    from utils.MySong import get_comments
    return get_comments(song_id)

@app.route('/wordcloud', methods=['GET', 'POST'])
@cross_origin()
def wordcloud():
    from utils.MyWordcloud import get_cloud
    get_cloud()
    imgPath = 'utils/wordcloud.png'
    mdict = {
        'jpeg': 'image/jpeg',
        'jpg': 'image/jpeg',
        'png': 'image/png',
        'gif': 'image/gif'
    }
    mime = 'image/png'
    with open(imgPath, 'rb') as f:
        image = f.read()
    return Response(image, mimetype=mime)

if __name__ == '__main__':
    app.run(host='0.0.0.0')