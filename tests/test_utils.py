from unittest import mock

import pytest

from aubrey_transcription.utils import (make_path, find_files, get_files_info, decrypt_filename,
                                        assign_val_for_sorting)
from aubrey_transcription import create_app
from aubrey_transcription.default_settings import FILENAME_PATTERN


@pytest.fixture()
def app():
    app = create_app(test_config={
        'PAIRTREE_BASE': '/some/path',
        'FILENAME_PATTERN': FILENAME_PATTERN,
        'EXTENSIONS_META': {'vtt': {'mimetype': 'text/vtt', 'use': 'vtt'}},
        'TRANSCRIPTION_URL': 'http://example.com'})
    return app


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
class TestFindFiles():
    @pytest.mark.parametrize('dir_contents, expected', [
        (
            ['metadc977400_m1_2-subtitles-eng.vtt', 'metadc977400_m1_1-subtitles-fre.vtt'],
            ['metadc977400_m1_1-subtitles-fre.vtt', 'metadc977400_m1_2-subtitles-eng.vtt']
        ),
        (['metadc977400_m1_1-subtitles-fre.vtt'], ['metadc977400_m1_1-subtitles-fre.vtt']),
        ([], []),
    ])
    @mock.patch('aubrey_transcription.utils.os.listdir')
    def test_path_is_dir(self, mock_listdir, mock_isdir,
                         app, dir_contents, expected):
        pairpath = '/so/me/pa/th/somepath'
        mock_isdir.return_value = True
        mock_listdir.return_value = dir_contents
        with app.app_context():
            result = find_files(pairpath)
        assert result == expected

    @mock.patch('aubrey_transcription.utils.sorted')
    @mock.patch('aubrey_transcription.utils.os.listdir')
    def test_non_int_filename(self, mock_listdir, mock_sorted, mock_isdir, app):
        pairpath = '/so/me/pa/th/somepath'
        mock_isdir.return_value = True
        expected = ['one.vtt', 'two.xml', 'three.jpg']
        mock_listdir.return_value = expected
        mock_sorted.side_effect = ValueError
        with app.app_context():
            result = find_files(pairpath)
        # When the sorting fails, we expect to get the files in the order listdir gave them
        assert result == expected

    def test_path_is_not_dir(self, mock_isdir, app):
        pairpath = '/so/me/fi/le/somefile'
        mock_isdir.return_value = False
        with app.app_context():
            result = find_files(pairpath)
        assert result == []

    def test_path_normalized(self, mock_isdir, app):
        pairpath = '///so/./././////me//fi/le/////somefile//////'
        expected = '/so/me/fi/le/somefile'
        mock_isdir.return_value = False
        with app.app_context():
            find_files(pairpath)
        assert mock_isdir.call_args[0][0].endswith(expected)


class TestAssignValForSorting():
    @pytest.mark.parametrize('item, expected_value', [
        # Captions should show up first so it gets the 'a' prefix
        ({'vtt_kind': 'captions', 'language': 'fre'}, 'afre'),
        # English should sort before other languages, so replace with 'aaa'
        ({'vtt_kind': 'thumbnails', 'language': 'eng'}, 'faaa'),
        ({'vtt_kind': 'chapters', 'language': 'ger'}, 'cger'),
        # Missing or unknown vtt kinds sort last
        ({'language': 'spa'}, 'gspa'),
        # Missing languages sort last
        ({'vtt_kind': 'metadata'}, 'ezzz'),
        ({}, 'gzzz'),
    ])
    def test_assigns_expected_values(self, item, expected_value):
        actual_value = assign_val_for_sorting(item)
        assert actual_value == expected_value


