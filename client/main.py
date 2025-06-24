import sys
import time
import os
import platform

import Ice
import DevicesIce


DEVICES = {
    "camera": (DevicesIce.CameraPrx, "Camera.Proxy"),
    "bulb": (DevicesIce.BulbPrx, "Bulb.Proxy"),
    "led-bulb": (DevicesIce.LEDBulbPrx, "LEDBulb.Proxy"),
    "rgb-bulb": (DevicesIce.RGBBulbPrx, "RGBBulb.Proxy"),
}

def clrscr():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def preview_mode(camera):
    def matrix_to_ascii(matrix):
        scale = "@%#*+=-:. "
        rows = []
        for row in matrix:
            ascii_row = "".join(scale[int(val * (len(scale) - 1))] for val in row)
            rows.append(ascii_row)

        return "\n".join(rows)
    while True:
        try:
            clrscr()
            frame = camera.getFrame()
            img = []
            row = []
            for i, p in enumerate(frame.buffer):
                row.append(p.value)
                if i % frame.cols == frame.cols - 1:
                    img.append(row)
                    row = []
                
            print(matrix_to_ascii(img))
            time.sleep(0.3)
        except KeyboardInterrupt:
            return


def loop():
    while True:
        try:
            inp = input(">> ")
            cmd, *args = inp.split()
            if cmd == "exit" and len(args) == 0:
                return
            yield (cmd, args)
        except EOFError:
            return
        except KeyboardInterrupt:
            return
        except Exception as e:
            print(e)
            yield None, None


def get_ice_obj(device_name: str, communicator):
    if device_name in DEVICES:
        obj_type, obj_property = DEVICES[device_name]
        proxy = communicator.propertyToProxy(obj_property)
        return obj_type.checkedCast(proxy), obj_type
    return None, None


def main():
    obj, obj_type = None, None
    with Ice.initialize(sys.argv) as communicator:
        for cmd, args  in loop():
            if cmd is None or args is None:
                continue
            match (cmd, args):
                case ("dev", [name]):
                    obj, obj_type = get_ice_obj(name, communicator)
                    print(f"{name} selected")
                    print(obj.info())
                case ("undev", []):
                    obj, obj_type = None, None
                    print("deselected")
                case _:
                    print(cmd, args)
        
            if obj is None or obj_type is None:
                continue

            if issubclass(obj_type, DevicesIce.DevicePrx):
                if cmd == "info":
                    print(obj.info())
            
            if issubclass(obj_type, DevicesIce.CameraPrx):
                if cmd == "preview" and len(args) == 0:
                    preview_mode(obj)

            if issubclass(obj_type, DevicesIce.BulbPrx):
                if cmd == "switch":
                    obj.switchLight()
                    print(obj.isOn())
                

            if issubclass(obj_type, DevicesIce.LEDBulbPrx):
                pass

            if issubclass(obj_type, DevicesIce.BulbPrx):
                pass
            
            



if __name__ == "__main__":
    main()