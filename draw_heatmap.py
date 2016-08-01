from PIL import Image
import sys
import re
import math
import json
import numpy as np
from scipy.interpolate import griddata

# Set boundaries in sample_distances.py
from sample_distances import MAX_LAT, MAX_LON, MIN_LAT, MIN_LON

# Define image resolution (eg. 1000x1000 is good, but very slow)
MAX_X = 1000
MAX_Y = 1000

DRAW_DOTS = True

colors = [
    (255, 0, 0),
    (255, 127, 0),
    (255, 208, 0),
    (255, 240, 0),
    (255, 255, 0),
    (218, 255, 0),
    (176, 255, 0),
    (128, 255, 0),
    (0, 255, 0),
    (0, 240, 255),
    (0, 213, 255),
    (0, 171, 255),
    (0, 127, 255),
]

buckets = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]
buckets.reverse()


def ll_to_01(lat, lon):
    return np.array([(lon - MIN_LON) / (MAX_LON - MIN_LON), 1.0 - (lat - MIN_LAT) / (MAX_LAT - MIN_LAT)])

def ll_to_pixel(lat, lon):
    return (ll_to_01(lat, lon) * [MAX_X, MAX_Y]).astype(np.int32)

def load_data(sample_file):
    raw = []
    with open(sample_file) as inf:
        for line in inf:
            if not len(line.strip()):
                continue

            lat, lon, timestamp, time = re.split(r'\t|,', line.strip())
            raw.append((float(time) / 60.0, float(lat), float(lon)))
    return raw


def color(val, buckets):
    if val is None:
        return 0, 0, 0, 0

    for threshold, color in zip(buckets, colors):
        if val > threshold:
            return color
    return 0, 0, 0, 0


def start(file_name):
    print "Loading data..."
    all_data = load_data(file_name)
    n_val = int(len(all_data) * 0.1)
    train = all_data[n_val:]
    val = all_data[:n_val]

    print "Interpolating..."
    grid_x, grid_y = np.mgrid[0:MAX_X, 0:MAX_Y]
    points = np.array([ll_to_pixel(lat, lon) for _, lat, lon in train])
    values = np.array([v for v, _, _ in train])
    grid = griddata(points, values, (grid_x, grid_y), method='linear')

    # Validate
    error = []
    for gt, lat, lon in val:
        x, y = ll_to_pixel(lat, lon)
        z = grid[x, y]
        if not np.isnan(z):
            # Some points are out of interpolation area. Exclude those.
            error.append((gt - grid[x, y]) ** 2)
    rmse = np.sqrt(np.mean(error))
    print 'RMSE (min): %.2f' % rmse

    # Color regions by time
    I = Image.new('RGBA', (MAX_X, MAX_Y))
    IM = I.load()
    for x in range(MAX_X):
        for y in range(MAX_Y):
            IM[x, y] = color(grid[x, y], buckets)

    if DRAW_DOTS:
        for _, lat, lon in all_data:
            x, y = ll_to_pixel(lat, lon)
            IM[int(x), int(y)] = (0, 0, 0)

    out_fname = str(MAX_X)
    I.save(out_fname + ".png", "PNG")
    with open(out_fname + ".metadata.json", "w") as outf:
        outf.write(json.dumps({
            "buckets": buckets,
            "colors": colors,
            "rmse" : rmse,
            "n": len(train)}))


if __name__ == "__main__":
    start('samples.txt')