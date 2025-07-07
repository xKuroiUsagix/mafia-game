from sqladmin import ModelView
from .models import RoolSet, GameRole


class RoolSetAdminView(ModelView, model=RoolSet):
    column_list = [RoolSet.id, RoolSet.name]


class GameRoleAdminView(ModelView, model=GameRole):
    column_list = [GameRole.id, GameRole.name, GameRole.is_special]
