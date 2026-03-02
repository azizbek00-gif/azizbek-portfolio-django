from django.db import models

class About(models.Model):
    full_name = models.CharField(max_length=100, verbose_name="To'liq ism")
    title = models.CharField(max_length=200, verbose_name="Kasb")
    bio = models.TextField(verbose_name="Bio")
    profile_image = models.ImageField(upload_to='profile/', verbose_name="Profil rasmi")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Tug'ilgan sana")
    address = models.CharField(max_length=200, verbose_name="Manzil")
    education = models.CharField(max_length=200, verbose_name="O'qish joyi")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, verbose_name="Telefon")
    github = models.CharField(max_length=100, verbose_name="GitHub username")
    
    def __str__(self):
        return self.full_name
    
    class Meta:
        verbose_name = "Men haqimda"
        verbose_name_plural = "Men haqimda"

class Project(models.Model):
    CATEGORY_CHOICES = [
        ('web', 'Veb-sayt'),
        ('bot', 'Telegram Bot'),
        ('iot', 'IoT'),
        ('mobile', 'Mobil'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Loyiha nomi")
    description = models.TextField(verbose_name="Tavsif")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name="Kategoriya")
    image = models.ImageField(upload_to='projects/', verbose_name="Rasm")
    technologies = models.CharField(max_length=200, verbose_name="Texnologiyalar")
    github_link = models.URLField(blank=True, verbose_name="GitHub link")
    live_link = models.URLField(blank=True, verbose_name="Demo link")
    featured = models.BooleanField(default=False, verbose_name="Muhim loyiha")
    created_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Loyiha"
        verbose_name_plural = "Loyihalar"
        ordering = ['-featured', '-created_date']

class Contact(models.Model):
    name = models.CharField(max_length=100, verbose_name="Ism")
    email = models.EmailField(verbose_name="Email")
    message = models.TextField(verbose_name="Xabar")
    created_date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False, verbose_name="O'qilganmi")
    
    def __str__(self):
        return f"{self.name} - {self.created_date}"
    
    class Meta:
        verbose_name = "Xabar"
        verbose_name_plural = "Xabarlar"
        ordering = ['-created_date']
