import uuid
from datetime import datetime, timedelta

import jwt
import slugify
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.db.models import Q
from safedelete.models import SafeDeleteMixin, SOFT_DELETE_CASCADE

from apps.users.models.user_manager import CustomUserManager
from core.models import UploadTo


class User(SafeDeleteMixin, AbstractBaseUser):
    _safedelete_policy = SOFT_DELETE_CASCADE
    USERNAME_FIELD = "username"
    objects = CustomUserManager()

    username = models.CharField(max_length=150, unique=True, blank=True, null=True)
    fullname = models.CharField(max_length=50)
    ascii_name = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=15)
    avatar_url = models.FileField(
        upload_to=UploadTo("locsharing", "user"),
        max_length=1024,
        blank=True,
        null=True,
    )
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "user"
        constraints = [
            models.UniqueConstraint(
                fields=["phone"],
                name="unique_user_phone",
                condition=Q(deleted__isnull=True),
            ),
        ]
        ordering = ["created_at"]

    @property
    def token(self):
        return self._generate_jwt_token()

    @property
    def is_staff(self):
        return self.is_superuser

    def clean(self):
        super().clean()

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def __str__(self):
        return (
            self.username
            if self.username
            else "{}-{}".format(self.fullname, self.phone)
        )

    def save(self, keep_deleted=False, **kwargs):
        self.ascii_name = slugify.slugify(self.fullname, separator=" ")
        super(User, self).save(keep_deleted=keep_deleted, **kwargs)

    def _generate_jwt_token(self):
        iat = datetime.now()
        exp = iat + timedelta(days=60)
        payload = {
            "id": str(self.id),
            "fullname": self.fullname,
            "phone": self.phone,
            "exp": exp,
            "iat": iat,
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

        return token.decode("utf-8")
