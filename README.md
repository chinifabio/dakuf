# DAKUF (Duet Adapter for Klipper Using Flask)

**DAKUF** is a Flask-based HTTP API adapter that allows users to use a new API by interfacing with the endpoint of the old one.

## Installation

To install DAKUF, run the following command:

```bash
sudo make install
```

Insert into the `moonraker.conf` file the following lines:

```ini
[update_manager dakuf]
type: git_repo
path: ~/dakuf
origin: https://github.com/chinifabio/dakuf.git
virtualenv: ~/dakuf/dakuf-env/
requirements: requirements.txt
install_script: install.sh
managed_service: dakuf
```
