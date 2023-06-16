import numpy


from .Definitions import MAP_SIZE

def noise(seed,x,y) :
    x = (x >> seed//2) ^ x
    y = (y >> seed//2) ^ y
    noisedX = (x * (x * x * 60493 + 19990303) + 1376312589) & 0x7fffffff
    noisedY = (y * (y * y * 60493 + 19990303) + 1376312589) & 0x7fffffff
    return 1.0 - (noisedX / 1073741824.0)

def randomMap() :
    from scipy.ndimage.interpolation import zoom
    #generation aleatoire : distribution uniforme de taille 4x4
    arr = numpy.random.uniform(size=(4,4))
    arr[0][0] = 0
    arr[0][3] = 0
    arr[3][0] = 0
    arr[3][3] = 0
    #zoome sur l'array d'un facteur 6
    arr = zoom(arr, MAP_SIZE/4)
    arr = arr > 0.9
    #if true : - . if false : #
    arr = numpy.where(arr, 'water', 'grass')
    return arr

print(randomMap())