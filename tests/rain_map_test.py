from PIL import Image
import random

from heightmaps.diamond_square import DiamondSquare
from heightmaps.terrain.terrain_converter import TerrainConverter

def digRiver(terrain, riverPos):
    neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    keepDigging = True
    terrain[riverPos[1]][riverPos[0]] = -1
    pX, pY = riverPos[0], riverPos[1]
    h, w = terrain.shape
    while keepDigging:
        paths = []
        random.shuffle(neighbors)
        for n in neighbors:
            pX, pY = pX + n[0], pY + n[1]
            if pX < w and pY < h:
                paths.append((terrain[pY, pX], pX, pY))
        paths.sort()

        foundPath = False
        for p in paths:
            if p[0] > -1 and terrain[p[2], p[1]] > 0.55:
                terrain[p[2], p[1]] = -1
                pX, pY = p[1], p[2]
                foundPath = True
                break

        if not foundPath:
            keepDigging = False

def addRivers(terrain, rainMap):
    rivers = []
    h, w = terrain.shape
    for y in xrange(h):
        for x in xrange(w):
            if rainMap[y][x] >= 0.65 and terrain[y][x] >= 0.73:
                if len(rivers) > 0 and abs(y - rivers[-1][1]) > 5 and abs(x - rivers[-1][0]) > 5:
                    rivers.append((x, y))
                elif len(rivers) == 0:
                    rivers.append((x, y))
  
    for x in rivers:
        digRiver(terrain, x)

if __name__ == '__main__':
    dim = 1024
    params = { 'dim': dim + 1 }
    terrainParams = { 'sampleSize': dim, 'roughness': 1.3 }
    rainParams = { 'sampleSize': dim, 'roughness': 0.5 }
    temperatureParams = { 'sampleSize': 2 * dim, 'roughness': 0.05 }

    diamondSquare = DiamondSquare(**params)    

    print 'Generating terrain...'
    terrain = diamondSquare.generate(**terrainParams)

    print 'Generating rainmap...'
    rain = diamondSquare.generate(**rainParams)

    print 'Generating temperature...'
    temperature = diamondSquare.generate(**temperatureParams)

    converter = TerrainConverter()
    converter.add(-1.0, -0.01, 'river', (75, 69, 255))
    converter.add(0, 0.25, 'deep_water', (0, 0, 140))
    converter.add(0.25, 0.32, 'shallow_water', (0, 0, 255))
    converter.add(0.32, 0.37, 'beach', (237, 242, 90))
    converter.add(0.37, 0.45, 'low_land', (0, 255, 0))
    converter.add(0.45, 0.53, 'land', (0, 255, 0))
    converter.add(0.53, 0.60, 'high_land', (12, 110, 7))
    converter.add(0.60, 0.76, 'mountain', (82, 82, 82))
    converter.add(0.76, 1.0, 'high_mountain', (32, 32, 32))

    rainConverter = TerrainConverter()
    rainConverter.add(0, 0.15, 'arid', (255, 242, 102))
    rainConverter.add(0.15, 0.25, 'semi-arid', (210, 242, 0))
    rainConverter.add(0.25, 0.6, 'moderate', (28, 242, 0))
    rainConverter.add(0.6, 0.85, 'semi-wet', (0, 242, 202))
    rainConverter.add(0.85, 1, 'wet', (0, 36, 242))

    temperatureConverter = TerrainConverter()
    temperatureConverter.add(0, 0.15, 'polar', (255, 255, 255))
    temperatureConverter.add(0.15, 0.35, 'cold', (189, 199, 255))
    temperatureConverter.add(0.35, 0.6, 'moderate', (230, 136, 255))
    temperatureConverter.add(0.6, 0.85, 'warm', (255, 97, 118))
    temperatureConverter.add(0.85, 1, 'very hot', (181, 9, 32))

    biomeDesert = (184, 171, 0)
    biomeTundra = (255, 255, 255)
    biomeRainForest = (1, 74, 12)
    biomeSwamp = (160, 0, 166)
    biomeGrass = (0, 255, 0)
    biomeSavanna = (196, 108, 8)
    biomeWasteland = (130, 72, 5)
    biomePolarDesert = (252, 158, 255)

    terrainImage = Image.new('RGB', (params['dim'], params['dim']))
    biomeImage = Image.new('RGB', (params['dim'], params['dim']))
    rainImage = Image.new('RGB', (params['dim'], params['dim']))
    temperatureImage = Image.new('RGB', (params['dim'], params['dim']))
    bPx = biomeImage.load()
    tPx = terrainImage.load()
    rPx = rainImage.load()
    tmpPx = temperatureImage.load()
    for y in xrange(params['dim']):
        for x in xrange(params['dim']):
            tT, vT = converter.get(terrain[y, x])
            tR, vR = rainConverter.get(rain[y, x])
            tTmp, vTmp = temperatureConverter.get(temperature[y, x])

            if tTmp == 'polar':
                if tR == 'arid' or tR == 'semi-arid':
                    bPx[y, x] = biomePolarDesert
                else:
                    bPx[y, x] = biomeTundra
            elif tTmp == 'warm':
                if tR == 'wet':
                    bPx[y, x] = biomeSwamp
                elif tR == 'semi-wet':
                    bPx[y, x] = biomeGrass
                elif tR == 'moderate':
                    bPx[y, x] = biomeGrass
                elif tR == 'semi-arid':
                    bPx[y, x] = biomeSavanna
                else:
                    bPx[y, x] = biomeWasteland
            elif tTmp == 'very hot':
                if tR == 'arid':
                    bPx[y, x] = biomeDesert
                elif tR == 'semi-arid':
                    bPx[y, x] = biomeWasteland
                elif tR == 'moderate':
                    bPx[y, x] = biomeSavanna
                elif tR == 'semi-wet':
                    bPx[y, x] = biomeSavanna
                elif tR == 'wet':
                    bPx[y, x] = biomeRainForest
            else:
                bPx[y, x] = biomeGrass

            tPx[y, x] = vT
            if terrain[y, x] >= 0.32:
                rPx[y, x] = vR
                tmpPx[y, x] = vTmp
            else:
                bPx[y, x] = (0, 0, 0)
                rPx[y, x] = (0, 0, 0)
                tmpPx[y, x] = (0, 0, 0)

    biomeImage.save('biome_rain_map_%d_%d.png' % (params['dim'], params['dim']))
    terrainImage.save('terrain_rain_map_%d_%d.png' % (params['dim'], params['dim']))
    rainImage.save('rain_rain_map_%d_%d.png' % (params['dim'], params['dim']))
    temperatureImage.save('temperature_rain_map_%d_%d.png' % (params['dim'], params['dim']))
