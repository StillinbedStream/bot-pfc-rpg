import re

# Checking management
NAME_PATTERN = r'^[0-9a-zA-Z]{5,25}$'
name_pattern = re.compile(NAME_PATTERN, flags=re.I)


from discord.ext.commands import BadArgument


def is_name(name: str):
    """For command annotation"""
    if not name_pattern.match(name):
        raise BadArgument("Le nom de l'utilisateur doit faire entre 5 et 25 caractères et ne contenir aucun caractère spécial.")
    return name
