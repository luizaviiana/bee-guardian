from random import randint, random
from math import sqrt
from pygame import Rect

TITLE = "Bee Guardian"
WIDTH = 768
HEIGHT = 576
CELL = 48

GRID_W = WIDTH // CELL
GRID_H = HEIGHT // CELL

STATE_MENU = "menu"
STATE_PLAY = "play"
STATE_OVER = "over"

BTN_W = 260
BTN_H = 64

START_SCORE = 100
KILL_SCORE = 5
FLOWER_PENALTY = 30 

mouse_pos = (0, 0)


def grid_to_px(cx, cy):
    return cx * CELL + CELL // 2, cy * CELL + CELL // 2


def draw_button(rect, text):
    hovered = rect.collidepoint(mouse_pos)

    bg = (70, 70, 70) if hovered else (40, 40, 40)
    border = (255, 220, 120) if hovered else (200, 200, 200)

    screen.draw.filled_rect(rect, bg)

    screen.draw.rect(rect, border)
    screen.draw.rect(rect.inflate(-2, -2), border)
    screen.draw.rect(rect.inflate(-4, -4), border)

    screen.draw.text(text, center=rect.center, fontsize=34, color="white")


def play_sound(name):
    if not sound_on:
        return
    if name == "click":
        sounds.click.play()
    elif name == "hit":
        sounds.hit.play()
    elif name == "flower_hit":
        sounds.flower_hit.play()


class SpriteAnimator:
    def __init__(self, frames, fps=8):
        self.frames = frames
        self.fps = fps
        self.time = 0
        self.index = 0

    def update(self, dt):
        self.time += dt
        if self.time >= 1 / self.fps:
            self.time = 0
            self.index = (self.index + 1) % len(self.frames)

    def image(self):
        return self.frames[self.index]


class GridMover:
    def __init__(self, actor, cx, cy, speed=260):
        self.actor = actor
        self.cx = cx
        self.cy = cy
        self.tx = cx
        self.ty = cy
        self.speed = speed
        self.moving = False
        self.actor.pos = grid_to_px(cx, cy)

    def move_to(self, cx, cy):
        if not self.moving:
            self.tx = max(0, min(GRID_W - 1, cx))
            self.ty = max(0, min(GRID_H - 1, cy))
            self.moving = True

    def update(self, dt):
        if not self.moving:
            return

        x, y = self.actor.pos
        tx, ty = grid_to_px(self.tx, self.ty)
        dx, dy = tx - x, ty - y
        dist = sqrt(dx * dx + dy * dy)

        if dist < 2:
            self.actor.pos = (tx, ty)
            self.cx, self.cy = self.tx, self.ty
            self.moving = False
            return

        x += dx / dist * self.speed * dt
        y += dy / dist * self.speed * dt
        self.actor.pos = (x, y)


class Bee:
    def __init__(self, cx, cy):
        self.actor = Actor("bee_idle_0")
        self.mover = GridMover(self.actor, cx, cy)

        self.idle = SpriteAnimator(
            ["bee_idle_0", "bee_idle_1", "bee_idle_2"], fps=5
        )
        self.move = SpriteAnimator(
            ["bee_move_0", "bee_move_1", "bee_move_2"], fps=10
        )

        self.queued_move = None

    def update(self, dt):
        self.mover.update(dt)

        if not self.mover.moving and self.queued_move:
            dx, dy = self.queued_move
            self.queued_move = None
            self.mover.move_to(self.mover.cx + dx, self.mover.cy + dy)

        if self.mover.moving:
            self.move.update(dt)
            self.actor.image = self.move.image()
        else:
            self.idle.update(dt)
            self.actor.image = self.idle.image()

    def try_move(self, dx, dy):
        nx = self.mover.cx + dx
        ny = self.mover.cy + dy

        if nx == GRID_W // 2 and ny == GRID_H // 2:
            return

        if not self.mover.moving:
            self.mover.move_to(nx, ny)
        else:
            self.queued_move = (dx, dy)


class Flower:
    def __init__(self, cx, cy):
        self.actor = Actor("flower_0")
        self.actor.pos = grid_to_px(cx, cy)

        self.actor.scale = 1.3

        self.anim = SpriteAnimator(
            ["flower_0", "flower_1", "flower_2", "flower_3"], fps=4
        )

        self.radius = CELL * 1.1

    def update(self, dt):
        self.anim.update(dt)
        self.actor.image = self.anim.image()

    def collides_with(self, other):
        dx = self.actor.x - other.x
        dy = self.actor.y - other.y
        return dx * dx + dy * dy < self.radius * self.radius


