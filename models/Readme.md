Credit: [Github Repo Link](https://github.com/xinntao/ESRGAN)

Download pretrained ESRGAN models from [Google Drive](https://drive.google.com/drive/u/0/folders/17VYV_SoZZesU6mbxz2dMAIccSSlqLecY). Place the models in ./models. Two models are provided with high perceptual quality and high PSNR performance (see model list).

1. `RRDB_ESRGAN_x4.pth`: the final ESRGAN model used in the [paper](https://arxiv.org/abs/1809.00219). 
2. `RRDB_PSNR_x4.pth`: the PSNR-oriented model with **high PSNR performance**.

*Note that* the pretrained models are trained under the `MATLAB bicubic` kernel. 
If the downsampled kernel is different from that, the results may have artifacts.
