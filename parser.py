#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
import datetime
import logging
import re

logger = logging.getLogger(__name__)


class Message(object):
    def __init__(self, text, msg_handlers):
        self.text = text
        self.r_msg = re.compile(ur"""
            (?<=\n)
            (\d{4}\-\d{1,2}\-\d{1,2}\s+\d{1,2}:\d{1,2}:\d{1,3})  # date
            \s+
            (.*?)                                                # nickname
            (?:\((\d+)\)|<([^>]+)>)\n                            # QQ number
            (.*?)                                                # message
            (?=(?:\d{4}-\d{1,2}-\d{1,2})|\n+$)
        """, re.I | re.X | re.S)
        self.msg_handlers = []
        self.msg_handlers.extend(msg_handlers)

    def _parse(self):
        for data in self.r_msg.findall(self.text):
            date_str, nickname, qq, email, msg = data
            qq = qq or email
            try:
                yield {
                    'date': datetime.datetime.strptime(
                        date_str,
                        '%Y-%m-%d %H:%M:%S'
                    ),
                    'nickname': nickname,
                    'qq': qq,
                    'msg': msg,
                }
            except Exception as e:
                logger.exception(e)

    def _handle(self, msg):
        for handler in self.msg_handlers:
            handler(msg)

    def __call__(self):
        for msg in self._parse():
            self._handle(msg)

if __name__ == '__main__':
    from collections import defaultdict
    from io import open
    check = defaultdict(lambda: defaultdict(dict))

    def handler(msg):
        if datetime.datetime.now() - msg['date'] < datetime.timedelta(days=7):
            if u"打卡" in msg['msg']:
                check[msg['qq']][msg['date'].date()] = msg

    with open('data.txt', encoding='utf-8-sig') as f:
        Message(f.read().replace('\r\n', '\n'), [handler])()

    for v in check.values():
        for x in v.values():
            print(x['nickname'] + ', ' + str(x['date']))
