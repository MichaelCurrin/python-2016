# Sublime For Python

My tips on setting up Sublime 3 with custom settings and packages for Python coding. Some of these might apply to bash or SQL as well.

## Sublime Settings

This is what I use. Note that though when changing the font size with mouse-wheel scroll and holding control, the
font_size is updated and the contents of user settings file is automatically rearranged by Sublime.
All comments are removed and keys are arranged alphabetically.
```
{
	"auto_complete_commit_on_tab": true,
	"bold_folder_labels": true,
	"color_scheme": "Packages/User/Monokai (Flake8Lint).tmTheme",
	"detect_indentation": true,
	"dictionary": "Packages/Language - English/en_GB.dic",
	"enable_tab_scrolling": true,
	"ensure_newline_at_eof_on_save": true,
	"font_size": 10,
	"highlight_modified_tabs": true,
	"ignored_packages":
	[
		"Vintage"
	],
	"indent_to_bracket": true,
	"remember_full_screen": true,
	"rulers":
	[
		80,
		120
	],
	"show_encoding": true,
	"show_line_endings": true,
	"tab_size": 4,
	"translate_tabs_to_spaces": true,
	"trim_trailing_white_space_on_save": true,
	"use_tab_stops": true,
	"word_wrap": true
}

```

## Linting

Install Flakes8 linter

Modify the package's user settings to
```
{
    "debug": true,
    "pep8_max_line_length": 80,
    "popup": false,
    "naming": false,
    "import-order": true,
    "import-order-style": "google"
}
```