@mock.patch('aubrey_transcription.utils.decrypt_filename')
class TestGetFilesInfo():
    @mock.patch('aubrey_transcription.utils.assign_val_for_sorting')
    @mock.patch('aubrey_transcription.utils.os.path.getsize')
    def test_returns_correct_info(self, mock_getsize, mock_assign_val_for_sorting,
                                  mock_decrypt_filename, app):
        pairpath = '/pa/th/path'
        files = ['metaid_m1_1-captions-eng.vtt']
        mock_decrypt_filename.return_value = {
            'manifestation': '1',
            'fileset': '1',
            'kind': 'captions',
            'language': 'eng',
        }
        mock_getsize.return_value = 256
        expected = {
            '1': {
                '1': [
                    {
                        'MIMETYPE': 'text/vtt',
                        'USE': 'vtt',
                        'flocat': 'http://example.com/pa/th/path/metaid_m1_1-captions-eng.vtt',
                        'SIZE': '256',
                        'vtt_kind': 'captions',
                        'language': 'eng',
                    }
                ]
            }
        }
        with app.app_context():
            result = get_files_info(pairpath, files)
        assert result == expected
        mock_assign_val_for_sorting.assert_called_once_with(expected['1']['1'][0])

    @pytest.mark.parametrize('transcription_url', [
        'http://example.com',
        'http://example.com/'
    ])
    @mock.patch('aubrey_transcription.utils.os.path.getsize')
    def test_flocat_has_single_slash(self, mock_getsize, mock_decrypt_filename,
                                     app, transcription_url):
        app.config[''] = transcription_url
        pairpath = '/pa/th/path'
        files = ['metaid_m1_1-captions-eng.vtt']
        mock_decrypt_filename.return_value = {
            'manifestation': '1',
            'fileset': '1',
            'kind': 'captions',
            'language': 'eng',
        }
        mock_getsize.return_value = 256
        expected_flocat = 'http://example.com/pa/th/path/metaid_m1_1-captions-eng.vtt'
        with app.app_context():
            result = get_files_info(pairpath, files)
        assert result['1']['1'][0]['flocat'] == expected_flocat

    @mock.patch('aubrey_transcription.utils.os.path.getsize')
    def test_manifestation_and_fileset_structure(self, mock_getsize,
                                                 mock_decrypt_filename, app):
        pairpath = '/pa/th/path'
        files = [
            'metaid_m1_8-captions-eng.vtt',
            'metaid_m2_5-captions-ger.vtt'
        ]
        mock_decrypt_filename.side_effect = [
            {
                'manifestation': '1',
                'fileset': '8',
                'kind': 'captions',
                'language': 'eng',
            },
            {
                'manifestation': '2',
                'fileset': '5',
                'kind': 'captions',
                'language': 'ger',
            }
        ]
        mock_getsize.return_value = 256
        with app.app_context():
            result = get_files_info(pairpath, files)
        assert result['1']['8']
        assert result['2']['5']
        assert not result['1']['1']

    @mock.patch('aubrey_transcription.utils.os.path.getsize')
    def test_removes_bad_extensions(self, mock_getsize, mock_decrypt_filename, app):
        pairpath = '/pa/th/path'
        files = ['id_m1_1-captions-eng.vtt', 'id_m1_1-captions-ger.txt', 'id_m1_1-captions-fr.vtt']
        mock_decrypt_filename.return_value = {
            'manifestation': '1',
            'fileset': '1',
            'kind': 'captions',
            'language': 'eng'
        }
        mock_getsize.return_value = 256
        with app.app_context():
            result = get_files_info(pairpath, files)
        assert len(result['1']['1']) == 2
        assert result['1']['1'][0]['flocat'].endswith('.vtt')
        assert result['1']['1'][1]['flocat'].endswith('.vtt')

    @mock.patch('aubrey_transcription.utils.os.path.getsize')
    def test_path_does_not_exist(self, mock_getsize, mock_decrypt_filename, app):
        pairpath = '/pa/th/path'
        files = ['id_m1_1-captions-eng.vtt']
        mock_decrypt_filename.return_value = {
            'manifestation': '1',
            'fileset': '1',
            'kind': 'captions',
            'language': 'eng'
        }
        mock_getsize.side_effect = OSError
        with app.app_context():
            result = get_files_info(pairpath, files)
        assert result == {}

    @pytest.mark.parametrize('files', [
        ['two'],
        ['two.vtt'],
    ])
    def test_bad_filenames(self, mock_decrypt_filename, app, files):
        pairpath = '/pa/th/path'
        mock_decrypt_filename.return_value = {}
        with app.app_context():
            result = get_files_info(pairpath, files)
        assert result == {}


class TestDecryptFilename():
    def test_compliant_filename(self, app):
        filename = 'metadc12345_m1_1-captions-eng.vtt'
        expected = {
            'metaid': 'metadc12345',
            'manifestation': '1',
            'fileset': '1',
            'kind': 'captions',
            'language': 'eng',
            'extension': 'vtt'}
        with app.app_context():
            result = decrypt_filename(filename)
        assert result == expected

    @pytest.mark.parametrize('filename', [
        'captions.txt',
        'bad',
        'this_is_missing-an-extension',
    ])
    def test_noncompliant_filename(self, app, filename):
        with app.app_context():
            result = decrypt_filename(filename)
        assert result == {}
