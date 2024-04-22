from django.db import models

from apps.corecode.models import (
    AcademicSession,
    AcademicTerm,
    StudentClass,
    Subject,
)
from apps.students.models import Student

from .utils import score_grade


# Create your models here.
class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)
    term = models.ForeignKey(AcademicTerm, on_delete=models.CASCADE)
    current_class = models.ForeignKey(StudentClass, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    assignment_score = models.IntegerField(default=0)
    test1_score = models.IntegerField(default=0)
    test2_score = models.IntegerField(default=0)
    test3_score = models.IntegerField(default=0)
    exam_score = models.IntegerField(default=0)
    remarks = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        ordering = ["subject"]

    def __str__(self):
        return f"{self.student} {self.session} {self.term} {self.subject}"

    def total_score(self):
        return self.test1_score + self.test2_score + self.test3_score + self.assignment_score + self.exam_score
    
    def total_ca(self):
        return self.test1_score + self.test2_score + self.test3_score + self.assignment_score

    def grade(self):
        return score_grade(self.total_score())


class ResultComments(models.Model):
    head_teacher_comment = models.CharField(max_length=200, null=True, blank=True)
    class_teacher_comment = models.CharField(max_length=200, null=True, blank=True)
    habits = models.CharField(max_length=200, null=True, blank=True)
    neatness = models.CharField(max_length=200, null=True, blank=True)
    attendance_made = models.CharField(max_length=200, null=True, blank=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)
    term = models.ForeignKey(AcademicTerm, on_delete=models.CASCADE)
    current_class = models.ForeignKey(StudentClass, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.student} {self.session} {self.term}"