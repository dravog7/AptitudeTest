from django.db import models
import datetime
from django.contrib.auth.models import  User

# Create your models here.
class Quiz(models.Model):
    name=models.CharField(max_length=100)
    description=models.CharField(max_length=800,blank=True)
    dept=models.CharField(max_length=40)
    date=models.DateTimeField(default=datetime.datetime.now())
    duration=models.DurationField(default=datetime.timedelta(minutes=30))
    no_of_question=models.IntegerField(blank=True,default=0)
    theme=models.ImageField(blank=True)
    active=models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Question(models.Model):
    text=models.TextField()
    score=models.IntegerField(default=1)
    quiz=models.ForeignKey(Quiz,on_delete=models.CASCADE,related_name="questions")

    def __str__(self):
        return self.text

class Option(models.Model):
    question=models.ForeignKey(Question,on_delete=models.CASCADE,related_name="options")
    value=models.CharField(max_length=1200)
    is_correct=models.BooleanField(default=False)

    def __str__(self):
        return str(self.value)


class Profile(models.Model):
    user=models.OneToOneField(User,related_name='Profile', on_delete=models.CASCADE)
    college=models.CharField(max_length=200)
    phone=models.IntegerField(blank=True,default=0)
    quiz=models.ManyToManyField(Quiz)

    def __str__(self):
        return self.user.username

class Answers(models.Model):
    user=models.ForeignKey(Profile,on_delete=models.CASCADE)
    question=models.ForeignKey(Question,on_delete=models.CASCADE)
    option=models.ForeignKey(Option,on_delete=models.CASCADE)
    right=models.BooleanField(default=False)

    class Meta:
        unique_together=('user','question','option')

    def __str__(self):
            return str(self.question)


class Result(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField()

    def __str__(self):
        return str(self.quiz)

    class Meta:
        ordering=('quiz','-score')
        unique_together = ('profile', 'quiz')
