from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from PIL import Image

# Create your models here.
class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add = True, blank=True, null=True)
    updated_date = models.DateTimeField(auto_now = True, blank=True, null=True)

    class Meta:
        abstract = True

class Photo(BaseModel):
    image = models.ImageField()
    caption = models.CharField(max_length=128, blank=True)
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
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

class Blog(BaseModel):
    photo = models.ForeignKey(Photo, null=True, on_delete=models.SET_NULL, blank=True)
    title = models.CharField(max_length=128)
    content = models.TextField(max_length=5000)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    #date_created = models.DateTimeField(auto_now_add=True)
    starred = models.BooleanField(default=False)
    #word_count = models.IntegerField(null=True,validators=[MinValueValidator(0)])
    #contributors = models.ManyToManyField(settings.AUTH_USER_MODEL, through='BlogContributor', related_name='contribution')
    def __str__(self):
        return f'{self.title}'

    def _get_word_count(self):
        return len(self.content.split(' '))

    def save(self, *args, **kwargs):
        self.word_count = self._get_word_count()
        super().save(*args, **kwargs)
