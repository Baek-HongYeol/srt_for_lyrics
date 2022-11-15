# Srt_for_Lyrics
make .srt file associated with music.  
음악에 맞춰 가사의 싱크를 편리하게 맞추세요.  
  
한 줄 가사만 지원합니다!  
srt 파일을 만들기 위해 txt 가사 파일이 필요합니다!  
같은 줄에 있는 가사는 모두 한 번에 출력됩니다.  
표현하고 싶은 대로 라인을 나눠주세요!  

# load files info
실행 전에, 같은 폴더에 test.txt를 만들어 주세요.  
공백 없이 첫째 줄에 음악 파일 경로, 둘째 줄에 가사 txt 파일 경로를 넣은 test.txt를 저장하면  
해당 파일에서 음악 파일과 가사 txt 파일 경로를 가져옵니다.  
직접 입력하는 일 없이 쉽게 사용하실 수 있습니다.

# Screenshots
- 첫 화면 : 음악 파일을 찾고 재생할 수 있는 화면입니다.  
  
  ![Main Screen](https://user-images.githubusercontent.com/24859233/201835034-6d0cd8bb-069b-4e34-9905-a812ba37190d.png)  
  start : 처음부터 재생합니다.  
  pause : 일시정지  
  unpause : 일시정지 해제  
  reset : 정지  
  get_pos : ms 단위 위치를 알려줍니다.  
  set_pos : sec 단위 위치를 설정할 수 있습니다.  
  change : 음악 파일을 다시 입력합니다.  
  sync : srt 파일을 만드는 화면으로 이동합니다.  
  
  
- Sync Lyric 화면 : srt 파일을 만들기 위해 싱크를 등록합니다.
  ![Sync Lyric Screen](https://user-images.githubusercontent.com/24859233/201836485-4c081c82-9cbf-4097-91b8-ff0ca300f4f7.png)  
  
  music_start : 음악을 시작합니다.  
  \n( 아무 입력 없이 enter ) : 한 줄씩 시간을 등록합니다. 각 가사의 시작 타이밍에 엔터를 누르면 이전 가사의 종료 타이밍과 함께 등록됩니다.  
  pause : 일시정지  
  unpause : 일시정지 해제  
  reset : 등록한 싱크를 초기화하고 음악을 정지합니다.  
  back : 싱크 하나를 지우고 이전 가사 시점으로 이동합니다.  
  cancel : 싱크 등록 과정을 중단합니다. (exit)  
  save : 현재 등록한 부분까지 저장합니다.  
  
