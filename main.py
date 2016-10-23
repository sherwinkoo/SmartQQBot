# -*- coding: utf-8 -*-
# Code by Yinzo:        https://github.com/Yinzo
# Origin repository:    https://github.com/Yinzo/SmartQQBot

import time
import sys
import socket
import json
from redis import Redis

from QQLogin import QQ, logging
from MsgHandler import MsgHandler

reload(sys)
sys.setdefaultencoding("utf-8")


def reload_login_state(c, bot):
    state = c.get("qq!login_state")
    if state:
        state = json.loads(state)
        bot.account = state['account']
        bot.username = state['username']
        bot.psessionid = state['session_id']
        bot.ptwebqq = state['ptwebqq']
        bot.vfwebqq = state['vfwebqq']
        bot.client_id = state['client_id']
        return True

    return False


def dump_login_state(c, bot):
    state = dict(
        account=bot.account,
        username=bot.username,
        session_id=bot.psessionid,
        ptwebqq=bot.ptwebqq,
        vfwebqq=bot.vfwebqq,
        client_id=bot.client_id
    )
    c.set("qq!login_state", json.dumps(state, ensure_ascii=False))


def main():
    client = Redis(host="127.0.0.1", db=2)

    bot = QQ()
    if True:
    # if not reload_login_state(client, bot):
        ok, message = bot.login_by_qrcode()
        if not ok:
            logging("Login failed: %s", message)
            return

    try:
        bot_handler = MsgHandler(bot)
        while True:
            time.sleep(0.5)
            try:
                new_msg = bot.check_msg()
                print "message: ", new_msg
            except socket.timeout as ex:
                logging.warning("check msg timeout, retrying... %s", ex)
                continue
            if new_msg is not None:
                bot_handler.handle(new_msg)
    except KeyboardInterrupt:
        logging.info("Stop Bot. Logout.")
    finally:
        dump_login_state(client, bot)
        logging.info("Dump login state... OK")

if __name__ == '__main__':
    logging.basicConfig(
        # filename='smartqq.log',
        level=logging.DEBUG,
        format='%(asctime)s  %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
        datefmt='%a, %d %b %Y %H:%M:%S',
    )
    main()
