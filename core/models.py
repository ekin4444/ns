from django.db import (models)


class AbstractModel(models.Model):
    updated_date = models.DateTimeField(
        blank=True,
        auto_now=True,
        verbose_name="Updated Date"
    )
    created_date = models.DateTimeField(
        blank=True,
        auto_now_add=True,
        verbose_name="Created Date"
    )

    class Meta:
        abstract = True
