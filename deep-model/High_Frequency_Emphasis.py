#!/usr/bin/env python
# coding: utf-8

# In[142]:


import numpy as np
import scipy.misc
import psychopy.visual
import psychopy.event
import psychopy.filters
import matplotlib.pyplot as plt
import cv2
import copy


# In[143]:


img_name = '26 Nov @1708 0001.jpg'
raw_img = cv2.imread(img_name)
gray_img = cv2.cvtColor(raw_img, cv2.COLOR_BGR2GRAY)
real_img.shape


# In[122]:


arr = np.array([[[1, 2], [3, 4], [5, 6]], [[11, 22], [33, 44], [55, 66]]])
arr2 = arr.T
arr2


# In[123]:


# conversion from color img to intensity modified img
def intensity_modify(modified_intensity):
    orig_intensity = np.average(real_img, axis=2)
    orig_img = (real_img.T * (modified_intensity.T / orig_intensity.T)).T
    # if orig_intensity == 0 then 0 else orig_img * (modified_img / orig_intensity)
    return orig_img.astype(int)


# In[124]:


# HE 
def HE(input_img): # input image has 3 channels 
    modified_img = input_img.T
    for i in range(3):
        img = modified_img[i]
        hist, bins = np.histogram(img.flatten(), 256,[0,256])
        cdf = hist.cumsum()
        cdf_m = np.ma.masked_equal(cdf,0)
        cdf_m = (cdf_m - cdf_m.min())*255/(cdf_m.max()-cdf_m.min())
        cdf = np.ma.filled(cdf_m,0).astype('uint8')
        modified_img[i] = cdf[img]
    print(modified_img.T.shape)
    return modified_img.T        


# In[125]:


fig = plt.gcf()
plt.subplot(121),plt.imshow(cv2.cvtColor(raw_img, cv2.COLOR_BGR2RGB)),plt.title('Original')
plt.subplot(122),plt.imshow(cv2.cvtColor(HE(raw_img), cv2.COLOR_BGR2RGB)),plt.title('Equalization')
plt.show()
fig.savefig('HE5.pdf', dpi=1200)


# In[157]:


# HFE
def HFE(input_image):
    modified_img = copy.deepcopy(input_image).T
    for i in range(3):
        img = modified_img[i]
        img = (img / 255.0) * 2.0 - 1.0
        img = np.flipud(img)
        rms = 0.2

        # make the mean to be zero
        img = img - np.mean(img)
        # make the standard deviation to be 1
        img = img / np.std(img)
        # make the standard deviation to be the desired RMS
        img = img * rms

        # convert to frequency domain
        img_freq = np.fft.fft2(img)

        # calculate amplitude spectrum
        img_amp = np.fft.fftshift(np.abs(img_freq))

        hp_filt = psychopy.filters.butter2d_hp(
            size=img.shape,
            cutoff=0.01,
            n=8
        )
        a = 0.5
        b = 1.5
        new_filt = a + b*hp_filt
        img_filt = np.fft.fftshift(img_freq) * new_filt
        # img_filt = np.fft.fftshift(img_freq) * (a + b * hp_filt)
        
        # convert back to an image
        img = np.real(np.fft.ifft2(np.fft.ifftshift(img_filt)))

        # convert to mean zero and specified RMS contrast
        img = img - np.mean(img)
        img = img / np.std(img)
        img = img * rms

        # there may be some stray values outside of the presentable range; convert < -1
        # to -1 and > 1 to 1
        img = np.clip(img, a_min=-1.0, a_max=1.0)
        
        #conversion to uint8
        img = ((img+1)/2*256).astype('uint8')
        modified_img[i] = img
    return modified_img.T


# In[158]:


fig = plt.gcf()
plt.axis('off')
plt.imshow(cv2.cvtColor(HE(HFE(raw_img)), cv2.COLOR_BGR2RGB))
plt.show()
fig.savefig('HFE2.jpg', dpi=1200, bbox_inches='tight')






