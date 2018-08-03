# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
started = False
class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated


# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim

# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# alternative upbeat soundtrack by composer and former IIPP student Emiel Stopler
# please do not redistribute without permission from Emiel at http://www.filmcomposer.nl
#soundtrack = simplegui.load_sound("https://storage.googleapis.com/codeskulptor-assets/ricerocks_theme.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.accel = [0,0]
    def get_pos(self):
        return self.pos
    def get_radius(self):
        return self.radius
    def shoot(self,shoot):
        global a_missile
        if shoot:
            a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [0,0], 0, 0, missile_image, missile_info, missile_sound)
            a_missile.pos = [self.pos[0] + 45*angle_to_vector(self.angle)[0],self.pos[1] + 45 *angle_to_vector(self.angle)[1]]
            a_missile.vel = [self.vel[0] + 10*angle_to_vector(self.angle)[0],self.vel[1] + 10*angle_to_vector(self.angle)[1]]
            missile_group.add(a_missile)
            missile_sound.play()
    def draw(self,canvas):
        #canvas.draw_circle(self.pos, self.radius, 1, "White", "White")
        canvas.draw_image(self.image,self.image_center,self.image_size,self.pos,self.image_size,self.angle)
    def ang_change(self,dire,ang):
        if dire == 'left':
            self.angle_vel -= ang
        elif dire == 'right':
            self.angle_vel += ang
    def thruster(self,bo):
        self.thrust = bo
        if self.thrust:
            self.image_center = [135,45]
            ship_thrust_sound.play()
            self.accel = [0.5*angle_to_vector(self.angle)[0],0.5*angle_to_vector(self.angle)[1]]

        else:
            self.image_center = [45,45]
            ship_thrust_sound.pause()
            self.accel = [0,0]
    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.vel[0] *= (1-0.03)
        self.vel[1] *= (1-0.03)
        self.vel[0] += self.accel[0]
        self.vel[1] += self.accel[1]
        if self.pos[0] > WIDTH:
            self.pos[0] = self.pos[0]%WIDTH
        elif self.pos[0] < 0:
            self.pos[0] = WIDTH + self.pos[0]
        if self.pos[1] > HEIGHT:
            self.pos[1] = self.pos[1]%HEIGHT
        elif self.pos[1] < 0 :
            self.pos[1] = HEIGHT + self.pos[1]

        self.angle += self.angle_vel
def keydown(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.ang_change('left',0.1)
    elif key == simplegui.KEY_MAP['right']:
        my_ship.ang_change('right',0.1)

    if key == simplegui.KEY_MAP['up']:
        my_ship.thruster(True)

    if key == simplegui.KEY_MAP['space']:
        my_ship.shoot(True)

def keyup(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.ang_change('left',-0.1)
    elif key == simplegui.KEY_MAP['right']:
        my_ship.ang_change('right',-0.1)

    if key == simplegui.KEY_MAP['up']:
        my_ship.thruster(False)
    if key == simplegui.KEY_MAP['space']:
        my_ship.shoot(False)


# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
    def get_pos(self):
        return self.pos
    def get_radius(self):
        return self.radius

    def draw(self, canvas):
        #canvas.draw_circle(self.pos, self.radius, 1, "Red", "Red")
        if self.animated == True:
            self.image_center = [self.image_center[0] + self.age*self.image_size[0],self.image_center[1]]
            canvas.draw_image(self.image,self.image_center,self.image_size,self.pos,self.image_size,self.angle)
        else:
            canvas.draw_image(self.image,self.image_center,self.image_size,self.pos,self.image_size,self.angle)
    def update(self):
        self.age += 1
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        if self.pos[0] > WIDTH:
            self.pos[0] = self.pos[0]%WIDTH
        elif self.pos[0] < 0:
            self.pos[0] = WIDTH + self.pos[0]
        if self.pos[1] > HEIGHT:
            self.pos[1] = self.pos[1]%HEIGHT
        elif self.pos[1] < 0 :
            self.pos[1] = HEIGHT + self.pos[1]
        self.angle += self.angle_vel
        if self.age <= self.lifespan:
            return False
        return True

    def collide(self,other_ob):
        if dist(self.pos,other_ob.get_pos())<= (self.radius+other_ob.get_radius()):
            return True
        else:
            return False

def group_collide(group,other_object):
    for s in set(group):
        if s.collide(other_object):
            explode = Sprite(s.get_pos(),[0,0],0,0,explosion_image,explosion_info,explosion_sound)
            explosion_group.add(explode)
            group.remove(s)
            return True

    return False
def group_group_collide(gr1,gr2):
    global score
    count = 0
    for s in set(gr1):
        if group_collide(gr2,s):
            count +=1
            score += 10
            gr1.discard(s)
    return count

def click(pos):
    global started
    soundtrack.pause()
    soundtrack.rewind()
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True



def draw(canvas):
    global time,lives,rock_group,score,started

    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_text("Lives: " + str(lives),[10,50],40,'White')
    canvas.draw_text("Score: " + str(score),[WIDTH - 160,50],40,'White')
    # draw ship and sprites
    my_ship.draw(canvas)
    process_sprite_group(canvas,rock_group)
    if group_collide(rock_group,my_ship):
        lives -= 1
    group_group_collide(rock_group,missile_group)
    process_sprite_group(canvas,explosion_group)
    process_sprite_group(canvas,missile_group)
    if lives == 0:
        rock_group = set([])
        lives = 3
        score = 0
        started = False
        soundtrack.play()
    # update ship and sprites
    my_ship.update()
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(),
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2],
                          splash_info.get_size())
# timer handler that spawns a rock
def rock_spawner():
    global rock_group
    if started:
        a_rock = Sprite([random.randrange(0,WIDTH),random.randrange(0,HEIGHT)], [random.randrange(-1,1),random.randrange(-1,1)], 0,(random.randrange(-2,2)/10), asteroid_image, asteroid_info)

        if len(rock_group)<12:
            rock_group.add(a_rock)
        else:
            pass

def process_sprite_group(canvas,sprite_set):
    for s in set(sprite_set):
        s.update()
        if s.update():
            sprite_set.remove(s)
        s.draw(canvas)

# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)
soundtrack.play()
# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
rock_group = set([])
missile_group = set([])
explosion_group = set([])
# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
timer = simplegui.create_timer(1000.0, rock_spawner)
frame.set_mouseclick_handler(click)
# get things rolling
timer.start()
frame.start()
