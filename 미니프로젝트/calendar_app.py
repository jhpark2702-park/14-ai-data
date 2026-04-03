from flask import Flask, render_template, request
from datetime import date
import holidays
##Flask install, holiday  instal
app = Flask(__name__)   #웹 서버 생성

# 연도, 월을 받아 일수 반환
def month_days(year, month):
    if month in [1, 3, 5, 7, 8, 10, 12]:
        days = 31
    elif month in [4, 6, 9, 11]:
        days = 30
    elif month == 2:    #윤년 계산
        if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
            days = 29
        else:
            days = 28
    else:
        days = None
    return days

# 연도, 월, 일을 받아 요일 반환(0~6: 일~토)
def get_weekday(year, month, day):
    d = date(year, month, day)
    return (d.weekday() + 1) % 7   # 0~6 : 일~토

# 해당 년도의 공휴일을 딕셔너리로 반환
def holiday(year):
    kr_holidays = holidays.KR(years=year)
    kr_holidays[date(year, 5, 1)] = "노동절"   #노동절(근로자의 날) 추가
    return kr_holidays

# 연도와 월을 받아 [[첫째주], [둘째주] ... ] 리스트 생성하는 함수
def make_calendar_data(year, month):
    last_day = month_days(year, month) #해당 달의 마지막 날짜
    start_weekday = get_weekday(year, month, 1) #해당 달 시작일의 요일
    holidays_dict = holiday(year) #공휴일을 딕셔너리 형태로 저장

    weeks = [] #해당 달의 전체 주 리스트
    week = [None] * 7 #하나의 주(초기값: 7개의 None)
    day = 1

    #첫번째 주 채우기
    for i in range(start_weekday, 7):
        current_date = date(year, month, day) #현재 계산중인 날짜(시작값 day=1로 설정함)
        holiday_name = holidays_dict.get(current_date) #해당 날짜가 공휴일인지 확인


        week[i] = {
            "day": day,
            "holiday": holiday_name #공휴일이 아닐경우 "holiday":None으로 저장됨
        }
        day += 1

    weeks.append(week)  #week(달의 전체주)에 추가

    #첫번째 주 외 나머지 주 채우기
    while day <= last_day:  #현재 계산중인 day가 달의 마지막 날보다 적으면 계속 생성
        week = [None] * 7 #추가할 하나의 주 리스트 초기화

        for i in range(7): #7번 시행
            if day <= last_day:
                current_date = date(year, month, day)
                holiday_name = holidays_dict.get(current_date) #공휴일인지 확인
                
                #리스트에 추가
                week[i] = {
                    "day": day,
                    "holiday": holiday_name #공휴일이 아닐경우 "holiday":None으로 저장됨
                }
                day += 1

        weeks.append(week) #week(달의 전체주)에 추가

    return weeks


@app.route("/") #아래의 함수를 적용
def calendar_view():
    today = date.today() #오늘 날짜 기준 캘린더 표시
    #request.args 딕셔너리에서 year과 month 키의 value값 가져옴
    #Flask가 request.args를 자동으로 받아옴
    year = request.args.get("year", default=today.year, type=int)
    month = request.args.get("month", default=today.month, type=int)

    # 월 보정
    if month < 1:
        month = 12
        year -= 1
    elif month > 12:
        month = 1
        year += 1

    weeks = make_calendar_data(year, month) #주별로 분리된 리스트 생성

    #파이썬에서 HTML로 전달
    return render_template(
        "calendar.html",
        year=year,
        month=month,
        weeks=weeks
    )


if __name__ == "__main__":
    app.run(debug=True)
