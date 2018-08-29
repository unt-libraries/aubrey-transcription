from __future__ import unicode_literals
import re

import pytest
import mock

from aubrey_transcription.utils import make_path, find_files, get_files_info, decrypt_filename


FILENAME_REGEX = re.compile(r'(?P<metaid>[^_]*)_(?P<manifestation>[^_]*)_(?P<fileset>[^-]*)'
                            r'-(?P<kind>[^-]*)-(?P<language>[^.]*)\.(?P<extension>.*)')


class TestMakePath():
    @pytest.mark.parametrize('identifier,expected', [
        ('something', '/so/me/th/in/g/something'),
        ('metadc1043497', '/me/ta/dc/10/43/49/7/metadc1043497'),
        ('.././~', '/,,/=,/=~/,,=,=~'),  # Spec defines these substitutions.
    ])
    def test_make_path_good_identifier(self, identifier, expected):
        result = make_path(identifier)
        assert result == expected


@mock.patch('aubrey_transcription.utils.os.path.isdir')
@mock.patch('aubrey_transcription.utils.current_app', config={'PAIRTREE_BASE': '/right/here'})
class TestFindFiles():
    @pytest.mark.parametrize('expected', [
        ['one.vtt'],
        ['one.vtt', 'two.xml', 'three.jpg'],
        [],
    ])
    @mock.patch('aubrey_transcription.utils.os.listdir')
    def test_path_is_dir(self, mock_listdir, mock_current_app, mock_isdir, expected):
        pairpath = '/so/me/pa/th/somepath'
        mock_isdir.return_value = True
        mock_listdir.return_value = expected
        result = find_files(pairpath)
        assert result == expected

    def test_path_is_not_dir(self, mock_current_app, mock_isdir):
        pairpath = '/so/me/fi/le/somefile'
        mock_isdir.return_value = False
        result = find_files(pairpath)
        assert result == []

    def test_path_normalized(self, mock_current_app, mock_isdir):
        pairpath = '///so/./././////me//fi/le/////somefile//////'
        expected = '/so/me/fi/le/somefile'
        mock_isdir.return_value = False
        find_files(pairpath)
        assert mock_isdir.call_args[0][0].endswith(expected)


@mock.patch('aubrey_transcription.utils.decrypt_filename')
@mock.patch('aubrey_transcription.utils.current_app', config={
    'EXTENSIONS_META': {'vtt': {'mimetype': 'text/vtt', 'use': 'vtt'}},
    'PAIRTREE_BASE': '/some/path',
    'TRANSCRIPTION_URL': 'http://example.com',
})
class TestGetFilesInfo():
    @mock.patch('aubrey_transcription.utils.os.path.getsize')
    def test_returns_correct_info(self, mock_getsize, mock_current_app, mock_decrypt_filename):
        pairpath = '/pa/th/path'
        files = ['metaid_m1_1-captions-eng.vtt']
        mock_decrypt_filename.return_value = {
            'kind': 'captions',
            'language': 'eng',
        }
        mock_getsize.return_value = 256
        expected = [
            {
                'mimetype': 'text/vtt',
                'use': 'vtt',
                'flocat': 'http://example.com/pa/th/path/metaid_m1_1-captions-eng.vtt',
                'file_size': 256,
                'vtt_kind': 'captions',
                'language': 'eng',
            }
        ]
        result = get_files_info(pairpath, files)
        assert result == expected

    @mock.patch('aubrey_transcription.utils.os.path.getsize')
    def test_removes_bad_extensions(self, mock_getsize, mock_current_app, mock_decrypt_filename):
        pairpath = '/pa/th/path'
        files = ['id_m1_1-captions-eng.vtt', 'id_m3_1-captions-ger.txt', 'id_m2_1-captions-fr.vtt']
        mock_decrypt_filename.return_value = {'kind': 'captions', 'language': 'eng'}
        mock_getsize.return_value = 256
        result = get_files_info(pairpath, files)
        assert len(result) == 2
        assert result[0]['flocat'].endswith('.vtt') and result[1]['flocat'].endswith('.vtt')

    @mock.patch('aubrey_transcription.utils.os.path.getsize')
    def test_path_does_not_exist(self, mock_getsize, mock_current_app, mock_decrypt_filename):
        pairpath = '/pa/th/path'
        files = ['id_m1_1-captions-eng.vtt']
        mock_decrypt_filename.return_value = {'kind': 'captions', 'language': 'eng'}
        mock_getsize.side_effect = OSError
        result = get_files_info(pairpath, files)
        assert result == []

    @pytest.mark.parametrize('files', [
        ['two'],
        ['two.vtt'],
    ])
    def test_bad_filenames(self, mock_current_app, mock_decrypt_filename, files):
        pairpath = '/pa/th/path'
        mock_decrypt_filename.return_value = {}
        result = get_files_info(pairpath, files)
        assert result == []


@mock.patch('aubrey_transcription.utils.current_app', config={'FILENAME_REGEX': FILENAME_REGEX})
class TestDecryptFilename():
    @pytest.mark.parametrize('filename,expected', [
        (
            'metaid_manifestation_fileset-kind-language.extension',
            {
                'metaid': 'metaid',
                'manifestation': 'manifestation',
                'fileset': 'fileset',
                'kind': 'kind',
                'language': 'language',
                'extension': 'extension'
            }
        ),
        (
            'metadc12345_m1_1-captions-eng.vtt',
            {
                'metaid': 'metadc12345',
                'manifestation': 'm1',
                'fileset': '1',
                'kind': 'captions',
                'language': 'eng',
                'extension': 'vtt'
            }
        ),
    ])
    def test_compliant_filename(self, mock_current_app, filename, expected):
        result = decrypt_filename(filename)
        assert result == expected

    @pytest.mark.parametrize('filename', [
        'captions.txt',
        'bad',
        'this_is_missing-an-extension',
    ])
    def test_noncompliant_filename(self, mock_current_app, filename):
        result = decrypt_filename(filename)
        assert result == {}
