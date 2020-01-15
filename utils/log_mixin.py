"""
基于tornado的提供的日志服务
"""
import logging
import settings
import os
from tornado.options import options
from utils.log_formatter import MyLogFormatter
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler


class MyLogger(logging.Logger):

    pass

class LogMixix(object):


    def _get_logger(self, level_name):
        if hasattr(self.__class__, 'logger_inited'):
            print("继续使用")
            log_base_name = getattr(self.__class__, 'log_base_name')
            min_level = getattr(logging, options.logging.upper())
            if getattr(logging, level_name.upper()) < min_level:
                level_name = options.logging
            logger_name = '%s_%s' % (self.log_base_name, level_name)
            logger = getattr(self.__class__, logger_name)
        else:
            log_to_file = hasattr(options, 'log_to_file') and options.log_to_file
            logging.setLoggerClass(MyLogger)
            if log_to_file and hasattr(self.__class__,"logBaseDir"):
                log_base_name = getattr(self.__class__,"logBaseDir")
            else:
                log_base_name = "default"
            setattr(self.__class__, 'log_base_name', log_base_name)
            log_dir = os.path.abspath(os.path.join(settings.log_base_dir, log_base_name))
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
            level_names = dict(debug=logging.DEBUG, info=logging.INFO, warning=logging.WARNING, error=logging.ERROR)
            min_level = getattr(logging, options.logging.upper())
            for n,l in level_names.items():
                if l < min_level:
                    continue
                log_name = '%s_%s' % (log_base_name,n)
                logger = self.create_logger(log_name,l)
                if log_to_file:
                    path = self.get_log_file(n, log_dir)
                    handler = self.create_TimedRotatingFileHandler(
                        l, path, settings.log_rotating_when, settings.log_backup_count
                    )
                    logger.addHandler(handler)
                else:
                    logger = self.create_logger(log_name, l)
                    chanel = logging.StreamHandler()  # 默认的handler
                    file_chanel = logging.FileHandler(self.get_log_file(n, log_dir))
                    formatter = MyLogFormatter(color=True)
                    chanel.setFormatter(formatter)
                    file_chanel.setFormatter(formatter)
                    logger.addHandler(chanel)
                    logger.addHandler(file_chanel)
                setattr(self.__class__, log_name, logger)
            setattr(self.__class__, 'logger_inited', True)

            if getattr(logging, level_name.upper()) < min_level:
                level_name = options.logging

            logger_name = '%s_%s' % (log_base_name,level_name)
            logger = getattr(self.__class__, logger_name)
        return logger

    def create_logger(self, name, level):
        logger = logging.getLogger(name)
        logger.propagate = False
        logger.setLevel(level)
        # logger 默认有多个 handler, 移除自己手动添加
        [logger.removeHandler(h) for h in logger.handlers]
        return logger

    def get_log_file(self, level_name, parent_file):
        """区分不同的日志输出文件"""
        return os.path.join(parent_file, '{}@{}.log'.format(level_name, options.port))

    # 以下是一些高级handler
    def create_RotatingFileHandler(self, file_prefix, level):
        """根据大小切割日志"""
        channel = RotatingFileHandler(
            filename=file_prefix, maxBytes=1024
        )
        channel.setLevel(level)
        channel.setFormatter(MyLogFormatter(color=True))
        return channel

    def create_TimedRotatingFileHandler(self, level, file_prefix, when, backup_count):
        """根据时间切割日志"""
        channel = TimedRotatingFileHandler(
            filename=file_prefix,
            when=when,
            backupCount=backup_count
        )
        channel.setLevel(level)
        channel.setFormatter(MyLogFormatter(color=True))
        return channel

    def log_info(self, msg, *args, **kwargs):
        self._get_logger('info').info(msg, *args, **kwargs)

    def log_debug(self, msg, *args, **kwargs):
        self._get_logger('debug').info(msg, *args, **kwargs)

    def log_warning(self, msg, *args, **kwargs):
        self._get_logger('warning').info(msg, *args, **kwargs)

    def log_error(self, msg, *args, **kwargs):
        self._get_logger('error').info(msg, *args, **kwargs)


if __name__ == "__main__":

    pass

