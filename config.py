import os
import json

class MyConfig:
    def __init__(self):
        self.load_config()
        self.audio_filename = None
        self.sample_rate = None
        self.lyric_filename = None
        self.isDefault = True

        self.find_audio_file()
        pass

    def load_config(self):
        """
        load configs from config.json in same directory.
        """
        self.config = {}
        if os.path.exists("config.json"):
            with open("config.json", "r", encoding="UTF-8") as f:
                self.config = json.loads(f.read())
    
    def get_setting(self, key):
        if key in self.config:
            return self.config[key]
        else:
            return None


    def find_audio_file(self, change:bool=False):
        self.isDefault = not change
        sample_rate = -1
        audio_filename = (self.get_setting('audio_filename') if self.isDefault else None) or input("오디오 파일 이름 혹은 경로를 입력하세요. :\n")
        while not os.path.exists(audio_filename):
            audio_filename = input("존재하지 않는 파일 혹은 경로입니다. \n오디오 파일 이름 혹은 경로를 입력하세요. :\n")
        self.audio_filename:str = audio_filename
        while True:
            #TODO 변경 취소 만들기
            try:
                sample_rate = self.get_setting('sample_rate') or int(input("오디오 sample rate를 입력하세요.(44100, 48000): "))
                sample_rate = int(sample_rate)
                if sample_rate > 0:
                    break
                print("sample_rate를 자연수로 입력해주십시오.")
            except Exception as e:
                print(e)
                return
        self.sample_rate = sample_rate
    
    def set_lyric_file(self):
        # TODO 취소 만들기
        lyric_filename = self.get_setting('lyric_filename') or input("등록할 스크립트 파일 이름 혹은 경로를 입력하세요. :\n")
        while not os.path.exists(lyric_filename):
            lyric_filename = input("존재하지 않는 파일 혹은 경로입니다. 다시 입력하세요.\n")
        self.lyric_filename = lyric_filename
