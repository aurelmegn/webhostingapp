def fa_icon_flash_filter(value):
    iname = "fa-"

    if value == "info":
        iname += "info"

    elif value == "error":
        iname += "times-circle-o"

    elif value == "success":
        iname += "check-circle-o"

    elif value == "warning":
        iname += "exclamation-triangle"

    else:
        iname += "circle"
    return iname
