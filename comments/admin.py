from django.contrib import admin
from import_export.admin import ExportActionModelAdmin

from .models import Comment

# Register your models here.


@admin.register(Comment)
class CommentAdmin(ExportActionModelAdmin, admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "short_content",
        "correlation_article",
        "correlation_software",
        "state",
        "created_time",
        "parent",
    ]
    search_fields = [
        "content",
        "user__username",
        "user__nickname",
        "correlation_article__title",
        "correlation_software__short_name",
    ]
    list_filter = ["state", "created_time", "correlation_article", "correlation_software"]
    ordering = ["-created_time", "id"]
    list_per_page = 10
    actions = ["pass_audit_batch", "reject_audit_batch"]

    def pass_audit_batch(self, request, queryset):
        for obj in queryset:
            if obj.state == 2:
                continue
            obj.state = 2
            obj.save()
        self.message_user(request, "已全部审核通过！", level="success")

    pass_audit_batch.short_description = "审核"

    def reject_audit_batch(self, request, queryset):
        for obj in queryset:
            if obj.state == 3:
                continue
            obj.state = 3
            obj.save()
        self.message_user(request, "已全部拒绝！", level="warning")

    reject_audit_batch.short_description = "拒绝"
