from django.db import models
from django.utils.translation import gettext as _


class ItemTypeCategory(models.Model):
    name = models.CharField(max_length=254, unique=True, verbose_name=_("name"))
    order_key = models.IntegerField(blank=False, default=1, verbose_name=_("ordering index"))

    class Meta:
        verbose_name = _("item type category")
        verbose_name_plural = _("item type categories")
        ordering = ("order_key", "name",)

    def __str__(self):
        return self.name


class ItemType(models.Model):
    name = models.CharField(max_length=254, unique=True, blank=False, verbose_name=_("name"))
    # TODO: Name with additional HTML formating
    category = models.ForeignKey(ItemTypeCategory, null=False, blank=False, on_delete=models.CASCADE,
                                 related_name="items", verbose_name = _("category"))
    notes = models.TextField(_("notes"), blank=True)
    deprecated = models.BooleanField(default=False, verbose_name=_("deprecated"))

    # TODO: Images / Thumbnails

    # TODO: Packaging Sizes

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("item type")
        verbose_name_plural = _("item types")
        ordering = ("category__order_key", "category__name", "name",)

    def __str__(self):
        return  f"{self.name} " + f" ({_('deprecated')})" if self.deprecated else self.name