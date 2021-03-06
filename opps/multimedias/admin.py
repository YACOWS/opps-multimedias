from django import forms
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from opps.articles.admin import ArticleAdmin

from .models import (Audio, Video, MediaBox, MediaBoxAudios,
                     MediaBoxVideos, MediaConfig)
from opps.core.admin import PublishableAdmin


class MediaAdminForm(forms.ModelForm):

    headline = forms.CharField(_(u"Headline"), widget=forms.Textarea,
                               required=True)


class VideoAdminForm(MediaAdminForm):
    class Meta:
        model = Video


class AudioAdminForm(MediaAdminForm):
    class Meta:
        model = Audio


class MediaAdmin(ArticleAdmin):
    add_form_template = 'admin/change_form.html'
    change_form_template = 'multimedias/admin/change_form.html'
    readonly_fields = ArticleAdmin.readonly_fields[:]
    readonly_fields += ['published', 'date_available']

    fieldsets = (
        (_(u'Identification'), {
            'fields': ('site', 'title', 'slug', 'get_http_absolute_url',
                       'short_url')}),
        (_(u'Content'), {
            'fields': ('short_title', 'headline', 'media_file', 'tags')}),
        (_(u'Relationships'), {
            'fields': ('channel', )}),
        (_(u'Publication'), {
            'classes': ('extrapretty'),
            'fields': ('published', 'date_available')}),
    )


class VideoAdmin(MediaAdmin):
    form = VideoAdminForm


class AudioAdmin(MediaAdmin):
    form = AudioAdminForm


#OPPS RELATIONS
class MediaBoxAudiosInline(admin.TabularInline):
    model = MediaBoxAudios
    fk_name = 'mediabox'
    raw_id_fields = ['audio']
    actions = None
    extra = 1
    fieldsets = [(None, {
        'classes': ('collapse',),
        'fields': ('audio', 'order')})]


class MediaBoxVideosInline(admin.TabularInline):
    model = MediaBoxVideos
    fk_name = 'mediabox'
    raw_id_fields = ['video']
    actions = None
    extra = 1
    fieldsets = [(None, {
        'classes': ('collapse',),
        'fields': ('video', 'order')})]


class MediaBoxAdmin(PublishableAdmin):
    prepopulated_fields = {"slug": ["name"]}
    list_display = ['name', 'date_available', 'published']
    list_filter = ['date_available', 'published']
    inlines = [MediaBoxVideosInline, MediaBoxAudiosInline]
    exclude = ('user',)
    raw_id_fields = ['channel', 'article']

    fieldsets = (
        (_(u'Identification'), {
            'fields': ('site', 'name', 'slug')}),
        (_(u'Relationships'), {
            'fields': (('channel', 'article'),)}),
        (_(u'Publication'), {
            'classes': ('extrapretty'),
            'fields': ('published', 'date_available')}),
    )


class MediaConfigAdmin(PublishableAdmin):
    list_display = ['key', 'key_group', 'channel', 'date_insert',
                    'date_available', 'published']
    list_filter = ["key", 'key_group', "channel", "published"]
    search_fields = ["key", "key_group", "value"]
    raw_id_fields = ['audio', 'video', 'channel', 'article']
    exclude = ('user',)


admin.site.register(Video, VideoAdmin)
admin.site.register(Audio, AudioAdmin)
admin.site.register(MediaBox, MediaBoxAdmin)
admin.site.register(MediaConfig, MediaConfigAdmin)
