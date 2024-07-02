Aubrey-transcription [![Build Status](https://www.github.com/unt-libraries/aubrey-transcription/actions/workflows/test.yml/badge.svg?branch=master)](https://www.github.com/unt-libraries/aubrey-transcription/actions)
====================


About
--------------------

This is a service that returns information about available transcription files
for a given record. The data is returned as JSON. This service is intended to
be placed on the same server that the actual transcription files are located on,
and it must have access to those files, which must be in a pairtree directory
structure.


Requirements
--------------------

* Python 3.8 - 3.12
* Flask 3.0.3
* pypairtree


Developing/Testing
--------------------

In order to start developing or run the tests, it is recommended that you set up
a virtual environment specifically for aubrey-transcription. To do so, download
virtualenv and then set up a virtual environment with Python according to the
documentation.

One you have a virtual environment, activate it and proceed with the following
directions to start developing/testing.

1. Clone this repository and move to the project root.
    ```sh
        $ git clone git@github.com:unt-libraries/aubrey-transcription.git
        $ cd aubrey-transcription
    ```

2. Install the required dependencies.
    ```sh
        $ pip install -r test-requirements.txt
    ```

3. Provide the proper configuration settings. This will be specific to how you
   are using this application. There are 5 main settings that should be configured
   properly, either by modifying the "default_settings.py" file in the
   aubrey_transcription package or by creating a directory called "instance" at the
   root of the project and putting a new file called "settings.py" there with the
   following 5 settings:

   SECRET_KEY: This string is fine to just leave as "dev" for development and testing,
   but MUST be changed to be more secure when being used in a production setting.

   PAIRTREE_BASE: This is a string that defines the path to the root of the pairtree
   that has all the transcription files. This should be a path that is accessible by
   the Flask app.

   TRANSCRIPTION_URL: This is a string which is prepended to the pairpaths for all the
   transcription files and returned in the JSON. No actual calls are made to this URL.
   It is expected that whoever is consuming the JSON from this app can then retrieve
   the specified transcription files by using the URLs provided.

   EXTENSIONS_META: This is a dictionary of dictionaries. The keys to this dictionary
   are the extensions that you deem appropriate indicators of transcription files, in
   our case "vtt" would be a key, as our transcription files end in the ".vtt" extension.
   The value for the key is another dictionary that has "use" and "mimetype" keys with
   their appropriate string values.

   FILENAME_PATTERN: This is a Python regex pattern string that is used to parse the
   transcription filenames into their various parts such as language, extensions, etc.
   All transcription filenames MUST follow the pattern described by this string or they
   will be ignored.

   Please see "default_settings.py" for an example of how a settings file should look.

4. Start the app.
    ```sh
        $ flask --app aubrey_transcription run --debug
    ```

5. You may now visit the app by visiting the location given to you after running the
   previous command, which should be something like "http://127.0.0.1:5000/identifier/",
   with "identifier" replaced by an existing identifier whose transcriptions can be found
   in your local pairtree.

6. To run the test suite against your current version of Python (whatever is in your virtualenv),
   do the following, which will also generate the coverage report.
    ```sh
        coverage run -m pytest
    ```

7. You may view the coverage report after running the tests.
    ```sh
        coverage report -m
    ```

8. If you have multiple of the compatible versions of Python installed, then you can test against
   them all with tox.
    ```sh
        tox
    ```


License
--------------------

See LICENSE.txt


Contributors
--------------------

* [Gio Gottardi](https://github.com/somexpert)
* [Gracie Flores-Hays](https://github.com/gracieflores)
* [Lauren Ko](https://github.com/ldko)
