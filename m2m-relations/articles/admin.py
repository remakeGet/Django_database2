from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet
from .models import Article, Scope, Tag

class ScopeInlineFormset(BaseInlineFormSet):
     def clean(self):
        super().clean()
        
        # Проверяем, что есть ровно один основной раздел
        main_tags_count = 0
        for form in self.forms:
            if not form.cleaned_data.get('DELETE', False):  # Игнорируем удаляемые формы
                if form.cleaned_data.get('is_main', False):
                    main_tags_count += 1
        
        if main_tags_count == 0:
            raise ValidationError('Укажите основной раздел для статьи')
        elif main_tags_count > 1:
            raise ValidationError('Основным может быть только один раздел')
        
        return self.cleaned_data

class ScopeInline(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormset

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display =['name', 'articles_count']
    search_fields = ['name']

    def articles_count(self, obj):
        return obj.articles.count()
    articles_count.short_description = 'Количество статей'

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'published_at', 'main_tag']
    list_filter = ['published_at', 'tags']
    search_fields = ['title', 'text']
    inlines = [ScopeInline]

    def main_tag(self, obj):
            main_scope = obj.scopes.filter(is_main=True).first()
            return main_scope.tag.name if main_scope else '—'
    main_tag.short_description = 'Основной раздел'