import datetime
from django.db import models
from django.utils import timezone


# Create your models here.
class Question(models.Model):
    """This class contains questions that will be shown on the web page."""
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', default=timezone.now())
    end_date = models.DateTimeField('end date', null=True)

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def is_published(self):
        return self.pub_date <= timezone.now()

    def can_vote(self):
        if self.pub_date < timezone.now() < self.end_date or self.end_date is None:
            return True
        return False


class Choice(models.Model):
    """This class contains choices to questions and how the format will be shown on the webpage"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
