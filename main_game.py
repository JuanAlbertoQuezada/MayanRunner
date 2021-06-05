import arcade as arc
from pygame import mixer
import serial

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650

MENU_MOVEMENT_SPEED = 70
MOVEMENT_SPEED = 6
JUMP_SPEED = 10
GRAVITY = 0.4
PLAYER_SCALE = 1
BLOCK_FLOOR_SCALE = 1
BLOCK_PIXEL_SIZE = 128
BLOCK_FLOOR_SIZE = int(BLOCK_FLOOR_SCALE * BLOCK_PIXEL_SIZE)
INITIAL_X = 10
INITIAL_Y = 120

PLAY_STATE_Y_COORD = 350
CONFIG_STATE_Y_COORD = 280
EXIT_STATE_Y_COORD = 210

#Variables de Juego
run_game = False
show_intro = False
actual_menu_state = 0
bg_texture_state = 0
global_counter = 0
class MusicPlayer(object):
    def __init__(self, path):
        mixer.init()
        mixer.music.load(path)
        mixer.music.play()

class Runner(arc.Window):
    def __init__(self, width, height):
        super().__init__(width, height)
        arc.set_background_color(arc.color.AMAZON)

    #Configuracion de Juego
    def setup(self):
        #variables globales del juego
        global run_game
        global actual_menu_state

        #abrimos el puerto Serial
        self.ser = serial.Serial("COM9",9600,timeout=0)

        #Textures
        self.bg_textures = [arc.load_texture("Backgrounds/MayanRunner_Intro.png"),
                       arc.load_texture("Backgrounds/aztlan.png"),
                       arc.load_texture("Backgrounds/Tenoc.png"),
                       arc.load_texture("Backgrounds/StoryBoard1.png"),
                       arc.load_texture("Backgrounds/bg_jungle.png")]

        #Sprites
        self.main_comp = arc.SpriteList()

        self.Selector = arc.Sprite("Backgrounds/BarraSeleccion.png")
        self.Selector.center_x = 120 # Starting position
        self.Selector.center_y = 350

        #Definimos la animacion Sprite
        self.player = arc.AnimatedWalkingSprite()

        #Cargamos la textura stand derecha
        self.player.stand_right_textures = []
        self.player.stand_right_textures.append(arc.load_texture("Player/stand.png",
                                                                    scale=PLAYER_SCALE))
        #Cargamos la textura stand derecha
        self.player.stand_left_textures = []
        self.player.stand_left_textures.append(arc.load_texture("Player/stand.png",
                                                                    scale=PLAYER_SCALE, mirrored=True))

        #Cargamos Sprites de Movimiento derechos
        self.player.walk_right_textures = []
        self.player.walk_right_textures.append(arc.load_texture("Player/walk1.png",scale=PLAYER_SCALE))
        self.player.walk_right_textures.append(arc.load_texture("Player/walk2.png",scale=PLAYER_SCALE))
        self.player.walk_right_textures.append(arc.load_texture("Player/walk3.png",scale=PLAYER_SCALE))
        self.player.walk_right_textures.append(arc.load_texture("Player/walk4.png",scale=PLAYER_SCALE))
        self.player.walk_right_textures.append(arc.load_texture("Player/walk5.png",scale=PLAYER_SCALE))
        self.player.walk_right_textures.append(arc.load_texture("Player/walk6.png",scale=PLAYER_SCALE))

        #Cargamos Sprites de Movimiento izquierdos
        self.player.walk_left_textures = []
        self.player.walk_left_textures.append(arc.load_texture("Player/walk1.png",scale=PLAYER_SCALE, mirrored=True))
        self.player.walk_left_textures.append(arc.load_texture("Player/walk2.png",scale=PLAYER_SCALE, mirrored=True))
        self.player.walk_left_textures.append(arc.load_texture("Player/walk3.png",scale=PLAYER_SCALE, mirrored=True))
        self.player.walk_left_textures.append(arc.load_texture("Player/walk4.png",scale=PLAYER_SCALE, mirrored=True))
        self.player.walk_left_textures.append(arc.load_texture("Player/walk5.png",scale=PLAYER_SCALE, mirrored=True))
        self.player.walk_left_textures.append(arc.load_texture("Player/walk6.png",scale=PLAYER_SCALE, mirrored=True))

        #Cargamos el Sprite de Caida
        self.player.walk_up_textures = []
        self.player.walk_down_textures = []
        self.player.walk_up_textures.append(arc.load_texture("Player/peace.png",scale=PLAYER_SCALE))
        self.player.walk_up_textures.append(arc.load_texture("Player/falling.png",scale=PLAYER_SCALE))

        self.player.center_x = 10
        self.player.center_y = 120

        #Sprites del piso
        self.floor_sprites_list = arc.SpriteList()
        for x in range(0, SCREEN_WIDTH, BLOCK_FLOOR_SIZE):
            floor_block = arc.Sprite("Extra/jungle_pack_05.png",BLOCK_FLOOR_SCALE)
            floor_block.bottom = -40
            floor_block.left = x

            self.floor_sprites_list.append(floor_block)

        x = 320
        y = 25
        for i in range(4):
            floor_block = arc.Sprite("Extra/jungle_pack_13.png",BLOCK_FLOOR_SCALE)
            floor_block.bottom = y
            floor_block.left = x
            x += 200
            y += 85

            self.floor_sprites_list.append(floor_block)

        for i in range(2):
            x -= 400
            y += 40
            floor_block = arc.Sprite("Extra/jungle_pack_13.png",BLOCK_FLOOR_SCALE)
            floor_block.bottom = y
            floor_block.left = x
            self.floor_sprites_list.append(floor_block)

        x = 60
        y = 350
        floor_block = arc.Sprite("Extra/jungle_pack_13.png",BLOCK_FLOOR_SCALE)
        floor_block.bottom = y
        floor_block.left = x

        self.floor_sprites_list.append(floor_block)

        self.coin = arc.AnimatedTimeSprite(scale=1)

        self.coin.textures = []
        self.coin.textures.append(arc.load_texture("Extra/coin2.png",scale=PLAYER_SCALE))
        self.coin.textures.append(arc.load_texture("Extra/coin3.png",scale=PLAYER_SCALE))
        self.coin.textures.append(arc.load_texture("Extra/coin4.png",scale=PLAYER_SCALE))
        self.coin.textures.append(arc.load_texture("Extra/coin5.png",scale=PLAYER_SCALE))
        self.coin.textures.append(arc.load_texture("Extra/coin6.png",scale=PLAYER_SCALE))

        self.coin.center_x = 125
        self.coin.center_y = 550


        self.main_comp.append(self.Selector)
        self.main_comp.append(self.player)

        #Configuramos motor de fisica
        self.Physics_Config = arc.PhysicsEnginePlatformer(self.player,self.floor_sprites_list,gravity_constant=GRAVITY)


    def on_key_press(self, key, modifiers):
        global actual_menu_state
        global run_game
        global bg_texture_state
        global show_intro
        global bg_textures

        if key == arc.key.UP:
            if run_game:
                self.player.change_y = JUMP_SPEED
            else:
                self.Selector.change_y = MENU_MOVEMENT_SPEED
        elif key == arc.key.DOWN:
            if not run_game:
                self.Selector.change_y = -MENU_MOVEMENT_SPEED
            else:
                self.player.change_y = -JUMP_SPEED
        elif key == arc.key.LEFT:
            if not run_game:
                self.Selector.change_x = -MENU_MOVEMENT_SPEED
            else:
                self.player.change_x = -MOVEMENT_SPEED
        elif key == arc.key.RIGHT:
            if not run_game:
                self.Selector.change_x = MENU_MOVEMENT_SPEED
            else:
                self.player.change_x = MOVEMENT_SPEED
        elif key == arc.key.ENTER and actual_menu_state==2:
            print("Closing AALKAB")
            quit()
        elif key == arc.key.ENTER and actual_menu_state == 0 and run_game == False and show_intro == False:
            show_intro = True
            bg_texture_state += 1
        elif key == arc.key.ESCAPE:
            print("Closing AALKAB")
            quit()

    def on_key_release(self, key, modifiers):
        global actual_menu_state
        global bg_texture_state
        global show_intro
        global run_game

        if key == arc.key.DOWN and actual_menu_state <= 1:
            actual_menu_state += 1
            self.Selector.change_y = 0
        elif key == arc.key.DOWN or key == arc.key.UP and run_game:
            self.player.change_y = 0
            print("X:{} Y:{}".format(self.player.center_x, self.player.center_y))
        elif key == arc.key.LEFT or key == arc.key.RIGHT and run_game:
            self.player.change_x = 0
        elif key == arc.key.UP and actual_menu_state >= 1:
            actual_menu_state -= 1
            self.Selector.change_y = 0
        elif key == arc.key.LEFT:
            self.Selector.change_x = 0
        elif key == arc.key.RIGHT:
            self.Selector.change_x = 0
            self.player.change_x = 0
            if(show_intro == True  and run_game == False):
                if(bg_texture_state < 4):
                    bg_texture_state += 1
                else:
                    run_game = True
                    show_intro = False
        elif key == arc.key.SPACE:
            self.player.center_x = INITIAL_X
            self.player.center_y = INITIAL_Y
    #Renderizado
    def on_draw(self):
        global bg_texture_state
        global run_game
        global show_intro

        arc.start_render()
        arc.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT// 2,
                                   SCREEN_WIDTH, SCREEN_HEIGHT,self.bg_textures[bg_texture_state])

        if(show_intro == False and run_game == False):
            self.main_comp[0].draw()
        elif(run_game):
            self.floor_sprites_list.draw()
            self.coin.draw()
            self.main_comp[1].draw()


    #Logica de Movimiento y
    #Logica de juego
    def update(self, delta_time):
        global bg_texture_state
        global run_game
        global global_counter

        recData = self.ser.read()
        #recData = recData.decode("utf-8")

        if(recData == b'w'):
            self.player.change_y = JUMP_SPEED
        elif(recData == b's'):
            self.player.change_y = -JUMP_SPEED
        elif(recData == b'a'):
            self.player.change_x = -MOVEMENT_SPEED
        elif(recData == b'd'):
            self.player.change_x = MOVEMENT_SPEED
        #elif(recData == 'j'):
        #    pass
        else:
            if(global_counter >= 8):
                self.Selector.change_y = 0
                self.Selector.change_x = 0
                self.player.change_y = 0
                self.player.change_x = 0
                global_counter = 0
            else:
                global_counter += 1

        if(not run_game):
            if actual_menu_state == 0:
                self.Selector.center_y = PLAY_STATE_Y_COORD
            elif actual_menu_state == 1:
                self.Selector.center_y = CONFIG_STATE_Y_COORD
            elif actual_menu_state == 2:
                self.Selector.center_y = EXIT_STATE_Y_COORD
        else:
            self.main_comp[1].update()
            self.main_comp[1].update_animation()
            self.coin.update()
            self.coin.update_animation()
            #Actualizamos la configuracion de fisica para evitar desplazamiento
            #hacia abajo del personaje
            self.Physics_Config.update()

            catched_coin = arc.check_for_collision(self.player, self.coin)
            if(catched_coin):
                print("Felicidades has conseguido la recompensa del dios kukulkan!")
                input("Press enter to finish!")
                quit()




def main():
    game = Runner(SCREEN_WIDTH,SCREEN_HEIGHT)
    game.setup()
    mp = MusicPlayer('Sound/prehispanic.mp3')
    arc.run()

#Arranca Rutina de Juego
if __name__ == "__main__":
    main()
