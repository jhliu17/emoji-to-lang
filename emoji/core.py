# -*- coding: UTF-8 -*-


"""
emoji.core
~~~~~~~~~~

Core components for emoji.

"""


import re
import sys

import xml.etree.ElementTree as ET
from tqdm import tqdm
from emoji import unicode_codes


__all__ = ['emojize', 'demojize', 'get_emoji_regexp',
           'emoji_lis', 'distinct_emoji_lis', 'import_from_annotation']


PY2 = sys.version_info[0] == 2

_EMOJI_REGEXP = None
_DEFAULT_DELIMITER = ":"
_STICKY_CHARACTER = "_"


def emojize(string, use_aliases=False, delimiters=(_DEFAULT_DELIMITER, _DEFAULT_DELIMITER), variant=None, language='en'):
    """Replace emoji names in a string with unicode codes.

    :param string: String contains emoji names.
    :param use_aliases: (optional) Enable emoji aliases.  See ``emoji.UNICODE_EMOJI_ALIAS``.
    :param delimiters: (optional) Use delimiters other than _DEFAULT_DELIMITER
    :param variant: （optional) Choose variation selector between "base"(None), VS-15 ("text_type") and VS-16 ("emoji_type")
        >>> import emoji
        >>> print(emoji.emojize("Python is fun :thumbsup:", use_aliases=True))
        Python is fun 👍
        >>> print(emoji.emojize("Python is fun :thumbs_up:"))
        Python is fun 👍
        >>> print(emoji.emojize("Python is fun __thumbs_up__", delimiters = ("__", "__")))
        Python is fun 👍
        >>> print(emoji.emojize("Python is fun :red_heart:"))
        Python is fun ❤
        >>> print(emoji.emojize("Python is fun :red_heart:",variant="emoji_type"))
        Python is fun ❤️ #red heart, not black heart
    """
    EMOJI_UNICODE = unicode_codes.EMOJI_UNICODE[language]
    pattern = re.compile(
        u'(%s[a-zA-Z0-9\\+\\-_&.ô’Åéãíç()!#*]+%s)' % delimiters)

    def replace(match):
        mg = match.group(1).replace(delimiters[0], _DEFAULT_DELIMITER).replace(
            delimiters[1], _DEFAULT_DELIMITER)
        if use_aliases:
            emj = unicode_codes.EMOJI_ALIAS_UNICODE.get(mg, mg)
        else:
            emj = EMOJI_UNICODE.get(mg, mg)
        if variant is None:
            return emj
        elif variant == "text_type":
            return emj+u'\uFE0E'
        elif variant == "emoji_type":
            return emj+u'\uFE0F'
    return pattern.sub(replace, string)


def demojize(string, use_aliases=False,
             delimiters=(_DEFAULT_DELIMITER, _DEFAULT_DELIMITER),
             sticky_character=None, language='en'):
    """Replace unicode emoji in a string with emoji shortcodes. Useful for storage.
    :param string: String contains unicode characters. MUST BE UNICODE.
    :param use_aliases: (optional) Return emoji aliases.  See ``emoji.UNICODE_EMOJI_ALIAS``.
    :param delimiters: (optional) User delimiters other than _DEFAULT_DELIMITER
        >>> import emoji
        >>> print(emoji.emojize("Python is fun :thumbs_up:"))
        Python is fun 👍
        >>> print(emoji.demojize(u"Python is fun 👍"))
        Python is fun :thumbs_up:
        >>> print(emoji.demojize(u"Unicode is tricky 😯", delimiters=("__", "__")))
        Unicode is tricky __hushed_face__
    """
    UNICODE_EMOJI = unicode_codes.UNICODE_EMOJI[language]
    sticky_character = sticky_character if sticky_character else "_"

    def replace(match):
        codes_dict = unicode_codes.UNICODE_EMOJI_ALIAS if use_aliases else UNICODE_EMOJI
        val = codes_dict.get(match.group(0), match.group(0)).split(unicode_codes.DEFAULT_STICKY_CHAR[language])
        val = sticky_character.join(val)
        return delimiters[0] + val[1:-1] + delimiters[1]

    return re.sub(u'\ufe0f', '', (get_emoji_regexp(language).sub(replace, string)))


def get_emoji_regexp(language='en'):
    """Returns compiled regular expression that matches emojis defined in
    ``emoji.UNICODE_EMOJI_ALIAS``. The regular expression is only compiled once.
    """

    global _EMOJI_REGEXP
    # Build emoji regexp once
    EMOJI_UNICODE = unicode_codes.EMOJI_UNICODE[language]
    if _EMOJI_REGEXP is None:
        # Sort emojis by length to make sure multi-character emojis are
        # matched first
        emojis = sorted(EMOJI_UNICODE.values(), key=len,
                        reverse=True)
        pattern = u'(' + u'|'.join(re.escape(u) for u in emojis) + u')'
        _EMOJI_REGEXP = re.compile(pattern)
    return _EMOJI_REGEXP


def emoji_lis(string, language='en'):
    """
    Returns the location and emoji in list of dict format
    >>> emoji.emoji_lis("Hi, I am fine. 😁")
    >>> [{'location': 15, 'emoji': '😁'}]
    """
    _entities = []

    for match in get_emoji_regexp(language).finditer(string):
        _entities.append({
            "location": match.start(),
            "emoji": match.group()
        })

    return _entities


def _parse_xml(file_path, sticky_character):
    """
    Parse CLDR xml file.
    Only the emoji exists in the `en` dict will be added into
    consideration.

    Args:
        file_path (str): the file path to xml.
    """
    xml = ET.parse(file_path)
    annotations = xml.find('annotations')

    def check_exist(unicode):
        res = demojize(unicode)
        return _DEFAULT_DELIMITER in res

    emoji_list = []
    unicode_list = []
    for an in tqdm(annotations):
        attrib = an.attrib
        if 'type' not in attrib:
            continue

        unic = attrib.get('cp', None)
        if unic and check_exist(unic):
            unicode_list.append(unic)
            lang_repr = an.text.strip().split(" ")
            emoji_list.append(
                f'{_DEFAULT_DELIMITER}%s{_DEFAULT_DELIMITER}' % sticky_character.join(lang_repr))

    emoji_unicode = {e: u for e, u in zip(emoji_list, unicode_list)}
    return emoji_unicode


def import_from_annotation(file_path, language, force_import=False, sticky_character=_STICKY_CHARACTER):
    if not force_import and (
            language in unicode_codes.EMOJI_UNICODE or
            language in unicode_codes.UNICODE_EMOJI):
        raise ValueError(f"Language {language} exists in default lib. Try to use `force_import`.")

    if not isinstance(sticky_character, str):
        raise ValueError("Sticky character must be a string.")

    emoji_unicode = _parse_xml(file_path, sticky_character)
    unicode_emoji = {v: k for k, v in emoji_unicode.items()}

    unicode_codes.EMOJI_UNICODE[language] = emoji_unicode
    unicode_codes.UNICODE_EMOJI[language] = unicode_emoji
    unicode_codes.DEFAULT_STICKY_CHAR[language] = sticky_character
    print(f"Language `{language}` annotation file imported successfully.")


def distinct_emoji_lis(string):
    """Resturns distinct list of emojis from the string"""
    distinct_list = list(
        {c for c in string if c in unicode_codes.UNICODE_EMOJI})
    return distinct_list


def emoji_count(string):
    """
    Returns the count of emojis in a string
    """
    return len(emoji_lis(string))
