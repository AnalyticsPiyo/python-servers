# memo
# del flask.session['名前']
from flask import Flask, render_template, request, make_response, jsonify
from flask_httpauth import HTTPBasicAuth
from flask_bootstrap import Bootstrap
from google.cloud import videointelligence, storage
import os

# portはIBM Cloud環境から割り当てられたものを利用
# if os.getenv('VCAP_APP_PORT'):
# #    import metrics_tracker_client
# #    # Trackingするなら必要
# #    metrics_tracker_client.track()
#     host = '0.0.0.0'
#     port = port = os.getenv('VCAP_APP_PORT', '8000')
# else:
#     # ローカル用の設定
#     host = '127.0.0.1'
#     port = 5000

users = {
    "****": "****"
}
auth_flask = HTTPBasicAuth()
@auth_flask.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="./VIDEO-INTELLIGENCE-.json"

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print('File {} uploaded to {}.'.format(
        source_file_name,
        destination_blob_name))

#UPLOAD_FOLDER = './uploads/'
UPLOAD_FOLDER = '/'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'UPLOAD_FOLDER'
app.config['SECRET_KEY'] = os.urandom(24)
#app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

""" Detects explicit content from the GCS path to a video. """
video_client = videointelligence.VideoIntelligenceServiceClient()
features = [videointelligence.enums.Feature.EXPLICIT_CONTENT_DETECTION]

@app.route('/')
@auth_flask.login_required
def index():
    return render_template('index.html')

@app.route('/test', methods=['POST'])
def test():
    resultStr = "<br>＜以下、詳細↓＞<br>"
    score = 0
    if 'uploadFile' not in request.files:
        make_response(jsonify({'result':'uploadFile is required.'}))

    a = './'
    file = request.files['uploadFile']
    file.save(a + file.filename)
    upload_blob('video-piyo', a + file.filename, file.filename)

    videoPath = 'gs://*******/' + file.filename

    operation = video_client.annotate_video(videoPath, features=features)
    print('\nProcessing video for explicit content annotations:')
    result = operation.result(timeout=90)
    print('\nFinished processing.')
    likely_string = ("判別できません", "健全", "ちょっと怪しい", "どちらともいえない",
                 "ちょっとエロい", "完全にエロです")

    i = 0
    for frame in result.annotation_results[0].explicit_annotation.frames:
        frame_time = frame.time_offset.seconds + frame.time_offset.nanos / 1e9
        resultStr = resultStr + 'Time: {}s'.format(frame_time) + '<br>'
        resultStr = resultStr + '　　Reslut: {}'.format(
            likely_string[frame.pornography_likelihood])  + '<br>'
        if int(frame.pornography_likelihood) == 0:
            score = int(score) + int(frame.pornography_likelihood)
        else:
            score = int(score) + int(frame.pornography_likelihood) - 1
        i = i + 1
    scorePer = int(score) / (int(i) * 4) * 100
    headStr = "<H1>結果は・・・</H1>"
    scorePerStr = "アダルトコンテンツ度：" + str(scorePer) + "%です！！<br>"
    topLink = '<a href = "https://piyo-video.mybluemix.net/">TOPページへ戻る</a><br>'
    os.remove(a + file.filename)

    return headStr + scorePerStr + topLink + resultStr

if __name__ == '__main__':
    app.debug = True
    # app.run(host=host, port=int(port))
    app.run(host='127.0.0.1', port=8080, debug=True)

