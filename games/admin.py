from django.contrib import admin
from .models import *

admin.site.register(BoardModel)
admin.site.register(PlayerModel)
admin.site.register(StateModel)
admin.site.register(PlayerStateModel)
admin.site.register(PieceModel)
admin.site.register(ChangeModel)