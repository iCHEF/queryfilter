def is_same_class(x_cls, y_cls):
    """
    Simply use "is" to compare two classes will not work,
    `cause class statement is an executable statement in python.

    So we'll need a customized comparing function.
    """
    full_path_of_x = x_cls.__module__ + "." + x_cls.__name__
    full_path_of_y = y_cls.__module__ + "." + y_cls.__name__
    return full_path_of_x == full_path_of_y
