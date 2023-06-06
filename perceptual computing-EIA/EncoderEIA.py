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

def EIA(L,R):
       
    nums = dict()
    L = np.array(L, dtype=float)
    R = np.array(R, dtype=float)
    nums['OrgLength']=L.shape[0]

    
    
    #remove incomplete data
    for i in range(L.shape[0]-1,-1,-1):
         if np.isnan(L[i]) or np.isnan(R[i]):
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
    QLeng25 = (1-np.remainder(0.25*n1,1)) * leng[NN1-1] + (np.remainder(0.25*n1,1)) * leng[NN1]
    QLeng75 = (1-np.remainder(0.75*n1,1)) * leng[NN2-1] + (np.remainder(0.75*n1,1)) * leng[NN2]
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
    
    
    
    for i in range(L.shape[0]-1,-1,-1):
         if (L[i]<(meanL-k*stdL)) or (L[i]>(meanL + k*stdL)) or (R[i]<(meanR-k*stdR)) or (R[i]>(meanR + k*stdR)):
              L = np.delete(L,i)
              R = np.delete(R,i)
              intLeng = np.delete(intLeng,i)
              
    
    n1 = L.shape[0]
    nums['TLRLength']=n1
    
    
    #Tolerance limit processing for interval length
    meanLeng = np.mean(intLeng)
    stdLeng  = np.std(intLeng,ddof=1)
    k=float(min([K[min(L.shape[0],24)],meanLeng/float(stdLeng+0.00001),(10.0-meanLeng)/float(stdLeng+0.00001)]))
    
    for i in range(L.shape[0]-1,-1,-1):
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
    for i in range(L.shape[0]-1,-1,-1):
         if (L[i] >= barrier) or (R[i] <= barrier) or (L[i]<2.0*meanRL-barrier) or (R[i]>2.0*meanRR-barrier):
              L = np.delete(L,i)
              R = np.delete(R,i)
              intLeng = np.delete(intLeng,i)
    
    
    
    nums['RIPLength']=L.shape[0]
    
    n = L.shape[0]
    #Admissible region determination
    tTable=np.array([6.314, 2.920, 2.353, 2.132, 2.015, 1.943, 1.895, 1.860, 1.833, 1.812, 1.796, 1.782, 1.771, 1.761, 1.753, 1.746, 1.740, 1.734, 1.729, 1.725, 1.721, 1.717, 1.714, 1.711, 1.708, 1.706, 1.703, 1.701, 1.699, 1.697, 1.684],dtype=float) # alpha = 0.05;
    tAlpha=float(tTable[min(n-1,30)])
    meanL = np.mean(L)
    meanR = np.mean(R)
    
        
    newRIPLA = L
    newRIPRA = R
    
    C = newRIPRA - 5.831*newRIPLA
    D = newRIPRA - 0.171*newRIPLA - 8.29
    
    
    
    shift1 = float(tAlpha * np.std(C,ddof=1)/float(np.sqrt(n)))
    shift2 = float(tAlpha * np.std(D,ddof=1)/float(np.sqrt(n)))
    
    if np.isnan(shift1):
         shift1 = 0.0
         
    if np.isnan(shift2):
         shift2 = 0.0
    
    
    
    FSL = np.zeros(L.shape[0]).astype(float)
    FSR = np.zeros(R.shape[0]).astype(float)
    
    #Establish nature of FOU, see Equation (19) in paper
    if (meanR>(5.831*meanL-shift1)) and (meanR<(0.171*meanL+8.29-shift2)):
         for i in range(L.shape[0]-1,-1,-1):
              #left shoulder embedded T1 FS
              FSL[i] = 0.5*(L[i]+R[i]) - (R[i]-L[i])/np.sqrt(6.0)
              FSR[i] = 0.5*(L[i]+R[i]) + np.sqrt(6.0)*(R[i]-L[i])/3.0
              #Delete inadmissible T1 FSs
              if FSL[i]<0.0 or FSR[i]>10.0:
                   FSL= np.delete(FSL,i)
                   FSR= np.delete(FSR,i)                   
         
         # Compute the mathematical model for FOU(A~)
         UMF =[0.0,  0.0, float(np.max(FSL)), float(np.max(FSR))]
         LMF = [0.0, 0.0, float(np.min(FSL)), float(np.min(FSR)), 1.0]
    elif (meanR<(5.831*meanL-shift1)) and (meanR>(0.171*meanL+8.29-shift2)):
          for i in range(L.shape[0]-1,-1,-1):
               # right shoulder embedded T1 FS
               FSL[i] = 0.5*(L[i]+R[i]) - (np.sqrt(6.0)*(R[i]-L[i]))/3.0
               FSR[i] = 0.5*(L[i]+R[i]) + (R[i]-L[i])/np.sqrt(6.0)
               #Delete inadmissible T1 FSs
               if FSL[i]<0.0 or FSR[i]>10.0:
                   FSL= np.delete(FSL,i)
                   FSR= np.delete(FSR,i)                    

          
          #Compute the mathematical model for FOU(A~)
          UMF =[float(np.min(FSL)), float(np.min(FSR)), 10.0, 10.0]
          LMF = [float(np.max(FSL)), float(np.max(FSR)), 10.0, 10.0, 1.0]
    else:
          
          
          for i in range(L.shape[0]-1,-1,-1):
               
               #internal embedded T1 FS
               FSL[i] = 0.5*float(L[i]+R[i]) - np.sqrt(2.0)*0.5*float(R[i]-L[i])
               FSR[i] = 0.5*float(L[i]+R[i]) + np.sqrt(2.0)*0.5*float(R[i]-L[i])
               
               #Delete inadmissible T1 FSs
               if FSL[i]<0.0 or FSR[i]>10.0:
                   FSL= np.delete(FSL,i)
                   FSR= np.delete(FSR,i)
          
          
          
          FSC=(FSL+FSR)/2.0
          #Compute the mathematical model for FOU(A~)
          L1 = float(np.min(FSL))
          L2 = float(np.max(FSL))
          R1 = float(np.min(FSR))
          R2 = float(np.max(FSR))
          C1 = float(np.min(FSC))
          C2 = float(np.max(FSC))
          
          n = len(FSL)
          hs = np.zeros(n*n).astype(float)
          for i in range(n):
               hs[i*n+np.arange(n)]=(FSR[i]-FSL)/(FSR[i]-FSL+FSC-FSC[i])   
               
          h,index = float(min(hs)),np.argmin(hs)
          i = float(np.ceil(index/n))
          j = int(index - i*n)
          p = float(FSL[j] + h * (FSC[j]-FSL[j]))
          

          UMF =[L1, C1, C2, R2]
          LMF = [L2, p, p, R1, h]

    nums['FLength']=FSL.shape[0]

        
    MF = reduce(operator.concat, [UMF,LMF])
    
    return MF, nums



