import gluoncv
import mxnet as mx
import numpy as np
from matplotlib import pyplot as plt
import random, time


def plot_bbox(img, bboxes, scores=None, labels=None, thresh=0.5,
              class_names=None, colors=None, ax=None,
              reverse_rgb=False, absolute_coordinates=True):

    if labels is not None and not len(bboxes) == len(labels):
        raise ValueError('The length of labels and bboxes mismatch, {} vs {}'
                         .format(len(labels), len(bboxes)))
    if scores is not None and not len(bboxes) == len(scores):
        raise ValueError('The length of scores and bboxes mismatch, {} vs {}'
                         .format(len(scores), len(bboxes)))

    ax = gluoncv.utils.viz.plot_image(img, ax=ax, reverse_rgb=reverse_rgb)

    if len(bboxes) < 1:
        return ax

    if isinstance(bboxes, mx.nd.NDArray):
        bboxes = bboxes.asnumpy()
    if isinstance(labels, mx.nd.NDArray):
        labels = labels.asnumpy()
    if isinstance(scores, mx.nd.NDArray):
        scores = scores.asnumpy()

    if not absolute_coordinates:
        # convert to absolute coordinates using image shape
        height = img.shape[0]
        width = img.shape[1]
        bboxes[:, (0, 2)] *= width
        bboxes[:, (1, 3)] *= height

    # use random colors if None is provided
    if colors is None:
        colors = dict()
    for i, bbox in enumerate(bboxes):
        if scores is not None and scores.flat[i] < thresh:
            continue
        if labels is not None and labels.flat[i] < 0:
            continue
        cls_id = int(labels.flat[i]) if labels is not None else -1
        if cls_id not in colors:
            if class_names is not None:
                colors[cls_id] = plt.get_cmap('hsv')(cls_id / len(class_names))
            else:
                colors[cls_id] = (random.random(), random.random(), random.random())
        xmin, ymin, xmax, ymax = [int(x) for x in bbox]
        rect = plt.Rectangle((xmin, ymin), xmax - xmin,
                             ymax - ymin, fill=False,
                             edgecolor=colors[cls_id],
                             linewidth=1)
        ax.add_patch(rect)
        if class_names is not None and cls_id < len(class_names):
            class_name = class_names[cls_id]
        else:
            class_name = str(cls_id) if cls_id >= 0 else ''
        score = '{:.3f}'.format(scores.flat[i]) if scores is not None else ''

#         if class_name or score:
#             ax.text(xmin, ymin - 2,
#                     '{:s} {:s}'.format(class_name, score),
#                     bbox=dict(facecolor=colors[cls_id], alpha=0.5),
#                     fontsize=12, color='white')
    ax.set_axis_off()

    return ax


def object_detection_pipeline(model, x, orig_img):
    height, width, _ = orig_img.shape
    print("(H,W): (%d,%d)"%(height,width))

    start = time.time()
    box_ids, scores, bboxes = [np.squeeze(xx.asnumpy()) for xx in model(x)] # bbox (x,y) [tl_x tl_y br_x br_y]
    thr_people_index = (scores > 0.5) & (box_ids == 0)
    cnt = sum(thr_people_index)
    end = time.time()
    print("Inference (gpu->cpu conversion) : %.5f sec"%(end-start))

    ax = plot_bbox(orig_img, bboxes[thr_people_index],scores[thr_people_index],box_ids[thr_people_index])
    ax.text(width-100, 50, str(int(cnt)), fontsize = 10, color = 'red')  
    print("[%d] people detected  Total time: %.5fsec"%(cnt, time.time()-start))

    return ax

def instance_segmentation_pipeline(model, x, orig_img):
    height, width, _ = orig_img.shape
    print("(H,W): (%d,%d)"%(height,width))

    print(x)
    print(orig_img)
    start = time.time()
    box_ids, scores, bboxes, _ = [np.squeeze(xx.asnumpy()) for xx in model(x)]
    thr_people_index = (scores > 0.5) & (box_ids == 0)
    cnt = sum(thr_people_index)
    end = time.time()
    # print("Inference (gpu->cpu conversion) : %.5f sec"%(end-start))

    ax = plot_bbox(orig_img, bboxes[thr_people_index],scores[thr_people_index],box_ids[thr_people_index])
    ax.text(width-100, 50, str(int(cnt)), fontsize = 10, color = 'red')  
    # print("[%d] people detected  Total time: %.5fsec"%(cnt, time.time()-start))

    return ax, cnt, end-start