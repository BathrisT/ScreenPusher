from pprint import pprint

import pyautogui
import telebot
import time

import config


class ScreenPusher:
    def __init__(self, token, user_list):
        self.BOT = telebot.TeleBot(token=token)
        self.USER_LIST = user_list

    def make_screenshot(self, path_for_save):
        myScreenshot = pyautogui.screenshot()
        myScreenshot.save(path_for_save)
        time.sleep(0.3)

    def notify_users(self, text=None, path_to_img=None):
        if text is None: text = ""
        if path_to_img != None:
            img = open(path_to_img, 'rb')
            file_id = 0
            for user in self.USER_LIST:
                try:
                    if file_id == 0:
                        file_id = self.BOT.send_photo(user, img, caption=text).json['photo'][-1]['file_id']
                    else:
                        self.BOT.send_photo(user, file_id, caption=text)
                except Exception as e:
                    print(e)
            img.close()
        else:
            for user in self.USER_LIST:
                try:
                    self.BOT.send_message(user, text)
                except Exception as e:
                    print(e)

    def screenshotWorker(self, text="Новый скриншот", timeout=3):
        while True:
            time.sleep(timeout)
            try:
                self.make_screenshot("./tmp.jpg")
                self.notify_users(text=text, path_to_img="./tmp.jpg")
            except Exception as e:
                self.notify_users(text=f"Произошла ошибка: {e}")



if __name__ == '__main__':
    sp = ScreenPusher(token=config.BOT_TOKEN, user_list=config.USER_LIST)
    sp.screenshotWorker(text=config.TEXT_FOR_SEND, timeout=config.TIMEOUT)
