from lib.ai import AI
from util import log

__author__ = 'samgu'
import hashlib
from lxml import etree

def valid_wx(token, timestamp, nonce, signature):
    valid_str = ''.join(sorted([token, timestamp, nonce]))
    valid_str = hashlib.sha1(valid_str).hexdigest()
    if valid_str.lower() == signature.lower():
        return 1
    else:
        return 0


def handle_wx_message(xml_str, logger):
    try:
        if xml_str:
            parser = WXMessageParser(xml_str)
            msg_dict = parser.parse()
            reply_dict = AI().get_wx_reuslt(msg_dict)
            reply = WXMessageReply(msg_dict['to_user_name'], msg_dict['from_user_name'], reply_dict)
            reply_xml = reply.reply_xml()
            logger.debug('succss to reply xml:{0}'.format(reply_xml))
            return reply_xml
        else:
            raise Exception('message xml is null')

    except:
        logger.error('fail to reply wx message')
        return 'failed'


class WXMessageParser(object):
    def __init__(self, xml_str):
        self.xml_str = xml_str
        self.logger = log.get_server_logger()

    def parse(self):
        msg_dict = {}
        try:
            if self.xml_str:
                self.xml_obj = etree.fromstring(self.xml_str)
                msg_dict['to_user_name'] = self.xml_obj.xpath('/ToUserName').text
                msg_dict['from_user_name'] = self.xml_obj.xpath('/FromUserName').text
                msg_dict['create_time'] = self.xml_obj.xpath('/CreateTime').text
                msg_dict['msg_type'] = self.xml_obj.xpath('/MsgType').text
                msg_dict['content_obj'] = getattr(self, msg_dict['msg_type'] + '_parse')(self)
                return msg_dict
        except Exception, e:
            self.logger.error('fail to parse wx message', exc_info=True)
            raise e

    def text_parse(self):
        return self.xml_obj.xpath('/Content').text


class WXMessageReply(object):
    def __init__(self, from_user_name, to_user_name, reply_dict):
        self.from_user_name = from_user_name
        self.to_user_name = to_user_name
        self.reply_dict = reply_dict

    def reply_xml(self):
        return getattr(self, self.reply_dict['msg_type'] + '_reply')(self)

    def text_reply(self):
        pass




