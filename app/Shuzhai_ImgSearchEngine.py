#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import Flask
from flask import request
import requests
import json
from flask import render_template

app = Flask(__name__)

defalutResultNumber = 20
queryText = ''
imgSearchUrl = "http://image.baidu.com/i?tn=baiduimagejson&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1349413075627_R&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&rn=%s&pn=1&ie=utf-8&word=%s"
imgSearchUrlGoogle = "https://www.googleapis.com/customsearch/v1?imgType=clipart&imgSize=medium&q={}&c2coff=true&cx=013330954888113726873%3Ajoas4g2uwxo&searchType=image&key=AIzaSyBI4xqycVazXujMCH4B3SWZbrzSrFHr5pg&start={}"
imgSearchHaosou = "http://image.haosou.com/j?q={}&src=srp&sn=30&pn={}"
imgSearchSougou = "http://pic.sogou.com/pics?query={}&mood=0&picformat=0&mode=1&di=2&w=05009900&dr=1&_asf=pic.sogou.com&_ast=1445969123&start=1&reqType=ajax&tn=0&reqFrom=result"
finalSearchUrl = ''

@app.route('/')
def hello_world():
    return render_template('query.html', name='')

@app.route('/query/<queryText>')
def queryText(queryText):
    rn = request.args.get('pc')
    resultList = []
    if rn is  None:
        rn = 20
    else:
        rn = int(rn.decode('utf-8'))

    resultList = resultList+processRequestSougou(rn,queryText)+processRequestHaosou(rn,queryText)

    return render_template('queryImg.html', imgArray=resultList,searchUrl = finalSearchUrl)

def processRequestSougou(pn,queryText):
    finalSearchUrl = imgSearchSougou.format(queryText.encode('utf-8'))
    r = requests.get(finalSearchUrl)
    d = json.loads(r.text)
    listingArray = d['items']
    imgList =  list(map(getImgArraySougou, listingArray))
    return imgList

def processRequestHaosou(pn,queryText):
    finalSearchUrl = imgSearchHaosou.format(queryText.encode('utf-8'),str(pn))
    r = requests.get(finalSearchUrl)
    d = json.loads(r.text)
    listingArray = d['list']
    imgList =  list(map(getImgArrayHaosou, listingArray))
    return imgList

def processRequestGoogle(pn,queryText):
    finalSearchUrl = imgSearchUrlGoogle.format(queryText.encode('utf-8'),str(pn)) #%(queryText,str(pn))
    r = requests.get(finalSearchUrl)
    d = json.loads(r.text)
    listingArray = d['items']
    imgList =  list(map(getImgArray, listingArray))
    return imgList

def getImgArraySougou(x):
    if x.has_key('pic_url'):
        return x['pic_url']
    else:
        return ""

def getImgArrayHaosou(x):
    if x.has_key('img'):
        return x['img']
    else:
        return ""

def getImgArray(x):
    if x.has_key('link'):
        return x['link']
    else:
        return ""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5656,debug=True)
