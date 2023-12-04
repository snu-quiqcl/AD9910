# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 21:08:21 2023

@author: alexi
"""

from pdf2docx import Converter
import sys
import re

# PDF 파일 경로와 변환할 페이지 범위 지정
pdf_file = 'arty_s7_sch-rev_b.pdf'
docx_file = 'arty_s7_sch-rev_b.docx'
pages_to_convert = [2]  # 예를 들어 3번째 페이지만 변환하고 싶다면 [2]로 설정

# Converter 객체 생성

# 특정 페이지를 Word 파일로 변환
cv = Converter(pdf_file)
cv.convert(docx_file, start=0, end=None)
cv.close()