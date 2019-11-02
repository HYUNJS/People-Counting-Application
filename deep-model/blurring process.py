#!/usr/bin/env python
# coding: utf-8

# In[67]:


import numpy as np
import scipy.misc
import psychopy.visual
import psychopy.filters
import matplotlib.pyplot as plt
import matplotlib.image as mpimg 
import cv2


# In[68]:


img = cv2.imread('metal bar.jpg')
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img.shape
# print(img_gray)


# In[69]:


# Change to frequency domain
f = np.fft.fft2(img_gray)
fshift = np.fft.fftshift(f)
magnitude_spectrum = 20*np.log(np.abs(fshift))
print(magnitude_spectrum.shape)
# plt.axis('off')
# # fig1 = plt.figure(frameon=False)
# # # fig1.patch.set_visible(False)
# # # cur_axes = plt.gca()
# # # cur_axes.axes.get_xaxis().set_visible(False)
# # # cur_axes.axes.get_yaxis().set_visible(False)
fig1 = plt.gcf()
plt.rcParams["figure.figsize"] = (9, 16)
plt.axis('off')
plt.imshow(magnitude_spectrum, cmap = 'gray')
fig1.savefig('spectrum.jpg', bbox_inches='tight', pad_inches=0, dpi=550.6)
# # fig1.savefig('spectrum.jpg')
# fig1 = plt.gcf()
# plt.imshow(magnitude_spectrum, cmap='gray')
# plt.savefig("spectrum.png", bbox_inches='tight')


# plt.imshow(magnitude_spectrum, cmap='gray')
# plt.show()


# In[70]:


img2 = cv2.imread('spectrum.jpg')
output = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
output.shape


# In[121]:


freq_filter = cv2.imread('frequency filter.jpg')
freq_filter = cv2.cvtColor(freq_filter, cv2.COLOR_BGR2GRAY)
freq_filter = (1.0 - freq_filter / 255.0)
shape = freq_filter.shape
cw = 30
freq_filter[int(shape[0]/2)-cw:int(shape[0]/2+cw), int(shape[1]/2-cw):int(shape[1]/2+cw)] = 1
plt.imshow(freq_filter, cmap = 'gray')
print(np.max(freq_filter))
print(freq_filter)
print(shape)


# In[122]:


# generating the filtered output
img = cv2.imread('26 Nov @1708 0001.jpg').T/255.0
# plt.imshow(img)
img = np.fft.fftshift(np.fft.fft2(img))
img = img * (freq_filter.T)
img = np.real(np.fft.ifft2(np.fft.ifftshift(img)) * 255.0).astype(np.uint8).T
print(img)
fig1 = plt.gcf()
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
fig1.savefig('output.jpg', bbox_inches='tight', pad_inches=0, dpi=550.6)


# In[80]:


plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))


# In[110]:


a1 = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
a1[1:2][0:] = 0
a1


# In[ ]:




