import mock
import pytest

from aubrey_transcription import create_app, default_settings


@mock.patch('aubrey_transcription.os.makedirs')  # We don't want 'instance' dirs everywhere.
class TestCreateApp:
    @pytest.fixture(scope="session")
    def settings_file(self, tmpdir_factory):
        settings = (
            "PAIRTREE_BASE = '/different/path'"
            "\nTRANSCRIPTION_URL = 'http://someothersite.com'"
            "\nEXTENSIONS_META = {'txt': {'use': 'text', 'mimetype': 'text'}}"
        )
        fn = tmpdir_factory.mktemp('data').join('settings.py')
        fn.write(settings)
        return fn

    def test_makes_instance_dir(self, mock_makedirs):
        app = create_app()
        mock_makedirs.assert_called_once_with(app.instance_path)

    def test_can_override_instance_dir(self, mock_makedirs):
        create_app(instance_path='/new/path')
        mock_makedirs.assert_called_once_with('/new/path')

    def test_default_settings(self, mock_makedirs):
        # Move instance path in case a settings file is already in the standard location.
        app = create_app(instance_path='/nothing/here')
        assert app.config['PAIRTREE_BASE'] == default_settings.PAIRTREE_BASE
        assert app.config['TRANSCRIPTION_URL'] == default_settings.TRANSCRIPTION_URL
        assert app.config['EXTENSIONS_META'] == default_settings.EXTENSIONS_META

    def test_instance_file_overrides_default_settings(self, mock_makedirs, settings_file):
        app = create_app(instance_path=settings_file.dirname)
        assert app.config['PAIRTREE_BASE'] != default_settings.PAIRTREE_BASE
        assert app.config['PAIRTREE_BASE'] == '/different/path'
        assert app.config['TRANSCRIPTION_URL'] != default_settings.TRANSCRIPTION_URL
        assert app.config['TRANSCRIPTION_URL'] == 'http://someothersite.com'
        assert app.config['EXTENSIONS_META'] != default_settings.EXTENSIONS_META
        assert app.config['EXTENSIONS_META'] == {'txt': {'use': 'text', 'mimetype': 'text'}}

    def test_settings_passed_in_overrides_instance_file(self, mock_makedirs, settings_file):
        app = create_app(
            test_config={'PAIRTREE_BASE': '/right/here', 'TRANSCRIPTION_URL': 'something.com',
                         'EXTENSIONS_META': {}},
            instance_path=settings_file.dirname
        )
        assert app.config['PAIRTREE_BASE'] == '/right/here'
        assert app.config['TRANSCRIPTION_URL'] == 'something.com'
        assert app.config['EXTENSIONS_META'] == {}
