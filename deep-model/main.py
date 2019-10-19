from matplotlib import pyplot as plt
import gluoncv
from gluoncv import model_zoo, data, utils
import mxnet as mx
import numpy as np
import os, shutil, time, sys, argparse, logging
from pathlib import Path
from concurrent import futures
import grpc
import prediction_pb2
import prediction_pb2_grpc
from gluon_utils import *


_ONE_DAY_IN_SECONDS = 60 * 60 * 24
_ONE_WEEK_IN_SECONDS =  60 * 60 * 24 * 7
_ONE_MONTH_IN_SECONDS = 60 * 60 * 24 * 31
OFFSET = os.path.dirname(os.path.abspath(__file__)).replace(os.getcwd(),"")[1:]+"/"
logger = logging.getLogger()


def gpu_device(gpu_number=0):
    try:
        _ = mx.nd.array([1, 2, 3], ctx=mx.gpu(gpu_number))
    except mx.MXNetError:
        return mx.cpu()
    return mx.gpu(gpu_number)


def rmfiles(dir):
    for root, dirs, files in os.walk(dir):
        for file in files:
            os.remove(os.path.join(root, file))


class Predictor(prediction_pb2_grpc.PredictorServicer):
    def __init__(self):
        ctx = gpu_device()
        mrcnn_model = model_zoo.get_model('mask_rcnn_fpn_resnet101_v1d_coco', pretrained=True, ctx=ctx)
        self.ctx = ctx
        self.model = mrcnn_model
        

    def Prediction(self, request, context):
        client_id_path = request.image_dir+"/" if len(request.image_dir)>1 else ""
        input_path =  "uploads/" + client_id_path 
        output_path = "output/" + client_id_path
        img_name = os.listdir(input_path)[0]
        input_file, output_file = input_path + img_name, output_path +img_name
                
        count, process_time = -1, -1
        try:
            print(input_file)
            x, orig_img = data.transforms.presets.rcnn.load_test(input_file)
            x = x.as_in_context(self.ctx)
            ax, count, process_time = instance_segmentation_pipeline(self.model, x, orig_img)
            os.mkdir(output_path)
            plt.savefig(output_file)
        except Exception as e:
            logger.exception()
            raise
        finally:
            if count > 0:
                pred_result = "%d people detected in %.4f sec"%(count,process_time)
            else:
                pred_result = "Fail to detect any person"            
            print("[RETURN SERVER] - ",pred_result)         
            return prediction_pb2.PredictReply(message=pred_result)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    prediction_pb2_grpc.add_PredictorServicer_to_server(Predictor(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Prediction server starts")
    try:
        while True:
            time.sleep(_ONE_MONTH_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()


