from django.contrib import admin
from .models import (
    UserProfile, Project, HiringRequest, ProjectComment, ProjectPurchase,
    PartnershipProposal, PartnershipMessage, UserSuggestion, UserFollow, Notification
)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'especialidade', 'location', 'available_for_hire', 'created_at')
    search_fields = ('user__username', 'especialidade', 'bio')
    list_filter = ('available_for_hire',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'price', 'is_for_sale', 'created_at')
    list_filter = ('category', 'is_for_sale')
    search_fields = ('title', 'author__username', 'description')

@admin.register(ProjectComment)
class ProjectCommentAdmin(admin.ModelAdmin):
    list_display = ('project', 'author', 'created_at')
    search_fields = ('project__title', 'author__username', 'text')

@admin.register(ProjectPurchase)
class ProjectPurchaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'project', 'buyer', 'price_paid', 'license_key', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('project__title', 'buyer__username', 'license_key')

@admin.register(HiringRequest)
class HiringRequestAdmin(admin.ModelAdmin):
    list_display = ('project_title', 'client_name', 'creator', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('project_title', 'client_name', 'client_email', 'creator__username')

@admin.register(PartnershipProposal)
class PartnershipProposalAdmin(admin.ModelAdmin):
    list_display = ('title', 'sender', 'receiver', 'roles', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'sender__username', 'receiver__username', 'roles', 'message')

@admin.register(PartnershipMessage)
class PartnershipMessageAdmin(admin.ModelAdmin):
    list_display = ('partnership', 'sender', 'created_at')
    search_fields = ('sender__username', 'text', 'partnership__title')

@admin.register(UserSuggestion)
class UserSuggestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'suggestion_type', 'user', 'name', 'created_at')
    list_filter = ('suggestion_type', 'created_at')
    search_fields = ('title', 'message', 'name', 'email', 'user__username')


@admin.register(UserFollow)
class UserFollowAdmin(admin.ModelAdmin):
    list_display = ('follower', 'following', 'created_at')
    search_fields = ('follower__username', 'following__username')
    list_filter = ('created_at',)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'sender', 'notification_type', 'title', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('recipient__username', 'sender__username', 'title', 'message')



