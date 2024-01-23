from dis import show_code
from multiprocessing import context
import folium
import webbrowser
import matplotlib
import psycopg2
import sys
import os
from urllib.request import urlopen

import pandas as pd
import numbers
import math

import urllib.request , bs4

import json
import requests

from xml.etree.ElementTree import parse
from urllib.parse import urlencode, quote_plus, unquote


from django.shortcuts import render
from django.views import generic
# Create your views here.
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


from .models import district_info
from .models import school_info
from .forms import TodoForm

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager, rc
from numpy import nan as na
import math

@csrf_exempt
def index(request):
    conn_string = "host='localhost' dbname ='postgres' user='postgres' password='9407740'"
    conn = psycopg2.connect(conn_string)
    cur = conn.cursor()
    selected_city = ""
    selected_district = ""
    district_list = ""
    city_list = ""
    school_name = ""
    find_school_name = ""
    find_school = ""
    school_type = ""
    #버튼누른경우
    if request.method == "POST":
        #city 와 district 값이 모두 선택 되어 전달 된 경우
        selected_city = request.POST['select_city']
        selected_district = request.POST['select_district']
        school_type = request.POST['select_school_type']
        
        if(school_type == "초등학교"):
            school_type = 2
        elif(school_type == "중학교"):
            school_type = 3
        elif(school_type == "고등학교"):
            school_type = 4
        else:
            school_type = 5
        if selected_district != "도시선택" :
            selected_city = request.POST['select_city']
            selected_district = request.POST['select_district']
            sql = "select id, name, ofice_name ,road_addr, addr from school_info where road_addr like '%"
            sql += selected_city
            sql += "%' and road_addr like '%"
            sql += selected_district
            sql += "%' and type = '"
            sql += str(school_type)
            sql += "';"
            cur.execute(sql)
            find_school = cur.fetchall()

            
            selected_city = request.POST['select_city']
            sql = "select district from district_info where city = '"
            sql +=  selected_city
            sql += "';"
            cur.execute(sql)
            district_list = cur.fetchall()
            

        #city만선택되고버튼눌러district값넣어야하는경우
        elif selected_district == "도시선택":
            selected_city = request.POST['select_city']
            sql = "select district from district_info where city = '"
            sql +=  selected_city
            sql += "';"
            cur.execute(sql)
            district_list = cur.fetchall()
        else :
            district_list = [("에러")]


    sql = "select distinct city from district_info"
    cur.execute(sql)
    city_list = cur.fetchall()
    
    sql = "select distinct city from district_info"
    cur.execute(sql)
    city_list = cur.fetchall()

    data = [
        {'mapx': '37.482867', 'mapy': '127.035621'}, 
        {'mapx': '37.504547', 'mapy': '126.994611'}, 
        {'mapx': '37.516083', 'mapy': '127.019694'}
        ]

    json_str = json.dumps(data)
    json_dict = json.loads(json_str)
    print(type(data))
    print(data)

    print(type(json_str))
    print(json_str)

    print(type(json_dict))
    print(json_dict)

    print(data[0])
    print(data[0]['mapx'])
    print(data[1]['mapx'])
    
    conn.close()

    context = {
            'city_list' : city_list,
            'district_list' : district_list,
            'selected_city' : selected_city,
            'selected_district' : selected_district,
            'find_school' : find_school,
            'find_school_name' : find_school_name,
            'school_name'  : school_name,
            }
    return render(request, 'index.html', context) 

@csrf_exempt
def name(request):
    if request.method== "POST":
        selected_city = ""
        selected_district = ""
        district_list = ""
        city_list = ""
        find_school = ""
        school_name = request.POST['school_name']
        conn_string = "host='localhost' dbname ='postgres' user='postgres' password='9407740'"
        conn = psycopg2.connect(conn_string)
        cur = conn.cursor()

        sql = "select id, name, ofice_name ,road_addr, addr from school_info where name like '%"
        sql += school_name
        sql += "%';"
        cur.execute(sql)
        find_school_name = cur.fetchall()

        sql = "select id, addr from school_info where name like '%"
        sql += school_name
        sql += "%';"
        cur.execute(sql)
        school_url = cur.fetchall()

        sql = "select distinct city from district_info"
        cur.execute(sql)
        city_list = cur.fetchall()
        conn.close()
        
        context = {
                'city_list' : city_list,
                'district_list' : district_list,
                'selected_city' : selected_city,
                'selected_district' : selected_district,
                'find_school' : find_school,
                'find_school_name' : find_school_name,
                'school_name'  : school_name,
                'school_url': school_url,
                }
    return render(request,'index.html',context)

