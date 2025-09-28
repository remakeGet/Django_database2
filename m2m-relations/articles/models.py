from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название раздела')
    
    class Meta:
            verbose_name = 'Раздел'
            verbose_name_plural = 'Разделы'
            ordering = ['name']  # Сортировка по умолчанию по названию
        
    def __str__(self):
        return self.name

class Article(models.Model):

    title = models.CharField(max_length=256, verbose_name='Название')
    text = models.TextField(verbose_name='Текст')
    published_at = models.DateTimeField(verbose_name='Дата публикации')
    image = models.ImageField(null=True, blank=True, verbose_name='Изображение',)
    tags = models.ManyToManyField(Tag, through='Scope', related_name='articles')
    
    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-published_at']  # Сортировка по дате публикации (новые сначала)
    
    def __str__(self):
        return self.title

class Scope(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='scopes')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='scopes')
    is_main = models.BooleanField(default=False, verbose_name='Основной раздел')
    
    class Meta:
        verbose_name = 'Тематика статьи'
        verbose_name_plural = 'Тематики статьи'
        # Уникальность: одна статья может иметь только один основной раздел
        constraints = [
            models.UniqueConstraint(
                fields=['article', 'is_main'],
                condition=models.Q(is_main=True),
                name='only_one_main_tag_per_article'
            )
        ]
    
    def __str__(self):
        return f"{self.article.title} - {self.tag.name} ({'основной' if self.is_main else 'дополнительный'})"