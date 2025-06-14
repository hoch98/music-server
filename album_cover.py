from PIL import Image
import stagger
import io
from os import listdir
from os.path import isfile, join
onlyfiles = [f for f in listdir("music") if isfile(join("music", f))]

songs = {

}

mp3 = stagger.read_tag("music/"+onlyfiles[0])
by_data = mp3[stagger.id3.APIC][0].data
im = io.BytesIO(by_data)
imageFile = Image.open(im)


imageFile.show()