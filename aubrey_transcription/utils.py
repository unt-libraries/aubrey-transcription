from __future__ import unicode_literals
import os

from pypairtree import pairtree
from flask import current_app


def make_path(identifier):
    """Convert the identifier into a pairpath prefixed by PAIRTREE_BASE."""
    sanitized_id = pairtree.sanitizeString(identifier)
    pairpath = pairtree.get_pair_path(sanitized_id)
    return os.path.normpath(pairpath)


def find_files(pairpath):
    """Get a list of all the files that exist under the path."""
    pairtree_base = current_app.config['PAIRTREE_BASE']
    full_path = '{}{}'.format(pairtree_base, pairpath)
    normalized_path = os.path.normpath(full_path)
    if not os.path.isdir(normalized_path):
        return []
    return os.listdir(normalized_path)


def get_files_info(pairpath, files):
    """Make a dictionary with information about each of the given files.

    The files are also checked to make sure that they have the expected
    extension. Files which are of the wrong type are not included in the dict.
    """
    extensions_meta = current_app.config['EXTENSIONS_META']
    pairtree_base = current_app.config['PAIRTREE_BASE']
    transcription_url = current_app.config['TRANSCRIPTION_URL']
    files_info = []
    for filename in files:
        extension = filename.split('.')[-1]
        if extension in extensions_meta:
            file_path = os.path.join(pairpath, filename)
            filename_dict = decrypt_filename(filename)
            if not filename_dict:
                continue
            local_flocat = os.path.normpath('{}{}{}'.format(pairtree_base, os.sep, file_path))
            try:
                file_size = os.path.getsize(local_flocat)
            except OSError:
                continue
            file_info = {
                'MIMETYPE': extensions_meta[extension]['mimetype'],
                'USE': extensions_meta[extension]['use'],
                'flocat': '{}{}'.format(transcription_url, file_path),
                'SIZE': file_size,
                'vtt_kind': filename_dict['kind'],
                'language': filename_dict['language'],
            }
            files_info.append(file_info)

    return files_info


def decrypt_filename(filename):
    """Break apart a transcription filename into it's various parts."""
    filename_regex = current_app.config['FILENAME_REGEX']
    filename_match = filename_regex.match(filename)
    if filename_match:
        return filename_match.groupdict()
    return {}
