from PIL import Image, ImageFilter

from heightmaps.hills import Hills
from heightmaps.terrain.terrain_converter import TerrainConverter

if __name__ == '__main__':
    params = { 'w': 256, 'h': 256 }
    terrainParams = { 'minRadius': 12, 'maxRadius': 13, 'iterations': 'auto' }
    hills = Hills(**params)
    terrain = hills.generate(**terrainParams)

    im = Image.new('RGB', (params['w'], params['h']))
    px = im.load()
    converter = TerrainConverter()
    converter.add(0, 0.42, 'deep_water', (0, 0, 140))
    converter.add(0.42, 0.55, 'shallow_water', (0, 0, 255))
    converter.add(0.55, 0.62, 'beach', (237, 242, 90))
    converter.add(0.62, 0.73, 'land', (0, 255, 0))
    converter.add(0.73, 0.89, 'mountains', (82, 82, 82))
    converter.add(0.89, 1.00, 'high_mountains', (38, 38, 38))
    for y in xrange(params['h']):
        for x in xrange(params['w']):
            t, v = converter.get(terrain[y, x])
            px[y, x] = v

    im.save('terrain_hills_%d_%d.png' % (params['w'], params['h']))
