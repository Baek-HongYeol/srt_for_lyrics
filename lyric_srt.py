import os
import sys
from pygame import mixer
from sync_lyrics import Sync_Lyrics

def load_dev(i):
    global audio_filename
    txt = ''
    if os.path.exists("test.txt"):
        with open("test.txt", "r", encoding="UTF-8") as f:
            txt = f.read().splitlines()
        return txt[i]

def init_audio():
    global p, audio_filename, sample_rate
    audio_filename = load_dev(0) or input("오디오 파일 이름 혹은 경로를 입력하세요. :\n")
    while not os.path.exists(audio_filename):
        audio_filename = input("존재하지 않는 파일 혹은 경로입니다. \n오디오 파일 이름 혹은 경로를 입력하세요. :\n")
    
    while True:
        try:
            sample_rate = load_dev(1) or int(input("오디오 sample rate를 입력하세요.(44100, 48000): "))
            sample_rate = int(sample_rate)
            break
        except Exception as e:
            print(e)

    if sample_rate:
        mixer.init(frequency=sample_rate)
    else:
        sample_rate = 44100
        mixer.init()
    mixer.music.load( audio_filename )
    p = mixer.music

# TODO get audio property from audio file. ex) 44.1kHz/48kHz
########### init ###########

offset = -1
sample_rate = -1
init_audio()

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
    global p, audio_filename
    p.stop()
    mixer.music.unload()
    init_audio()
    

def sync_lyrics():
    global p, audio_filename, title, sample_rate
    p.unload()

    lyric_filename = load_dev(2) or input("등록할 스크립트 파일이름 혹은 경로를 입력하세요. :\n")
    while not os.path.exists(lyric_filename):
        lyric_filename = input("존재하지 않는 파일 혹은 경로입니다. 다시 입력하세요.\n")
    lyrics = []
    try:
        with open(lyric_filename, "r", encoding='UTF-8') as f:
            lyrics = f.read().splitlines()
    except Exception as e:
        print("file is not readable.", file = sys.stderr)
        raise e
    audio_options = {'frequency': sample_rate}
    a = Sync_Lyrics(audio_filename, audio_options, lyrics)
    a.sync_lyrics()
    title = True


########### Start ###########
title = True
cmds = {'s': start, 'p': pause, 'up':unpause, 'r':reset, 'g':get_pos, 'sync':sync_lyrics, 'change': change, 'q': quit}
while True:
    if title:
        print("\nThis page is for Audio Player! \nThe commands are below:")
        title = False
    ch = input("\
        s: start, p: pause, up: unpause, r: reset, g: get_pos, set n.n: set_pos(n.n), \n\
        change: change_audio_file, sync: sync_lyrics, q: quit\n")
    if ch in cmds.keys():
        cmds[ch]()
    elif ch.startswith('set '):
        pos = ch.split(' ')[1]
        set_pos(pos)
    print('')
    