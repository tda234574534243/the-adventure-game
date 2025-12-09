import pygame

WIDTH, HEIGHT = 640, 384

# Giữ tỉ lệ ảnh theo kích thước mục tiêu
def scale_keep_ratio(image, target):
    w, h = image.get_size()
    if w > h:
        new_w = target
        new_h = int(h * (target / w))
    else:
        new_h = target
        new_w = int(w * (target / h))
    return pygame.transform.scale(image, (new_w, new_h))


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Player, self).__init__()

        # Hitbox nhỏ (chuẩn collision)
        self.size = 24

        # Sprite lớn cho nhìn rõ ràng
        self.sprite_scale = 64

        # Animation lists
        self.idle_list = []
        self.walk_left = []
        self.walk_right = []
        self.attack_list = []
        self.death_list = []
        self.hit_list = []

        # ---------------------------
        # LOAD ANIMATION
        # ---------------------------

        for i in range(1, 3):
            img = pygame.image.load(f'Assets/Player/PlayerIdle{i}.png').convert_alpha()
            img = scale_keep_ratio(img, self.sprite_scale)
            self.idle_list.append(img)

        for i in range(1, 6):
            img = pygame.image.load(f'Assets/Player/PlayerWalk{i}.png').convert_alpha()
            right = scale_keep_ratio(img, self.sprite_scale)
            left = pygame.transform.flip(right, True, False)
            self.walk_right.append(right)
            self.walk_left.append(left)

        for i in range(1, 5):
            img = pygame.image.load(f'Assets/Player/PlayerAttack{i}.png').convert_alpha()
            img = scale_keep_ratio(img, self.sprite_scale)
            self.attack_list.append(img)

        for i in range(1, 11):
            img = pygame.image.load(f'Assets/Player/PlayerDead{i}.png').convert_alpha()
            img = scale_keep_ratio(img, self.sprite_scale)
            self.death_list.append(img)

        for i in range(1, 3):
            img = pygame.image.load(f'Assets/Player/PlayerHit{i}.png').convert_alpha()
            img = scale_keep_ratio(img, self.sprite_scale)
            self.hit_list.append(img)

        # Animation indexing
        self.idle_index = 0
        self.walk_index = 0
        self.attack_index = 0
        self.death_index = 0
        self.hit_index = 0

        # Physics
        self.jump_height = 20
        self.speed = 3
        self.vel = self.jump_height
        self.mass = 1
        self.gravity = 1

        self.counter = 0
        self.direction = 0

        self.alive = True
        self.attack = False
        self.hit = False
        self.jump = False

        self.grenades = 5
        self.health = 100

        # Sprite + hitbox
        self.image = self.idle_list[self.idle_index]
        self.rect = pygame.Rect(0, 0, self.size, self.size)
        self.rect.center = (x, y)

    # ------------------------------------------------
    # COLLISION
    # ------------------------------------------------
    def check_collision(self, world, dx, dy):

        # Ground collision
        for tile in world.ground_list:
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.size, self.size):
                if self.rect.y + dy <= tile[1].y:
                    dy = tile[1].top - self.rect.bottom

        # Rock collision
        for tile in world.rock_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.size, self.size):
                dx = 0
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.size, self.size):
                if self.vel > 0 and self.vel != self.jump_height:
                    dy = 0
                    self.jump = False
                    self.vel = self.jump_height
                else:
                    dy = tile[1].top - self.rect.bottom

        return dx, dy

    # ------------------------------------------------
    # ANIMATION UPDATE
    # ------------------------------------------------
    def update_animation(self):
        self.counter += 1
        if self.counter % 7 == 0:

            if self.health <= 0:
                self.death_index += 1
                if self.death_index >= len(self.death_list):
                    self.alive = False

            else:
                if self.attack:
                    self.attack_index += 1
                    if self.attack_index >= len(self.attack_list):
                        self.attack_index = 0
                        self.attack = False

                if self.hit:
                    self.hit_index += 1
                    if self.hit_index >= len(self.hit_list):
                        self.hit_index = 0
                        self.hit = False

                if self.direction == 0:
                    self.idle_index = (self.idle_index + 1) % len(self.idle_list)

                if self.direction in (-1, 1):
                    self.walk_index = (self.walk_index + 1) % len(self.walk_left)

            self.counter = 0

        # Select final sprite
        if self.alive:
            if self.health <= 0:
                self.image = self.death_list[self.death_index]

            elif self.attack:
                self.image = self.attack_list[self.attack_index]
                if self.direction == -1:
                    self.image = pygame.transform.flip(self.image, True, False)

            elif self.hit:
                self.image = self.hit_list[self.hit_index]

            elif self.direction == 0:
                self.image = self.idle_list[self.idle_index]

            elif self.direction == -1:
                self.image = self.walk_left[self.walk_index]

            elif self.direction == 1:
                self.image = self.walk_right[self.walk_index]

    # ------------------------------------------------
    # MOVEMENT + PHYSICS
    # ------------------------------------------------
    def update(self, moving_left, moving_right, world):
        self.dx = 0
        self.dy = 0

        # Movement input
        if moving_left:
            self.dx = -self.speed
            self.direction = -1
        if moving_right:
            self.dx = self.speed
            self.direction = 1
        if not moving_left and not moving_right and not self.jump:
            self.direction = 0
            self.walk_index = 0

        # Jump physics
        if self.jump:
            F = (1 / 2) * self.mass * self.vel
            self.dy -= F
            self.vel -= self.gravity

            if self.vel < -15:
                self.vel = self.jump_height
                self.jump = False
        else:
            self.dy += self.vel

        # Collision
        self.dx, self.dy = self.check_collision(world, self.dx, self.dy)

        # Clamp X
        if self.rect.left + self.dx < 0 or self.rect.right + self.dx > WIDTH:
            self.dx = 0

        # Apply movement
        self.rect.x += self.dx
        self.rect.y += self.dy

        # Animation
        self.update_animation()

    # ------------------------------------------------
    # DRAW (FULL FIX)
    # ------------------------------------------------
    def draw(self, win):
        # Tự tính offset chân không lún
        foot_offset = (self.image.get_height() - self.size) // 2

        img_x = self.rect.centerx - self.image.get_width() // 2
        img_y = self.rect.centery - self.image.get_height() // 2 - foot_offset

        win.blit(self.image, (img_x, img_y))
