from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from PIL import Image
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

from authentication.models import User


# Create your models here.
class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add = True, blank=True, null=True)
    updated_date = models.DateTimeField(auto_now = True, blank=True, null=True)

    class Meta:
        abstract = True

class Photo(BaseModel):
    image = models.ImageField()
    caption = models.CharField(max_length=128, blank=True)
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    #date_created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.caption}'

    IMAGE_MAX_SIZE = (800, 800)
    def resize_image(self):
        image = Image.open(self.image)
        image.thumbnail(self.IMAGE_MAX_SIZE)
        # sauvegarde de l’image redimensionnée dans le système de fichiers
        # ce n’est pas la méthode save() du modèle !
        image.save(self.image.path)

        def save(self, *args, **kwargs):
            super().save(*args, **kwargs)
            self.resize_image()

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Libellé de la categorie")
    description = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Categorie de l'article"
        verbose_name_plural = "Categories des articles"
    def __str__(self):
        return self.name

    def post_count(self):
        return self.blog_set.count()


class Blog(BaseModel):
    title = models.CharField(max_length=255, unique=True, verbose_name="Titre")
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Auteur")
    last_updated = models.DateTimeField(auto_now=True, verbose_name="Dernière modification")
    created_on = models.DateField(default=timezone.now, blank=True, null=True, verbose_name="Date de publication")
    published = models.BooleanField(default=False, verbose_name="Publié")
    content = models.TextField(blank=True, verbose_name="Contenu")
    main_image = models.ImageField(upload_to='blog_images/', blank=True, null=True, verbose_name="Image principale")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Categorie")
    class Meta:
        ordering = ['-created_on']
        verbose_name = "Article"
        verbose_name_plural = "Articles"
    def __str__(self):
        return f'{self.title}'

    def _get_word_count(self):
        return len(self.content.split(' '))

    def save(self, *args, **kwargs):
        self.word_count = self._get_word_count()
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    @property
    def author_or_default(self):
        if self.author:
            self.author.username
        return "Auteur inconnu"

    def get_absolute_url(self):
        return reverse('blog:home')

class BlogPostImage(models.Model):
    post = models.ForeignKey(Blog, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blog_images/', verbose_name="Image secondaire")

    class Meta:
        verbose_name = "Image de l'article"
        verbose_name_plural = "Images des articles"

    def __str__(self):
        return f"Image for {self.post.title}"

