from flask import Flask, send_file, send_from_directory, jsonify
from io import StringIO
import io
from os import listdir
from os.path import isfile, join
import stagger
from PIL import Image
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

onlyfiles = [f for f in listdir("music") if isfile(join("music", f))]

songs = []

for i, file in enumerate(onlyfiles):
    mp3 = stagger.read_tag("music/"+file)
    by_data = mp3[stagger.id3.APIC][0].data
    im = io.BytesIO(by_data)
    songs.append({
        "filename": file,
        "cover": im,
        "artist": mp3.artist,
        "album": mp3.album,
        "title": mp3.title,
        "id": i
    })

def serve_pil_image(pil_img):
    img_io = io.BytesIO()
    pil_img.save(img_io, 'PNG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')

@app.route("/item/")
def index():
    return jsonify({"items": [{k: v for k, v in item.items() if k != "cover"} for item in songs]})

@app.route("/item/<i>/file")
def song(i):
    i = int(i)
    return send_from_directory('music', songs[i]["filename"], mimetype='audio/mpeg')

@app.route("/cover/<i>")
def cover(i):
    i = int(i)
    imageFile = Image.open(songs[i]["cover"])
    return serve_pil_image(imageFile)

if __name__ == "__main__":
    app.run(ssl_context=('cert.pem', 'key.pem'), host="0.0.0.0")