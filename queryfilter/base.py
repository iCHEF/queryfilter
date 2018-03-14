import abc

from .exceptions import (
    FilterOnNoneValue,
    FieldNotFound
)


class FieldFilter(object):
    __metaclass__ = abc.ABCMeta

    def __init__(
            self,
            field_name,
            filter_args,
            options=None
    ):
        self.field_name = field_name
        self.filter_args = filter_args
        self.options = {
            "drop_none": True
        }
        passed_in_options = options if options else {}
        self.options.update(passed_in_options)

    # TODO: Put it back when we need it
    # @abc.abstractmethod
    def on_django_query(self, query):
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

        if not field_name:
            return handle_missing_field(field_name)

        # To support access key like user__name__phone
        level_field_names = field_name.split("__")

        final_field_name = level_field_names[-1]
        parent_field_names = level_field_names[:-1]

        for index, parent_field_name in enumerate(parent_field_names):
            dictobj = dictobj.get(parent_field_name)
            if not dictobj:
                # Point to which level doesn't exist exactly
                return handle_missing_field(
                    "__".join(level_field_names[:index+1])
                )
        if final_field_name not in dictobj:
            return handle_missing_field(field_name)
        return dictobj.get(final_field_name)
