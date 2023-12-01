#!/bin/bash
#SBATCH --export=ALL
#SBATCH --gpus-per-node=a100:2
#SBATCH --mem-per-gpu=80G
#SBATCH --time=4:00:00
#SBATCH --nodes=4

module load  Python/3.10.8-GCCcore-12.2.0
source /scratch/p306726/alpaca_lora/bin/activate
python own_train.py
