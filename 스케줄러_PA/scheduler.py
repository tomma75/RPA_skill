import schedule
import time
import re
from pywinauto import findwindows
from pywinauto.application import Application

def click_RPA():
    procs = findwindows.find_elements()
    test = ''
    for proc in procs:
        test += (f"{proc} / 프로세스 : {proc.process_id}\n")
    testpattern = r"Power Automate',.*?프로세스 : (\d+)"
    testmatch = re.search(testpattern, test, re.DOTALL)
    RPA_process = testmatch.group(1)

    with open("RPAname.txt", "r", encoding="utf-8") as file:
        content = file.read()
        # '실행 RPA명 : ' 뒤에 오는 모든 텍스트를 추출하기 위한 정규 표현식 수정
        pattern = r'실행 RPA명 : (.*)'
        match = re.search(pattern, content)
        match2 = match.group(1)

    app = Application(backend='uia') 
    app.connect(process=int(RPA_process))
    dlg = app['Power Automate']

    path_input = dlg.child_window(title=f"{match2}", control_type="DataItem")
    path_input.click_input()

    path_input = dlg.child_window(auto_id="StartFlowButton", control_type="Button")
    path_input.click_input()

def read_schedule_time():
    with open("settime.txt", "r", encoding="utf-8") as file:
        content = file.read()
        match = re.search(r'실행시간 : (\d+)시 (\d+)분', content)
        if match:
            return int(match.group(1)), int(match.group(2))
        else:
            raise ValueError("settime.txt 파일에서 실행 시간을 찾을 수 없습니다.")

def timeschedule():
    hour, minute = read_schedule_time()
    schedule.every().day.at(f"{hour:02d}:{minute:02d}").do(click_RPA)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    timeschedule()
