# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 15:42:04 2020

@author: Dell
"""

import numpy as np
import math
import random 
from functools import reduce
import operator
  




def HMA(L, R, *args):
            
    varargin = args
    nargin = 2 + len(varargin)
    
    nums = dict()
    L = np.array(L, dtype=float)
    R = np.array(R, dtype=float)
    nums['OrgLength']=L.shape[0]
    
    
    #remove incomplete data
    for i in range(len(L)):
         if np.isnan(L[i]) or np.isnan(R[i]) :
              L =  np.delete(L,i)
              R =  np.delete(R,i)
     
    
    
    #Bad data processing, see Equation (1) in paper
    for i in range(L.shape[0]-1,-1,-1):
        if L[i]<0.0 or L[i]>10.0 or R[i]<0.0 or R[i]>10.0 or R[i]<=L[i] or R[i]-L[i]>=10.0:
            L = np.delete(L,i)
            R = np.delete(R,i)
    
    nums['BDLength']=L.shape[0]
    
    
    
    #Outlier processing, see Equation (2) in paper
    intLeng = R-L
    left = sorted(L)
    right = sorted(R)
    leng = sorted(intLeng)
    
    n = L.shape[0]

    NN1 = math.floor(n * 0.25)
    NN2 = math.floor(n * 0.75)
    
    #Compute Q(0.25), Q(0.75) and IQR for left-ends
    QL25 = (1.0-np.remainder(0.25*n,1)) * left[NN1-1] + (np.remainder(0.25*n,1)) * left[NN1]
    QL75 = (1.0-np.remainder(0.75*n,1)) * left[NN2-1] + (np.remainder(0.75*n,1)) * left[NN2]
    LIQR = QL75 - QL25

    
    
    #Compute Q(0.25), Q(0.75) and IQR for right-ends.
    QR25 = (1.0-np.remainder(0.25*n,1)) * right[NN1-1] + (np.remainder(0.25*n,1)) * right[NN1]
    QR75 = (1.0-np.remainder(0.75*n,1)) * right[NN2-1] + (np.remainder(0.75*n,1)) * right[NN2]
    RIQR = QR75 - QR25

    
    
    #outlier processing for L and R
    for i in range(n-1,-1,-1):
        if (L[i]<(QL25-1.5*LIQR)) or (L[i]>(QL75+1.5*LIQR)) or (R[i]<(QR25-1.5*RIQR)) or (R[i]>(QR75+1.5*RIQR)):
            L = np.delete(L,i)
            R = np.delete(R,i)
            intLeng = np.delete(intLeng,i)
    

    
    
    nums['OLRLength']=L.shape[0]        
    
    n1 = L.shape[0]
    
    #Compute Q(0.25), Q(0.75) and IQR for interval length.
    NN1 = math.floor(n1 * 0.25);
    NN2 = math.floor(n1 * 0.75);
    QLeng25 = (1.0-np.remainder(0.25*n1,1)) * leng[NN1-1] + (np.remainder(0.25*n1,1)) * leng[NN1]
    QLeng75 = (1.0-np.remainder(0.75*n1,1)) * leng[NN2-1] + (np.remainder(0.75*n1,1)) * leng[NN2]
    lengIQR = QLeng75 - QLeng25
    
    #outlier processing for interval length
    
    for i in range(n1-1,-1,-1):
        if (intLeng[i]<(QLeng25-1.5*lengIQR)) or (intLeng[i]>(QLeng75+1.5*lengIQR)):
            L = np.delete(L,i)
            R = np.delete(R,i)
            intLeng = np.delete(intLeng,i)
    
    nums['OLIntervalLength']=L.shape[0]        
    
    
    
    n1 = L.shape[0]
    
    #Tolerance limit processing, see Equation (3) in paper
    
    meanL = np.mean(L)
    stdL  = np.std(L,ddof=1)
    meanR = np.mean(R) 
    stdR  = np.std(R,ddof=1)
 
    
    K=np.array([32.019,32.019,8.380,5.369,4.275,3.712,3.369,3.136,2.967,2.839,2.737,2.655,2.587,2.529,2.48,2.437,2.4,2.366,2.337,2.31,2.31,2.31,2.31,2.31,2.208],dtype=float)
    
    k=K[min(n1-1,24)]
    
    
    
    for i in range(n1-1,-1,-1):
         if (L[i]<(meanL-k*stdL)) or (L[i]>(meanL + k*stdL)) or (R[i]<(meanR-k*stdR)) or (R[i]>(meanR + k*stdR)):
              L = np.delete(L,i)
              R = np.delete(R,i)
              intLeng = np.delete(intLeng,i)
              
    
    
    
    n1 = L.shape[0]
    nums['TLRLength']=n1
    
    #Tolerance limit processing for interval length
    meanLeng = np.mean(intLeng)
    stdLeng  = np.std(intLeng,ddof=1)
    k=float(min([K[min(n1-1,24)],meanLeng/float(stdLeng+0.00001),(10.0-meanLeng)/float(stdLeng+0.00001)]))
    
    for i in range(n1-1,-1,-1):
         if (intLeng[i]<(meanLeng-k*stdLeng)) or (intLeng[i]>(meanLeng+k*stdLeng)):
              L = np.delete(L,i)
              R = np.delete(R,i)
              intLeng = np.delete(intLeng,i)
    
    
    
    n1 = L.shape[0]
    nums['TIntervalLength']=n1
    
    #Reasonable interval processing, see Equation (4)-(6) in paper
    
  
    
    meanRL = np.mean(L)
    stdRL  = np.std(L,ddof=1)
    meanRR = np.mean(R) 
    stdRR  = np.std(R,ddof=1)
     

    #Determine sigma*, see formula (5) in paper
    if stdRL==stdRR:
         barrier = (meanRL + meanRR)/2.0
    elif stdRL==0.0:
         barrier = meanRL+0.01
    elif stdRR==0.0:
         barrier = meanRR-0.01
    else:
         barrier1 =((meanRR*stdRL**2-meanRL*stdRR**2) + stdRL*stdRR*np.sqrt((meanRL-meanRR)**2+2*(stdRL**2-stdRR**2)*np.log(stdRL/stdRR)))/(stdRL**2-stdRR**2)
         barrier2 =((meanRR*stdRL**2-meanRL*stdRR**2) - stdRL*stdRR*np.sqrt((meanRL-meanRR)**2+2*(stdRL**2-stdRR**2)*np.log(stdRL/stdRR)))/(stdRL**2-stdRR**2)
         if  barrier1>=meanRL and barrier1<=meanRR:
              barrier = barrier1
         else:
              barrier = barrier2
     
   
    #Reasonable interval processing
    for i in range(n1-1,-1,-1):
         if (L[i] >= barrier) or (R[i] <= barrier) or (L[i]<2.0*meanRL-barrier) or (R[i]>2.0*meanRR-barrier):
              L = np.delete(L,i)
              R = np.delete(R,i)
              intLeng = np.delete(intLeng,i)
    
    
    
     
    n = L.shape[0]
    nums['RIPLength']=n
    
    meanL = np.mean(L)
    stdL = np.std(L, ddof=1)
    meanR = np.mean(R)
    stdR = np.std(R, ddof=1)
    
    
    
    #Admissible region determination
    K=np.array([32.019,32.019,8.380,5.369,4.275,3.712,3.369,3.136,2.967,2.839,2.737,2.655,2.587,2.529,2.48,2.437,2.4,2.366,2.337,2.31,2.31,2.31,2.31,2.31,2.208],dtype=float)
    k=K[min(n1-1,24)]
    
   
    #n = L.shape[0]
    
    # Allow user to type the input shape: 1 left-shoulder, 2: interior and 3: right-shoulder
    if nargin < 3:
         if (meanL-k*stdL) <= 0.0:
              shape = 1  #left
         elif (meanR + k*stdR) >= 10.0:
              shape = 3  #right
         else:
              shape = 2  #interior
    elif nargin == 3:
         shape = int(args[0])    
    
    
    #Establish nature of FOU, see Equation (19) in paper
    if shape == 1:
         #left shoulder
         switchPoint = min(R)
         nums['LeftShoulderLength']=R.shape[0]
         
         
         
         if np.sum(R-switchPoint) == 0.0:
              UMF =[0.0,  0.0, float(switchPoint), float(switchPoint)]
              LMF = [0.0, 0.0, float(switchPoint), float(switchPoint), 1.0]  
              shape = 1
              MF = reduce(operator.concat, [UMF,LMF])
              return MF, nums
         
         #side parts
         c = switchPoint
         subsetRightLength = np.array(R - c,dtype=float)
         
         #remove the empty intervals
         subsetRightLength = subsetRightLength[subsetRightLength>0.0]
         
            
         #calculate the mean and sd of the lengths
         lengthMean = np.mean(subsetRightLength)
         lengthSD   = np.std(subsetRightLength,ddof=1)
          
         #map the center of the std and upper mean
         d = np.nanmin([c + 3.0 * np.sqrt(2.0) * lengthSD, 10.0])
         i = np.nanmin([6.0 * (c + lengthMean) - 4.0 * c - d, 10.0])
          
         bl = max(min(d, i), c)
         br = max(d, i)
          
         UMF = [0.0, 0.0, float(switchPoint), float(br)]
         LMF = [0.0, 0.0, float(switchPoint), float(bl), 1.0]
          
    elif shape == 3:
         #right shoulder
         switchPoint = max(L)
         nums['RightShoulderLength']=L.shape[0]
            
        
            
         if (np.sum(L-switchPoint) == 0.0):
              UMF =[float(switchPoint), float(switchPoint),10.0,10.0]
              LMF = [float(switchPoint), float(switchPoint),10.0,10.0, 1.0]  
              shape = 3
              MF = reduce(operator.concat, [UMF,LMF])
              return MF, nums
            
         #side parts
         c = switchPoint;
         subsetRightLength = np.array(c - L,dtype=float)
         
         #remove the empty intervals
         subsetRightLength = subsetRightLength[subsetRightLength>0.0]
          
         #calculate the mean and sd of the lengths
         lengthMean = np.mean(subsetRightLength)
         lengthSD   = np.std(subsetRightLength,ddof=1)
         
         
         #map the center of the std and lower mean
         a = np.nanmax([0.0, c - 3.0 * np.sqrt(2.0) * lengthSD])
         e = np.nanmax([6.0 * (c - lengthMean) - 4.0 * c - a, 0.0])
         
         al = min(a, e)
         ar = max(e, a)
         
         UMF = [float(al), float(switchPoint), 10.0, 10.0]
         LMF = [float(ar), float(switchPoint), 10.0, 10.0, 1.0]
    else:
         overlapLeft = max(L)
         overlapRight = min(R)
         nums['InteriorRightShoulderLength'] = R.shape[0]  
         nums['InteriorLeftShoulderLength']  = L.shape[0]  
         
         
         
         
         
         #side parts
         c = overlapLeft
         subsetRightLength = np.array(c - L,dtype=float)
         
         #remove the empty intervals
         subsetRightLength = subsetRightLength[subsetRightLength>0.0]
             
               
         #calculate the mean and sd of the lengths
         lengthMean = np.mean(subsetRightLength)
         lengthSD   = np.std(subsetRightLength,ddof=1)
         
         
         
         #map the center of the std and lower mean
         a = np.nanmax([0.0, c - 3.0 * np.sqrt(2.0) * lengthSD]);
         e = np.nanmax([0.0, 6.0 * (c - lengthMean) - 4.0 * c - a])
         
         al = min(a, e)
         ar = min(max(e, a), c)
         
         c = overlapRight
         
         subsetRightLength = np.array(R - c,dtype=float)
         
         
          
         #remove the empty intervals
         subsetRightLength = subsetRightLength[subsetRightLength>0.0]
          
        
         #calculate the mean and sd of the lengths
         lengthMean = np.mean(subsetRightLength)
         lengthSD   = np.std(subsetRightLength,ddof=1)
         
         #map the center of the std and upper mean
         d = np.nanmin([c + 3.0 * np.sqrt(2.0) * lengthSD, 10.0])
         i = np.nanmin([6.0 * (c + lengthMean) - 4.0 * c - d, 10.0])
         
         
         bl = max(min(d, i), c)
         br = max(d, i)
         
         UMF = [float(al), float(overlapLeft), float(overlapRight), float(br)]
         LMF = [float(ar), float(overlapLeft), float(overlapRight), float(bl), 1.0]
         
     
    MF = reduce(operator.concat, [UMF,LMF])
    
    return MF, nums