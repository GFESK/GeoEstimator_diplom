from argparse import ArgumentParser
from pathlib import Path
import pandas as pd
import torch

from classification.train_base import MultiPartitioningClassifier
from classification.dataset import FiveCropImageDataset


# def parse_args():
#     args = ArgumentParser()
#     args.add_argument(
#         "--checkpoint",
#         type=Path,
#         default=Path("models/base_M/epoch=014-val_loss=18.4833.ckpt"),
#         help="Checkpoint to already trained model (*.ckpt)",
#     )
#     args.add_argument(
#         "--hparams",
#         type=Path,
#         default=Path("models/base_M/hparams.yaml"),
#         help="Path to hparams file (*.yaml) generated during training",
#     )
#     args.add_argument(
#         "--image_dir",
#         type=Path,
#         default=Path("upload"),
#         help="Folder containing images. Supported file extensions: (*.jpg, *.jpeg, *.png)",
#     )
#     # environment
#     args.add_argument(
#         "--gpu",
#         action="store_true",
#         help="Use GPU for inference if CUDA is available",
#     )
#     args.add_argument("--batch_size", type=int, default=64)
#     args.add_argument(
#         "--num_workers",
#         type=int,
#         default=4,
#         help="Number of workers for image loading and pre-processing",
#     )
#     return args.parse_args()

def prediction_of_geo(LOCAL):

    # args = parse_args()
    if LOCAL == True:
        model = MultiPartitioningClassifier.load_from_checkpoint(
            LOCAL=LOCAL,
            checkpoint_path="models/base_M/epoch=014-val_loss=2.4460.ckpt",
            hparams_file="models/base_M/hparams_leti.yaml",
            map_location=None)

    elif LOCAL == False:
        model = MultiPartitioningClassifier.load_from_checkpoint(
            LOCAL=LOCAL,
            checkpoint_path="models/base_M/epoch=014-val_loss=18.4833.ckpt",
            hparams_file="models/base_M/hparams.yaml",
            map_location=None)

    model.eval()

    dataloader = torch.utils.data.DataLoader(
        FiveCropImageDataset(meta_csv=None, image_dir="upload"), shuffle=False)

    rows = []
    for X in dataloader:
        img_paths, pred_classes, pred_latitudes, pred_longitudes = model.inference(X)
        for p_key in pred_classes.keys():
            for img_path, pred_class, pred_lat, pred_lng in zip(
                img_paths,
                pred_classes[p_key].cpu().numpy(),
                pred_latitudes[p_key].cpu().numpy(),
                pred_longitudes[p_key].cpu().numpy(),
            ):
                rows.append(
                    {
                        "p_key": p_key,
                        "pred_lat": pred_lat,
                        "pred_lng": pred_lng,
                    }
                )

    return rows