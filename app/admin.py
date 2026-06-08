from django.contrib import admin
from .models import Survey, Product, Choice, Vote
from django.contrib.auth.models import User
# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "launch_date", "create_at")
    search_fields = ("name", "description")
    list_filter = ("launch_date", ) # فیلتر بر اساس تاریخ عرضه

@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ("product", "question",  "created_at", "is_active")
    list_filter = ("is_active", "product")
    list_editable = ("is_active", ) # توی صفحه لیست بشه فعال/غیر فعال کرد.
    search_fields = ("question", )
    list_select_related = ("product", )

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ("survey", "choice_text", "votes")

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ("user", "choice", "voted_at")
    list_filter = ("voted_at", )
    readonly_fields = ("user", "choice", "voted_at")#جلوگیری از ویرایش رای ها

