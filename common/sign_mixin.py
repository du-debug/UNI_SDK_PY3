import hashlib

from utils import to_utf8


class SignMixin(object):


    def calc_sign(self, params):
        keys = sorted(filter(lambda x: x != "sign", params.keys()))
        sign_str = '&'.join(
            ["%s=%s" % (key, to_utf8(params.get(key, ''))) for key in keys if params.get(key, "") != ""])
        print("sign_str:{}".format(sign_str))
        sign = hashlib.md5((sign_str + self._app['key']).encode('utf-8')).hexdigest()
        print("sign:{}".format(sign))
        return sign


if __name__ == "__main__":

    pass