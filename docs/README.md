# GUIfy

![PyPI_version](https://img.shields.io/pypi/v/guify?style=for-the-badge)

![PyPI_downloads](https://img.shields.io/pypi/dm/guify?style=for-the-badge)

![PyPI_wheel](https://img.shields.io/pypi/wheel/guify?style=for-the-badge)

Simplest form of GUI for automation scripts.

Made with eel as python backend and react used as frontend.

## **[For Quick Start docs click here](../README.md)**

## Main tab

![main tab](./images/main_tab.png)

## Config tab

![config tab](./images/config_tab.png)

# Running the source code

Since we're using react, there's a custom script [run_debug.py](../run_debug.py) to run the eel backend so it does not conflict with the react dev server port.

If you're working on the frontend use

```bash
npm run start
```

This will start react dev server and run python too in same terminal instance.

If you're working on the python side, it is recommended to run the code in 2 seperate terminals:

```bash
# In first terminal
npm run start:js

# In second terminal
npm run start:guify # or "py ./run_debug.py"
```

This is because unlike React, python won't restart eel session on change of the guify source, so you'd end up restarting python a lot.

# Building

To build the package (wheel and source) in dist folder, run the following:

`npm run build`
