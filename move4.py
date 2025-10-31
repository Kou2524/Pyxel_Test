import pyxel


# タッチが指定の四角の中にあるかどうか調べる関数
def touch_in_rect(touch_id, x, y, w, h):
    if not pyxel.touch(touch_id):
        return False
    tx = pyxel.touch_x(touch_id)
    ty = pyxel.touch_y(touch_id)
    return x <= tx < x + w and y <= ty < y + h


class App:
    def __init__(self):
        # 画面サイズはちょっと横長にしておく
        pyxel.init(160, 120, title="Touch Gamepad", fps=60)

        # プレイヤー
        self.x = 60
        self.y = 80
        self.vx = 0
        self.vy = 0

        # 簡単な床
        self.ground_y = 96

        # ゲームパッドの位置・サイズ
        # 左下に十字キー、右下にAボタンを出す
        self.dpad_x = 4
        self.dpad_y = 68
        self.dpad_size = 40  # 全体の大きさ

        self.btn_a_x = 120
        self.btn_a_y = 78
        self.btn_a_r = 14  # 円だけど当たりは四角でとる

        pyxel.run(self.update, self.draw)

    # 画面左下の十字キーのどれかを触ってるか判定する
    def _read_touch_gamepad(self):
        move_left = False
        move_right = False
        jump = False

        # 最大5本くらいタッチを見る
        for i in range(5):
            if not pyxel.touch(i):
                continue

            tx = pyxel.touch_x(i)
            ty = pyxel.touch_y(i)

            # Aボタン領域（右下）
            if (
                self.btn_a_x <= tx < self.btn_a_x + self.btn_a_r * 2
                and self.btn_a_y <= ty < self.btn_a_y + self.btn_a_r * 2
            ):
                jump = True
                continue

            # 十字キーのベース
            # ここでは十字を「中心＋上下左右の小さい四角」で見る
            cx = self.dpad_x + self.dpad_size // 2
            cy = self.dpad_y + self.dpad_size // 2
            pad_w = self.dpad_size // 3
            pad_h = self.dpad_size // 3

            # 左
            if cx - pad_w * 2 <= tx < cx - pad_w and cy - pad_h <= ty < cy + pad_h:
                move_left = True
            # 右
            if cx + pad_w <= tx < cx + pad_w * 2 and cy - pad_h <= ty < cy + pad_h:
                move_right = True
            # 上（今回はジャンプにしてもいいが一旦無視）
            # if cx - pad_w <= tx < cx + pad_w and cy - pad_h * 2 <= ty < cy - pad_h:
            #     jump = True

        return move_left, move_right, jump

    def update(self):
        # 入力の初期値
        move_left = False
        move_right = False
        jump_pressed = False

        # ① PCキーボードの入力
        if pyxel.btn(pyxel.KEY_LEFT):
            move_left = True
        if pyxel.btn(pyxel.KEY_RIGHT):
            move_right = True
        if pyxel.btnp(pyxel.KEY_SPACE):
            jump_pressed = True

        # ② Web/iPhone用のタッチ入力（↑を上書きしていい）
        t_left, t_right, t_jump = self._read_touch_gamepad()
        if t_left or t_right or t_jump:
            move_left = t_left
            move_right = t_right
            jump_pressed = t_jump

        # ③ 実際の横移動
        self.vx = 0
        speed = 1.5
        if move_left:
            self.vx = -speed
        elif move_right:
            self.vx = speed

        self.x += self.vx

        # 画面外に出ないように
        if self.x < 0:
            self.x = 0
        if self.x > pyxel.width - 8:
            self.x = pyxel.width - 8

        # ④ 重力＆ジャンプ
        gravity = 0.3
        self.vy += gravity

        # 地面にいるかどうか
        on_ground = self.y >= self.ground_y - 8 - 0.01

        # ジャンプ（地面にいるときだけ）
        if jump_pressed and on_ground:
            self.vy = -5

        self.y += self.vy

        # 地面で止める
        if self.y > self.ground_y - 8:
            self.y = self.ground_y - 8
            self.vy = 0

    def draw(self):
        pyxel.cls(0)

        # 背景
        pyxel.rect(0, self.ground_y, pyxel.width, pyxel.height - self.ground_y, 3)

        # プレイヤー
        pyxel.rect(self.x, self.y, 8, 8, 11)

        # --- ここからUI（ゲームパッド） ---
        # 十字キーのベース
        x = self.dpad_x
        y = self.dpad_y
        s = self.dpad_size
        pyxel.rectb(x, y, s, s, 5)

        cx = x + s // 2
        cy = y + s // 2
        w = s // 3
        h = s // 3

        # 左
        pyxel.rect(cx - w * 2, cy - h, w, h * 2, 5)
        # 右
        pyxel.rect(cx + w, cy - h, w, h * 2, 5)
        # 上
        pyxel.rect(cx - w, cy - h * 2, w * 2, h, 5)
        # 下
        pyxel.rect(cx - w, cy + h, w * 2, h, 5)

        # Aボタン（右下）
        pyxel.circ(self.btn_a_x + self.btn_a_r,
                   self.btn_a_y + self.btn_a_r,
                   self.btn_a_r,
                   8)
        pyxel.text(self.btn_a_x + self.btn_a_r - 2,
                   self.btn_a_y + self.btn_a_r - 2,
                   "A", 0)


App()
