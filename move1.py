import pyxel

class App:
    def __init__(self):
        pyxel.init(160, 120, title="Move Test")
        self.x = 70
        self.y = 90
        self.vy = 0
        self.on_ground = True
        pyxel.run(self.update, self.draw)

    def update(self):
        # 左右
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= 1.5
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += 1.5

        # 画面外に出さない
        if self.x < 0:
            self.x = 0
        if self.x > 160 - 16:
            self.x = 160 - 16

        # ジャンプ
        if self.on_ground and (pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A)):
            self.vy = -4
            self.on_ground = False

        # 重力
        if not self.on_ground:
            self.vy += 0.2
            self.y += self.vy
            if self.y >= 90:
                self.y = 90
                self.vy = 0
                self.on_ground = True

    def draw(self):
        pyxel.cls(0)
        pyxel.rect(0, 106, 160, 14, 3)     # 地面
        pyxel.rect(self.x, self.y, 16, 16, 11)  # プレイヤー
        pyxel.text(5, 5, "D-PAD: MOVE", 7)
        pyxel.text(5, 14, "A: JUMP", 7)

App()
