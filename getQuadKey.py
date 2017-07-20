
import math


def Clip(n, minValue, maxValue):
    return min(max(n, minValue), maxValue);


def LatLongToPixelXY( latitude,  longitude,  mapSize):
    x = (longitude+180)/360
    sinLatitude = math.sin(latitude * math.pi / 180)
    y = 0.5 - math.log((1+sinLatitude) / (1- sinLatitude)) / (4*math.pi)
    pixelX = int(Clip(x * mapSize + 0.5, 0, mapSize - 1));
    pixelY = int(Clip(y * mapSize + 0.5, 0, mapSize - 1));
    return [pixelX, pixelY]

def pixelXYTotileXY(pixelArray):
    x = pixelArray[0]
    y = pixelArray[1]
    tilex = int(x / 256)
    tiley = int(y / 256)
    return [tilex, tiley]

def tilexyztoquad(x,y,z):
    quad = ""
    for i in range(z, 0, -1):
        digit = '0'
        mask = (1 << (i - 1)) & 0xffffffff  # python int is not size-fixed

        if (x & mask) != 0:
            digit = chr(ord(digit) + 1)
        if (y & mask) != 0:
            digit = chr(ord(digit) + 1)
            digit = chr(ord(digit) + 1)
        quad += digit
    return quad

def polyToTiles(x1, y1, x2, y2, level):
    xmin = x1;
    tiles = []
    while(y1> y2-1):
        xrow = []
        x1 = xmin
        while(x1< x2+1):
            xrow.append(tilexyztoquad(x1,y1,level))
            x1 += 1
        tiles.append(xrow)
        y1 -= 1
    return tiles