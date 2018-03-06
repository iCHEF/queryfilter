

class QueryFilterException(Exception):
    pass


class FieldNotFound(QueryFilterException):
    pass


class FilterOnNoneValue(QueryFilterException):
    pass
