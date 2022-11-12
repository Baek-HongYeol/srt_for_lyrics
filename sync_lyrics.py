import pygame
import os
from typing import List, Tuple

class Sync_Lyrics:
    def __init__(self, audio_filename:str = None, script:List[str] = None) -> None:
        if audio_filename is None:
            raise ValueError("audio_file is required for sync_lyrics")

        self.audio_filename = audio_filename
        if not os.path.exists(self.audio_filename):
            raise FileNotFoundError("audio_file is not Exists!")
        if script is None:
            raise ValueError("script is required for sync_lyrics")
        
        self.script = script
        self.is_pause = True
        self.sync_started = False
        pygame.mixer.init()
        pygame.mixer.music.load( self.audio_filename )
        self.p = pygame.mixer.music
        self.offset = -1
        print("This page is for making srt file sync with audio file!")
    
    def get_srt_filename(self):
        path = self.audio_filename
        ext_idx = path.rfind('.')
        if ext_idx != -1:
            path = path[:ext_idx]
        name_idx = path.rfind('/')
        if name_idx != -1:
            path = path[name_idx+1:]
        else:
            name_idx = path.rfind('\\')
            if name_idx != -1:
                path = path[name_idx+1:]
        return path+".srt"

    def start(self):
        self.p.play()
        self.offset = -1
        self.is_pause = False

    def pause(self):
        self.p.pause()
        self.is_pause = True

    def unpause(self):
        self.p.unpause()
        self.is_pause = False
    
    def set_pos(self, pos:float):
        try:
            pos = float(pos)
        except Exception as e:
            print("Wrong position!:", pos)
            print(e)
        self.p.play()
        self.p.set_pos(pos)
        self.offset = pos

    def get_pos(self):
        t = self.p.get_pos()
        if self.offset != -1:
            t += int(self.offset*1000)
        print(t)
        return t


    def timestamp_to_string(self, ms: int):
        if type(ms) is not int:
            return ''
        sec = ms // 1000
        ms = ms% 1000
        min = sec // 60
        sec = sec % 60
        hour = min // 60
        min = min % 60
        return '%02d:%02d:%02d,%03d'%(hour,min,sec,ms)

    def get_row_with_format(self, row:Tuple[int,any,str]):
        if len(row) != 3:
            print('wrong row')
            return
        output = self.timestamp_to_string(row[0]) + ' --> ' + self.timestamp_to_string(row[1]) + "\n"
        output += row[2] + "\n"
        return output

    def print_row(self, row:Tuple[int,any,str]):
        if len(row) != 3:
            print('wrong row')
            return
        print(self.get_row_with_format(row), end='')
    
    def reset(self):
        self.p.stop()
        self.offset = -1
        self.sync_list:list[Tuple[int,int,str]] = []
        self.idx = 0
        self.sync_started = False
        self.is_pause = True

    def cancel(self):
        self.reset()
        print("Cancel making sync lyrics")
        return

    def back_line(self):
        if len(self.sync_list) == 0:
            self.start()
            self.sync_started = False
            return
        tmp:Tuple[int, int, str] = self.sync_list.pop()
        self.idx -= 1
        self.set_pos(tmp[0]/1000)
        print('')
        print(tmp[0]/1000)
        print('')
        self.start_pos = tmp[0]
        self.print_row((tmp[0], '', tmp[2]))
    
    def first_sync(self):
        self.idx = 0
        pos = self.p.get_pos()
        if(pos == -1):
            print("start music first.")
            return
        self.start_pos = pos
        self.sync_started = True
    
    def save(self):
        filename = self.get_srt_filename()
        if os.path.exists(filename):
            raise FileExistsError("Target .srt file already exists!")
        with open(filename, "w", encoding='UTF-8') as f:
            for i, row in enumerate(self.sync_list):
                f.write(i+"\n")
                f.write(self.get_row_with_format(row)+"\n")


    def sync_lyrics(self):
        lyrics = self.script
        
        self.sync_list = []
        self.idx = 0
        self.start_pos = 0
        
        cmds = {'m': self.start, 'p': self.pause, 'up': self.unpause, 'r': self.reset, 'c': self.cancel, 'b': self.back_line}
        while True:
            ch = input("m: music_start, p: pause, up: unpause, r: reset, b: 1 line back, c: cancel, save: save, \\n: sync line.\n")
            
            if ch in cmds.keys():
                if ch == 'm':
                    print('\n' + lyrics[self.idx])
                    self.start()
                elif ch == 's':
                    self.sync_start()
                    self.print_row((self.start_pos, '', lyrics[self.idx]))
                else:
                    cmds[ch]()
                    if ch == 'c':
                        return
                # TODO save, quit, unpause features.

            elif ch == '' and not self.is_pause:
                if not self.sync_started:
                    self.first_sync()
                    self.print_row((self.start_pos, '', lyrics[self.idx]))
                    continue
                t = self.get_pos()
                tmp = (self.start_pos, t, lyrics[self.idx])
                self.start_pos = t
                self.idx += 1
                self.sync_list.append(tmp)
                print('')
                self.print_row(tmp)
                if self.idx == len(lyrics):
                    print("\n모든 가사의 싱크를 등록하셨습니다. 이제 파일을 확인중입니다.")
                    try:
                        self.save()
                    except Exception as e:
                        print(e)
                    ex = input("종료하시겠습니까? (Yes or not)")
                    if ex.lower() == 'y' or ex.lower() == 'yes':
                        self.reset()
                        return
                else:
                    self.print_row((self.start_pos, '', lyrics[self.idx]))
            elif ch == 'save':
                print("\n파일을 확인중입니다.")
                try:
                    self.save()
                except Exception as e:
                    print(e)
                ex = input("종료하시겠습니까? (Yes or not)")
                if ex.lower() == 'y' or ex.lower() == 'yes':
                    self.reset()
                    return