@csrf_exempt
def show_map2(request):
    info = "null"
    if request.method== "GET" and request.GET.copy():
        info = request.GET.copy()
        
        for i in info:
            ID = str(i)[2:]
        
        conn_string = "host='localhost' dbname ='postgres' user='postgres' password='9407740'"
        conn = psycopg2.connect(conn_string)
        cur = conn.cursor()

        sql = "select latitude from school_info where id = '"
        sql += ID
        sql += "';"
        cur.execute(sql)
        latitude = str(cur.fetchall())[3 :-4]
        
        sql = "select longitude from school_info where id = '"
        sql += ID
        sql += "';"
        cur.execute(sql)
        longitude = str(cur.fetchall())[3 :-4]
        
        sql = "select name from school_info where id = '"
        sql += ID
        sql += "';"
        cur.execute(sql)
        name = str(cur.fetchall())[3 :-4]
        
        sql = "select id from school_info where id = '"
        sql += ID
        sql += "';"
        cur.execute(sql)
        info = cur.fetchall()

        conn.close()
        
        Map = folium.Map(location=[latitude, longitude], tiles = "OpenStreetMap", zoom_start=17)
        folium.Marker(location = [latitude, longitude], icon = folium.Icon(color='blue', icon = 'star', popup = name)).add_to(Map)
        Map_dir = 'C:/Users/jsl11/Desktop/web(1017)/apps/templates/map.html'
        Map.save(Map_dir)

#    return HttpResponse(name)
    return render(request,'map.html')
    
def show_map(request):
    info = "null"
    if request.method== "GET" and request.GET.copy():
        info = request.GET.copy()
        
        for i in info:
            ID = str(i)[2:]
        
        conn_string = "host='localhost' dbname ='postgres' user='postgres' password='9407740'"
        conn = psycopg2.connect(conn_string)
        cur = conn.cursor()

        sql = "select latitude from school_info where id = '"
        sql += ID
        sql += "';"
        cur.execute(sql)
        latitude = str(cur.fetchall())[3 :-4]
        
        sql = "select longitude from school_info where id = '"
        sql += ID
        sql += "';"
        cur.execute(sql)
        longitude = str(cur.fetchall())[3 :-4]
        
        sql = "select name from school_info where id = '"
        sql += ID
        sql += "';"
        cur.execute(sql)
        name = str(cur.fetchall())[3 :-4]
        
        conn.close()
        
        Map = folium.Map(location=[latitude, longitude], tiles = "OpenStreetMap", zoom_start=17)
        folium.Marker(location = [latitude, longitude], icon = folium.Icon(color='blue', icon = 'star', popup = name)).add_to(Map)
        Map_dir = 'C:/Users/jsl11/Desktop/web(1017)/apps/templates/map.html'
        Map.save(Map_dir)

#    return HttpResponse(name)
    return render(request,'map.html')

