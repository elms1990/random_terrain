from PIL import Image

from heightmaps.diamond_square import DiamondSquare
from heightmaps.terrain.terrain_converter import TerrainConverter

if __name__ == '__main__':
    params = { 'dim': 1025 }
    terrainParams = { 'sampleSize': 1024 }

    diamondSquare = DiamondSquare(**params)    
    terrain = diamondSquare.generate(**terrainParams)

    im = Image.new('RGB', (params['dim'], params['dim']))
    px = im.load()
    converter = TerrainConverter()
    converter.add(0, 0.25, 'deep_water', (0, 0, 140))
    converter.add(0.25, 0.32, 'shallow_water', (0, 0, 255))
    converter.add(0.32, 0.37, 'beach', (237, 242, 90))
    converter.add(0.37, 0.60, 'land', (0, 255, 0))
    converter.add(0.60, 0.76, 'mountain', (82, 82, 82))
    converter.add(0.76, 1.0, 'high_mountain', (32, 32, 32))
    for y in xrange(params['dim']):
        for x in xrange(params['dim']):
            t, v = converter.get(terrain[y, x])
            px[y, x] = v

    im.save('terrain_diamond_square_%d_%d.png' % (params['dim'], params['dim']))
