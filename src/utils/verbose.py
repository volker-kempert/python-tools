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

    @classmethod
    def _verbose(cls, level, text):
        if cls._level >= level:
            print '## ', text

    @classmethod
    def verbose_min(cls, text):
        cls._verbose(cls.LEVEL_MIN, text)

    @classmethod
    def verbose(cls, text):
        cls._verbose( cls.LEVEL_NORM, text)

    @classmethod
    def verbose_max(cls, text):
        cls._verbose(cls.LEVEL_MAX, text)

    @classmethod
    def set_level(cls, level):
        cls._level = level