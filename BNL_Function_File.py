#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Functions


# In[ ]:


def plotter(dim): #creates plot
    plt.figure(100, figsize=(dim, dim))
    plt.imshow(np.log10(img2+3), cmap="gist_stern")
    cbar=plt.colorbar(label="scalarized point brightness")
    
    

#this method is just the distance formula. You input x and y which is one coordinate and then a and which is the second.
def euclidean_distance(x,y,a,b):
    d=((a-x)**2+(b-y)**2)**0.5
    return d



#this method takes an array and if values are close together it "combines them". 
#It groups values that are less than 10 apart and then finds the average of these clusters. This forms a smaller array, 
#comprised of the averages. This array of averages is then averaged. This value is outputted. 
#METHOD USED FOR LIST OF INDICIES NOT INTENSITY VALUES
def cluster_avg(val_list):
    hold_avgs=np.array([])
    hold_indices=np.array([])
    lastindex=0
    for j in range(len(val_list)-1):#we don't want to go out of bounds. so keep the j+1 from going too far.
        if(val_list[j+1]>(val_list[j]+10)): #The +10 is just a number I have to be the amount above to split. So if values differ by 10, the array splits between these indices.
            for k in range(lastindex, (j+1)): #go from previous cluster's last index to the next one that starts a new cluster.
                hold_indices=np.append(hold_indices, val_list[k]) #put the cluster's indices in an array
            hold_avgs=np.append(hold_avgs, np.nanmean(hold_indices)) #put the mean of the cluster's indices in an array
            hold_indices=np.array([]) #empty the array that holds the indices
            lastindex=j+1 # move the last index up so we will not look at the same cluster again in our for loop
    
        elif(val_list[j+1]==val_list[-1]): #at the end of the array
            for k in range(lastindex, (j+1)): #go from previous cluster's last index to the next one that starts a new cluster. This doesn't include the final array element
                hold_indices=np.append(hold_indices, val_list[k]) #put the cluster's indices in an array
            hold_indices=np.append(hold_indices, val_list[-1]) #include the final element of save
            hold_avgs=np.append(hold_avgs, np.nanmean(hold_indices)) #put the mean of the cluster's indices in an array
            hold_indices=np.array([]) #empty the array that holds the indices
            lastindex=j+1 # move the last index up so we will not look at the same cluster again in our for loop
    avg_of_clusters=np.nanmean(hold_avgs)  #the average of the clusters we got in the row or column above the threshold
    
    return(avg_of_clusters)



#you input a list and the mode of the list is found
def mode_finder(list_input):
    vals,counts = np.unique(list_input, return_counts=True)
    mode = np.argmax(counts)
    true_mode=vals[mode]
    
    return(true_mode)



#This array takes the maximum value in a row. It then multiplies this value by a threshold 
#(between 0 and 1 noninclusive) to get a lowerbound
#It goes through the array, finding the indicies corresponding to values above this lowerbound. These indicies are put into 
#another array. The method cluster_avg is used on this array. The cluster_avg output is put into a storing array.
#This whole process is repeated for each row. And each output is appended to the storing array. 
#This storing array is the output of this method.
def one_dim_search_rows(array_input,threshold_value):
    hold_avg=np.array([])
    holding_array=np.array([])
    for a in range(len(array_input)):
        valmax=np.amax(array_input[a]) #get the actual max value in the array
        lowerbound=threshold_value*valmax #we want to see where values above this are. The high intensity values. 
        for i in range(len(array_input[a])): #go through one row at a time
            if img2[a][i]>lowerbound:
                holding_array=np.append(holding_array,i) #get indices of higher values in an array
        
        hold_avg=np.append(hold_avg,cluster_avg(holding_array))
        holding_array=np.array([])
        
    return(hold_avg)



#This is the exact same as the method above, but for columns. It was easier to make separate methods because 
#rows in general are accesed with array[z] while columns are array[:,z]
def one_dim_search_cols(array_input,threshold_value):
    hold_avg=np.array([])
    holding_array=np.array([])
    for b in range(len(array_input[0])): #go through every column and note that img2[0] is the size of the number of columns.
        valmax=np.amax(array_input[:,b]) #get the actual max value in that column. 
        lowerbound=threshold_value*valmax #we want to see where values above this are. The high intensity values. I chose a 15% threshold.
        for j in range(len(img2[:,b])): #go through each index of the column
            if img2[:,b][j]>lowerbound: #if the element is larger than our bound
                holding_array=np.append(holding_array,j) #get the indicies of the larger elements and add them all to a list
                
        hold_avg=np.append(hold_avg,cluster_avg(holding_array))
        holding_array=np.array([])
                
    return(hold_avg)



