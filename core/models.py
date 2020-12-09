import os

from django.utils.deconstruct import deconstructible


@deconstructible
class UploadTo:
    def __init__(self, model, field):
        self.model = model
        self.field = field

    def __eq__(self, other):
        return self.model == other.model and self.field == other.field

    def __call__(self, instance, filename):
        model_pk = instance.tenant.pk if hasattr(instance, "tenant") else instance.pk
        return os.path.join(
            self.model, str(model_pk), self.field, str(instance.pk), filename
        )
