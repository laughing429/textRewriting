#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os

from onmt.utils.logging import init_logger
from onmt.translate.translator import build_translator
from onmt.opts import translate_opts

def trans(n_bset,content_src):
    parser = argparse.ArgumentParser()
    translate_opts(parser)

    opt = parser.parse_args()

    model_dir = os.path.join(os.path.dirname(__file__), 'available_models')
    opt.model=os.path.join(model_dir, 'zh2zh_model_2000000.pt')
    opt.n_best=n_bset
    opt.gpu=-1
    opt.data_type='text'

    translator = build_translator(opt, report_score=True)
    result = translator.translate(src_path=opt.src,
                                  src_data_iter=content_src,
                                  tgt_path=opt.tgt,
                                  src_dir=opt.src_dir,
                                  batch_size=opt.batch_size,
                                  attn_debug=opt.attn_debug)
    return result


if __name__ == "__main__":
    content = ['星期五 到 了 真 开心！']
    ss=trans(2,content)
    for i in ss:
        print('/'.join(i))