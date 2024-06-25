from unittest import mock


class TestListFiles:
    @mock.patch('aubrey_transcription.aubrey_transcription.get_files_info')
    @mock.patch('aubrey_transcription.aubrey_transcription.find_files')
    @mock.patch('aubrey_transcription.aubrey_transcription.make_path')
    def test_200_ok(self, mock_make_path, mock_find_files, mock_get_files_info, client):
        mock_make_path.return_value = None
        mock_find_files.return_value = None
        mock_get_files_info.return_value = None
        response = client.get('/metadc123456/')
        assert response.status_code == 200

    @mock.patch('aubrey_transcription.aubrey_transcription.get_files_info')
    @mock.patch('aubrey_transcription.aubrey_transcription.find_files')
    @mock.patch('aubrey_transcription.aubrey_transcription.make_path')
    def test_no_slash_redirect(self, mock_make_path, mock_find_files, mock_get_files_info, client):
        mock_make_path.return_value = None
        mock_find_files.return_value = None
        mock_get_files_info.return_value = None
        response = client.get('/metadc123456')  # No trailing slash.
        assert response.status_code == 308

    @mock.patch('aubrey_transcription.aubrey_transcription.get_files_info')
    @mock.patch('aubrey_transcription.aubrey_transcription.find_files')
    @mock.patch('aubrey_transcription.aubrey_transcription.make_path')
    def test_returns_json(self, mock_make_path, mock_find_files, mock_get_files_info, client):
        mock_make_path.return_value = None
        mock_find_files.return_value = None
        mock_get_files_info.return_value = []
        response = client.get('/metadc123456/')
        json = response.get_json()
        assert response.is_json
        assert json == []

    @mock.patch('aubrey_transcription.aubrey_transcription.get_files_info')
    @mock.patch('aubrey_transcription.aubrey_transcription.find_files')
    @mock.patch('aubrey_transcription.aubrey_transcription.make_path')
    def test_returns_expected(self, mock_make_path, mock_find_files, mock_get_files_info, client):
        mock_make_path.return_value = 'alpha'
        mock_find_files.return_value = ['bravo', 'charlie']
        mock_get_files_info.return_value = ['charlie']
        response = client.get('/metadc123456/')
        mock_make_path.assert_called_once_with('metadc123456')
        mock_find_files.assert_called_once_with('alpha')
        mock_get_files_info.assert_called_once_with('alpha', ['bravo', 'charlie'])
        assert response.get_json() == ['charlie']
