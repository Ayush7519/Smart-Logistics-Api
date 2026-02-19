from django.db import models
from django.utils import timezone
import uuid


# -----------------------------------------------------------------------------------------------
# this is the part of the soft delete process.
# -----------------------------------------------------------------------------------------------
class SoftDeleteQuerySet(models.QuerySet):
    # here we convert default delete function into update function.
    def delete(self):
        return super().update(
            is_deleted=True,
            deleted_at=timezone.now(),
            updated_at=timezone.now(),
        )

    # this is the hard delete.
    def hard_delete(self):
        return super().delete()

    # this is the function to call the active records.
    def alive(self):
        return self.filter(is_deleted=False)

    # this is the function to call all the inactive data.
    def dead(self):
        return self.filter(is_deleted=True)


# -----------------------------------------------------------------------------------------------
# this is the manager of the soft delete part.
# -----------------------------------------------------------------------------------------------
class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return SoftDeleteQuerySet(
            self.model,
            using=self._db,
        ).filter(is_deleted=False)


# -----------------------------------------------------------------------------------------------
# this is the base model that will be used in the entire system.
# -----------------------------------------------------------------------------------------------
class BaseModel(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    # this is the soft delete flag.
    is_deleted = models.BooleanField(
        default=False,
    )
    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    # integrating the manager in the model.
    objects = SoftDeleteManager()  # active data.
    all_objects = models.Manager()  # everything

    # override the delete function.
    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(using=using, update_fields=["is_deleted", "deleted_at"])

        # integrating the soft delete helper.

    def soft_delete(self):
        self.delete()

        # integrating the hard delete helper.

    def hard_delete(self):
        super().delete()

    class Meta:
        abstract = True
