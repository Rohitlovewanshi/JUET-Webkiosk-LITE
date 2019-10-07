import requests
from bs4 import BeautifulSoup
from os import system, name
import collections


session = requests.Session()
url = 'https://webkiosk.juet.ac.in/CommonFiles/UserAction.jsp'
data = {
    'InstCode' : 'JUET',
    'UserType' : 'S',
    'MemberCode' : '171B099',
    'Password' : 'your_password'
}
kiosk_session = session.post(url,data)
def attendence():
    attendence = session.get("https://webkiosk.juet.ac.in/StudentFiles/Academic/StudentAttendanceList.jsp")
    html_form = attendence.text
    clean_data  = BeautifulSoup(html_form, 'html.parser')
    lst=[]
    for link in clean_data.findAll("tbody"):
            x=str(link.text)
            raw_data=(x.split('\n'))
    # this raw_data has \xa0 and some null enteries, I need to fuck that issue first :)
    refined_data = []
    for data in raw_data:
        if not (str(data) == '\xa0' or str(data)==''):
            refined_data.append(data)
    dict_data = { }
    for i in range(0,len(refined_data)):
        if len(refined_data[i])>3:
            dict_data[refined_data[i]] = refined_data[i+1]
    print(dict_data)
def cgpa():
    cgpa = session.get("https://webkiosk.juet.ac.in/StudentFiles/Exam/StudCGPAReport.jsp")
    html_form = cgpa.text
    clean_data = BeautifulSoup(html_form,'html.parser')
    lst=[]
    for tab in clean_data.findAll("table",{"align" : "center","id":"table-1"}):
        for link in tab.findAll("td"):
            h=str(link.text)
            d=(h.split('\n'))
            for i in d:
                lst.append(i)
    lst = lst[8:]
    dict_data = { }
    semester = 1
    sgpa = 6
    for i in range(0,int(len(lst)/8)):
        dict_data.update({str(semester): str(lst[sgpa])})
        sgpa+=8
        semester+=1
    dict_data.update({'CGPA':str(lst[-1])})
    print(dict_data)
def personalData():
    personal_data = session.get("https://webkiosk.juet.ac.in/StudentFiles/PersonalFiles/StudPersonalInfo.jsp")
    html_format = personal_data.text
    clean_data = BeautifulSoup(html_format,'html.parser')
    per_info=[]
    for link in clean_data.findAll("tr"):
        for y in link.findAll("td"):
            for x in y.findAll("font",{"color" : "black"}):
                if x not in y.findAll("font",{"face" : "Arial"}):
                    d=str(x.text)
                    per_info.append(d)
    refined_data = []
    for data in per_info:
        if not (str(data) == '\xa0' or str(data) == '\xa0  ' or str(data)==''):
            refined_data.append(data[1:])
    dict_data = { }
    name = refined_data[0]
    enrollment = refined_data[2]
    fatherName = refined_data[3]
    degree_data = refined_data[4]
    aadhar = refined_data[6]
    phone = refined_data[7]
    gmail = refined_data[11].lower().split(',')[0]
    city = refined_data[22].split("/")[0]
    pinCode = refined_data[22].split("/")[1]
    state = refined_data[23]

    enrollment = enrollment[1:]
    fatherName = fatherName[2:]
    course = degree_data[1:5]
    branch = degree_data[-7:]
    aadhar = aadhar[3:]
    city = city[1:]
    state = state[1:]
    branch = branch[2:]
    branch = branch[:-2]

    dict_data.update({'1Name': str(name)})
    dict_data.update({'2Enrollment': str(enrollment)})
    dict_data.update({'3FatherName': str(fatherName)})
    dict_data.update({'4Course': str(course)})
    dict_data.update({'5Branch': str(branch)})
    dict_data.update({'6Aadhar': str(aadhar)})
    dict_data.update({'7Phone': str(phone)})
    dict_data.update({'8Gmail': str(gmail)})
    dict_data.update({'99City': str(city)})
    dict_data.update({'9State': str(state)})
    dict_data  = sorted(dict_data.items())
    print(dict_data)
#cgpa()
#attendence()
personalData()
