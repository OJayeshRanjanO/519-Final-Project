rm -rf venv
python3 -mvenv venv
source venv/bin/activate

pip install pip --upgrade
pip install -r ./requirements.txt

deactivate
