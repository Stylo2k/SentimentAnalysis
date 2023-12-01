#!/bin/bash

#SBATCH --export=ALL
#SBATCH --gpus-per-node=a100:4
#SBATCH --mem-per-gpu=40G

module load Python/3.10.8-GCCcore-12.2.0
# virtualenv ownenv
source /home3/p306726/stanford_alpaca/ownenv/bin/activate
pip install --upgrade pip

pip install -r install.sh
echo "removing bitsandbytes"
ls /home3/p306726/stanford_alpaca/ownenv/lib/python3.10/site-packages/ | grep bitsandbytes
rm -rf /home3/p306726/stanford_alpaca/ownenv/lib/python3.10/site-packages/bitsandbytes-0.37.2.dist-info
rm -rf /home3/p306726/stanford_alpaca/ownenv/lib/python3.10/site-packages/bitsandbytes
echo "installing bitsandbytes"
pip install bitsandbytes
ls /home3/p306726/stanford_alpaca/ownenv/lib/python3.10/site-packages/ | grep bitsandbytes

pip install accelerate==0.20.3
pip install scipy

echo "=============================================="
echo "Running own_train.py"

python own_train.py