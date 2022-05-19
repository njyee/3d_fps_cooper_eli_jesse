from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import sys
from ursina.prefabs.health_bar import HealthBar

class Screen(Ursina):
  def __init__(self):
    super().__init__(
      title = "super_fps",
      fullscreen = False)


def update():
  if held_keys['q']:
    sys.exit()
  if player.y < -5:
    player.position = (0, 2, 0)
  if held_keys["left mouse"]:
    shoot()

game = Screen()

######################################
# Level / round rules
level_one_limit = 10
enemy_counter = 0
######################################

gun_model = load_model("colt.obj")

def shoot():
    gun.rotation_z = 8
    if not gun.on_cooldown:
        gun.on_cooldown = True
        gun.muzzle_flash.enabled=True
        from ursina.prefabs.ursfx import ursfx
        ursfx([(0.0, 0.0), (0.1, 0.9), (0.15, 0.75), (0.3, 0.14), (0.6, 0.0)], volume=0.5, wave='noise', pitch=random.uniform(-13,-12), pitch_change=-12, speed=3.0)
        invoke(gun.muzzle_flash.disable, delay=.4)
        if mouse.hovered_entity:
            mouse.hovered_entity.hp -= 20
        
        


# LOAD TEXTURES HERE
crate_texture = load_texture('crate.jpg')
class Crate(Entity):
  def __init__(self):
    super().__init__(
      model = "cube",
      texture = crate_texture,
      scale = 2,  
      collider = "box",
      z = 5
    )
    
  def update(self):
    # we use intersects to check for collision
    if self.intersects(player):
      self.color = color.red
      player.y += 100

class Enemy(Entity):
  def __init__(self):
    super().__init__(
      z = 40,
      y = 0.5,
      scale = 0.1,
      collider = "box",
      model = load_model('warrior.obj'),
      color = color.orange
    )
    self.spawn = False
    self.hp = 100
    global enemy_counter
    enemy_counter += 1
    
  def update(self):
    distance = distance_xz(player.position, self.position)
    if distance > 20:
      return
    if distance > 0.5:
      self.look_at_2d(player.position, 'y')
      self.position += self.forward * time.dt * 50
    if self.intersects(player):
      player_health.value -= 10
      Audio(sound_file_name='slap.mp3')
      self.position -= self.forward * time.dt * 200
    # check if player shoots me
    if self.hp == 0:
      self.position = (4999, 3568, 2122)
      self.spawn = True
    if self.spawn:
      if enemy_counter < level_one_limit:
        spawn_enemies()
        self.spawn = False


def spawn_enemies():
  for i in range(5):
    en = Enemy()
    en.x = i
    

ground = Entity(model='plane', collider='box', scale=100, texture='grass', texture_scale=(4,4))
sky = Sky()
crate = Crate()
player = FirstPersonController(collider="box", speed = 10, scale=1)
player_health = HealthBar(bar_color=color.green, value=100)
gun = Entity(model=gun_model, parent=player, z = 1, y = 1.9, x=0.35, scale=(2), color=color.black, rotation=(0,90,0), on_cooldown=False)
gun.muzzle_flash = Entity(parent=gun, z=0, x=-.30, world_scale=.2, model='quad', rotation=(0,0,45), color=color.yellow, enabled=False)
# enemy_health = HealthBar(bar_color=color.red, value=100, x=0.2)
# spawn Enemy
enemy = Enemy()
game.run()

