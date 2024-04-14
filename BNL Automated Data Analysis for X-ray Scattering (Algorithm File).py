#!/usr/bin/env python
# coding: utf-8

# In[1]:


#All test files:
#1) "C:\Users\Bradley\Videos\New folder\AgBH_cali_5m_13.5kev_2_1961.7s_RH661.032_x0.300_th0.000_5.00s_458795_waxs.tiff"
#2) "C:\Users\Bradley\Videos\New folder\AgBH_cali_5m_13.5kev_6_2795.4s_RH-28.010_x0.300_th0.000_5.00s_458825_saxs.tiff"
#3) "C:\Users\Bradley\Videos\New folder\AgBH_cali_5m_13.5kev_WAXSx-193_y22_x0.300_th0.000_5.00s_1000930_waxs.tiff"
#4) "C:\Users\Bradley\Videos\New folder\AgBH_cali_5m_13.5kev_x0.000_y0.000_10.00s_988715_saxs.tiff"
#5) "C:\Users\Bradley\Videos\New folder\AgBH_cali_5m_13.5kev_x0.000_y0.000_10.00s_988715_waxs.tiff"

#6) "C:\Users\Bradley\Videos\New folder\Second batch\AgBH_5m_openarea_x0.450_th0.000_10.00s_1094599_saxs.tiff"
#7) "C:\Users\Bradley\Videos\New folder\Second batch\AgBH_cali_3m_13.5kev_WAXSx-194_y17_x0.000_th0.000_10.00s_922280_waxs.tiff"
#8) "C:\Users\Bradley\Videos\New folder\Second batch\AgBH_cali_3m_13.5kev_x1.000_th0.000_10.00s_916432_saxs.tiff"
#9) "C:\Users\Bradley\Videos\New folder\Second batch\AgBH_cali_3m_WAXSx-195_y17_x0.000_th0.000_10.00s_954694_waxs.tiff"
#10) "C:\Users\Bradley\Videos\New folder\Second batch\AgBH_cali_5m_13.5kev_1_34450.6s_x0.900_y-0.400_LinkamnanC_20.00s_892406_saxs.tiff"
#11) "C:\Users\Bradley\Videos\New folder\Second batch\AgBH_cali_5m_13.5kev_WAXSx-195_y20_good_x0.300_th0.000_5.00s_1000932_waxs.tiff"
#12) "C:\Users\Bradley\Videos\New folder\Second batch\AgBH_cali_5m_13.5kev_WAXSx-217_y20_x0.500_th0.000_5.00s_1160446_waxs.tiff"
#13) "C:\Users\Bradley\Videos\New folder\Second batch\AgBH_cali_5m_13.5kev_WAXSx-225_y24_x0.300_th0.000_5.00s_1000919_waxs.tiff"
#14) "C:\Users\Bradley\Videos\New folder\Second batch\AgBH_cali_5m_13.5kev_x0.000_y0.000_10.00s_1135050_saxs.tiff"
#15) "C:\Users\Bradley\Videos\New folder\Second batch\AgBH_cali_13.5kev_5m_sam7_2_360.1s_LinkamnanC_5.00s_1148340_saxs.tiff"
#16) "C:\Users\Bradley\Videos\New folder\Second batch\AgBH_MAXSx-65_y-55_346_5506.4s_T42.821C_x0.001_th0.250_10.00s_1166652_maxs.tiff"
#17) "C:\Users\Bradley\Videos\New folder\Second batch\AgBH_WAXSx-225_WAXSy22_13_x0.000_th0.000_10.00s_1136604_waxs.tiff"
#18) "C:\Users\Bradley\Videos\New folder\Second batch\AgBH_WAXSx-235_WAXSy45_11_x0.000_th0.000_10.00s_1136602_waxs.tiff"


# In[8]:



import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import math
import import_ipynb


# In[9]:


#uncomment if this is for python
import BNL_Function_File 

#uncomment if this is for jupyter
#%run BNL_Function_File.ipynb


# In[10]:


file=r"C:\Users\Bradley\Videos\New folder\Second batch\AgBH_MAXSx-65_y-55_346_5506.4s_T42.821C_x0.001_th0.250_10.00s_1166652_maxs.tiff"
img = Image.open(file)
npformconvert=file.replace("\\", "/")
npformconvert=npformconvert.replace("C:", "")
img2 = np.asarray(Image.open(npformconvert))
#For numpy version of file all backslashes are turned into forward slashes. Also no r C:

img.convert('I').show()


# In[11]:


plotter(15)


# In[12]:


#plot to show all possible centers (if the same center was predicted multiple times, one is removed). So repeats are removed.

plotter(12)



threshold=0.999
count=20
saved_point_x=np.array([])
saved_point_y=np.array([])

#Go through multiple times, varying the threshold. If multiple thresholds yield the same possible center, remove the repeats.
while(threshold>0):
    
    #Getting the corresponding coordinate components for possible centers
    saved_point_x=np.append(saved_point_x,repeated_operation_rows(img2,threshold))
    saved_point_y=np.append(saved_point_y,repeated_operation_cols(img2,threshold))
    
    
    threshold-=0.05
    print(count)
    count-=1
    

    
#just removing repeat elements from each array
lasthold=np.array_split(two_dim_remove_repeat(saved_point_x,saved_point_y),2)    
#Note for case 1 the second array has 1 more element but this removes that extra

print()
for i in range(len(lasthold[0])-1):
    print("Possible center: ["+str(lasthold[0][i])+","+str(lasthold[1][i])+"]")
    plt.scatter(lasthold[0][i], lasthold[1][i], marker="x", s=200, c="green")
    


# In[13]:


plotter(12)

#This just expands the points for each possible center and sees which has the highest "score"
keep_score=np.array([])
for i in range(len(lasthold[0])-1):
    keep_score=np.append(keep_score,extend_unitcircle_outwards(lasthold[0][i],lasthold[1][i]))


plt.scatter(lasthold[0][np.argmax(keep_score)], lasthold[1][np.argmax(keep_score)], marker="x", s=200, c="green")
print("Center ["+str(lasthold[0][np.argmax(keep_score)])+","+str(lasthold[1][np.argmax(keep_score)])+"]")


# In[ ]:




