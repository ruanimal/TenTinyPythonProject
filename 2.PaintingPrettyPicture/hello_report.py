#!/usr/bin/env python
# -*- coding:utf-8 -*-

from reportlab.graphics.shapes import Drawing, String
from reportlab.graphics import renderPDF

d = Drawing(100, 100)   # 新建画布
s = String(50, 50, 'Hello, world', textAnchor='middle')     # 新建文本对象

d.add(s)

renderPDF.drawToFile(d, 'Hello.pdf', 'A simple PDF file')   # 将画布写入文件
