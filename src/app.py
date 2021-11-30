from color_map import plotMaps
from rover import PredictPath

if __name__ == '__main__':
    origin = 1000,2000
    destination = 5000, 2000

    rover = PredictPath(origin,destination)

    try:
        path = rover.result.path()
    except AttributeError:
        path = None
    plotMaps(path)
