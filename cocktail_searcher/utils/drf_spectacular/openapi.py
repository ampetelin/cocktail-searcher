from typing import Optional

from drf_spectacular.openapi import AutoSchema
from drf_spectacular.plumbing import get_view_model


class CustomAutoSchema(AutoSchema):
    DEFAULT_ACTION_DESCRIPTION_MAP = {
        'list': 'Get a list of "{verbose_name}" entities',
        'create': 'Create new entity "{verbose_name}"',
        'retrieve': 'Get single entity "{verbose_name}"',
        'destroy': 'Delete entity "{verbose_name}"',
        'partial_update': 'Partially update an entity "{verbose_name}"',
        'update': 'Update entity "{verbose_name}"',
    }

    def get_summary(self) -> Optional[str]:
        """Получить краткое описание метода"""
        action_or_method = getattr(self.view, getattr(self.view, 'action', self.method.lower()), None)
        summary = self.DEFAULT_ACTION_DESCRIPTION_MAP.get(action_or_method.__name__)
        if not summary:
            return None

        summary = summary.format(verbose_name=get_view_model(self.view)._meta.verbose_name)

        return summary
