# -*- coding: utf-8 -*-

import time
import json

from redis import Redis


class Vampire(object):

    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.redis = kwargs['redis']
        self.from_key = "qq!private_messages: 695817458"
        self.to_key = "qq!private_replies: 695817458"

    def run(self):
        while True:
            time.sleep(0.5)

            lines, _ = self.redis.pipeline().lrange(self.from_key, 0, 1).delete(self.from_key).execute()
            if not lines:
                continue

            line = json.loads(lines[0])
            message = line['message'].strip(u' ')

            print "receive: ", type(message), len(message), message, len(u'你是谁')
            if message == u"你是谁":
                reply = u'我是{}'.format(self.name)
            else:
                reply = u'我不明白什么是: {}'.format(message)

            self.redis.lpush(self.to_key, reply)


if __name__ == "__main__":

    girl = Vampire(
        name=u'Mavis Dracula',
        redis=Redis(host='115.28.33.37', db=1)
    )
    try:
        girl.run()
    except KeyboardInterrupt:
        print "I'm going to bed. Call me later."
