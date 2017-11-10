# Fractal Editor

This is a set of tools for rendering and editing fractals, using [iterated function systems](https://en.wikipedia.org/wiki/Iterated_function_system).

## Getting started

The demo site is maintained at: http://fractaleditor.com/

If you want to run the software locally, clone this repository and:

* cd FractalEditorSite
* virtualenv venv/
* source venv/bin/activate
* pip install -r requirements.txt
* cp fractaleditor/settings.example.py fractaleditor/settings.py
* python manage.py migrate
* python manage.py runserver

## License

This project is distributed under the GPLv3 license, see [LICENSE](LICENSE).
