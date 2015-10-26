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
finalSearchUrl = ''

@app.route('/')
def hello_world():
    return render_template('query.html', name='')

@app.route('/query/<queryText>')
def queryText(queryText):
    rn = request.args.get('pc')
    resultList = []
    if rn is  None:
        rn = 2
    else:
        rn = int(rn.decode('utf-8'))
    for i in range(1,rn):
            resultList = resultList+processRequest(i,queryText)

    return render_template('queryImg.html', imgArray=resultList,searchUrl = finalSearchUrl)


def processRequest(pn,queryText):
    finalSearchUrl = imgSearchUrlGoogle.format(queryText.encode('utf-8'),str(pn)) #%(queryText,str(pn))
    r = requests.get(finalSearchUrl)
    d = json.loads(r.text)
    listingArray = d['items']
    imgList =  list(map(getImgArray, listingArray))
    return imgList

def getImgArray(x):
    if x.has_key('link'):
        return x['link']
    else:
        return ""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5656,debug=True)
