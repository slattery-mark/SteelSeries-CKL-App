from json import load
from os import getenv
from time import sleep
from requests import Session, post
from random import choice

class CKL:
    def __init__(self):
        corePropsPath = getenv('PROGRAMDATA') + "\SteelSeries\SteelSeries Engine 3\coreProps.json" 
        self.sseAddress = f'http://{load(open(corePropsPath))["address"]}'
        self.game = 'CUSTOM_KEYBOARD_LIGHTING'
        self.game_display_name = 'Custom Keyboard Lighting'
        self.event = 'BITMAP_EVENT'
        self.bitmap = [
            [0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],
            [0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],
            [0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],
            [0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],
            [0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],
            [0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],
            [0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],
            [0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],
            [0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],
            [0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],
            [0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],
            [0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],
        ]
        self.registerGame()
        self.bindGameEvent()

    def getGameDisplayName(self):
        return self.game_display_name

    def bindGameEvent(self):
        endpoint = f'{self.sseAddress}/bind_game_event'
        payload = {
            "game": self.game,
            "event": self.event,
            "value_optional": r'"true"',
            "handlers": [
                {
                    "device-type": "rgb-per-key-zones",
                    "zone": "all",
                    "mode": "bitmap"
                }
            ]
        }
        post(endpoint, json=payload)

    def registerGame(self):    
        endpoint = f'{self.sseAddress}/game_metadata'
        payload = {
            "game" : self.game,
            "game_display_name" : self.game_display_name,
            "developer" : "yrfriendmark"
        }
        post(endpoint, json=payload)

    def removeGame(self):
        endpoint = f'{self.sseAddress}/remove_game'
        payload = {
            "game": self.game
        }
        post(endpoint, json=payload)

    def removeGameEvent(self):
        endpoint = f'{self.sseAddress}/remove_game_event'
        payload = {
            "game": self.game,
            "event" : self.event
        }
        post(endpoint, json=payload)

    def sendHeartbeat(self):
        endpoint = f'{self.sseAddress}/game_heartbeat'
        payload = {
                "game": self.game
        }
        post(endpoint, json=payload)

    def sendGameEvent(self, args, kill_switch):
        endpoint = f'{self.sseAddress}/game_event'
        frame = self.bitmap
        payload = {
            "game": self.game,
            "event": self.event,
            "data" : {
                "value" : 100,
                "frame" : {
                    "bitmap" : frame
                }
            }
        }
        rows = [
            [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21],
            [22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43],
            [44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65],
            [66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87],
            [88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109],
            [110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131]
        ]
        lighting_steps = 15
        dim_to_off = hold_light = light_to_full = [0,0,0]
        startup_colors = [[255, 0, 0], [255, 255, 0], [0, 255, 0], [0, 255, 255], [0, 0, 255], [255, 0, 255]]
        rgb_value = choice(startup_colors)
        rgb_modifier = 17

        with Session() as s:
            while not kill_switch.is_set():
                for row in reversed(rows):
                    if rgb_value[0] == 255:
                        if rgb_value[2] > 0: rgb_value[2] -= rgb_modifier 
                        elif rgb_value[1] < 255: rgb_value[1] += rgb_modifier
                        else: rgb_value[0] -= rgb_modifier
                    elif rgb_value[1] == 255:
                        if rgb_value[0] > 0: rgb_value[0] -= rgb_modifier
                        elif rgb_value[2] < 255: rgb_value[2] += rgb_modifier
                        else: rgb_value[1] -= rgb_modifier
                    elif rgb_value[2] == 255:
                        if rgb_value[1] > 0: rgb_value[1] -= rgb_modifier
                        elif rgb_value[0] < 255: rgb_value[0] += rgb_modifier
                        else: rgb_value[2] -= rgb_modifier

                    dim_to_off = hold_light
                    hold_light = light_to_full
                    light_to_full = [rgb_value[0]/lighting_steps, rgb_value[1]/lighting_steps,rgb_value[2]/lighting_steps]

                    for i in range(0, lighting_steps + 1):
                        for key in row:
                            frame[key] = [
                                light_to_full[0] * i,
                                light_to_full[1] * i,
                                light_to_full[2] * i,
                            ]
                            frame[(key + (21 * 2)) % 132] = [
                                dim_to_off[0] * ((lighting_steps) - i),
                                dim_to_off[1] * ((lighting_steps) - i),
                                dim_to_off[2] * ((lighting_steps) - i)
                            ]
                        s.post(endpoint, json=payload)
                        if kill_switch.is_set(): break
                        sleep(0.01)