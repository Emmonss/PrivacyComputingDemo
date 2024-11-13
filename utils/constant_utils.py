

import os


PICKLE_VERSION=3
ABS_PROJECT_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

#http client get interval
DEFAULT_GET_SLEEP_TIME = 0.1
DEFAULE_GET_OVERTIME = 3600*2


#http
HTTP_SUPPORT_PROTOCOLS = ["http","https"]
HTTP_MAX_BODY_LENGTH = 10*1024*1024
HTTP_RETRY_TIMES = 3
HTTP_SLEEP_TIME = 0.5

#logger
LOG_DIR = os.path.join(ABS_PROJECT_PATH,"logs")
LOG_WHEN = 'D'
LOG_INTERVAL = 1 
LOG_BACKUP = 3
LOG_FILE_LEVEL = "debug"
LOG_SCREEN_LEVEL = "debug"
LOG_PLATFORM_LEVEL = "info"


#hash
HASH_MD5 = 'md5'
HASH_SHA1 = 'sha1'
HASH_SHA224 = 'sha224'
HASH_SHA256 = 'sha256'
HASH_SHA384 = 'sha384'
HASH_SHA512 = 'sha512'
HASH_SM3 = 'sm3'
HASH_NONE = 'none'


#grpc
GRPC_PORT = 50004

if __name__ == '__main__':
    pass
    print(ABS_PROJECT_PATH)