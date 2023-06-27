import json
import pygame

class Tile:
    def __init__(self, image_path: str, id: str, name: str, width: int, height: int, description=''):
        self.image_path = image_path
        self.name = name
        self.description = description
        self.id = id
        self.width = width
        self.height = height
        self.image = pygame.image.load(image_path)
    
    def reload_image(self):
        self.image = pygame.image.load(self.image_path)
class Engine:
    def __init__(self, width: int, height: int, title: str, background_color=(255, 255, 255)):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.background_color = background_color
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.tiles = []
        self.layers = []
        self.camera_x = 115
        self.camera_y = 320
    
    def create_layer(self, tile_coords):
        self.layers.append(tile_coords)
    
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.move_camera(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        self.move_camera(1, 0)
                    elif event.key == pygame.K_UP:
                        self.move_camera(0, -1)
                    elif event.key == pygame.K_DOWN:
                        self.move_camera(0, 1)
            
            pygame.draw.rect(self.screen, self.background_color, pygame.Rect(0, 0, self.width, self.height))

            tile_width = self.tiles[0].width
            tile_height = self.tiles[0].height

            for i, layer in enumerate(self.layers):
                for x, row in enumerate(layer):
                    for y, tile_id in enumerate(row):
                        tile = None
                        for l in self.tiles:
                            if l.id == tile_id:
                                tile = l
                                break
                        if tile is not None:
                            screen_x = ((x - y) * tile_width / 2) + (self.width / 2) - (len(layer[0]) * tile_width / 4) + self.camera_x
                            screen_y = (((x + y) * tile_height / 2) - 12 * i) + self.camera_y
                            self.screen.blit(tile.image, (screen_x, screen_y))

            pygame.display.flip()
            self.clock.tick(60)
    
    def add_tile(self, tile_object: Tile):
        if tile_object not in self.tiles:
            self.tiles.append(tile_object)
        else:
            print('ERROR: Duplicate tile')
    
    def move_camera(self, dx, dy):
        self.camera_x += dx * self.tiles[0].width
        self.camera_y += dy * self.tiles[0].height

engine = Engine(600, 600, 'Isometric Game', background_color=(135, 206, 235))

# Load JSON data from file
with open('map.json') as json_file:
    data = json.load(json_file)

# Iterate through the layers in the JSON data
for layer_data in data['layers']:
    tiles = layer_data['tiles']
    repeat = layer_data['repeat']

    # Repeat the layer multiple times
    for _ in range(repeat):
        engine.create_layer(tiles)

# Load JSON data from file
with open('tile_sets.json') as json_file:
    data = json.load(json_file)

# Iterate through the layers in the JSON data
for tile_set in data:
    for tile_data in data[tile_set]:
        tile = Tile('./tiles/' + tile_set + '/' + tile_data['id'] + '.png', tile_set + ':' + tile_data['id'], tile_data['name'], tile_data['width'], tile_data['height'])
        engine.add_tile(tile)

# Run the game engine
engine.run()
