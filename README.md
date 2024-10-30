# RGBVIZ

Visualize 3D data cubes with 2D color images. The third dimension is visualized by mixing different colors together based on the intensity of the values within the third dimension.

Example code in __main__ of:
```
# create a 3d data cube of noise
n.random.seed(42)
I = n.random.randn(100*100*100)
I.shape=(100,100,100)
# fft 3d
I2 = n.fft.fftn(I)
# frequency 
freq=n.fft.fftfreq(100)
f1,f2,f3=n.meshgrid(freq,freq,freq)
# colored noise with k**(5/3)
I=n.abs(n.real(n.fft.ifftn(I2*(1e-2+n.sqrt(f1**2+f2**2+f3**2))**(-5/3.0))))
# create color representation and show it
rgb_image(I)
plt.show()
```

This should give you a visualization of a simulation of a turbulent scalar quantity:

<img width="575" alt="Screenshot 2024-10-30 at 10 03 03" src="https://github.com/user-attachments/assets/a34d91d7-ca24-4b2c-9f5c-023e2afe54d7">

Other examples:

<img width="1475" alt="Screenshot 2024-10-29 at 09 34 06" src="https://github.com/user-attachments/assets/2f73b7a9-4c01-4a37-a257-9a42a99b8401">

<img width="1469" alt="Screenshot 2024-10-29 at 09 34 25" src="https://github.com/user-attachments/assets/d1c83ccf-c363-4244-966c-fef7e353fa7c">
