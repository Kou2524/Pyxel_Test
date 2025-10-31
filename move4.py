import pyxel

class App:
    def __init__(self):
        pyxel.init(160, 120, title="Move Test (Gamepad Fix)")
        self.x = 70
        self.y = 90
        self.vy = 0
        self.on_ground = True
        pyxel.run(self.update, self.draw)

    def update(self):
        move = 0

        # --- キーボード（PC） ---
        if pyxel.btn(pyxel.KEY_LEFT):
            move -= 1
        if pyxel.btn(pyxel.KEY_RIGHT):
            move += 1

        # --- モバイル仮想ゲームパッド（アナログ軸） ---
        axis_x = pyxel.gamepad_axis_value(0, 0)  # 左右スティックのX軸
        if axis_x < -0.2:
            move -= 1
        elif axis_x > 0.2:
            move += 1

        # --- 位置更新 ---
        self.x += move * 1.5
        if self.x < 0:
            self.x = 0
        if self.x > 160 - 16:
            self.x = 160 - 16

        # --- ジャンプ（Aボタンまたは↑キー） ---
        if self.on_ground and (
            pyxel.btnp(pyxel.KEY_SPACE)
            or pyxel.btnp(pyxel.KEY_UP)
            or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A)
        ):
            self.vy = -4
            self.on_ground = False

        # --- 重力処理 ---
        if not self.on_ground:
            self.vy += 0.2
            self.y += self.vy
            if self.y >= 90:
                self.y = 90
                self.vy = 0
                self.on_ground = True

    def draw(self):
        pyxel.cls(0)
        pyxel.rect(0, 106, 160, 14, 3)
        pyxel.rect(self.x, self.y, 16, 16, 11)
        pyxel.text(5, 5, "D-PAD or STICK: MOVE", 7)
        pyxel.text(5, 14, "A: JUMP", 7)
#test!!

App()
