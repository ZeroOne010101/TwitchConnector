import re
# The regex compilations are saved in this seperate file for performance reasons
mainRegex = re.compile(r"^(?::(?P<prefix>\S+) )?(?P<command>\S+)(?: (?!:)(?P<params>.+?))?(?: :(?P<message>.+))?$")
prefixRegex = re.compile(r"^(?:\S+!\S+@)?(?P<user>\S+).tmi.twitch.tv$") # Twitch specific, ?P<user> is usually the hostname