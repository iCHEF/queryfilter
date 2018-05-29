import abc
import six

from .exceptions import (
    FilterOnNoneValue,
    FieldNotFound,
    UnassignedFieldName
)


class FieldFilter(object):
    __metaclass__ = abc.ABCMeta

    def __init__(
            self,
            field_name,
            filter_args,
            options=None
    ):
        if field_name is None:
            raise UnassignedFieldName(self.__class__.__name__)

        self.field_name = field_name
        self.filter_args = filter_args
        self.options = {
            "drop_none": True
        }
        passed_in_options = options if options else {}
        self.options.update(passed_in_options)

    # TODO: Put it back when we need it
    # @abc.abstractmethod
    def on_django_query(self, queryset):
        pass

    # TODO: Put it back when we need it
    # @abc.abstractmethod
    def on_sqlalchemy_query(self, query):
        pass

    @abc.abstractmethod
    def on_dicts(self, dicts):
        pass

    def false_with_drop_none_else_raise(self, field_name):
        if self.options["drop_none"]:
            return False
        raise FilterOnNoneValue(field_name)


class DjangoQueryFilterMixin(object):
    __metaclass__ = abc.ABCMeta

    def on_django_query(self, queryset):
        from django.core.exceptions import FieldError
        try:
            return self._do_django_query(queryset)
        except FieldError as e:
            if self.options.get("none_for_missing_field"):
                return queryset.none()
            else:
                raise FieldNotFound(six.text_type(e))

    @abc.abstractmethod
    def _do_django_query(self, queryset):
        pass


class DictFilterMixin(object):
    def __init__(self, *args, **kwargs):
        super(DictFilterMixin, self).__init__(*args, **kwargs)
        options_kwargs = kwargs.get("options", {})
        option_kw_value = options_kwargs.get("none_for_missing_field", True)
        self.options["none_for_missing_field"] = option_kw_value

    def get(self, dictobj, field_name):
        def handle_missing_field(missing_field_name):
            if self.options["none_for_missing_field"]:
                return None
            raise FieldNotFound(missing_field_name)

        def get_node_from_dict(node, keys_to_iterate, iterated_key_list=None):
            if not iterated_key_list:
                iterated_key_list = []
            if not keys_to_iterate:
                return node
            node_key = keys_to_iterate.pop(0)
            node = node.get(node_key)
            if node is None:
                return handle_missing_field("__".join(iterated_key_list))
            return get_node_from_dict(
                node,
                keys_to_iterate,
                iterated_key_list + [node_key]
            )

        # To support access key like user__name__phone
        # [field_name] will never be None which defended by UnassignedFieldName
        dict_keys = field_name.split("__")
        return get_node_from_dict(dictobj, dict_keys)
