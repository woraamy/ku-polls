import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from polls.models import Question


def create_question(question_text='', days=0, end_time=0):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    time_end = timezone.now() + datetime.timedelta(days=end_time)
    return Question.objects.create(question_text=question_text, pub_date=time, end_date=time_end)


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self) -> None:
        """
        was_published_recently() returns False for questions whose pub_date is in the future.
        """
        future_question = create_question(days=30)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self) -> None:
        """
        was_published_recently() returns False for questions whose pub_date is older than 1 day.
        """
        old_question = create_question(days=1)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self) -> None:
        """
        was_published_recently() returns True for questions whose pub_date is within the last day.
        """
        recent_question = create_question()
        self.assertIs(recent_question.was_published_recently(), True)

    def test_future_pub_date(self):
        """
        Cannot publish questions in the future
        """
        question = create_question(question_text='Future Question', days=5)
        self.assertEqual(question.is_published(), False)

    def test_present_pub_date(self):
        """
        Can publish questions in the present
        """
        question = create_question(question_text='Present Question', days=0)
        self.assertEqual(question.is_published(), True)

    def test_past_pub_date(self):
        """
        Can publish questions in the past
        """
        question = create_question(question_text='Past Question', days=0)
        self.assertEqual(question.is_published(), True)

    def test_can_vote(self):
        """
        Test if method can_vote() returns true if the user votes during voting period
        """
        question = create_question(question_text='Question', days=0, end_time=1)
        self.assertEqual(question.can_vote(), True)

    def test_no_end_date(self):
        """
        Test if method can_vote() returns true if there is no end_date
        """
        question = create_question(question_text='Question', days=7)
        question.end_date = None
        self.assertEqual(question.can_vote(), True)

    def test_cannot_vote_after_end_date(self):
        """
        Test if can_vote() returns False for questions that end_date has passed
        """
        question = create_question(question_text='Question', days=0, end_time=-5)
        self.assertEqual(question.can_vote(), False)