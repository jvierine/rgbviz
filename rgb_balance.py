import numpy as n
import h5py 
import matplotlib.pyplot as plt
import matplotlib

def lognormalize(I):

    v=(1/3)*(I[:,:,0]+I[:,:,1]+I[:,:,2])
    I2=n.log10(I)
    idx=n.where(I>0)
    idx0=n.where(I==0)
    low,high=n.percentile(I2[idx],[1,99])
    I2[idx]=(I2[idx]-low)/(high-low)
    I2[idx0]=0
    return(I2)

def rgb_image(A3,
              ax0=[0,1],
              ax0label="",
              ax1=[0,1],
              ax1label="",              
              cax=[0,1],
              peak_fraction=1,  # 1 = all 0 = only maximum
              cblabel="par 3",
              cmap=matplotlib.colormaps["gist_rainbow"],
              gain=1.0,
              maxv=None,
              autogain=True,
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
    if maxv == None:
        maxv=n.max(A3)

    for i in range(A3.shape[0]):
        print("%d/%d"%(i,A3.shape[0]))
        for j in range(A3.shape[1]):
            dist=A3[i,j,:]
            hv=n.arange(len(dist))/len(dist)
  #          sv=n.repeat(1,len(dist))
            vv=dist/maxv
 #           B=n.array([hv,sv,vv])
            sort_idx=n.argsort(vv)[::-1]
            i1=n.min([int(len(vv)*peak_fraction),len(vv)])
            if i1==0:
                i1=1
            sort_idx=sort_idx[0:i1]
            #            B=B[:,sort_idx]

            vvv=vv[sort_idx]
            #vvv[vvv>1]=1


            B=cmap(hv[sort_idx])[:,0:3]*vvv[:,None]
            # color
            I[i,j,:]=n.sum(B,axis=0)


#    ho=h5py.File("rgb.h5","w")
 #   ho["I"]=I
  #  ho.close()


   # if autogain:
    #    I=gain*I/n.max(I)
#    else:
 #       I=gain*I
   # I[I>1]=1
    I=lognormalize(I)
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


    h=h5py.File("data/rgb.h5","r")
    I=h["I"][()]

    I2=lognormalize(I)
    plt.style.use('dark_background')


    plt.imshow(I2[::-1,:],aspect="auto")
    plt.show()

