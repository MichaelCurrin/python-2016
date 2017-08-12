# Sublime For Python

My tips on setting up Sublime 3 with custom settings and packages for Python coding. Some of these might apply to bash or SQL as well.

## Linting

Install Flakes8 linter

Modify the package's user settings to
```
{
    "debug": true,
    "lint_on_save": false,
    "pep8_max_line_length": 80,
    "popup": false,
    "naming": false,
    "import-order": true,
    "import-order-style": "google"
}
```
