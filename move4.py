import pyxel


def touch_pos_list(max_touches=5):
    """今あるタッチの(x, y)を全部リストで返す"""
    pts = []
    for i in range(max_touches):
        if pyxel.touch(i):
            pts.append((i, pyxel.touch_x(i), pyxel.touch_y(i)))
    return pts


class App:
    def __init__(self):
        pyxel.init(160, 120, title="Touch Gamepad", fps=60)

        self.x = 60
        self.y = 70
        self.vy = 0
        self.ground_y = 96

        # パッドの基準位置（ちょっと上げる）
        self.dpad_x = 4
        self.dpad_y = 60   # ← ここを少し上にした
        self.dpad_w = 50
        self.dpad_h = 50

        self.btn_x = 110
        self.btn_y = 60    # ← ここも上にした
        self.btn_size = 28

        pyxel.run(self.update, self.draw)

    def update(self):
        move_left = False
        move_right = False
        jump = False

        # 1) PCキーボード
        if pyxel.btn(pyxel.KEY_LEFT):
            move_left = True
        if pyxel.btn(pyxel.KEY_RIGHT):
            move_right = True
        if pyxel.btnp(pyxel.KEY_SPACE):
            jump = True

        # 2) タッチを全部見る
        for tid, tx, ty in touch_pos_list():
            # 左パッド（ちょっと大きめにとる）
            if (
                self.dpad_x <= tx <= self.dpad_x + self.dpad_w
                and self.dpad_y <= ty <= self.dpad_y + self.dpad_h
            ):
                # 真ん中より左 → 左
                if tx < self.dpad_x + self.dpad_w / 2:
                    move_left = True
                else:
                    move_right = True

            # 右ボタン
            if (
                self.btn_x <= tx <= self.btn_x + self.btn_size
                and self.btn_y <= ty <= self.btn_y + self.btn_size
            ):
                jump = True

        # 横移動
        speed = 1.5
        if move_left:
            self.x -= speed
        if move_right:
            self.x += speed

        # 重力
        self.vy += 0.3

        # ジャンプ（地面のときだけ）
        on_ground = self.y >= self.ground_y - 8 - 0.01
        if jump and on_ground:
            self.vy = -5

        self.y += self.vy

        # 地面で止める
        if self.y > self.ground_y - 8:
            self.y = self.ground_y - 8
            self.vy = 0

        # はみ出し防止
        if self.x < 0:
            self.x = 0
        if self.x > pyxel.width - 8:
            self.x = pyxel.width - 8

    def draw(self):
        pyxel.cls(0)

        # 地面
        pyxel.rect(0, self.ground_y, pyxel.width, 120 - self.ground_y, 3)

        # プレイヤー
        pyxel.rect(self.x, self.y, 8, 8, 11)

        # --- パッド描画（見た目だけ） ---
        # 左
        pyxel.rectb(self.dpad_x, self.dpad_y, self.dpad_w, self.dpad_h, 12)
        # 縦棒
        pyxel.rect(self.dpad_x + self.dpad_w // 2 - 4,
                   self.dpad_y + 5,
                   8,
                   self.dpad_h - 10,
                   12)
        # 横棒
        pyxel.rect(self.dpad_x + 5,
                   self.dpad_y + self.dpad_h // 2 - 4,
                   self.dpad_w - 10,
                   8,
                   12)

        # 右ボタン
        pyxel.rectb(self.btn_x, self.btn_y, self.btn_size, self.btn_size, 8)
        pyxel.text(self.btn_x + 9, self.btn_y + 8, "A", 8)


App()
