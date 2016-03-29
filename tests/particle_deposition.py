from PIL import Image
import random

from heightmaps.utils.filters import meanFilter
from heightmaps.particle_deposition import ParticleDeposition
from heightmaps.terrain.terrain_converter import TerrainConverter

def digRiver(terrain, riverPos):
    neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    keepDigging = True
    terrain[riverPos[1]][riverPos[0]] = -1
    pX, pY = riverPos[0], riverPos[1]
    while keepDigging:
        paths = []
        for n in neighbors:
            pX, pY = pX + n[0], pY + n[1]
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

def generateImprovedTerrain(obj, w, h, dropPoints, maxStabilityRadius, minParticles, maxParticles,
        iterations):
    terrain = obj.generateTerrain(dropPoints, maxStabilityRadius, minParticles, maxParticles,
            iterations)
    rainMap = obj.generateTerrain(800, 3, minParticles, maxParticles,
            iterations)
    rainMap = meanFilter(rainMap, 5)

    rivers = []
    for y in xrange(h):
        for x in xrange(w):
            if rainMap[y][x] >= 0.65 and terrain[y][x] >= 0.73:
                if len(rivers) > 0 and abs(y - rivers[-1][1]) > 5 and abs(x - rivers[-1][0]) > 5:
                    rivers.append((x, y))
                elif len(rivers) == 0:
                    rivers.append((x, y))
  
    for x in rivers:
        digRiver(terrain, x)

    snowyW = int(0.12 * w)
    for y in xrange(h):
        for x in xrange(0, snowyW + 1):
            if x == snowyW:
                if random.uniform(0, 1) < 0.50 and terrain[y, x] > 0.55 and terrain[y, x] <= 0.73:                    
                    terrain[y, x] = -2
            elif terrain[y, x] > 0.55 and terrain[y, x] <= 0.73:
                terrain[y, x] = -2

    return terrain

if __name__ == '__main__':
    params = { 'w': 128, 'h': 128 }
    terrainParams = { 'dropPoints': 2750, 'maxStabilityRadius': 5,
        'minParticles': 21, 'maxParticles': 43, 'iterations': 5 }
    terrainParams.update(params)

    particleDeposition = ParticleDeposition(**params)
    terrainParams['obj'] = particleDeposition
    terrain = generateImprovedTerrain(**terrainParams)

    im = Image.new('RGB', (params['w'], params['h']))
    px = im.load()
    converter = TerrainConverter()
    converter.add(-1.0, -0.01, 'river', (43, 227, 202))
    converter.add(-2.01, -1.01, 'frost', (255, 255, 255))
    converter.add(0, 0.42, 'deep_water', (0, 0, 140))
    converter.add(0.42, 0.55, 'shallow_water', (0, 0, 255))
    converter.add(0.55, 0.62, 'beach', (237, 242, 90))
    converter.add(0.62, 0.73, 'land', (0, 255, 0))
    converter.add(0.73, 0.89, 'mountain', (82, 82, 82))
    converter.add(0.89, 1.0, 'high_mountain', (32, 32, 32))
    for y in xrange(params['h']):
        for x in xrange(params['w']):
            t, v = converter.get(terrain[y, x])
            px[y, x] = v

    im.save('terrain_particle_deposition_%d_%d.png' % (params['w'], params['h']))
