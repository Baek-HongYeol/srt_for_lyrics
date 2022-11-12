import os
import sys
import pygame
from sync_lyrics import Sync_Lyrics

audio_filename = "C:/Users/BoBHongY/Downloads/POPSTAR X THE BADDEST.mp3"

pygame.mixer.init()
pygame.mixer.music.load( audio_filename )
p = pygame.mixer.music

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
    global p
    try:
        pos = float(pos)
    except Exception as e:
        print("Wrong position!:", pos)
        print(e)
    p.rewind()
    p.set_pos(pos)

def get_pos():
    global p
    t = p.get_pos()
    print(t)
    return t


def unpause():
    global p
    p.unpause()

def rewind():
    global p
    p.rewind()

def sync_lyrics():
    global p, audio_filename, title
    p.unload()
    lyric_filename = "C:/Users/BoBHongY/Downloads/POPSTAR X THE BADDEST [LILPA] cover.txt"
    lyrics = []
    try:
        with open(lyric_filename, "r", encoding='UTF-8') as f:
            lyrics = f.read().splitlines()
    except Exception as e:
        print("file is not readable.", file = sys.stderr)
        raise e
    a = Sync_Lyrics('' , lyrics)
    a.sync_lyrics()
    title = True
    
title = True
cmds = {'s': start, 'p': pause, 'up':unpause, 'r':rewind, 'g':get_pos, 'sync':sync_lyrics,  'q': quit}
while True:
    if title:
        print("This page is for Audio Player! The commands are below.")
        title = False
    ch = input("s: start, p: pause, up: unpause, r: rewind, g: get_pos, set n.n: set_pos(n.n), sync: sync_process, q: quit\n")
    if ch in cmds.keys():
        cmds[ch]()
    elif ch.startswith('set '):
        pos = ch.split(' ')[1]
        set_pos(pos)
    print('')
    