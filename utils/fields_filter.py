def filter_empty_string(*args) -> str | tuple | None:
    """
    过滤空字符串
    """
    filtered_args = tuple(arg for arg in args if arg and arg.strip() != "")
    if not filtered_args or len(filtered_args) <= 0:
        return None
    if len(filtered_args) == 1:
        return filtered_args[0]
    return filtered_args
