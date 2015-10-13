#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import Flask
from flask import request
import requests
import json
from flask import render_template

app = Flask(__name__)

defalutResultNumber = 10
queryText = ''
imgSearchUrl = "http://image.baidu.com/i?tn=baiduimagejson&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1349413075627_R&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&rn=%s&pn=1&ie=utf-8&word=%s"

@app.route('/')
def hello_world():
    return render_template('query.html', name='')

@app.route('/query/<queryText>')
def queryText(queryText):
    rn = request.args.get('rn')
    finalSearchURL= ''
    if rn is not None:
        finalSearchURL = imgSearchUrl %(rn,queryText)
    else:
        finalSearchURL = imgSearchUrl %(defalutResultNumber,queryText)
    r = requests.get(finalSearchURL)
    d = json.loads(r.text)
    listingArray = d['data']
    imgList =  list(map(getImgArray, listingArray))
    return json.dumps(imgList)




def getImgArray(x):
    if x.has_key('middleURL'):
        return x['middleURL']
    else:
        return ""

if __name__ == '__main__':
    app.run(debug=True)
