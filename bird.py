from pico2d import get_time, load_image, load_font, clamp,  SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT
import game_world
import game_framework
import random

PIXEL_PER_METER = (10.0/ 0.2)
RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM= RUN_SPEED_KMPH * 1000.0 / 60.0
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

FRAMES_PER_TIME = ACTION_PER_TIME * FRAMES_PER_ACTION

class AutoFly:

    @staticmethod
    def enter(bird, e):
        pass

    @staticmethod
    def exit(bird, e):
        pass

    @staticmethod
    def do(bird):
        bird.frame = (bird.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 5
        bird.x += bird.dir * RUN_SPEED_PPS * game_framework.frame_time
        bird.x = clamp(50, bird.x, 1600-50)
        if bird.x == 1600 - 50:
            bird.dir = -1
        elif bird.x == 50:
            bird.dir = 1


    @staticmethod
    def draw(bird):
        if bird.dir == 1:
            bird.image.clip_draw(int(bird.frame) * 182, bird.action * 100, 180, 210, bird.x, bird.y, bird.w, bird.h)
        elif bird.dir == -1:
            bird.image.clip_composite_draw(int(bird.frame) * 182, bird.action * 100, 180, 210, 0, 'h', bird.x, bird.y, bird.w, bird.h)


class StateMachine:
    def __init__(self, Bird):
        self.Bird = Bird
        self.cur_state = AutoFly

    def start(self):
        pass

    def update(self):
        self.cur_state.do(self.Bird)

    def handle_event(self, e):
        pass

    def draw(self):
        self.cur_state.draw(self.Bird)





class Bird:
    def __init__(self):
        self.x, self.y = random.randint(100,1500), random.randint(100,550)
        self.w, self.h = 100, 120
        self.frame = 0
        self.action = 3
        self.dir = 1
        self.image = load_image('bird_animation.png')
        self.font = load_font('ENCR10B.TTF', 16)
        self.state_machine = StateMachine(self)
        self.state_machine.start()


    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        # self.state_machine.handle_event(('INPUT', event))
        pass

    def draw(self):
        self.state_machine.draw()
        self.font.draw(self.x - 60, self.y + 50, f'{get_time()}', (255,255,0))
        # self.font.draw(self.x - 60, self.y + 70, f'{self.w,self.h}', (255,255,0))
