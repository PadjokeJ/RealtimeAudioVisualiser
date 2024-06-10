#pynput initialise
from pynput import keyboard
kb = keyboard.Controller()


# notes to genshin implementation -> genshin doesn't detect the inputs?
n = [["y", "Y", "x", "X","c", "v", "V", "b", "B", "n", "N", "m"], ["a", "A", "s", "S", "d", "f", "F", "g", "G", "h", "H", "j"], ["q", "Q", "w", "W", "e", "r", "R", "t", "T", "z", "Z", "u"]]
def playPitch(octave, note):
    try:
        kb.press(n[octave-3][note])
        return n[octave-3][note]
    except:
        print("Note out of range")
        return "l" # unused key --> so it doesn't return null to pynput who won't be happy 

def releaseAllKeys(keys):
    for i in keys:
        kb.release(i) #release previous used keys