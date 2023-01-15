import os
from pygame import mixer
from sync_lyrics import Sync_Lyrics
from config import MyConfig

def load_dev(i):
    txt = ''
    if os.path.exists("test.txt"):
        with open("test.txt", "r", encoding="UTF-8") as f:
            txt = f.read().splitlines()
        return txt[i]

def init_audio():
    global p, config
    audio_filename = config.audio_filename
    sample_rate = config.sample_rate
    if isinstance(sample_rate, int) and sample_rate > 0:
        print("sample_rate cannot be recognized. using 44.1khz.")
        mixer.init(frequency=sample_rate)
    else:
        config.sample_rate = 44100
        mixer.init()
    mixer.music.load( audio_filename )
    p = mixer.music

def init():
    init_audio()

# TODO get audio property from audio file. ex) 44.1kHz/48kHz
########### init ###########

offset = -1
sample_rate = -1
config = MyConfig()
init()

############################


def start():
    global p
    if p.get_pos() != -1:
        p.rewind()
    else:
        p.play()

def pause():
    global p
    p.pause()
    

def set_pos(pos):
    global p, offset
    try:
        pos = float(pos)
    except Exception as e:
        print("Wrong position!:", pos)
        print(e)
        return
    p.play()
    p.set_pos(pos)
    offset = pos

def get_pos():
    global p, offset
    t = p.get_pos()
    if offset != -1:
        t += int(offset*1000)
    print(t)
    return t


def unpause():
    global p
    if p.get_pos() == -1:
        print("not started yet")
    else:
        p.unpause()

def reset():
    global p, offset
    p.stop()
    offset = -1

def change():
    global p, config
    p.stop()
    mixer.music.unload()
    config.find_audio_file(True)
    init_audio()


def sync_lyrics():
    global p, title, config
    p.unload()

    
    a = Sync_Lyrics(config)
    a.sync_lyrics()
    title = True


########### Start ###########
title = True
cmds = {'s': start, 'p': pause, 'up':unpause, 'r':reset, 'g':get_pos, 'sync':sync_lyrics, 'change': change, 'q': quit}
while True:
    if title:
        print("\nThis page is for Audio Player! \nThe commands are below:")
        title = False
    ch = input( f"\t[ s: start, p: pause, up: unpause, r: reset, g: get_pos, set n.n: set_pos(n.n), ]\n"
                f"\t[ change: change_audio_file, sync: sync_lyrics, q: quit ]\n")
    if ch in cmds.keys():
        cmds[ch]()
    elif ch.startswith('set '):
        pos = ch.split(' ')[1]
        set_pos(pos)
    print('')
    