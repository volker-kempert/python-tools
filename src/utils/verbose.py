# -*- UTF-8 -*-

class Verboser(object):
    """
    Always log to stdout
    """

    _level = 0
    LEVEL_NONE = 0
    LEVEL_MIN = 1
    LEVEL_NORM = 2
    LEVEL_MAX = 3
    LEVEL_DEBUG = 4

    @classmethod
    def _verbose(cls, level, prefix, text):
        if cls._level >= level:
            print prefix + text

    @classmethod
    def verbose_min(cls, text):
        prefix = '# '
        cls._verbose(cls.LEVEL_MIN, prefix, text)

    @classmethod
    def verbose(cls, text):
        prefix = '## '
        cls._verbose( cls.LEVEL_NORM, prefix, text)

    @classmethod
    def verbose_max(cls, text):
        prefix = '### '
        cls._verbose(cls.LEVEL_MAX, prefix, text)

    @classmethod
    def verbose_debug(cls, text, func=None):
        prefix = '#### '
        if func:
            prefix = "{0}{1}: ".format(prefix, func)
        cls._verbose(cls.LEVEL_DEBUG, prefix, text)

    @classmethod
    def set_level(cls, level):
        cls._level = level