#!/bin/bash
#SBATCH --job-name=ego4d_val_center_framing
#SBATCH --gres=gpu:1
#SBATCH -o ego4dval_center_framing.out
#SBATCH -e ego4dval_center_framing.err
#SBATCH --mem-per-gpu=25G 
#SBATCH --cpus-per-gpu=16
#SBATCH -p batch_ce_ugrad
#SBATCH --time=3-00:00:0
#SBATCH -w sw2

python centerframing.py
