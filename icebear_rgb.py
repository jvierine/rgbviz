import numpy as n
import matplotlib.pyplot as plt
plt.style.use('dark_background')
import h5py

import matplotlib
import rgb_balance as rb

fs=["data/ib3d_normal_01dB_1000ms_2024_08_12_17_prelate_bakker.h5","data/ib3d_normal_01dB_1000ms_2024_08_12_18_prelate_bakker.h5"]
#fs=["data/ib3d_normal_01dB_1000ms_2024_08_12_17_prelate_bakker.h5"]

max_dop=200
min_dop=-450
dop_step=10
N_dop=int((max_dop-min_dop)/dop_step)

max_range=2100
min_range=1150
range_step=1.5
N_range=int((max_range-min_range)/range_step)

Nk=0
for f in fs:
    h=h5py.File(f,"r")
    Nk+=len(h["data"].keys())
    h.close()
N_time=Nk

A3=n.zeros([N_time,N_range,N_dop],dtype=n.float32)
tv=[]
snrs=[]

mindops=[]
maxdops=[]

ti=0
for f in fs:
    h=h5py.File(f,"r")
    for ki,k in enumerate(h["data"].keys()):
        print("%d/%d"%(ki,N_time))
        tv.append(int(k))
        if "snr_db" in h["data/%s"%(k)].keys(): 
            
            snr=h["data/%s/snr_db"%(k)][()].real
            r=h["data/%s/rf_distance"%(k)][()]
            dop=h["data/%s/doppler_shift"%(k)][()]

            d_idx=n.array(N_dop*(dop-min_dop)/(max_dop-min_dop),dtype=int)
            d_idx[d_idx<0]=0
            d_idx[d_idx>=N_dop]=N_dop-1
            r_idx=n.array(N_range*(r-min_range)/(max_range-min_range),dtype=int)
            r_idx[r_idx<0]=0
            r_idx[r_idx>=N_range]=N_range-1
            A3[ti,r_idx,d_idx]=10**((snr-1)/10)
#            A3[ti,r_idx,d_idx]=snr-1

            print(n.max(snr))
            mindops.append(n.min(dop))
            maxdops.append(n.max(dop))

            snrs.append(10.0**( (n.max(snr)-1)/10 ))
#            snrs.append(n.max(snr)-1)

            ti+=1
            if False:
                plt.pcolormesh(A3[ki,:,:])
                plt.show()
            #print(k)
    h.close()
tv=n.array(tv)
snrs=n.array(snrs)


if False:
    plt.subplot(131)
    plt.hist(snrs,bins=100)
    plt.subplot(132)
    plt.hist(mindops,bins=100)
    plt.subplot(133)
    plt.hist(maxdops,bins=100)
    plt.show()

max_snr=15
min_snr=0

if False:
    A3[A3<min_snr]=min_snr
    A3[A3>max_snr]=max_snr
    A3=A3-min_snr
# SNR+1
#A3=10.0*n.log10(A3+1)

A3=n.moveaxis(A3,[0,1],[1,0])

#A3=10.0*n.log10(A3+1)
plt.figure(figsize=(16,9))
rb.rgb_image(A3[:,:,:],peak_fraction=1,ax1=[min_range,max_range],ax1label="Range (km)",ax0=[n.min(tv),n.max(tv)],ax0label="Unix time (s)",
             cax=[min_dop,max_dop],cblabel="Doppler shift (Hz)")

plt.tight_layout()
plt.show()