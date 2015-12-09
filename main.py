__author__ = 'samhauck'
import pyglet
from pyglet.window import key
import cocos
from cocos import actions, layer, sprite, scene
from cocos.director import director
import cocos.collision_model as cm
import cocos.euclid as eu



def main():

    global keyboard

    #  initialzing the director. the director creates the window for the game
    director.init(width=400, height= 600, autoscale=True, resizable = True)

    #  creating a layer using the cocos2d platform
    #  different layers are used for each aspect of the game, i.e. the main character or background
    game_layer = layer.Layer()

    #creating a Sprite for the main character
    heroimage = pyglet.resource.image('hero.png')
    player = HeroShip(heroimage)
    #heroShip.cshape = cm.AARectShape(eu.Vector2(heroShip.position), 32, 32)

    #adding the main character to the 'player_layer' layer
    game_layer.add(player)

    #initializing the main character's position and velocity
    #heroShip.position = (100, 100)
    #heroShip.velocity = (0, 0)

    #creating a background layer
    background_layer = layer.Layer()
    background = sprite.Sprite('space_wallpaper.png')

    #adding backgound image to background layer
    background_layer.add(background)


    AsteroidImage = pyglet.resource.image('asteroid.png')

    asteroid = Asteroid(AsteroidImage, (200, 400))


    #adding asteroids to game layer
    game_layer.add(asteroid)

    game_layer.add(CollisionManager(player, asteroid))






    #initializing pyglet, which allows for keyboard import for character movement

    keyboard = key.KeyStateHandler()
    director.window.push_handlers(keyboard)

    #assigning the movement class to the heroShip sprite
    player.do(HeroShipMovement())

    #asteroid_1.do(actions.MoveBy( (0, -600), 4) )
    #asteroid_2.do(actions.MoveBy( (100, -600), 8) )

    main_scene = scene.Scene(background_layer, game_layer)

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

class CollisionManager(cocos.collision_model.CollisionManager):
    def __init__(self, obj1, obj2):
        cm.CollisionManager.add(obj1)
        cm.CollisionManager.add(obj2)
        collision = cm.CollisionManager.they_collide(self, obj1, obj2)
        return collision





main()



