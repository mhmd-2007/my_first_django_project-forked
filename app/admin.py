from django.contrib import admin
from .models import Survey, Product, Choice, Vote

# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "launch_date", "create_at")
    search_fields = ("name", )

@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ("product", "question",  "created_at", "is_active")
    list_filter = ("is_active", "product")

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ("survey", "choice_text", "votes")

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ("user", "choice", "voted_at")

