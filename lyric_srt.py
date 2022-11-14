import os
import sys
import pygame
from sync_lyrics import Sync_Lyrics

def load_dev(i):
    global audio_filename
    txt = ''
    if os.path.exists("test.txt"):
        with open("test.txt", "r", encoding="UTF-8") as f:
            txt = f.read().splitlines()
        return txt[i]

audio_filename = load_dev(0) or input("오디오 파일 이름 혹은 경로를 입력하세요. :\n")
while not os.path.exists(audio_filename):
    audio_filename = input("존재하지 않는 파일 혹은 경로입니다. 다시 입력하세요.\n")

pygame.mixer.init()
pygame.mixer.music.load( audio_filename )
p = pygame.mixer.music
offset = -1

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
    global audio_filename
    audio_filename = input("\n오디오 파일 이름 혹은 경로를 입력하세요. :\n")
    while not os.path.exists(audio_filename):
        audio_filename = input("존재하지 않는 파일 혹은 경로입니다. 다시 입력하세요.\n")


def sync_lyrics():
    global p, audio_filename, title
    p.unload()

    lyric_filename = load_dev(1) or input("등록할 스크립트 파일이름 혹은 경로를 입력하세요. :\n")
    while not os.path.exists(lyric_filename):
        lyric_filename = input("존재하지 않는 파일 혹은 경로입니다. 다시 입력하세요.\n")
    lyrics = []
    try:
        with open(lyric_filename, "r", encoding='UTF-8') as f:
            lyrics = f.read().splitlines()
    except Exception as e:
        print("file is not readable.", file = sys.stderr)
        raise e
    a = Sync_Lyrics(audio_filename, lyrics)
    a.sync_lyrics()
    title = True
    
title = True
cmds = {'s': start, 'p': pause, 'up':unpause, 'r':reset, 'g':get_pos, 'sync':sync_lyrics, 'change': change,  'q': quit}
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
    