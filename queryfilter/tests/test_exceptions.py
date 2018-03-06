

from .. import exceptions as queryfilter_exceptions


def test_all_exceptions_should_inherit_QueryFilterException():
    exception_class_names = []
    for name in dir(queryfilter_exceptions):
        if (
                (not name.startswith("_"))
                and name != "QueryFilterException"
        ):
            exception_class_names.append(name)

    exception_classes = [getattr(queryfilter_exceptions, name)
                         for name in exception_class_names]
    for exc in exception_classes:
        assert queryfilter_exceptions.QueryFilterException in exc.__mro__
