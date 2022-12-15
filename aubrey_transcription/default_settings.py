SECRET_KEY = 'dev'
PAIRTREE_BASE = '/home/transcriptions/pairtree'
TRANSCRIPTION_URL = 'http://example.com'
EXTENSIONS_META = {
    'vtt': {
        'mimetype': 'text/vtt',
        'use': 'vtt',
    },
}
FILENAME_PATTERN = (r'(?P<metaid>[^_]*)_m?(?P<manifestation>[^_]*)_(?P<fileset>[^-]*)'
                    r'-(?P<kind>[^-]*)-(?P<language>[^.]*)\.(?P<extension>.*)')
JSON_SORT_KEYS = False
