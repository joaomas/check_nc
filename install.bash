# for module @ cluster Egeon
module load python-3.9.13-gcc-9.4.0-moxjnc6 

echo "Creating python environment .venvj >>> $(pwd)"
python -m venv .venvj
source .venvj/bin/activate
pip install -r requirements.txt
