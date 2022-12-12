from typing import Tuple, List
import pyautogui as pag
import time
import math

class AutoInput:

    _velocity = 50 # px / sec
    _sleep_interval = 1

    def __init__(self):
        self.status = 0

    @classmethod
    def set_velocity(cls, velocity):
        cls._velocity = velocity

    def _duration(self, x_coord: int, y_coord: int) -> int:
        pos = pag.position()
        current_x, current_y = pos.x, pos.y
        distance = math.sqrt((x_coord - current_x) ** 2 + (y_coord - current_y) ** 2)
        duration = distance / self._velocity
        return duration

    def move_to(self, x_coord: int, y_coord: int, duration: float = 1, auto_calc_duration: bool =True, tween=pag.easeInOutQuad):
        if auto_calc_duration:
            duration = self._duration(x_coord, y_coord)
        pag.moveTo(x_coord, y_coord, duration=duration, tween=tween)
        self.sleep(self._sleep_interval) 
        return self
    
    def click(self, x_coord: int, y_coord: int, tween=pag.easeInOutQuad):
        duration = self._duration(x_coord, y_coord)
        pag.click(x_coord, y_coord, duration=duration, tween=tween,)
        self.sleep(self._sleep_interval) 
        return self
    
    def sleep(self, sleep_time: float):
        time.sleep(sleep_time)
        return self

    def send_keys(self, string: str, interval: float = 0.1):
        pag.typewrite(string, interval=interval)
        self.sleep(self._sleep_interval) 
        return self
    
    def hankaku(self):
        pag.press("hanja")
        self.sleep(self._sleep_interval) 
        return self

    def zenkaku(self):
        pag.press("kanji")
        self.sleep(self._sleep_interval) 
        return self
    
    def enter(self, count: int = 1):
        self.press("enter", count)
        self.sleep(self._sleep_interval) 
        return self
    
    def down(self, count: int = 1):
        self.press("down", count)
        self.sleep(self._sleep_interval) 
        return self

    def tab(self, count: int = 1):
        self.press("tab", count)
        self.sleep(self._sleep_interval) 
        return self

    def scroll(self, clicks: int, count: int = 1, interval: float = 0.25):
        for _ in range(count):
            pag.scroll(clicks)
            self.sleep(interval)
        return self
    
    def press(self, key: str | List[str], count: int = 1, interval: float = 0.1):
        for i in range(count):
            pag.press(key)
            self.sleep(interval)
        self.sleep(self._sleep_interval - interval)
        return self
 
    def drag(self, coord_from: Tuple[int, int], coord_to: Tuple[int, int]):
        self.move_to(*coord_from, duration=self._duration(*coord_from), tween=pag.easeInOutQuad)
        pag.mouseDown(*coord_from)
        self.move_to(*coord_to, duration=self._duration(*coord_from), tween=pag.easeInOutQuad)
        pag.mouseUp(*coord_to)
        self.sleep(self._sleep_interval) 
        return self

    def hotkey(self, *keys: str):
        """
        Caution:
                self.hotkey("shift", "alt", "down")
            etc doesn't work properly(the shift key doesn't work). Instead, use
                self.hotkey("shiftleft", "shiftright", "alt", "down")
            (both shiftleft & shiftright have to be pressed simultaneously).
            On the other hand, capitalizing letters like
                self.hotkey("shift", z)
            works.
            For more information please refer to
            https://stackoverflow.com/questions/56949628/keydown-function-not-working-with-shift-key.
        """
        pag.hotkey(*keys)
        self.sleep(self._sleep_interval)
        return self

    def run(self, op_chain) -> int:
        return self.status
    

if __name__ == "__main__":

    auto = AutoInput()
    status = auto.run(
        auto
            .sleep(1)
            .move_to(90, 150, duration=1, auto_calc_duration=False)
            .sleep(1)
            .move_to(550, 50)
    )
    print(status)