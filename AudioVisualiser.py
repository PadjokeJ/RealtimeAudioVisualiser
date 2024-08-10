print("import time at 0.0")
import time
print("import pyaudio at " + str(time.thread_time()))
import pyaudio
print("import numpy at " + str(time.thread_time()))
import numpy as np
print("import pygame at " + str(time.thread_time()))
import pygame
print("finished imports at "  + str(time.thread_time()))

#pygame initialise
pygame.init()
pygame.mixer.init()
scr = (width, height) = (1024, 1024)
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
print("intit pygame done " + str(time.thread_time()))

#PyAudio initialise
p=pyaudio.PyAudio()
FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 44100
CHUNK = 2000 
print("intit pyaudio done " + str(time.thread_time()))

#Get all audio devices for debugging, uncomment to find your input device
#for i in range(p.get_device_count()):
#    print(p.get_device_info_by_index(i))
#print(p.get_default_input_device_info())
stream = p.open(format = FORMAT,
            channels = CHANNELS,
            rate = RATE,
            input = True,
            output= False,
            input_device_index= 1,
            frames_per_buffer = CHUNK)
stop = True
print("audio stream open " + str(time.thread_time()))

#frequency to note+octave string
A4 = 440
C0 = A4*pow(2, -4.75)
name = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
def pitch(freq):
    try:
        z = round(12*np.log2(freq/C0))
    except:
        z = 0
    octave = z // 12
    n = z % 12
    return name[n] + str(octave)

#frequency to octave number
def octave(f):
    y = round(12*np.log2(f/C0))
    octave = y // 12
    return octave

# frequency to note number (half tones)
def note(f):
    n = round(12*np.log2(f/C0)) % 12
    return n

    
#update the frequency(data) to be in tune with current audio    
def update_line(s):
    try:
        data = np.fft.rfft(np.fromstring(
            stream.read(CHUNK), dtype=np.float32)
        )[:s] #limit data size to reduce lag 
    except IOError:
        pass
    data = np.log10(np.sqrt(
        np.real(data)**2+np.imag(data)**2) / CHUNK) * 10
    return data
print("finished declaring " + str(time.thread_time()))

font = pygame.font.Font('freesansbold.ttf', 8)
notes = []
keys = []

h = 0
h2 = 0
screen.fill((255, 255, 255))

size = 10


while stop:
    keys = []
    val = []
    clock.tick(120)
    screen.fill((255, 255, 255))

    data = update_line(1000//size) #fetch new audio data
    notes.clear()
    pygame.draw.line(screen, (0, 125, 0), (0, height/2), (1024, height/2), 5)
    for j in range(0, 1000//size):
        h  = (h *0 + ((data[j    ] + 60)/10) ** 6)/8

        if abs(data[j    ]+60) < 15: # remove noise
            h = 0
        if(h - h2 > 30 ): # select freqs that are above the rest
            notes.append(j * 21.62) # set them as notes
            pygame.draw.circle(screen, (255, 0, 0), ((j)*size, height/2 - h), 8)

            text = font.render(pitch(j* 21.62), True, (120, 0, 0))  # show on screen the note of a frequency
            screen.blit(text, (j *size + 10, height/2 - h + 15))

        pygame.draw.line(screen, (0  , 0, 0), ((j-1)*size, height/2 - h2), ((j)*size, height/2 - h), 5) # render audio waves
        h2 = h
    text = font.render("Fps: " + str(round(clock.get_fps())), True, (0, 0, 0))  # show frames
    screen.blit(text, (0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stop = False
            break
    if not stop:
        break
    _fps = font.render(f"{clock.get_fps()} fps", True, (0, 0, 0))
    screen.blit(_fps, (0, 0))
    pygame.display.flip()
#end of program --> close unneeded ressources
stream.stop_stream()
stream.close()
p.terminate()
