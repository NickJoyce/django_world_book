from django.db import models
from django.urls import reverse
from datetime import date

from django.contrib.auth.models import User


# Create your models here.

class Genre(models.Model):
    name = models.CharField(max_length=200, verbose_name='Жанр книги', help_text="Введите жанр книги")

    def __str__(self):
        return self.name

class Language(models.Model):
    name = models.CharField(max_length=50, verbose_name='Язык книги', help_text="Введите язык книги")

    def __str__(self):
        return self.name

class Author(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="Имя автора", help_text=" Введите имя автора")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия автора", help_text=" Введите фамилию автора")
    date_of_birth = models.DateField(verbose_name="Дата рождения", help_text="Введите дату рождения",
                                     null=True, blank=True)
    date_of_death = models.DateField(verbose_name="Дата смерти", help_text="Введите дату смерти",
                                     null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        """Возвращает URL-адрес для доступа к определенному автору"""
        return reverse('author-detail', args=[str(self.id)])



class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название книги", help_text="Введите название книги")
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE, verbose_name="Жанр книги",
                              help_text="Выберете жанр книги", null=True)
    language = models.ForeignKey('Language', on_delete=models.CASCADE, verbose_name="Язык книги",
                              help_text="Выберете язык книги", null=True)
    author = models.ManyToManyField('Author', verbose_name="Автор книги", help_text="Выберете автора книги")
    summary = models.TextField(max_length=1000, verbose_name="Краткое описание книги",
                               help_text="Введите краткое описние книги")
    isbn = models.TextField(max_length=13, verbose_name="ISBN книги", help_text="Должно содержать 13 символов")

    def display_author(self):
        return ", ".join([author.last_name for author in self.author.all()])

    display_author.short_description = 'Авторы'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Возвращает URL-адрес для доступа к определенному экземпляру книги"""
        return reverse('book-detail', args=[str(self.id)])

class Status(models.Model):
    name = models.CharField(max_length=20, verbose_name="Статус экземпляра книги",
                            help_text="Введите статус экземпляра книги")

    def __str__(self):
        return self.name


class BookInstance(models.Model):
    book = models.ForeignKey('Book', on_delete = models.CASCADE, null=True)
    inv_nom = models.CharField(max_length=20, null=True, verbose_name="Инвентарный номер",
                               help_text="Введите инвентарнй номер экземпляра")
    imprint = models.CharField(max_length=200, verbose_name="Издательство",
                               help_text="Введите наименвоание издательства и год выпуска")
    status = models.ForeignKey('Status', on_delete=models.CASCADE, null=True,
                               verbose_name="Статус", help_text="Изменить статус экземпляра")
    due_back = models.DateField(null=True, blank=True, verbose_name="Дата окончания статуса",
                                help_text="Введите конец срока статуса")
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Заказчик",
                                 help_text='Выберете заказчика книги')

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False


    def __str__(self):
        return f"{self.inv_nom}, {self.book}, {self.status}"



