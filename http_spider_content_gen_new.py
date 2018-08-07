#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# Create on: 2018/4/3 0003 15:13 
# Author: Lyu 
# Annotation:

# from __future__ import division, unicode_literals
import web,jieba,string
import json
import os
import argparse
import codecs

from onmt.utils.logging import init_logger
from onmt.translate.translator import build_translator
# import onmt.inputters
# import onmt.translate
import onmt
# import onmt.model_builder
# import onmt.modules
# import onmt.opts

# from html_parse import htmlExtract
import random
import time
from urllib.parse import unquote, urlparse
# from dbhandle.LogHandle import loghandle

# logger = loghandle('info', 'content_gen')
urls = ('/1101/content_gen/', 'content_gen')

# web.config.debug = True

# with codecs.open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'stopword'), 'r', 'utf8') as f:
#     stopword = set(map(lambda x: x.strip(), f.readlines()))

# def extract_keyword(texts, nkey=20):
#     keywords = ja.extract_tags(texts, nkey)
#     return filter(lambda x: x not in stopword, keywords)

DELIMITER = {u'?', u'!', u';', u'？', u'！', u'。', u'；', u'……', u'…', '\n', u'.',u'——'}

def trans(n_bset,content_src):
    parser = argparse.ArgumentParser()
    parser.add_argument('x', type=int, help="the base")
    onmt.opts.translate_opts(parser)

    opt = parser.parse_args()

    model_path = os.path.join(os.path.dirname(__file__), 'available_models')

    opt.model=os.path.join(model_path, 'zh2zh_model_2000000.pt')
    opt.n_best=n_bset
    opt.gpu=-1
    opt.data_type='text'
    opt.replace_unk = True

    translator = build_translator(opt, report_score=True)
    result = translator.translate(src_path=opt.src,
                                  src_data_iter=content_src,
                                  tgt_path=opt.tgt,
                                  src_dir=opt.src_dir,
                                  batch_size=opt.batch_size,
                                  attn_debug=opt.attn_debug)
    return result

def seg_sentence(content):
    """拆分文本为一个一个句子"""
    senList = []
    sen = []
    dellim=[]
    for word in content:
        if word not in DELIMITER:
            sen.append(word)
        else:
            sentence = ''.join(sen).strip()
            dellim.append(word)
            if sentence not in DELIMITER:
                senList.append(sentence)
            sen = []
    if sen:
        sentence = ''.join(sen)
        senList.append(sentence)

    return senList,dellim


def key_words(original_text):
    """取关键词"""
    try:
        text = original_text.decode('utf-8')
    except:
        text = original_text
    clean_text = []
    for i in text:
        if i not in string.printable + u'\u3000' + u'。，‘’“”；：':
            clean_text.append(i)
    clean_text = ''.join(clean_text)
    final_text = [w.word for w in jieba.posseg.cut(clean_text) if 'n'in w.flag or 'v' in w.flag or 'i' in w.flag]
    return final_text

class content_gen:
    def POST(self):
        # sendData = web.data().decode(encoding='utf8', errors='strit')
        sendData = web.input()
        print(sendData)
        # da = urlparse(sendData)

        text = sendData['data']
        count = int(sendData['count'])

        #
        # while(len(logger.handlers)>1):
        #     logger.handlers.pop()

        # ss = subSecond(rootPath) # 两次调取接口的时间间隔
        # if ss < 10:
        #     time.sleep(10-ss)

        if not text:
            return json.dumps({'content': "Error ! Please check your senddata!",
                               'type': 0})

        # if not isinstance(text, unicode):
        #     text = unicode(text, 'utf8')

        # logger.info({'senddata': text, 'count': count})

        # keywords = extract_keyword(text)
        # if not keywords:
        #     return json.dumps({'content': "The senddata is meaningless!",
        #                        'type': 0})
        text_cut=' '.join(jieba.lcut(text, cut_all=False))

        if count<2:
            count=2
        senList,dellim=seg_sentence(text_cut)
        sentencs = []
        result = trans(count, senList)
        nu_sen=0
        for ij in range(count):
            sen=''
            del_n=0
            for re in result:
                sen=sen+re[ij-1]
                if sen[-1]!=dellim[del_n]:
                    sen += dellim[del_n]
                del_n+=1
            if sen!=text:
                nu_sen+=1
                sentencs.append(sen)
                if nu_sen>=count-1:
                    break
        return json.dumps({'content': sentencs,'type': 1})

if __name__ == '__main__':
    app = web.application(urls, globals(), autoreload=True)
    app.run()