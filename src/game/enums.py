from enum import Enum


class RoomType(str, Enum):
    PUBLIC = 'public'
    PRIVATE = 'private'


class RoolSetType(str, Enum):
    CUSTOM = 'custom'
    PERMANENT = 'permanent'


class ActionType(str, Enum):
    NO_ACTION = 'no_action'
    KILL = 'kill'
    SAVE = 'save'
    INVESTIGATE = 'investigate'
