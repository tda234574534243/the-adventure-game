import pygame

class Button:
    def __init__(self, x, y, image, scale, text=None, xoff=None):
        self.width = int(image.get_width() * scale)
        self.height = int(image.get_height() * scale)
        self.image = pygame.transform.scale(image, (self.width, self.height))
        self.rect = self.image.get_rect(topleft=(x, y))

        self.text = text
        if text:
            self.xoff = xoff if xoff else text.get_width() // 2
            self.yoff = text.get_height() // 2

        # trạng thái click
        self.held_inside = False
        self.released = False

    def draw(self, surface, mouse_pos, mouse_pressed):
        action = False
        inside = self.rect.collidepoint(mouse_pos)

        # Nếu chuột đang đè và hover
        if inside and mouse_pressed[0]:
            self.held_inside = True

        # Khi thả chuột
        if not mouse_pressed[0]:
            if self.held_inside and inside:  
                action = True  # nhả trong nút → click hợp lệ
            self.held_inside = False

        surface.blit(self.image, self.rect)

        if self.text:
            surface.blit(
                self.text,
                (self.rect.x + self.width // 2 - self.xoff,
                 self.rect.y + self.height // 2 - self.yoff)
            )

        return action
