\# URL Categorizer

An extensible tool for real-time URL classification.

\- FastAPI REST API with live docs

\- Live blacklists (Steven Black’s hosts, URLHaus malware)

\- ML fallback (zero-shot transformer, customizable categories)

\- Modern Tkinter desktop GUI (with live API logs, single launch)

\- Easy local and batch use

* * *

\## Features

\- \*\*Hybrid classification\*\*: Combines blacklist lookups with ML content analysis

\- \*\*API-first\*\*: REST API for web and automation

\- \*\*Modern GUI\*\*: Tkinter app (shows API logs, auto-launches everything)

\- \*\*Live blacklists\*\*: Downloads latest Steven Black hosts + URLHaus

* * *

\## Screenshot

* * *

\## Quickstart

\### 1. Install dependencies

```shell
pip install -r requirements.txt
```

### 2\. Run the GUI (auto-starts API in background, logs shown live)

[](https://github.com/Escaroth07/url_categorizer/blob/main/README.md#2-run-the-gui-auto-starts-api-in-background-logs-shown-live)

```shell
python gui_app.py
```

*   The "Categorize" button is enabled when the API is ready.

\- All FastAPI logs are visible in the GUI.

\- Enter a URL and click Categorize to see results.

### 3.(Optional) Run API manually

[](https://github.com/Escaroth07/url_categorizer/blob/main/README.md#3optional-run-api-manually)

If you want just the API (e.g., for server/cloud use):

```shell
uvicorn main:app --reload
```

API docs at: [http://localhost:8000/docs](http://localhost:8000/docs)
