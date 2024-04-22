from .models import AcademicSession, AcademicTerm, Staff
# from staffs.models import Staff


class SiteWideConfigs:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_session = AcademicSession.objects.get(current=True)
        current_term = AcademicTerm.objects.get(current=True)
        if request.user.is_authenticated:
            if Staff.objects.filter(user=request.user).exists():
                current_staff = Staff.objects.get(user=request.user)
            else:
                current_staff = None
        else:
            current_staff = None

        request.current_session = current_session
        request.current_term = current_term
        request.current_staff = current_staff

        response = self.get_response(request)

        return response
