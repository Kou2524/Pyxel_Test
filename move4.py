import pyxel


class App:
    def __init__(self):
        pyxel.init(160, 120, title="bare touch pad", fps=60)

        # プレイヤー
        self.x = 60
        self.y = 70
        self.vy = 0
        self.ground_y = 96

        # 左パッド
        self.dpad_x = 4
        self.dpad_y = 58
        self.dpad_w = 50
        self.dpad_h = 50

        # 右ボタン
        self.btn_x = 110
        self.btn_y = 58
        self.btn_w = 28
        self.btn_h = 28

        pyxel.run(self.update, self.draw)

    def mouse_in_rect(self, x, y, w, h):
        """
        できるだけ原始的に判定する:
        - ボタンは pyxel.btn(0) で見る
        - 座標は pyxel.mouse_x / pyxel.mouse_y を使う
        """
        if not pyxel.btn(0):
            return False
        mx = pyxel.mouse_x
        my = pyxel.mouse_y
        return x <= mx <= x + w and y <= my <= y + h

    def update(self):
        move_left = False
        move_right = False
        jump = False

        # キーボード（PC用）は残しておく
        if pyxel.btn(pyxel.KEY_LEFT):
            move_left = True
        if pyxel.btn(pyxel.KEY_RIGHT):
            move_right = True
        if pyxel.btnp(pyxel.KEY_SPACE):
            jump = True

        # スマホ/タップ：ボタン0で見る
        # 左パッド
        if self.mouse_in_rect(self.dpad_x, self.dpad_y, self.dpad_w, self.dpad_h):
            cx = self.dpad_x + self.dpad_w / 2
            if pyxel.mouse_x < cx:
                move_left = True
            else:
                move_right = True

        # 右ボタン
        if self.mouse_in_rect(self.btn_x, self.btn_y, self.btn_w, self.btn_h):
            jump = True

        # 横移動
        speed = 1.5
        if move_left:
            self.x -= speed
        if move_right:
            self.x += speed

        # 画面外に出ない
        if self.x < 0:
            self.x = 0
        if self.x > pyxel.width - 8:
            self.x = pyxel.width - 8

        # 重力＋ジャンプ
        self.vy += 0.3
        on_ground = self.y >= self.ground_y - 8 - 0.01
        if jump and on_ground:
            self.vy = -5

        self.y += self.vy

        if self.y > self.ground_y - 8:
            self.y = self.ground_y - 8
            self.vy = 0

    def draw(self):
        pyxel.cls(0)

        # 地面
        pyxel.rect(0, self.ground_y, 160, 120 - self.ground_y, 3)

        # プレイヤー
        pyxel.rect(self.x, self.y, 8, 8, 11)

        # 左パッド
        pyxel.rectb(self.dpad_x, self.dpad_y, self.dpad_w, self.dpad_h, 12)
        cx = self.dpad_x + self.dpad_w // 2
        cy = self.dpad_y + self.dpad_h // 2
        pyxel.rect(cx - 3, self.dpad_y + 4, 6, self.dpad_h - 8, 12)
        pyxel.rect(self.dpad_x + 4, cy - 3, self.dpad_w - 8, 6, 12)

        # 右ボタン
        pyxel.rectb(self.btn_x, self.btn_y, self.btn_w, self.btn_h, 8)
        pyxel.text(self.btn_x + 9, self.btn_y + 9, "A", 8)

        # デバッグで座標も出しとくと安心
        pyxel.text(0, 0, f"{pyxel.mouse_x},{pyxel.mouse_y}", 7)


App()
