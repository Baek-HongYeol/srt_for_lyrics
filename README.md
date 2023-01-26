# Srt_for_Lyrics
make .srt file associated with music.  
음악에 맞춰 가사의 싱크를 편리하게 맞추세요.  
  
python 파일을 실행하기 위해 pygame 모듈을 설치해야합니다!  
```bash
pip install pygame
```
srt 파일을 만들기 위해 txt 가사 파일이 필요합니다!  
같은 줄에 있는 가사는 한 라인에 출력됩니다.  
표현하고 싶은 대로 라인을 나눠주세요!

# Load configure 
실행 전에, 같은 폴더에 config.json을 만들어 주세요. (sample_config.json을 복사)  
각 항목에 음악 파일 경로, 음악 파일의 샘플링 레이트, 가사 파일 경로를 적고 저장하면  
해당 파일에서 음악 파일과 가사 txt 파일 경로를 가져옵니다.  

- 샘플링 레이트(sample rate)란?  
디지털 오디오의 음질을 표시할 때 bit-depth와 함께 사용되는 값.  
소리를 디지털로 변환할 때 1초에 몇 개의 시점을 변환했는지를 나타내는 수치
대표적으로 44.1khz(44100) / 48khz(48000)을 가장 많이 사용한다.  
확인 방법:
  - 알송  
  알송에 추가 후 우클릭 > 파일 정보 보기 / 수정 (ALT+3)> 속성 자세히 보기  
    
  - 팟플레이어  
  재생 후 우클릭 > 재생 정보 >  오디오 정보 섹션에 샘플레이트 화살표 왼쪽 값  



# Screenshots
- 첫 화면 : 음악 파일을 찾고 재생할 수 있는 화면입니다.  
  
  ![Main Screen](https://user-images.githubusercontent.com/24859233/212577278-ab311aef-6b1b-472f-97df-e9092f2bdefc.png)

  start : 처음부터 재생합니다.  
  pause : 일시정지  
  unpause : 일시정지 해제  
  reset : 정지  
  get_pos : ms 단위 위치를 알려줍니다.  
  set_pos : sec 단위 위치를 설정할 수 있습니다.  
  change : 음악 파일을 다시 입력합니다.  
  sync : srt 파일을 만드는 화면으로 이동합니다.  
  
  
- Sync Lyric 화면 : srt 파일을 만들기 위해 싱크를 등록합니다.
  ![Sync Lyric Screen](https://user-images.githubusercontent.com/24859233/212575837-3b34fcf1-8955-4dd2-b0c3-d54dffa91156.png)  
  
  start : 음악을 시작합니다.  
  \n( 아무 입력 없이 enter ) : 한 줄씩 시간을 등록합니다. 각 가사의 **시작** 타이밍에 엔터를 누르면 이전 가사의 종료 타이밍과 함께 등록됩니다.  
  pause : 일시정지  
  unpause : 일시정지 해제  
  reset : 등록한 싱크를 초기화하고 음악을 정지합니다.  
  back : 이전 가사 시점으로 이동합니다.  
  cancel : 싱크 등록 과정을 중단합니다. (exit)  
  save : 현재 등록한 부분까지 저장합니다.  
  dev : 개발 중인 기능 - 현재 등록한 싱크 가사를 재생시켜보는 모드입니다.  

  ---
  피드백과 아이디어는 환영입니다!  
