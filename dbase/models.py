from django.db import models

class Place(models.Model):
    short_name = models.CharField('короткое название',max_length=50)
    full_name = models.CharField('полное название',max_length=250, blank=True)
    address = models.CharField('адрес',max_length=250, blank=True)
    def __str__(self):
        return self.short_name

class RestrictionOfVictim(models.Model):
    restriction = models.CharField('ограничения', max_length=150)
    def __str__(self):
        return self.restriction

class Victim(models.Model):
    name = models.CharField('ФИО',max_length=250)
    date_of_birth = models.DateField('Дата рождения', blank=True, null=True)
    place = models.ForeignKey(Place, on_delete=models.CASCADE, blank=True, null=True)
    restriction = models.ForeignKey(RestrictionOfVictim, on_delete=models.CASCADE, default="На свободе")
    biography = models.TextField('биография', blank=True)
    photo = models.ImageField(upload_to='dbase/images/victims',default='images/Noface.JPG')
    def __str__(self):
        return self.name

class Guilty(models.Model):
    name = models.CharField('ФИО',max_length=250)
    date_of_birth = models.DateField('Дата рождения', blank=True, null=True)
    citizenship = models.CharField('гражданство', max_length=50, blank=True, null=True)
    organization = models.CharField('организация', max_length=150, blank=True, null=True)
    position = models.CharField('должность', max_length=150, blank=True, null=True)
    photo = models.ImageField(upload_to='dbase/images/guilty', default='images/Noface.JPG')
    def __str__(self):
        return self.name

class StatusOfVictimInPers(models.Model):
    status = models.CharField('статус', max_length=50)
    def __str__(self):
        return self.status

class TypeOfPersecution(models.Model):
    type = models.CharField('тип преследования', max_length=150)
    def __str__(self):
        return self.type

class Case(models.Model):
    name = models.CharField('Дело', max_length=250)
    overview = models.TextField('описание', blank=True, null=True)
    photo = models.ImageField(upload_to='static/images/cases',default='images/Noface.JPG')
    def __str__(self):
        return self.name

class Perseqution(models.Model):
    date = models.DateField('Дата преследования')
    victim = models.ForeignKey(Victim, on_delete=models.CASCADE)
    date_of_end = models.DateField('Окончание преследования', blank=True, null=True)
    type_of_pers = models.ForeignKey(TypeOfPersecution, on_delete=models.CASCADE)
    case = models.ForeignKey(Case, on_delete=models.CASCADE, blank=True, null=True)
    status = models.ForeignKey(StatusOfVictimInPers, on_delete=models.CASCADE)
    overview = models.TextField('описание', blank=True, null=True)
    def __str__(self):
        return "%s_%s_%s" % (self.date,self.type_of_pers,self.victim)

class GuiltyInPersecutions(models.Model):
    guilty = models.ForeignKey(Guilty, on_delete=models.CASCADE)
    perseqution = models.ForeignKey(Perseqution, on_delete=models.CASCADE)

class Article(models.Model):
    codes_choices = [
        ('УК', 'Уголовный кодекс'),
        ('КоАП', 'Кодекс об административных правонарушениях')
    ]
    number = models.CharField('статья', max_length=10)
    parts = models.CharField('часть', max_length=10,  blank=True, null=True)
    code = models.CharField('кодекс', max_length=10, choices = codes_choices, default='УК')
    title = models.CharField('название', max_length=250, blank=True, null=True)
    text = models.TextField('текст', blank=True, null=True)

    def __str__(self):
        return "ст.%s ч.%s %s" % (self.number,self.parts,self.code)

class ArticlesInPersecution(models.Model):
    persecution = models.ForeignKey(Perseqution, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

class Violation(models.Model):
    rights = models.CharField('нарушение права', max_length=150)
    content = models.TextField('описание', blank=True, null=True)
    def __str__(self):
        return self.rights

class ViolationInPersecution(models.Model):
    persecution = models.ForeignKey(Perseqution, on_delete=models.CASCADE)
    rights = models.ForeignKey(Violation, on_delete=models.CASCADE)



# Create your models here.
