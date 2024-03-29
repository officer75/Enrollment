from bs4 import BeautifulSoup
import requests
from twilio.rest import Client
import time

def send_sms(account_sid, auth_token, from_number, to_number, message):
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=message,
        from_=from_number,
        to=to_number
    )

    print("SMS를 전송했습니다. SID:", message.sid)

def check_availability(course_url, target_string):
    # 웹 페이지 가져오기
    page = requests.get(course_url)
    soup = BeautifulSoup(page.content, 'html.parser')

    # 원하는 정보 추출
    availability = soup.find(text=target_string)

    # 수강정원 확인
    if availability:
        return True
    else:
        return False

def main():
    # Twilio 계정 정보 설정
    account_sid = "your_account_sid"
    auth_token = "your_auth_token"
    from_number = "your_twilio_phone_number"
    to_number = "your_phone_number"  # 수신자 핸드폰 번호

    # 강좌 정보와 URL 설정
    course_url = "https://course.mfac.or.kr/fmcs/3?page=1&lecture_type=R&center=MAPOARTCENTER&event=1000000000&class=1000020000&subject=&target=&lerturer_name="
    target_string = "접수종료"  # 수강 가능한 상태를 나타내는 문자열

    while True:
        # 수강정원 확인
        if check_availability(course_url, target_string):
            print("수강 가능한 자리가 열렸습니다!")
            send_sms(account_sid, auth_token, from_number, to_number, "수영 강좌에 자리가 열렸습니다. 빨리 확인하세요!")
            break
        else:
            print("아직 수강 가능한 자리가 없습니다. 잠시 후 다시 확인합니다.")
            time.sleep(300)  # 5분 후에 다시 확인

if __name__ == "__main__":
    main()
