#!/usr/bin/env python
# coding: utf-8
import json
import requests

r = requests.post('http://10.60.1.71:9902/op', data =
                  {'query':'不是一个区间刷学生证能有票吗',
                   'passages':'||||'.join(['目前，中国很多地方，票处取票的时候，售票员会刷你学生磁条，比如北京--上海，如果你购买的是北京--昆明，与售票区间显示不符，系统自动拒绝，无法出票，售票员无法继续操作，按打印键出票。',
                               '目前，中国很多地方，学生火车票磁条都已经升级了，在磁条里已经写入了你乘车区间，你在火车站售票处取票的时候，售票员会刷你学生磁条，这时候，电脑屏幕上会显示你的乘车区间，无法出票，售票员无法继续操作，按打印键出票。',
                               '目前，中国很多地方，学生火车票磁条都已经升级了，在磁条里已经写入了你乘车区间，你在火车站售票处取票的时候，售票员会刷你学生磁条，这时候，电脑屏幕上会显示你的乘车区间，比如北京--上海，如果你购买的是北京--昆明，与售票区间显示不符，系统自动拒绝'])})
print(json.dumps(r.json(), ensure_ascii=False))


r = requests.post('http://10.60.1.71:9902/op', data =
                  {'query':'不是一个区间刷学生证能有票吗',
                   'passages':'||||'.join(['不是一个区间没有票的'])})
print(json.dumps(r.json(), ensure_ascii=False))

r = requests.post('http://10.60.1.71:9900/rc', data =
                  {'query':'日本的首都在哪里？',
                   'passages':'||||'.join(['日本首都在东京',
                               '日本首都是东京，错不了',
                               '日本首都在东京吗？是的'])})
print(json.dumps(r.json(), ensure_ascii=False))