@csrf_exempt
def show_detail(request):
    info = ""
    info2 = ""
    info3 = ""
    name = ""
    # pmdata = []
    if request.method== "GET" and request.GET.copy():
        info = request.GET.copy()
        for i in info:
            ID = str(i)[2:]

        conn_string = "host='localhost' dbname ='postgres' user='postgres' password='9407740'"
        conn = psycopg2.connect(conn_string)
        cur = conn.cursor()

        sql = "select name from school_info where id = '"
        sql += ID
        sql += "';"
        cur.execute(sql)
        name = cur.fetchall()
        name = str(name)[3:-4]

        
        sql = "select id, name, type, public, branch from school_info where id = '"
        sql += ID
        sql += "';"
        cur.execute(sql)
        info = cur.fetchall()
        
        
        sql = "select state, addr, support_name, office_code, ofice_name from school_info  where id = '"
        sql += ID
        sql += "';"
        cur.execute(sql)
        info2 = cur.fetchall()
        

        sql = "select support_code,road_addr , latitude, longitude from school_info where id = '"
        sql += ID
        sql += "';"
        cur.execute(sql)
        info3 = cur.fetchall()
        
        
        sql = "select tm_x, tm_y from school_tm where id = '"
        sql += ID
        sql += "';"
        
        cur.execute(sql)
        school_tm = cur.fetchall()

        school_tmX = school_tm[0][0]
        school_tmY = school_tm[0][1]
        
        url = 'http://apis.data.go.kr/B552584/MsrstnInfoInqireSvc/getNearbyMsrstnList'
        key = unquote('yAjjtx1OUcLowdF%2BnNlhPCbhn7Pc8%2FWmttXZDxYNsIzS56BMNuauBJLHZnhpyghFshpV9Fwz2XNXeB%2FqhP0YAw%3D%3D')
        key = requests.utils.unquote(key)
        
        queryParams = '?' + urlencode({ 
            quote_plus('ServiceKey') : key,
            quote_plus('tmX') : school_tmX, 
            quote_plus('tmY') : school_tmY, 
            quote_plus('returnType') : 'xml'
            }) 

        try:
            request_api = requests.get(url + queryParams).text.encode('utf-8')
            station_info = bs4.BeautifulSoup(request_api, 'lxml-xml')
    
            station_name = station_info.find("stationName")
            station_name = station_name.text
            tm_dis = station_info.find("tm")
            tm_dis = tm_dis.text
    
            
            url = 'http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty'
            queryParams = '?' + urlencode({ 
                quote_plus('ServiceKey') : key,
                quote_plus('numOfRows') : '30', 
                quote_plus('pageNo') : '1', 
                quote_plus('stationName') : station_name, 
                quote_plus('dataTerm') : 'MONTH', 
                quote_plus('ver') : '1.2' 
            })
    
            request_api = requests.get(url + queryParams).text.encode('utf-8')
            air_info = bs4.BeautifulSoup(request_api, 'lxml-xml')
        except:
            request_api = requests.get(url + queryParams).text.encode('utf-8')
            station_info = bs4.BeautifulSoup(request_api, 'lxml-xml')
    
            station_name = station_info.find("stationName")
            station_name = station_name.text
    
            tm_dis = station_info.find("tm")
            tm_dis = tm_dis.text
            
            url = 'http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty'
            queryParams = '?' + urlencode({ 
                quote_plus('ServiceKey') : key,
                quote_plus('numOfRows') : '30', 
                quote_plus('pageNo') : '1', 
                quote_plus('stationName') : station_name, 
                quote_plus('dataTerm') : 'MONTH', 
                quote_plus('ver') : '1.2' 
            })
    
            request_api = requests.get(url + queryParams).text.encode('utf-8')
            air_info = bs4.BeautifulSoup(request_api, 'lxml-xml')

        time = air_info.find_all("dataTime")
        pm10 = air_info.find_all("pm10Value")
        pm10_24 = air_info.find_all("pm10Value24")
        pm25 = air_info.find_all("pm25Value")
        pm25_24 = air_info.find_all("pm25Value24")
        pmdata = []
        a = 0

        for i,j,k,x,y in zip(time, pm10, pm10_24, pm25, pm25_24):

            pmdata.append([])
            pmdata[a].append((i.text, j.text, k.text, x.text, y.text))
            a += 1

        
        conn.close()  
        
    context = {
            'detail_info' : info,
            'detail_info2' : info2,
            'detail_info3' : info3,
            'dis':tm_dis,
            'pmdata' : pmdata,          
            'name' : name
            }

    return render(request,'detail.html', context)


