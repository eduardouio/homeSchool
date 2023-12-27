from api.serializers import (
    StudyPlanSerializer,
    UserSerializerPrivate,
    studyPlanDetailSerializer,
    ActiveCourseSerializer,
    SubscriptionSerializer,
    PaymentSubscriptionSerializer
)
from permissions.AppPermissionsProfile import IsNotUserAS
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from accounts.models import CustomUserModel as UserModel
from studyPlans.models import StudyPlan, StudyPlanDetail
from activeCourses.models import ActiveCourse
from subscriptions.models import Subscription


# /api/study-plans/ -> api-list-study-plans
class ListStudyPlanAPIView(ListAPIView):
    queryset = StudyPlan.objects.all()
    serializer_class = StudyPlanSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)

        for i in response.data:
            i.pop('details', None)

        return response


# /api/users-by-role/<str:role>/ -> api-users-by-role-list
class ListUserByRoleAPIView(ListAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializerPrivate
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        role = self.kwargs['role_name']
        return UserModel.objects.filter(role=role)