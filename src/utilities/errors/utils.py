from pydantic import ValidationError


def human_readable_errors(e: ValidationError) -> str:
    response = ""
    for i in e.errors():
        try:
            error_loc = i.get("loc")[0]
            error_message = i.get("msg")
            response += f"{error_loc} {error_message} , "
        except:
            pass
    return response
