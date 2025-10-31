import pyxel


class App:
    def __init__(self):
      # 画面サイズは好きに変えてね
      pyxel.init(160, 120, title="move4")

      # プレイヤーの位置とか
      self.x = 80
      self.y = 60
      self.speed = 2

      pyxel.run(self.update, self.draw)

    def update(self):
        # --- ここが今回のポイント ---
        # Web版(pyxel.js)には gamepad_axis_value がないので、
        # 無かったら 0 を入れておく
        if hasattr(pyxel, "gamepad_axis_value"):
            axis_x = pyxel.gamepad_axis_value(0, 0)  # 左スティックX
        else:
            axis_x = 0
        # --- ここまで ---

        # ゲームパッドが無い環境でも動くように、キーボードも見る
        # （iPhoneだとここがメインになる）
        if pyxel.btn(pyxel.KEY_LEFT):
            axis_x = -1
        elif pyxel.btn(pyxel.KEY_RIGHT):
            axis_x = 1

        # 位置を更新
        self.x += axis_x * self.speed

        # 画面外に出ないように
        if self.x < 0:
            self.x = 0
        if self.x > pyxel.width - 8:
            self.x = pyxel.width - 8

    def draw(self):
        pyxel.cls(0)
        # プレイヤーを描く（四角で仮）
        pyxel.rect(self.x, self.y, 8, 8, 11)

#test

App()
