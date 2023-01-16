import os
import sys
from pygame import mixer
import tempfile
from typing import List, Tuple
from threading import Thread
from time import sleep
from config import MyConfig

class Sync_Lyrics:
    def __init__(self, config:MyConfig = None) -> None:
        self.config = config
        if config.audio_filename is None:
            raise ValueError("audio_file is required for sync_lyrics")

        if not os.path.exists(config.audio_filename):
            raise FileNotFoundError("audio_file is not Exists!")
        
        self.audio_filename = config.audio_filename
        self.config.set_lyric_file()
        self.filename = self.get_srt_filename()
        self.script = None
        self.is_pause = True
        self.sync_started = False
        self.tmpfile = None
        
        audio_options = {'frequency': config.sample_rate}
        if audio_options and "frequency" in audio_options:
            try:
                frequency = int(audio_options['frequency'])
                mixer.init(frequency)
            except:
                mixer.init()
        else:
            mixer.init()
        mixer.music.load( self.audio_filename )
        self.p = mixer.music
        self.offset = -1
        self.read_script()

        self.isDev = False
        self.th1 = None
        print("This page is for making srt file with audio file!")
        print("The commands are below:")
        # TODO 공백 라인을 기준으로 가사 라인 수 조절하는 옵션 추가하기 (중요도: low)
    
    def read_script(self, lyric_filename:str = None):
        if lyric_filename is None:
            lyric_filename = self.config.lyric_filename
        
        self.block_line = self.config.get_multiline_setting()

        lyrics = []
        lines = []
        if not os.path.exists(lyric_filename):
            self.config.set_lyric_file()
            #TODO 가사 파일 변경 기능 + 변경 취소 시 예외 처리
        try:
            with open(lyric_filename, "r", encoding='UTF-8') as f:
                lines = f.read().splitlines()
        except Exception as e:
            print("file is not readable.", file = sys.stderr)
            raise e
        if self.block_line == 1:
            pass
            #return lines
        for i in range(0, len(lines), self.block_line):
            end = i + self.block_line
            if end > len(lines):
                end = len(lines)
            lyrics.append('\n'.join(lines[i:end]))

        self.script = lyrics

    def get_srt_filename(self, path = ''):
        isdefault = False
        if path == '':
            path = self.audio_filename
            isdefault = True
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
        
        if path == '':
            if isdefault:
                raise FileNotFoundError("파일 이름을 식별할 수 없습니다.")
            return self.get_srt_filename()
        return path+".srt"

    def clear_tmpfile(self):
        if self.tmpfile != None:
            self.tmpfile.close()
            if not self.tmpfile.closed:
                print("tmp not closed!!")
            
            os.unlink(self.tmppath)
            if os.path.exists(self.tmppath):
                    print("tmpfile was not removed!")
            self.tmpfile = None
        
    def make_tmpfile(self):
        self.clear_tmpfile()
        fd, self.tmppath = tempfile.mkstemp(suffix="_"+self.filename, dir='.')
        self.tmpfile = os.fdopen(fd, "w", encoding="utf-8")


    def get_row(self, start:str, end:str, line:str):
        """
        start: time string with format {HH:MM:SS,mmm} (H: hour, M: minutes, S: seconds, mmm: milliseconds)
        end: time string with format {HH:MM:SS,mmm} (H: hour, M: minutes, S: seconds, mmm: milliseconds)
        line: 1 line lyric string
        """
        start_time  = int(start[0:2])*3600 + int(start[3:5])*60 + int(start[6:8]) 
        start_time = start_time * 1000 + int(start[-3:])
        end_time    = int(end[0:2])*3600 + int(end[3:5])*60 + int(end[6:8]) 
        end_time   = end_time * 1000 + int(end[-3:])
        return (start_time, end_time, line)
    
    def parse_srt(self, file_name):
        import re
        if self.sync_list and len(self.sync_list) > 0:
            overwrite = input("sync_list has data in memory. Overwrite?(y/N) ")
            if overwrite.lower() == 'y' or overwrite.lower() == 'yes':
                self.sync_list = []
            else:
                return False
        
        lines = []
        with open(file_name, "r", encoding="utf-8") as f:
            lines = f.readlines()

        start = ""
        end = ""
        idx = 0
        lyric = ""
        time_pattern = "(\d{2,2}:\d{2,2}:\d{2,2},\d{3,3}) --> (\d{2,2}:\d{2,2}:\d{2,2},\d{3,3})"
        time_gotten = False
        multiline = False
        p = re.compile(time_pattern)
        # TODO 파싱 예외 처리
        for line in lines:
            if line.strip() == "":
                if start != "" and end != "" and lyric != "":
                    row = self.get_row(start, end, lyric[1:-1])
                    self.sync_list.append(row)
                idx += 1
                start = ""
                end = ""
                lyric = ""
                time_gotten = False
            else:
                m = p.match(line)
                if time_gotten:
                    if not multiline: # 첫 줄
                        lyric += "\n" + line
                        multiline = True
                    else:   # 여러 줄
                        lyric += line
                elif  m is not None and len(m.groups()) == 2:
                    start = m.group(1)
                    end = m.group(2)
                    multiline = False
                    time_gotten = True


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

    def row_with_string_format(self, row:Tuple[int,any,str]):
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
        print(self.row_with_string_format(row), end='')

    def exit(self):
        if self.th1 and self.isDev:
            self.isDev = False
            self._isDev = False
        return
        

    def work(self):
        self.idx = 0
        if len(self.sync_list) == 0:
            print("Dev finished due to empty list.")
            return
        self.start()
        printed = False
        while self._isDev and not self.is_pause:
            if self.get_pos() > self.sync_list[0][0] and not printed:
                print(self.sync_list[0][2])
                printed = True
                break
                
            sleep(0.01)
        while self._isDev and not self.is_pause:
            if self.get_pos() > self.sync_list[self.idx][1]:
                self.idx += 1
                if len(self.sync_list) == self.idx:
                    break
                print(self.sync_list[self.idx][2])
            sleep(0.01)
        print("Dev finished dev를 입력하면 dev 모드가 종료됩니다.")
        return
    # TODO 함수 이름 변경
    def dev(self):
        if self.isDev:
            self._isDev = False
            if self.th1:
                self.th1.join()
            self.isDev = False
            self.pause()
            self.th1 = None
        else:
            self.p.stop()
            self.offset = -1
            self.isDev = True
            self._isDev = True
            if self.sync_list is not None and len(self.sync_list) == 0:
                self.parse_srt(self.get_srt_filename())
            self.th1 = Thread(target=self.work)
            self.th1.start()


    def sync_lyrics(self):
        lyrics = self.script
        
        self.sync_list = []
        self.idx = 0
        self.start_pos = 0
        
        cmds = {'m': self.start, 'p': self.pause, 'up': self.unpause, 'r': self.reset, 'c': self.cancel, 'b': self.back_line, 'dev': self.dev}
        while True:
            ch = input("\t[ m: music_start, p: pause, up: unpause, r: reset, b: 1 line back, c: cancel, save: save, \\n: sync line. ]\n")
            
            if ch in cmds.keys():
                if ch == 'm':
                    print('\n' + lyrics[self.idx])
                    self.start()
                else:
                    cmds[ch]()
                    if ch == 'c':
                        return

            elif ch == '' and not self.is_pause and not self.isDev:
                if not self.sync_started:
                    self.first_sync()
                    self.print_row((self.start_pos, '', lyrics[self.idx]))
                    continue
                t = self.get_pos()
                tmp = (self.start_pos, t, lyrics[self.idx])
                if len(self.sync_list) > self.idx:
                    self.sync_list[self.idx] = tmp
                else:
                    self.sync_list.append(tmp)
                
                self.start_pos = t
                self.idx += 1
                print('')
                self.print_row(tmp)
                if self.idx == len(lyrics):
                    print("\n모든 가사의 싱크를 등록하셨습니다. ", end='')
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
                try:
                    self.pause()
                    self.save()
                except Exception as e:
                    print(e)
                    print("위 오류로 인해 저장에 실패했습니다.")
                ex = input("종료하시겠습니까? (Yes or not)")
                if ex.lower() == 'y' or ex.lower() == 'yes':
                    self.reset()
                    return


