
## User Utils

USER_NAME_MAX_LENGTH = 64
DISPLAY_NAME_MAX_LENGTH = 64
DESCRIPTION_MAX_LENGTH = 128

def user_name_length_validation(user_name):
    return len(user_name) <= USER_NAME_MAX_LENGTH

def display_name_length_validation(display_name):
    return len(display_name) <= DISPLAY_NAME_MAX_LENGTH

def description_length_validation(description):
    return len(description) <= DESCRIPTION_MAX_LENGTH

def is_empty(field):
    return bool(field) == False

def display_name_validaton(display_name):
    if is_empty(display_name):
        raise ValueError(f"display_name should not be empty")

    if not display_name_length_validation(display_name):
        raise ValueError("{display_name} should be less than {DISPLAY_NAME_MAX_LENGTH} characters")

## Team Utils

TEAM_NAME_MAX_LENGTH = 64

def team_name_length_validation(team_name):
    return len(team_name) <= TEAM_NAME_MAX_LENGTH
