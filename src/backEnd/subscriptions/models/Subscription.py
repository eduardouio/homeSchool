from django.db import models
from common import BaseModel
from accounts.models import CustomUserModel
from activeCourses.models import ActiveCourse

TYPE_SUBSCRIPTION = (
    ('COLEGIO', 'COLEGIO'),
    ('PROFESOR', 'PROFESOR'),
    ('ESTUDIANTE', 'ESTUDIANTE'),
    ('OTRO', 'OTRO'),
)


class Subscription(BaseModel):
    id_subscription = models.AutoField(primary_key=True)
    id_user = models.ForeignKey(
        CustomUserModel,
        on_delete=models.RESTRICT
    )
    id_active_course = models.ForeignKey(
        ActiveCourse,
        on_delete=models.RESTRICT
    )
    date_start = models.DateTimeField(
        'Fecha Inicio',
        blank=True,
        null=True,
        default=None
    )
    date_end = models.DateTimeField(
        'Fecha Fin',
        blank=True,
        null=True,
        default=None
    )
    type_subscription = models.CharField(
        'Tipo de Suscripción',
        max_length=60,
        choices=TYPE_SUBSCRIPTION,
        default='OTHER',
    )
    cost = models.FloatField(
        'Valor',
        blank=True,
        null=True,
        default=None,
    )
