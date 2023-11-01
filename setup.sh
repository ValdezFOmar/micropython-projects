# First create a virtual enviroment with
#
# `python -m venv .venv`

mkdir lib
mkdir typings && pip install --target typings micropython-rp2-pico_w-stubs==1.20.0.post3 -U
pip install -r requirements.txt
