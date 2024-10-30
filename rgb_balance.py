import numpy as n
import h5py 
import matplotlib.pyplot as plt
import matplotlib

def lognormalize(I):
    I2=n.log10(I)
    idx=n.where(I!=0)
    idx0=n.where(I==0)
    low,high=n.percentile(I2[idx],[1,99])
   
    I2[I2<low]=low
    I2[I2>high]=high
    I2[idx]=(I2[idx]-low)/(high-low)
    I2[idx0]=0
    return(I2)

def rgb_image(A3,
              ax0=[0,1],
              ax0label="par 1",
              ax1=[0,1],
              ax1label="par 2",              
              cax=[0,1],
              peak_fraction=1,  # 1 = all 0 = only maximum
              cblabel="par 3",
              cmap=matplotlib.colormaps["gist_rainbow"],
              gain=1.0,
              maxv=None,
              log=True,
              plot=True
            ):
    """
    return float32 rgb image with values between 0..1 on each of the rgb channels 
    representing the spectrum of values on the third dimension at each pixel of the image
    the idea is that each value of the thrid dimension is a color on the rainbow
    light of each color is mixed together corresponding to the value of the function in the 
    third dimension. It doesn't preserve any sort of linear perception of the distribution, but
    it allows you to quickly see what is where.
    logarithmic intensities supported only currently.
    """
    # x,y 0,1
    # color 2
#    MFm=n.max(MF,axis=marginalize)
#    print(MFm.shape)
    import matplotlib.colors as mc
    I=n.zeros([A3.shape[0],A3.shape[1],3],dtype=n.float32)

    # use this as the normalization constant for all histogram counts
    if maxv == None:
        maxv=n.max(A3)

    for i in range(A3.shape[0]):
        print("%d/%d"%(i,A3.shape[0]))
        for j in range(A3.shape[1]):
            # extract distribution for pixel i,j of histogram
            dist=A3[i,j,:]
            # linear values along third axis
            hv=n.arange(len(dist))/len(dist)
            # normalize histogram value 
            vv=dist/maxv

            # sort by value in decreasing order
            sort_idx=n.argsort(vv)[::-1]
            # select peak_fraction of the largest histogram bins
            # 1 = use everything 0 = use only peak bin
            i1=n.min([int(len(vv)*peak_fraction),len(vv)])
            # we have to select at least one bin
            if i1==0:
                i1=1
            
            # peak values
            sort_idx=sort_idx[0:i1]
            vvv=vv[sort_idx]

            # use a colormap to generate rgb color values for each histogram bin
            # scale intensity by histogram of each bin
            B=cmap(hv[sort_idx])[:,0:3]*vvv[:,None]

            # sum rgb values together to get a pixel color
            I[i,j,:]=n.sum(B,axis=0)

    # logarithmic or linear scaling
    if log:
        I=lognormalize(I)

    else:
        I=I/n.max(I)

    # plot or no plot
    if plot:
        plt.imshow(I[::-1,:],aspect="auto",extent=[ax0[0],ax0[1],ax1[0],ax1[1]])
        plt.xlabel(ax0label)
        plt.ylabel(ax1label)    
        plt.scatter([-1,-1],[-1,-1],c=[cax[0],cax[1]],cmap=cmap)
        cb=plt.colorbar()
        cb.set_label(cblabel)
        plt.xlim(ax0)
        plt.ylim(ax1)
    return(I)

if __name__ == "__main__":

    n.random.seed(42)
    I = n.random.randn(100*100*100)
    I.shape=(100,100,100)
    I2 = n.fft.fftn(I)
    freq=n.fft.fftfreq(100)
    f1,f2,f3=n.meshgrid(freq,freq,freq)
    # colored noise with k**(5/3)
    I=n.abs(n.real(n.fft.ifftn(I2*(1e-2+n.sqrt(f1**2+f2**2+f3**2))**(-5/3.0))))
#    print(n.min(I))
 #   print(n.max(I))
  #  exit(0)
#    plt.imshow(I[:,:,0])
 #   plt.show()
#    exit(0)
    rgb_image(I,peak_fraction=1.0)
    plt.show()
#    h=h5py.File("data/rgb.h5","r")
 #   I=h["I"][()]

  #  I2=lognormalize(I)
   # plt.style.use('dark_background')


    #plt.imshow(I2[::-1,:],aspect="auto")
    #plt.show()

