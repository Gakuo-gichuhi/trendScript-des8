from django.contrib import admin
from django_quill.forms import QuillFormField
from django import forms
from django.db.models import Count

from .models import Blog, Comment, Like, ContactMessage, DailyVisitor, DonationInfo, Advert

# =======================
# Monetization/Admin models
# =======================
@admin.register(Advert)
class AdvertAdmin(admin.ModelAdmin):
    list_display = ('title', 'position', 'active', 'start_date', 'end_date')
    list_filter = ('position', 'active')
    search_fields = ('title',)


@admin.register(DonationInfo)
class DonationInfoAdmin(admin.ModelAdmin):
    list_display = ('title', 'mpesa_paybill', 'mpesa_account', 'active')


# =======================
# Blog Admin Inlines
# =======================
class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ('name', 'content', 'time')
    can_delete = False
    show_change_link = False


# Custom Blog Form with Quill
class BlogAdminForm(forms.ModelForm):
    Content = QuillFormField()

    class Meta:
        model = Blog
        fields = '__all__'


# Custom Like Filter
class NoLikesFilter(admin.SimpleListFilter):
    title = 'Like Count'
    parameter_name = 'like_count'

    def lookups(self, request, model_admin):
        return [('0', 'No Likes')]

    def queryset(self, request, queryset):
        if self.value() == '0':
            return queryset.annotate(like_count=Count('likes')).filter(like_count=0)


# =======================
# Blog Admin
# =======================
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    form = BlogAdminForm
    list_display = ('Title', 'Slug', 'Category', 'time', 'total_likes_display')
    list_filter = ('Category', 'time', NoLikesFilter)
    search_fields = ('Title', 'Content', 'overlay_text', 'short_description')
    prepopulated_fields = {'Slug': ('Title',)}
    inlines = [CommentInline]
    readonly_fields = ('time', 'total_likes')
    date_hierarchy = 'time'
    ordering = ('-time',)

    fieldsets = (
        (None, {'fields': ('Title', 'Slug', 'Content', 'Category', 'Image',
                           'overlay_text', 'short_description')}),
        ('Event Info', {'fields': ('event_time', 'event_place')}),
        ('Metadata', {'fields': ('time', 'total_likes')}),
    )

    def total_likes_display(self, obj):
        return obj.total_likes()


# =======================
# Comment Admin
# =======================
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'blog', 'time', 'short_content')
    list_filter = ('time', 'blog')
    search_fields = ('name', 'content')
    readonly_fields = ('time',)
    ordering = ('-time',)
    actions = ['delete_selected_comments']

    def short_content(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content

    def delete_selected_comments(self, request, queryset):
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f"{count} comment(s) deleted.")
    delete_selected_comments.short_description = "Delete selected comments"


# =======================
# Like Admin
# =======================
@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'blog', 'timestamp')
    list_filter = ('timestamp', 'blog')
    search_fields = ('user__username', 'blog__Title')
    readonly_fields = ('timestamp',)
    ordering = ('-timestamp',)


# =======================
# Contact Message Admin
# =======================
# Register ContactMessage
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'time')  # Columns to show
    search_fields = ('name', 'email', 'message')  # Searchable fields
    list_filter = ('time',)  # Filter by date
# =======================
# Daily Visitor Admin
# =======================
@admin.register(DailyVisitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ('date', 'count')
    ordering = ('-date',)


# =======================
# Admin Panel Titles
# =======================
admin.site.index_title = "Dashboard"
admin.site.site_header = "Blog Admin Panel"
admin.site.site_title = "Blog Admin Panel"