######### control methods #########    

    def start(self):
        self.p.play()
        self.offset = -1
        self.is_pause = False

    def pause(self):
        self.p.pause()
        self.is_pause = True

    def unpause(self):
        if self.p.get_pos() == -1:
            print("not started yet")
        else:
            self.p.unpause()
            self.is_pause = False
    
    def set_pos(self, pos:float):
        try:
            pos = float(pos)
        except Exception as e:
            print("Wrong position!:", pos)
            print(e)
            return
        self.p.play()
        self.p.set_pos(pos)
        self.offset = pos

    def get_pos(self):
        t = self.p.get_pos()
        if self.offset != -1:
            t += int(self.offset*1000)
        return t

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
        self.exit()
        return

    def back_line(self):
        if self.idx == 0 or len(self.sync_list) == 0:
            self.start()
            self.sync_started = False
            return
        tmp:Tuple[int, int, str] = self.sync_list[self.idx-1]
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
        print("\n파일을 확인중입니다.")
        print("Default filename depends on audio file name.")
        if self.tmpfile is None:
            self.make_tmpfile()
        for i, row in enumerate(self.sync_list):
                self.tmpfile.write(f"{i+1}\n")
                self.tmpfile.write(self.row_with_string_format(row)+"\n")

        filename = self.filename
        while os.path.exists(filename):
            overwrite = input(filename + " already exists. Overwrite?(y/N) ")
            if overwrite.lower() == 'y' or overwrite.lower() == 'yes':
                break
            path = input("Enter the srt filename except extension(.srt): ")
            filename = self.get_srt_filename(path)
        
        with open(filename, "w", encoding='UTF-8') as f:
            for i, row in enumerate(self.sync_list):
                f.write(f"{i+1}\n")
                f.write(self.row_with_string_format(row)+"\n")

        print(filename + " is saved!\n")
        self.filename = filename
        self.clear_tmpfile()