#This method uses the distace formula to see which point is the farthest from a certain point.
#Two arrays are inputted. The first has x-coordinates and the second has y-coordinates. The corresponding indices form a point.
#These points are compared to a third array, which is actually just length 2 (this array is just a single x and y pair).
#which ever of the x and y coordinates are closest to that single point are the coordinates kept.
def closest_point_index(input_array1, input_array2,compare_point):
    hold_index=0
    lowest_dist=euclidean_distance(input_array1[0],input_array2[0],compare_point[0],compare_point[1])
    for i in range(len(input_array1)):
        c=euclidean_distance(input_array1[i],input_array2[i],compare_point[0],compare_point[1])
        if c<lowest_dist:
            hold_index=i
    return(hold_index)



#this method just removes the repeated indices from the x-coordinate and y-coordinate arrays, thus removing repeated points
def two_dim_remove_repeat(val_list_x,val_list_y): 
    result =[] 
    for i in val_list_x: 
        if i not in result: 
            result.append(i)
    
    result2=[]
    for i in val_list_y: 
        if i not in result2: 
            result2.append(i)

    return(result+result2)



#This method creates the circle and makes sure it is in the bounds of the image. If not, the intensity is set to euler's number.
def circle_point(main_array,center_x,center_y,radius,angle): 
    point_x=round(center_x+radius*np.cos(angle))
    point_y=round(center_y+radius*np.sin(angle))
    if(point_x>0 and point_y>0 and point_x<len(main_array) and point_y<len(main_array[0])):
        #the horizontal and vertical bounds seem to be switched because the first index in a 2D array tells you the row to 
        #access which is technically dealing with the vertical part of the image
        intensity=main_array[point_x][point_y]
        return(intensity)
    else:
        intensity=np.e
        return(intensity)

    

#See if enough of the points have stopped to end the run. Count the values in the array equal to euler's number.
#If this amounts to all of the values in the array, the run is finished
def helperloop(full_list): 
    value=0
    for i in full_list: 
        if i==np.e:
            value+=1
    if (value==len(full_list)-1 or value==len(full_list)): #the second part is for if two points somehow end together
        end_run=True
    else:
        end_run=False
        
    return(end_run)



def win_counter_help(intensity_array): #removes elements that are euler's number
    x=[value for value in intensity_array if value != np.e]
    return x


      
def one_dim_remove_repeat(val_list_x): #remove repeat elements from an array
    result =[] 
    for i in val_list_x: 
        if i not in result: 
            result.append(i)
    return(result)



def quasicount(intensitylist,val): #counts amount of times numbers in an array between 0.8 and 1.2 times away from an 
    occur_amount=0                 #inputted value appear
    for i in intensitylist:        #it's like count method but counts element "close" instead of exactly same
        if (i<val*1.2 and i>val*0.8):
            occur_amount+=1
    return(occur_amount)



#This method gets unique values from an array anduses them to form a "score". This score is how the actual center is determined.
def find_similar_count_and_scale(val_list_x):
    winquantity=0
    win_quantity_scale=np.empty([])
    val_list_x2=val_list_x
    holdlist=one_dim_remove_repeat(val_list_x) #remove repeat elements
    no_e_list=win_counter_help(val_list_x2) #remove euler's number (which there should be only one of)
    for i in holdlist:
        win_quantity_scale=np.append(win_quantity_scale,quasicount(no_e_list,i)) 
        #take all unique elements and get the amount of times they each occur (searching for SIMILAR values)
    for j in win_quantity_scale: #if we just added the occurences we would get the length of the no_e_list array
        if(j!=None): #None can't be passed as a power. This was an issue that stopped the code
            winquantity+=1.01**j       #scale each of these amounts up so that higher occurence numbers mean more, do exponent
    return(winquantity)
     
    
