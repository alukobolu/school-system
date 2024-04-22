from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import DetailView, ListView, View
from django.urls import reverse

from apps.students.models import Student,StudentClass
from apps.corecode.models import AcademicSession,AcademicTerm,Subject

from .forms import CreateResults, EditResults
from .models import Result,ResultComments


@login_required
def create_result(request):
    students = Student.objects.all()
    if request.method == "POST":

        # after visiting the second page
        if "finish" in request.POST:
            form = CreateResults(request.POST)
            if form.is_valid():
                subjects = form.cleaned_data["subjects"]
                
                session = form.cleaned_data["session"]
                term = form.cleaned_data["term"]
                students = request.POST["students"]
                ses = AcademicSession.objects.get(name = session)
                ter = AcademicTerm.objects.get(name = term)
                subs = ""
                for subj in subjects:
                    subjs = Subject.objects.get(name = subj)
                    subs = subs + "," + str(subjs.id)
                results = []
                for student in students.split(","):
                    stu = Student.objects.get(pk=student)
                    if stu.current_class:
                        for subject in subjects:
                            check = Result.objects.filter(
                                session=session,
                                term=term,
                                current_class=stu.current_class,
                                subject=subject,
                                student=stu,
                            ).first()
                            if not check:
                                results.append(
                                    Result(
                                        session=session,
                                        term=term,
                                        current_class=stu.current_class,
                                        subject=subject,
                                        student=stu,
                                    )
                                )
                url = reverse('edit-student-results') + f'?student_ids={ students }&term={ ter.id }&session={ ses.id }&subjects={ subs }'
                Result.objects.bulk_create(results)
                return redirect(url)

        # after choosing students
        id_list = request.POST.getlist("students")
        if id_list:
            form = CreateResults(
                initial={
                    "session": request.current_session,
                    "term": request.current_term,
                }
            )
            studentlist = ",".join(id_list)
            return render(
                request,
                "result/create_result_page2.html",
                {"students": studentlist, "form": form, "count": len(id_list)},
            )
        else:
            messages.warning(request, "You didnt select any student.")
    return render(request, "result/create_result.html", {"students": students})


