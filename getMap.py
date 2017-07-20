import sys
import urllib.request
import json
from PIL import Image
import io
from getQuadKey import Clip
from getQuadKey import LatLongToPixelXY as l2p
from getQuadKey import pixelXYTotileXY as p2t
from getQuadKey import tilexyztoquad as t2q
from getQuadKey import polyToTiles as bondingBox
level = 23 #default value
pixel1 = None
tile1 = None

print("Bounding box is formed using 2 pairs of Longitudes and Latitudes")
print(" Latitude 1 = ")
lat1 = sys.stdin.readline()[:-1]
#lat1 = 41.879769
lat1 = float(lat1)
print("Longitutde 1 = ")
lon1 = sys.stdin.readline()[:-1]
#lon1 = -87.643842
lon1 = float(lon1)
print("Latitude 2 = ")
lat2 = sys.stdin.readline()[:-1]
#lat2 = 41.879981
lat2 = float(lat2)
print("Longitutde 2 = ")
lon2 = sys.stdin.readline()[:-1]
#lon2 = -87.643715
lon2 = float(lon2)


lat1 = Clip(lat1,-85.05112878, 85.05112878)
lat2 = Clip(lat2,-85.05112878, 85.05112878)
lon1 = Clip(lon1,-180, 180)
lon2 = Clip(lon2,-180, 180)
if lat1 >= lat2:
    print('invalid latitude and longitude. ')
    exit()


def isSameImage(im1, im2):
    if im1.size != im2.size:
        return False
    for i in range(0, im1.height):
        for j in range(0, im1.width):
            if im1.getpixel((j, i)) != im2.getpixel((j, i)):
                return False
    return True

while level > 0:
    mapsize = 256 * 2 ** level
    pixel1 = l2p(lat1, lon1, mapsize)
    tile1 = p2t(pixel1)
    quad = t2q(tile1[0], tile1[1], level)
    request = "http://t0.tiles.virtualearth.net/tiles/a%s.jpeg?g=854&mkt=en-US&token=Anz84uRE1RULeLwuJ0qKu5amcu5rugRXy1vKc27wUaKVyIv1SVZrUjqaOfXJJoI0"%quad
    url = urllib.request.urlopen(request)
    testImage = Image.open(io.BytesIO(url.read()))
    if level == 23:
        urllib.request.urlretrieve(request, "scrapImage.jpeg")
    scrapImage = Image.open('scrapImage.jpeg')
    if isSameImage(testImage, scrapImage):
        print('Not level %d ' % level)
    else:
        break
    level -= 1

if level == 0:
    print('no available level in the bounding area. ')
    exit()


pixel2 = l2p(lat2, lon2, mapsize)
tile2 = p2t(pixel2)


quads = bondingBox(tile1[0], tile1[1], tile2[0], tile2[1], level)


if len(quads) == 0:
    print("no bounding area.")
    exit()


imageHeight = len(quads)
imageWidth = len(quads[0])
total = imageHeight * imageWidth
count = 0
image = Image.new('RGB', (imageWidth * 256, imageHeight * 256))
y = len(quads)
while(y >= 0):
    for x in range(0, len(quads[0])):
        quad = quads[y-1][x]
        request = "http://t0.tiles.virtualearth.net/tiles/a%s.jpeg?g=854&mkt=en-US&token=Anz84uRE1RULeLwuJ0qKu5amcu5rugRXy1vKc27wUaKVyIv1SVZrUjqaOfXJJoI0"%quad
        url = urllib.request.urlopen(request)
        result = url.read()
        count += 1
        if url.getcode() != 200:
            obj = json.loads(result)
            errors = obj["errorDetails"]
            for string in errors:
                print(string)
        else:
            subImage = Image.open(io.BytesIO(result))
            image.paste(subImage, (x * 256, y * 256))
            print("%d/%d" % (y, x))
    y -=1

p2level = 2 ** level
left = pixel1[0] - tile1[0] * 256
upper = pixel2[1] - tile2[1] * 256
width = pixel2[0] - tile1[0] * 256
height = pixel1[1] - tile2[1] * 256
cropImage = image.crop((left, upper, left+width, upper+height))
image.save("ArialImage.jpeg")
cropImage.save("Finalresult.jpeg")
print('Image is saved to ArialImage.jpeg')
print('Image Resolution :', p2level * 256, 'Image tile size:', p2level)
print('Cropped bounding box is saved to Finalresult.jpeg')