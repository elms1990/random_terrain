from PIL import Image

from heightmaps.value_noise import ValueNoise
from heightmaps.terrain.terrain_converter import TerrainConverter

if __name__ == '__main__':
    params = { 'w': 128, 'h': 128 }
    terrainParams = { 'smoothFactor': 1, 'gaussianSmooth': 1.5, 'levels': 10 }

    valueNoise = ValueNoise(**params)    
    terrain = valueNoise.generateTerrain(**terrainParams)

    im = Image.new('RGB', (params['w'], params['h']))
    px = im.load()
    converter = TerrainConverter()
    converter.add(0, 0.25, 'deep_water', (0, 0, 140))
    converter.add(0.25, 0.32, 'shallow_water', (0, 0, 255))
    converter.add(0.32, 0.37, 'beach', (237, 242, 90))
    converter.add(0.37, 0.60, 'land', (0, 255, 0))
    converter.add(0.60, 0.76, 'mountain', (82, 82, 82))
    converter.add(0.76, 1.0, 'high_mountain', (32, 32, 32))
    for y in xrange(params['h']):
        for x in xrange(params['w']):
            t, v = converter.get(terrain[y, x])
            px[y, x] = v

    im.save('terrain_value_noise_%d_%d.png' % (params['w'], params['h']))
