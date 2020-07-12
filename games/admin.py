from django.contrib import admin
from .models import *

admin.site.register(Board)
admin.site.register(Player)
admin.site.register(State)
admin.site.register(Piece)
admin.site.register(Message)