#This method takes a possible center point and then expands 16 points outwards from it (equidistant from the possible center).
def extend_unitcircle_outwards(center_x,center_y): 
    end_run=False
    win_counter=0
    radius=1 
    
    while(end_run==False):    
           
        #point 1 at 0 degrees
        keep1=circle_point(img2,center_x,center_y,radius,0)
        intensity1=keep1
        #point 2 at 30 degrees
        keep2=circle_point(img2,center_x,center_y,radius,np.pi/6)
        intensity2=keep2
        #point 3 at 45 degrees
        keep3=circle_point(img2,center_x,center_y,radius,np.pi/4)
        intensity3=keep3
        #point 4 at 60 degrees
        keep4=circle_point(img2,center_x,center_y,radius,np.pi/3)
        intensity4=keep4 
        #point 5 at 90 degrees
        keep5=circle_point(img2,center_x,center_y,radius,np.pi/2)
        intensity5=keep5
        #point 6 at 120 degrees
        keep6=circle_point(img2,center_x,center_y,radius,2*np.pi/3)
        intensity6=keep6
        #point 7 at 135 degrees
        keep7=circle_point(img2,center_x,center_y,radius,3*np.pi/4)
        intensity7=keep7
        #point 8 at 150 degrees
        keep8=circle_point(img2,center_x,center_y,radius,5*np.pi/6)
        intensity8=keep8
        #point 9 at 180 degrees
        keep9=circle_point(img2,center_x,center_y,radius,np.pi)
        intensity9=keep9
        #point 10 at 210 degrees
        keep10=circle_point(img2,center_x,center_y,radius,7*np.pi/6)
        intensity10=keep10   
        #point 11 at 225 degrees
        keep11=circle_point(img2,center_x,center_y,radius,5*np.pi/4)
        intensity11=keep11
        #point 12 at 240 degrees
        keep12=circle_point(img2,center_x,center_y,radius,4*np.pi/3)
        intensity12=keep12   
        #point 13 at 270 degrees
        keep13=circle_point(img2,center_x,center_y,radius,3*np.pi/2)
        intensity13=keep13   
        #point 14 at 300 degrees
        keep14=circle_point(img2,center_x,center_y,radius,5*np.pi/3)
        intensity14=keep14
        #point 15 at 315 degrees
        keep15=circle_point(img2,center_x,center_y,radius,7*np.pi/4)
        intensity15=keep15  
        #point 16 at 330 degrees
        keep16=circle_point(img2,center_x,center_y,radius,11*np.pi/6)
        intensity16=keep16
            
        
        hold_intensities=np.array([intensity1,intensity2,intensity3,intensity4,intensity5,intensity6,intensity7,intensity8,intensity9,intensity10,intensity11,intensity12,intensity13,intensity14,intensity15,intensity16])
        #Holds all of the intensity values from each of the 16 points that expand outwards
        all_end=np.array([intensity1,intensity2,intensity3,intensity4,intensity5,intensity6,intensity7,intensity8,intensity9,intensity10,intensity11,intensity12,intensity13,intensity14,intensity15,intensity16])
        #Also holds all of the intensity values from each of the 16 points that expand outwards.
        #We need two arrays because each is used and using the same arrays so may change values
        win_counter+=find_similar_count_and_scale(hold_intensities)
        #Scores the 16 points together and adds the score to a running total
        
        #we want to know if 15 of the 16 (or 16 out of 16) points are done running. If so, the method is finished.
        end_run=helperloop(all_end)

        radius+=10 #expand the ring of 16 points outwards to analyze new points.
    
    return win_counter #returns the total combined score of each of the groups of 16 points




#Goes through the array_input rows and gets the indicies of values above the threshold_value.
#The list of indicies is searched for close together indicies, then these are clustered together (through an average).
#All of these clustered index groups are averaged and this average of indicies is put into an array. This is repeated for
#each row, where this value is put into an array. Then the mode of this final array is found.
#Repeat for columns
def repeated_operation_rows(array_input,threshold_value): 
    a=mode_finder(one_dim_search_rows(array_input,threshold_value))
    return a

def repeated_operation_cols(array_input,threshold_value): 
    a=mode_finder(one_dim_search_cols(array_input,threshold_value))
    return a

