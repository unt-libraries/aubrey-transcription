from __future__ import unicode_literals

from flask import Blueprint, jsonify

from utils import make_path, find_files, get_files_info


bp = Blueprint('aubrey_transcription', __name__, url_prefix='')


@bp.route('/<identifier>/')
def list_files(identifier):
    """Returns a JSON structure detailing the record's transcription files.

    If no files can be found, then an empty JSON object is returned.
    """
    pairtree_path = make_path(identifier)
    files = find_files(pairtree_path)
    file_info = get_files_info(pairtree_path, files)
    return jsonify(file_info)
