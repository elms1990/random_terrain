from PIL import Image

from heightmaps.sparks import Sparks
from heightmaps.terrain.terrain_converter import TerrainConverter

if __name__ == '__main__':
    params = { 'w': 32, 'h': 32 }
    terrainParams = { 'initialScatter': 'auto', 'landProb': 0.77 }
    sparks = Sparks(**params)
    terrain = sparks.generateTerrain(**terrainParams)

    im = Image.new('RGB', (params['w'], params['h']))
    px = im.load()
    converter = TerrainConverter()
    converter.add(0, 0.01, 'water', (0, 255, 0))
    converter.add(0.99, 1.01, 'water', (0, 0, 255))
    for y in xrange(params['h']):
        for x in xrange(params['w']):
            t, v = converter.get(terrain[y, x])
            px[y,x] = v

    im.save('terrain_sparks_%d_%d.png' % (params['w'], params['h']))
