from .models import AcademicSession, AcademicTerm, SiteConfig,Staff


def site_defaults(request):
    current_session = AcademicSession.objects.get(current=True)
    current_term = AcademicTerm.objects.get(current=True)
    vals = SiteConfig.objects.all()

    contexts = {
        "current_session": current_session.name,
        "current_term": current_term.name,
    }
    if request.user.is_authenticated:
        if Staff.objects.filter(user=request.user).exists():
            current_staff = Staff.objects.get(user=request.user)
            contexts["staff_type"] = current_staff.staff_type
            if current_staff.subject !=None:
                contexts["staff_subject"] = current_staff.subject.name
                contexts["staff_subject_id"] = current_staff.subject.id
            contexts["staff_name"] = f"{current_staff.surname} {current_staff.firstname} {current_staff.other_name}"

    for val in vals:
        contexts[val.key] = val.value

    return contexts
