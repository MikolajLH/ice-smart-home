import sys
import time
import os
import platform

import Ice
import DevicesIce


DEVICES = {
    "camera-1": (DevicesIce.CameraPrx, "Camera1.Proxy"),
    "bulb-1": (DevicesIce.BulbPrx, "Bulb1.Proxy"),
    "led-bulb-1": (DevicesIce.LEDBulbPrx, "LEDBulb1.Proxy"),
    "rgb-bulb-1": (DevicesIce.RGBBulbPrx, "RGBBulb1.Proxy"),

    "camera-2": (DevicesIce.CameraPrx, "Camera2.Proxy"),
    "bulb-2": (DevicesIce.BulbPrx, "Bulb2.Proxy"),
    "led-bulb-2": (DevicesIce.LEDBulbPrx, "LEDBulb2.Proxy"),
    "rgb-bulb-2": (DevicesIce.RGBBulbPrx, "RGBBulb2.Proxy"),
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
            yield None


def get_ice_obj(device_name: str, communicator):
    if device_name in DEVICES:
        obj_type, obj_property = DEVICES[device_name]
        proxy = communicator.propertyToProxy(obj_property)
        return obj_type.checkedCast(proxy), obj_type
    return None, None


def handle_camera(obj):
    clrscr()
    print("Camera menu")
    print("Possible commands:")
    print(" - preview - shows camera feed")
    print(" - info - prints device's info")
    print(" - q - deselect device")
    inp = input(">> ")
    if inp == "info":
        print(obj.info())
        input("Press enter to continue")
    if inp == "q":
        return None
    if inp == "preview":
        preview_mode(obj)
    return DevicesIce.CameraPrx

def handle_led_bulb(obj):
    clrscr()
    print("LED Bulb menu")
    print("Possible commands:")
    print(" - info - prints device's info")
    print(" - turnon")
    print(" - turnoff")
    print(" - switch")
    print(" - ison")
    print(" - get")
    print(" - set <brightness>")
    print(" - set-default <brightness>")
    print(" - q - deselect device")
    inp = input(">> ")
    cmd, *args = inp.split()
    if cmd == "info":
        print(obj.info())
    if cmd == "turnon":
        obj.lightOn()
        print("Light turned on")
    if cmd == "turnoff":
        obj.lightOff()
        print("Light turned off")
    if cmd == "switch":
        obj.switchLight()
        on = obj.isOn()
        print(f"Light bulb turned {'on' if on else 'off'}")
    if cmd == "ison":
        print(obj.isOn())
    if cmd == "get":
        b = obj.getBrightness()
        print(f"Brightness is {b}")
    if cmd == "set" and len(args) == 1:
        try:
            b = float(args[0])
            obj.setBrightness(b)
        except Exception as e:
            print("Exception:", e)
    if cmd == "set-default" and len(args) == 1:
        try:
            b = float(args[0])
            obj.setDefaultBrightness(b)
            print("Default brightness set to", b)
        except Exception as e:
            print("Exception:", e)
    if cmd == "q":
        return None
    
    input("Press enter to continue")    
    return DevicesIce.LEDBulbPrx


def handle_rgb_bulb(obj):
    clrscr()
    print("RGB Bulb menu")
    print("Possible commands:")
    print(" - info - prints device's info")
    print(" - turnon")
    print(" - turnoff")
    print(" - switch")
    print(" - ison")
    print(" - get-color")
    print(" - set-color <r> <g> <b>")
    print(" - set-default <r> <g> <b>")
    print(" - q - deselect device")
    inp = input(">> ")
    cmd, *args = inp.split()
    if cmd == "info":
        print(obj.info())
    if cmd == "turnon":
        obj.lightOn()
        print("Light turned on")
    if cmd == "turnoff":
        obj.lightOff()
        print("Light turned off")
    if cmd == "switch":
        obj.switchLight()
        on = obj.isOn()
        print(f"Light bulb turned {'on' if on else 'off'}")
    if cmd == "ison":
        print(obj.isOn())
    if cmd == "get-color":
        print(obj.getColor())
    if cmd == "set-color" and len(args) == 3:
        try:
            r = float(args[0])
            g = float(args[1])
            b = float(args[2])
            obj.setColor(DevicesIce.RGBColor(r,g,b))
        except Exception as e:
            print("Exception:", e)
    if cmd == "set-default" and len(args) == 3:
        try:
            r = float(args[0])
            g = float(args[1])
            b = float(args[2])
            obj.setDefaultColor(DevicesIce.RGBColor(r,g,b))
        except Exception as e:
            print("Exception:", e)

    if cmd == "q":
        return None
    
    input("Press enter to continue")
    return DevicesIce.RGBBulbPrx


def handle_bulb(obj):
    clrscr()
    print("Bulb menu")
    print("Possible commands:")
    print(" - info - prints device's info")
    print(" - turnon")
    print(" - turnoff")
    print(" - switch")
    print(" - ison")
    print(" - q - deselect device")
    inp = input(">> ")
    if inp == "info":
        print(obj.info())
    if inp == "turnon":
        obj.lightOn()
        print("Light turned on")
    if inp == "turnoff":
        obj.lightOff()
        print("Light turned off")
    if inp == "switch":
        obj.switchLight()
        on = obj.isOn()
        print(f"Light bulb turned {'on' if on else 'off'}")
    if inp == "ison":
        print(obj.isOn())
    if inp == "q":
        return None
    
    input("Press enter to continue")
    return DevicesIce.BulbPrx
    

def handle_device(obj):
    clrscr()
    print("Device menu")
    print("Possible commands:")
    print(" - info - prints device's info")
    print(" - q - deselect device")
    inp = input(">> ")
    if inp == "q":
        return None
    if inp == "info":
        print(obj.info())
    
    input("Press enter to continue")
    return DevicesIce.DevicePrx


def main():
    obj, obj_type = None, None
    with Ice.initialize(sys.argv) as communicator:
        print("Smart Home menu")
        print("possible commands:")
        print(" - select <device> - selects given device")
        print(" - list - lists possible devices")
        print(" - list-info")
        print(" - exit - exits program")
        print()
        for inp in loop():
            if inp is None:
                continue
            cmd, args = inp
            match (cmd, args):
                case ("select", [name]):
                    obj, obj_type = get_ice_obj(name, communicator)
                    if obj is None or obj_type is None:
                        print("No such device")
                        continue
                case ("list", _):
                    for dv in DEVICES.keys():
                        print(dv)
                    continue
                case ("list-info", _):
                    for dv in DEVICES.keys():
                        print(dv)
                        temp_obj, _ = get_ice_obj(dv, communicator)
                        print(temp_obj.info())
                        print()
                    continue

            while obj is not None and obj_type is not None:
                try:
                    if issubclass(obj_type, DevicesIce.CameraPrx):
                        obj_type = handle_camera(obj)

                    elif issubclass(obj_type, DevicesIce.RGBBulbPrx):
                        obj_type = handle_rgb_bulb(obj)

                    elif issubclass(obj_type, DevicesIce.LEDBulbPrx):
                        obj_type = handle_led_bulb(obj)

                    elif issubclass(obj_type, DevicesIce.BulbPrx):
                        obj_type = handle_bulb(obj)
                    
                    elif issubclass(obj_type, DevicesIce.DevicePrx):
                        obj_type = handle_device(obj)
                    
                    else:
                        print("Unsupported device")
                        break
                except Exception as e:
                    print("Exception occured:", e)
                    break

            print("deselected")
            obj = None
            obj_type = None
            clrscr()
            print("Smart Home menu")
            print("possible commands:")
            print(" - select <device> - selects given device")
            print(" - list - lists possible devices")
            print(" - list-info")
            print(" - exit - exits program")
            print()
            


if __name__ == "__main__":
    main()