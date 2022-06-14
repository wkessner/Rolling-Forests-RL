from time import sleep
from selenium import webdriver
from io import BytesIO
import base64
import numpy as np
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

class WebInterface:
    def __init__(self, game_url='https://rollingforests.rayhanadev.repl.co/', chrome_driver_path="/usr/bin/chromedriver"):
        # sleep(1)
        self.game_url = game_url
        chrome_options = Options()
        chrome_options.add_argument("disable-infobars")
        chrome_options.add_argument("--mute-audio")
        chrome_options.add_argument('--no-sandbox')

        self._driver = webdriver.Chrome(
            executable_path=chrome_driver_path, chrome_options=chrome_options)
        self._driver.set_window_position(x=-10, y=0)
        self._driver.get(game_url)
        self._driver.execute_script("""doDifficultyLogic = function doDifficultyLogic() {
  if (score === 0) {
    treeReleaseInterval = 0.5;
  } else if (treeReleaseInterval > 0.2) {
    treeReleaseInterval -= Math.log(score) / 1000
  }
}""")
        self._driver.execute_script("rollingSpeed = 0.003")

    def end(self):
        self._driver.close()

    def grab_screen(self):
        screen = np.asarray(Image.open(BytesIO(base64.b64decode(self._driver.get_screenshot_as_base64()))))
        return screen[..., :3]

    def go_left(self):
        # print("Going left")
        self._driver.find_element_by_tag_name("body").send_keys(Keys.ARROW_LEFT)

    def go_right(self):
        # print("Going right")
        self._driver.find_element_by_tag_name(
            "body").send_keys(Keys.ARROW_RIGHT)

    def jump(self):
        # print("Jumping")
        self._driver.find_element_by_tag_name("body").send_keys(Keys.SPACE)

    def pause(self):
        self._driver.find_element_by_tag_name("body").send_keys("P")