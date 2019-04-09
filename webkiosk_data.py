import requests
from bs4 import BeautifulSoup
from os import system, name
import collections


session = requests.Session()
url = 'https://webkiosk.juet.ac.in/CommonFiles/UserAction.jsp'
data = {
    'InstCode' : 'JUET',
    'UserType' : 'S',
    'MemberCode' : '171B102',
    'Password' : '****'
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
    last = collections.OrderedDict(dict_data)
    print(last)

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
        dict_data.update({'sem'+str(semester): str(lst[sgpa])})
        sgpa+=8
        semester+=1
    dict_data.update({'CGPA':str(lst[-1])})
    print(dict_data)
#cgpa()
attendence()
