import enum


class RoomType(str, enum.Enum):
    PUBLIC = 'public'
    PRIVATE = 'private'


class RoolSetType(str, enum.Enum):
    CUSTOM = 'custom'
    PERMANENT = 'permanent'


class ActionType(str, enum.Enum):
    NO_ACTION = 'no_action'
    KILL = 'kill'
    SAVE = 'save'
    INVESTIGATE = 'investigate'
