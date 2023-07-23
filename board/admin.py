from django.contrib import admin
from board.models import Question

admin.site.register(Question)


class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['subject']


admin.site.register(Question, QuestionAdmin)

