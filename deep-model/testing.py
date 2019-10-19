from matplotlib import pyplot as plt
import gluoncv
from gluoncv import model_zoo, data, utils
import mxnet as mx
import numpy as np
import os, shutil, time, sys, argparse, logging, time
from pathlib import Path
from concurrent import futures
from gluon_utils import *


def gpu_device(gpu_number=0):
    try:
        _ = mx.nd.array([1, 2, 3], ctx=mx.gpu(gpu_number))
    except mx.MXNetError:
        return mx.cpu()
    return mx.gpu(gpu_number)


ctx = gpu_device()
model = model_zoo.get_model('mask_rcnn_fpn_resnet101_v1d_coco', pretrained=True, ctx=ctx)

image_dir = "1570083162385_--1"
client_id_path = image_dir+"/" if len(image_dir)>1 else ""
input_path =  "uploads/" + client_id_path 
output_path = "output/" + client_id_path
img_name = os.listdir(input_path)[0]
input_file, output_file = input_path + img_name, output_path +img_name

x, orig_img = data.transforms.presets.rcnn.load_test(input_file)
x = x.as_in_context(ctx)
ax, count, process_time = instance_segmentation_pipeline(model, x, orig_img)
print("Count: %d"%count)
os.mkdir(output_path)
plt.savefig(output_file)

if count > 0:
    pred_result = "%d people detected in %.4f sec"%(count,process_time)
else:
    pred_result = "Fail to detect any person"         

print("[RETURN SERVER] - ",pred_result)         
