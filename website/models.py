from django.db import models
from blog.models import BaseModel
from django.utils.text import slugify

class coordinator(BaseModel):
    last_name = models.CharField(max_length=255, verbose_name='Nom du coordonnateur')
    first_name = models.CharField(max_length=255, verbose_name='Prénom du coordonnateur')
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    full_name_of_coordinator_position = models.CharField(max_length=255, verbose_name='Nom complet du poste')
    word_from_the_coordinator = models.TextField(max_length=5000, verbose_name='Mot du coordonnateur')
    biography = models.TextField(max_length=5000, verbose_name='Biographie')
    image_coordinator = models.ImageField(upload_to='Coordonnateur_image/', verbose_name='Photo du coordonnateur')
    is_current = models.BooleanField(default=False, verbose_name='En fonction actuellement')

    class Meta:
        verbose_name_plural = "Coordonnateurs"

    def __str__(self):
        return self.full_name_of_coordinator_position

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.first_name)
            unique_slug = base_slug
            num = 1
            while coordinator.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{num}"
                num += 1
            self.slug = unique_slug

        if self.is_current:
            coordinator.objects.filter(is_current=True).update(is_current=False)

        super().save(*args, **kwargs)