@login_required
def edit_results(request):
    if request.method == "POST":
        form = EditResults(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Results successfully updated")
            return redirect("edit-results")
    else:
        if request.current_staff.staff_type == "teacher":
            subject  = request.current_staff.subject
            results = Result.objects.filter(
                session=request.current_session, term=request.current_term, subject = subject
            )
        else:
            results = Result.objects.filter(
                session=request.current_session, term=request.current_term
            )
        form = EditResults(queryset=results)
    return render(request, "result/edit_results.html", {"formset": form})

@login_required
def edit_student_results(request):
    student_ids = request.GET.get("student_ids","")
    session = request.GET["session"]
    term = request.GET["term"]
    
    if request.method == "POST":
        form = EditResults(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Results successfully updated")
            if request.GET.get("subjects"):
                subs = request.GET.get("subjects","")
                url = reverse('edit-student-results') + f'?student_ids={ student_ids }&term={ term }&session={ session }&subjects={ subs }'
            else:
                url = reverse('edit-student-results') + f'?student_ids={ student_ids }&term={ term }&session={ session }'
            return redirect(url)
    else:
        student_ids = [int(id) for id in student_ids.split(',') if id.isdigit()]
        students = Student.objects.filter(id__in=student_ids)
        results = Result.objects.filter(
            session=session, term=term, student__in=students
        )
        if request.current_staff.staff_type == "teacher":
            subject  = request.current_staff.subject
            results = results.filter(subject=subject)
        else:
            if request.GET.get("subjects"):
                subjects = request.GET.get("subjects","").strip("%20")
                subject_ids = [int(id) for id in subjects.split(',') if id.isdigit()]
                subject = Subject.objects.filter(id__in=subject_ids)
                results = results.filter(subject__in=subject)
        
        form = EditResults(queryset=results)
    return render(request, "result/edit_results.html", {"formset": form})

@login_required
def view_result(request):
    if request.method == "GET":
        student_id = request.GET.get("student")
        session = request.GET["session"]
        term = request.GET["term"]
        student = Student.objects.get(id=student_id)
        results = Result.objects.filter(
            session=session, term=term, student=student
        )
        a_session = AcademicSession.objects.get(id = session)
        a_term = AcademicTerm.objects.get(id = term)
        bulk = []
        for result in results:
            ass_total = 0
            test1_total = 0
            test2_total = 0
            test3_total = 0
            exam_total = 0
            count = 0
            subjects = []
            for subject in results:
                if subject.student == result.student:
                    count += 1
                    subjects.append(subject)
                    test1_total += subject.test1_score
                    test2_total += subject.test2_score
                    test3_total += subject.test3_score
                    ass_total += subject.assignment_score
                    exam_total += subject.exam_score
        
        context = {
            "results": subjects,
            "exam_total": exam_total,
            "student_name": f"{student.surname} {student.firstname} {student.other_name} ({student.registration_number})",
            "student_class": student.current_class.name,
            "student_result_session": a_session.name,
            "student_result_term": a_term.name,
            }
        if ResultComments.objects.filter(
            student = student,session = a_session,
            term = a_term, current_class = student.current_class
        ).exists() == True:
            comment = ResultComments.objects.get(
            student = student,session = a_session,
            term = a_term, current_class = student.current_class
            )
            context["head_teacher_comment"] = comment.head_teacher_comment
            context["class_teacher_comment"] = comment.class_teacher_comment
            context["habits"] = comment.habits
            context["neatness"] = comment.neatness
            context["attendance_made"] = comment.attendance_made
        return render(request, "result/view_result.html", context)

@login_required
def add_comment(request):
    student_id = request.GET.get("student")
    session = request.GET["session"]
    term = request.GET["term"]
    if request.method == "GET":  
        a_session = AcademicSession.objects.get(id = session)
        a_term = AcademicTerm.objects.get(id = term)
        student = Student.objects.get(id=student_id)
        context = {
            "term_id": term,
            "session_id": session,
            "student_id": student.id,
            "student_name": f"{student.surname} {student.firstname} {student.other_name} ({student.registration_number})",
            "student_class": student.current_class.name,
            "student_class_id": student.current_class.id,
            "student_result_session": a_session.name,
            "student_result_term": a_term.name,
            }
        if ResultComments.objects.filter(
            student = student,session = a_session,
            term = a_term, current_class = student.current_class
        ).exists() == True:
            comment = ResultComments.objects.get(
            student = student,session = a_session,
            term = a_term, current_class = student.current_class
            )
            context["head_teacher_comment"] = comment.head_teacher_comment
            context["class_teacher_comment"] = comment.class_teacher_comment
            context["habits"] = comment.habits
            context["neatness"] = comment.neatness
            context["attendance_made"] = comment.attendance_made
        return render(request, "result/create_comment.html", context)
    else:
        student_id = request.POST["student_id"]
        session_id = request.POST["session_id"]
        term_id = request.POST["term_id"]
        student_class_id = request.POST["class_id"]
        attendance_made = request.POST["attendance_made"]
        habits = request.POST["habits"]
        neatness = request.POST["neatness"]
        class_teacher_comment = request.POST["class_teacher_comment"]
        head_teacher_comment = request.POST["head_teacher_comment"]

        a_session = AcademicSession.objects.get(id = session_id)
        a_term = AcademicTerm.objects.get(id = term_id)
        student = Student.objects.get(id=student_id)
        student_class = StudentClass.objects.get(id=student_class_id)

        comment = ResultComments.objects.get_or_create(
            student = student,session = a_session,
            term = a_term, current_class = student_class
        )
        comment[0].head_teacher_comment = head_teacher_comment
        comment[0].class_teacher_comment = class_teacher_comment
        comment[0].habits = habits
        comment[0].neatness = neatness
        comment[0].attendance_made = attendance_made
        comment[0].save()

        url = reverse('add-comment') + f'?student={ student_id }&term={ term_id }&session={ session_id }'
        return redirect(url)



class ResultListView(LoginRequiredMixin, View):
    def get(self, request,class_id="all"):
        all_session = AcademicSession.objects.all()
        all_term = AcademicTerm.objects.all()
        if class_id == "all":
            student_class = StudentClass.objects.all()
        else:
            student_class = "no"

        if not request.GET.get("session") and not request.GET.get("session"):
            context = {
                "results": {},
                "all_session": all_session,
                "all_term": all_term,
                "student_classes": student_class,
                }
            return render(request, "result/all_results.html", context)
        
        session = request.GET.get("session")
        term = request.GET.get("term")
        if class_id == "all":
            if request.GET.get("result_class_id"):
                result_class_id = request.GET.get("result_class_id")
                studentclass = StudentClass.objects.get(id = result_class_id)
                results = Result.objects.filter(
                    session=session, term=term, current_class = studentclass
                )
            else:
                results = Result.objects.filter(
                    session=session, term=term
                )
        else:
            studentclass = StudentClass.objects.get(id = class_id)
            results = Result.objects.filter(
                session=session, term=term, current_class = studentclass
            )
        bulk = {}

        for result in results:
            ass_total = 0
            test1_total = 0
            test2_total = 0
            test3_total = 0
            exam_total = 0
            count = 0
            subjects = []
            for subject in results:
                if subject.student == result.student:
                    count += 1
                    subjects.append(subject)
                    test1_total += subject.test1_score
                    test2_total += subject.test2_score
                    test3_total += subject.test3_score
                    ass_total += subject.assignment_score
                    exam_total += subject.exam_score
            test_total = test1_total + test2_total + test3_total + ass_total
          
            percentage = ((test_total + exam_total)/(count*100))*100
            if percentage >= 70:
                total_grade = "A"
            elif percentage >= 60 and percentage < 70:
                total_grade = "B"
            elif percentage >= 50 and percentage < 60:
                total_grade = "C"
            elif percentage >= 40 and percentage < 50:
                total_grade = "D"
            elif percentage >= 30 and percentage < 40:
                total_grade = "E"
            elif percentage >= 0 and percentage < 30:
                total_grade = "F"
            else:
                total_grade = "N/A"

            bulk[result.student.id] = {
                "student": result.student,
                "session": result.session,
                "term": result.term,
                "subjects": subjects,
                "test_total": test_total,
                "exam_total": exam_total,
                "total_total": percentage,
                "total_grade": total_grade,
            }
        context = {
            "results": bulk,
            "all_session": all_session,
            "all_term": all_term,
            "student_classes": student_class,
            }
        return render(request, "result/all_results.html", context)