class Bug:
    def __init__(self, cx, cy, area):
        self.actor = Actor("bug_idle_0")
        self.mover = GridMover(self.actor, cx, cy, speed=160)
        self.area = area
        self.wait = random()
        self.damage_cooldown = 0

        self.idle = SpriteAnimator(
            ["bug_idle_0", "bug_idle_1", "bug_idle_2"], fps=4
        )
        self.move = SpriteAnimator(
            ["bug_move_0", "bug_move_1", "bug_move_2"], fps=8
        )

    def update(self, dt):
        self.damage_cooldown = max(0, self.damage_cooldown - dt)

        if not self.mover.moving:
            self.wait -= dt
            if self.wait <= 0:
                self.wait = 0.5
                cx = randint(self.area.left, self.area.right - 1)
                cy = randint(self.area.top, self.area.bottom - 1)
                self.mover.move_to(cx, cy)

        self.mover.update(dt)

        if self.mover.moving:
            self.move.update(dt)
            self.actor.image = self.move.image()
        else:
            self.idle.update(dt)
            self.actor.image = self.idle.image()


game_state = STATE_MENU
sound_on = True

bee = None
flower = None
bugs = []
spawn_timer = 1.5
score = START_SCORE

btn_start = Rect(WIDTH // 2 - BTN_W // 2, 230, BTN_W, BTN_H)
btn_sound = Rect(WIDTH // 2 - BTN_W // 2, 310, BTN_W, BTN_H)
btn_exit = Rect(WIDTH // 2 - BTN_W // 2, 390, BTN_W, BTN_H)


def reset_game():
    global bee, flower, bugs, spawn_timer, game_state, score
    bee = Bee(2, GRID_H // 2)
    flower = Flower(GRID_W // 2, GRID_H // 2)
    bugs = []
    spawn_timer = 1.5
    score = START_SCORE
    game_state = STATE_PLAY


def update(dt):
    global spawn_timer, game_state, score

    if game_state != STATE_PLAY:
        return

    bee.update(dt)
    flower.update(dt)

    for b in bugs[:]:
        b.update(dt)

        if b.actor.colliderect(bee.actor):
            score += KILL_SCORE
            play_sound("hit")
            bugs.remove(b)
            continue

        if flower.collides_with(b.actor) and b.damage_cooldown <= 0:
            score -= FLOWER_PENALTY
            b.damage_cooldown = 1.0
            play_sound("flower_hit")
            bugs.remove(b)

    if score <= 0:
        game_state = STATE_OVER

    spawn_timer -= dt
    if spawn_timer <= 0:
        zone = Rect(0, 0, GRID_W, GRID_H)
        bugs.append(Bug(GRID_W - 1, randint(0, GRID_H - 1), zone))
        spawn_timer = max(0.8, spawn_timer * 0.98)  


def draw():
    screen.clear()

    if game_state == STATE_MENU:
        screen.blit("ui_bg", (0, 0))

        screen.draw.text(
            "BEE GUARDIAN",
            center=(WIDTH // 2 + 3, 153),
            fontsize=72,
            color=(0, 0, 0)
        )
        screen.draw.text(
            "BEE GUARDIAN",
            center=(WIDTH // 2, 150),
            fontsize=72,
            color=(255, 230, 120)
        )

        draw_button(btn_start, "START")
        draw_button(btn_sound, "SOUND: ON" if sound_on else "SOUND: OFF")
        draw_button(btn_exit, "EXIT")
        return

    screen.blit("arena_bg", (0, 0))

    flower.actor.draw()
    for b in bugs:
        b.actor.draw()
    bee.actor.draw()

    screen.draw.text(f"Score: {score}", (10, 10))

    if game_state == STATE_OVER:
        screen.draw.text(
            "GAME OVER",
            center=(WIDTH // 2, HEIGHT // 2),
            fontsize=70
        )


def on_key_down(key):
    if game_state != STATE_PLAY:
        return
    if key == keys.LEFT:
        bee.try_move(-1, 0)
    elif key == keys.RIGHT:
        bee.try_move(1, 0)
    elif key == keys.UP:
        bee.try_move(0, -1)
    elif key == keys.DOWN:
        bee.try_move(0, 1)


def on_mouse_move(pos):
    global mouse_pos
    mouse_pos = pos


def on_mouse_down(pos):
    global sound_on

    if game_state == STATE_MENU:
        if btn_start.collidepoint(pos):
            play_sound("click")
            reset_game()

        elif btn_sound.collidepoint(pos):
            sound_on = not sound_on
            if sound_on:
                music.play("theme")
            else:
                music.stop()
            play_sound("click")

        elif btn_exit.collidepoint(pos):
            raise SystemExit


music.play("theme")
music.set_volume(0.5)
