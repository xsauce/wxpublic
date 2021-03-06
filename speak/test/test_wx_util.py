# coding:utf-8
import logging

from speak.util import handle_wx_message

__author__ = 'samgu'

def test_handle_wx_message():
    logger = logging.getLogger(__name__)
    test_xml = u'<xml><URL><![CDATA[http://133.130.120.211/wx]]></URL><ToUserName><![CDATA[111]]></ToUserName><FromUserName><![CDATA[222]]></FromUserName><CreateTime>13414141</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[你好]]></Content><MsgId>11</MsgId></xml>'
    reply_txt = handle_wx_message(test_xml)
    if reply_txt == 'nihao':
        logger.info('test handle wx message ok')
    else:
        logger.info('test handle wx message reply txt:%s' % reply_txt)

if __name__ == '__main__':
    test_handle_wx_message()