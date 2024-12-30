import matplotlib.pyplot as plt
import numpy as np
import math
import urllib.request as urllib2
from io import BytesIO
from PIL import Image

def deg2num(lat_deg, lon_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
    return (xtile, ytile)
  
def num2deg(xtile, ytile, zoom):
    n = 2.0 ** zoom
    lon_deg = xtile / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
    lat_deg = math.degrees(lat_rad)
    return (lat_deg, lon_deg)
  
def get_image_cluster(lat_deg, lon_deg, delta_lat, delta_long, zoom):
    smurl = r"http://a.tile.openstreetmap.org/{0}/{1}/{2}.png"
    xmin, ymax = deg2num(lat_deg, lon_deg, zoom)
    xmax, ymin = deg2num(lat_deg + delta_lat, lon_deg + delta_long, zoom)
    
    cluster = Image.new('RGB', ((xmax - xmin + 1) * 256 - 1, (ymax - ymin + 1) * 256 - 1)) 
    for xtile in range(xmin, xmax + 1):
        for ytile in range(ymin, ymax + 1):
            try:
                imgurl = smurl.format(zoom, xtile, ytile)
                print("Opening: " + imgurl)
                imgstr = urllib2.urlopen(imgurl).read()
                tile = Image.open(BytesIO(imgstr))
                cluster.paste(tile, box=((xtile - xmin) * 256, (ytile - ymin) * 256))
            except Exception as e: 
                print(f"va te faire foutre fucking user: {e}")

    return cluster
    
def main():
    a = get_image_cluster(38.5, -77.04, 0.02, 0.05, 13)
    fig = plt.figure()
    fig.patch.set_facecolor('white')
    plt.imshow(np.asarray(a))
    plt.axis('off')
    plt.show()