#09-16(금) 빡세네....
@csrf_exempt
def show_new_detail(request):
    if request.method== "GET" and request.GET.copy():
        #info - 히든 값으로 넘긴 학교ID 값
        info = request.GET.copy()
        for i in info:
            #학교Id 추출
            ID = str(i)[2:]

        #DB 접속
        conn_string = "host='localhost' dbname ='postgres' user='postgres' password='9407740'"
        conn = psycopg2.connect(conn_string)
        cur = conn.cursor()

        #학교이름 조회
        sql = "select name, latitude, longitude from school_info where id = '"
        sql += ID
        sql += "';"
        cur.execute(sql)
        school_info = cur.fetchall()
        school_name = school_info [0][0] # 학교이름
        school_mapx = school_info [0][1] # 위도 37 ~
        school_mapy = school_info [0][2] # 경도 127 ~

        #학교 tm 좌표 조회
        sql = "SELECT tm_x, tm_y from school_tm where id='"
        sql += ID
        sql += "';"
        cur.execute(sql)

        school_tm = cur.fetchall()
        school_tmX = school_tm[0][0]
        school_tmY = school_tm[0][1]

        #에어코리아 - 근접 측정소 조회
        url = 'http://apis.data.go.kr/B552584/MsrstnInfoInqireSvc/getNearbyMsrstnList'
        key = unquote('Vg6FAsjwouWNL3Z4VtFe1jfEFnxwP60bKiDlp9OGJRVwg0A5WXdI%2F6%2FaZEP6daj3uZ%2FHBdhkEX16wlIFvzFIsw%3D%3D')

        key = requests.utils.unquote(key)
        queryParams = '?' + urlencode({
                    quote_plus('ServiceKey') : key,
                    quote_plus('tmX') : school_tmX,
                    quote_plus('tmY') : school_tmY,
                    quote_plus('returnType') : 'xml'
                    })

        
        request_api = requests.get(url + queryParams).text.encode('utf-8')
        station_info = bs4.BeautifulSoup(request_api, 'lxml-xml')

        #측정소 정보 가져오기(XML 태그 없애서 가져오기)
        station_name_list = station_info.find_all("stationName")
        station_name_list = [station_name_list[i].text for i in range(len(station_name_list))]

        #학교,측정소 사이 거리
        tm_dis_list = station_info.find_all("tm")
        tm_dis_list = [tm_dis_list[i].text for i in range(len(tm_dis_list))]


        #근접측정소 미세먼지 data 가져오기
        pm10 = [
        ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
        ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
        ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"]]

        pm25 = [
            ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
            ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
            ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"]]

        dataTime = ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0",
                    "0", "0"]

        #위*경도
        location = [[0, 0], [0, 0], [0, 0]]

        #url(측정소 미세먼지 데이터), url_location(측정소 위경도 표기)
        url = 'http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty'
        url_location = 'http://apis.data.go.kr/B552584/MsrstnInfoInqireSvc/getMsrstnList'

        for i in range(len(station_name_list)):
            #미세먼지 데이터 API 요청
            queryParams = '?' + urlencode({
                quote_plus('ServiceKey'): key,
                quote_plus('numOfRows'): '30',
                quote_plus('pageNo'): '1',
                quote_plus('stationName'): station_name_list[i],
                quote_plus('dataTerm'): 'DAILY',
                quote_plus('ver'): '1.2'
            })

            #측정소 위경도 API 요청
            queryParams1 = '?' + urlencode({
                quote_plus('ServiceKey'): key,
                quote_plus('returnType'): 'xml',
                quote_plus('numOfRows'): '10',
                quote_plus('pageNo'): '1',
                quote_plus('stationName'): station_name_list[i]
            })

            # 측정소 데이터 가져오기
            request_api = requests.get(url + queryParams).text.encode('utf-8')
            measuring_data_info = bs4.BeautifulSoup(request_api, 'lxml-xml')
            tmp = measuring_data_info.find_all("pm10Value")
            pm10[i] = [j.text for j in tmp]
            tmp = measuring_data_info.find_all("pm25Value")
            pm25[i] = [j.text for j in tmp]

            # 측정소 위경도 가져오기
            location_request_api = requests.get(url_location + queryParams1).text.encode('utf-8')
            ll_data_info = bs4.BeautifulSoup(location_request_api, 'lxml-xml')
            location[i][0] = ll_data_info.find("dmX").text
            location[i][1] = ll_data_info.find("dmY").text

        #시간가져오기
        tmp = measuring_data_info.find_all("dataTime")
        dateTime = [j.text for j in tmp]


        pmdata = [[dateTime[i], pm10[0][i], pm25[0][i], pm10[1][i], pm25[1][i], pm10[2][i], pm25[2][i]] for i in range(len(dateTime))]


        #DB 접속 종료
        conn.close()  


        # # # 지도 데이터 세팅
        # Map1 = folium.Map(location=[location[0][0], location[0][1]], tiles = "OpenStreetMap", zoom_start=15)
        # Map2 = folium.Map(location=[location[1][0], location[1][1]], tiles = "OpenStreetMap", zoom_start=15)
        # Map3 = folium.Map(location=[location[2][0], location[2][1]], tiles = "OpenStreetMap", zoom_start=15)

        # # folium.Marker(location = [location[0][0], location[0][1]], icon = folium.Icon(color='blue', icon = 'star', popup = name)).add_to(Map1)
        # maps=Map1._repr_html_()  #지도를 템플릿에 삽입하기위해 iframe이 있는 문자열로 반환

        attractiondict = []
    #불러온 json 객체들 중 필요한 데이터만 뽑기
        for attraction in location:
            content = {
                "mapx": attraction[0],
                "mapy": attraction[1]
            }
            attractiondict.append(content)
        
        content = {
            "mapx" : school_mapx,
            "mapy" : school_mapy
        }
        attractiondict.append(content)
        attractionJson = json.dumps(attractiondict, ensure_ascii=False)
        print(type(attractiondict))
        print(attractionJson)

        print(school_mapx, school_mapy)
        
        

        # df1 = pd.DataFrame(pm10, columns=dataTime)
        # df2 = pd.DataFrame(pm25, columns=dataTime)

        # df1 = df1.replace('-', -1)
        # df2 = df2.replace('-', -1)

        # df1 = df1.transpose()
        # df2 = df2.transpose()

        # df1 =df1.astype(float)
        # df2 =df2.astype(float)

        # df1 = df1.replace(-1, np.nan)
        # df2 = df2.replace(-1,  np.nan)

        # df1 = df1.fillna(round(df1.mean()))
        # df2 = df2.fillna(round(df2.mean()))

        # font_location = "C:/Windows/fonts/malgun.ttf"
        # font_name = font_manager.FontProperties(fname=font_location).get_name()
        # matplotlib.rc('font', family=font_name)

        # df1.plot(figsize=(20,10), title="PM10", marker='o', markerfacecolor='black', markersize=4, legend=True, label=station_name_list)
        # plt.title(school_name + "의 인근 PM10 측정 자료(24시간)", fontsize=26)
        # plt.legend(station_name_list, fontsize=18)
        # plt.savefig('C:/Users/jsl11/Desktop/web(1017)/apps/static/image/pm10.png', dpi=300)
        
        # df2.plot(figsize=(20,10), title="PM25", marker='o', markerfacecolor='black', markersize=4, legend=True, label=station_name_list)
        # plt.title(school_name + "의 인근 PM2.5 측정 자료(24시간)", fontsize=26)
        # plt.legend(station_name_list, fontsize=18)
        # plt.savefig('C:/Users/jsl11/Desktop/web(1017)/apps/static/image/pm25.png')

        json_pmdata = json.dumps(pmdata)
        json_station_name = json.dumps(station_name_list)
        json_school_name = json.dumps(school_name)
        #넘겨줄 data 세팅
        result = {
            'school_name' : school_name,
            'station_name_list' : station_name_list,
            'tm_dis_list' : tm_dis_list,
            'location_list' : location,
            'pmdata_list' : pmdata,
            'attractionJson' : attractionJson,
            'school_mapx' : school_mapx,
            'school_mapy' : school_mapy,
            'tmp_test' : json_pmdata,
            'tmp_station_name' : json_station_name,
            'tmp_school_name' : json_school_name
            # 'map' : maps
        }


    return render(request, 'new_detail.html', result)

