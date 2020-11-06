# How to Contribute

## Setting up the Development Environment

1. Git clone the repository

```
git clone https://github.com/kxr/o-must-gather
```

2. Create and activate a separate python virtual environment for o-must-gather

```
# Create a new venv
python3 -m venv o-must-gather-venv
# Activate the venv
source o-must-gather-venv/bin/activate
```
3. Install o-must-gather in the venv

```
pip3 install -e o-must-gather/
```

If the above steps were executed successfully, you should now have:

  - Code directory `o-must-gather`(which we cloned from github)
  - Python venv directory `o-must-gather-venv` (all the dependencies/libraries are contained here)
  - `omg` executable binary in your path

Any change in the code will now be directly reflected and can be tested.
To deactivate the python venv, simply run `deactivate`.
Note that since we installed o-must-gather in a venv, `omg` binary will only be available when the venv is activated (`source o-must-gather-venv/bin/activate`).
