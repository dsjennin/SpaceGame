__author__ = 'samhauck'
import pyglet
from pyglet.window import key
import cocos
from cocos import actions, layer, sprite, scene
from cocos.director import director
import cocos.collision_model as cm
import cocos.euclid as eu
import random



def main():

    global keyboard

    #  initialzing the director. the director creates the window for the game
    director.init(width=400, height= 600, autoscale=True, resizable = True)

    #  creating a layer using the cocos2d platform
    #  different layers are used for each aspect of the game, i.e. the main character or background
    game_layer = layer.Layer()

    #creating a Sprite for the main character
    # heroimage = pyglet.resource.image('hero.png')
    # player = HeroShip(heroimage)
    #heroShip.cshape = cm.AARectShape(eu.Vector2(heroShip.position), 32, 32)

    #adding the main character to the 'player_layer' layer
    # game_layer.add(player)

    #initializing the main character's position and velocity
    #heroShip.position = (100, 100)
    #heroShip.velocity = (0, 0)

    #creating a background layer
    background_layer = layer.Layer()
    background = sprite.Sprite('space_wallpaper.jpeg')
    background.position = (200, 300)

    #adding backgound image to background layer
    background_layer.add(background)

    #adding sprites that contain the asteroid images.
    # asteroid_1 = sprite.Sprite('asteroid.png')
    # asteroid_1.cshape = cm.CircleShape(eu.Vector2(asteroid_1.position), 16)
    # asteroid_2 = sprite.Sprite('asteroid_2.png')
    # asteroid_2.cshape = cm.CircleShape(eu.Vector2(asteroid_1.position), 16)

    # asteroid_1.position = (150, 550)
    # asteroid_1.velocity = (0, 1000)
    # asteroid_2.position = (200, 550)
    # asteroid_2.velocity = (100, 25)

    #adding asteroids to game layer
    # game_layer.add(asteroid_1)
    # game_layer.add(asteroid_2)


    #initializing pyglet, which allows for keyboard import for character movement

    keyboard = key.KeyStateHandler()
    director.window.push_handlers(keyboard)

    #assigning the movement class to the heroShip sprite
    # player.do(HeroShipMovement())

    # asteroid_1.do(actions.MoveBy( (0, -600), 4) )
    # asteroid_2.do(actions.MoveBy( (100, -600), 8) )

    game_layer2 = GameLayer()

    main_scene = scene.Scene(background_layer, game_layer, game_layer2)

    director.run(main_scene)


#class for movement of main character
class HeroShipMovement(actions.Move):
    def step(self, dt):
        super(HeroShipMovement, self).step(dt)
        velocity_x = 200 * (keyboard[key.RIGHT] - keyboard[key.LEFT])
        velocity_y = 200 * (keyboard[key.UP] - keyboard[key.DOWN])
        self.target.velocity = (velocity_x, velocity_y)

        #move = self.target.position
        #for move in range(0, 400):
           # move = move + 25
           # self.target.position = move;


class HeroShip(cocos.sprite.Sprite):
    def __init__(self, image):
        super(HeroShip, self).__init__(image)
        self.image = image
        self.position = (100, 100)
        self.velocity = (0,0)
        self.cshape = cm.AARectShape(eu.Vector2(self.position), 32, 32)


class Asteroid(cocos.sprite.Sprite):
    def __init__(self, image, position):
        super(Asteroid, self).__init__(image)
        self.image = image
        self.position = position
        self.velocity = (0,0)
        self.cshape = cm.CircleShape(eu.Vector2(self.position), 16)


class GameLayer(cocos.layer.Layer):

    is_event_handler = True

    def __init__(self):
        super(GameLayer, self).__init__()
        self.add_hero()
        self.add_asteroids()
        # self.add_boss()
        self.CollMan = cm.CollisionManagerBruteForce()
        self.schedule(self.update)


    def add_hero(self):
        heroImage = pyglet.resource.image('hero.png')
        # hero = cocos.sprite.Sprite(heroImage)
        self.hero = HeroShip(heroImage)
        # hero.position = (150, 150)
        self.hero.do(HeroShipMovement())
        self.add(self.hero)

    #def add_boss(self):
        #bossImage = pyglet.resource.image('boss.png')
        #boss = cocos.sprite.Sprite(bossImage)
        #boss.position = (300, 200)
        #self.add(boss)

    def add_asteroids(self):
        #creating an array that stores the two images for the asteroid sprite
        asteroid_pics = [pyglet.resource.image('asteroid.png'), pyglet.resource.image('asteroid_2.png')]
        asteroid_x = random.randrange(10, 390)
        asterPosition = (asteroid_x, 610)
        asterVelocity = (0, 1000)

        #RNG for choosing an image when the sprite is created
        randomPic = random.randrange(0, 1)
        self.asteroid = Asteroid(asteroid_pics[randomPic], asterPosition)

        self.add(self.asteroid)

        #creating a random number for the speed of the asteroid
        randomAsteroidSpeed = random.randrange(2, 5)

        self.asteroid.do(actions.MoveBy((0, -700), randomAsteroidSpeed))


    def update(self, dt):
        self.CollMan.clear()
        #self.CollMan.add(self.hero)
        #self.CollMan.add(self.asteroid)
        collide = self.CollMan.they_collide(self.hero, self.asteroid)
        if collide == True:
                label = cocos.text.Label('Hello, World!',
                                 font_name='Times New Roman',
                                 font_size=32,
                                 anchor_x='center', anchor_y='center')

                label.position = 320, 240


main()
