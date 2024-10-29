# RGBVIZ

Visualize 3D data cubes with 2D color images. The third dimension is visualized by mixing different colors together based on the intensity of the values within the third dimension. The example pictures hopefully explain the concept. 

<code>
import rgb_balance as rb
import numpy as n
I = n.random.randn(100*100*100,dtype=n.float32)
I.shape = (100,100,100)
Irgb=rb.rgb_image(I)
plt.show()
</code>



<img width="1475" alt="Screenshot 2024-10-29 at 09 34 06" src="https://github.com/user-attachments/assets/2f73b7a9-4c01-4a37-a257-9a42a99b8401">

<img width="1469" alt="Screenshot 2024-10-29 at 09 34 25" src="https://github.com/user-attachments/assets/d1c83ccf-c363-4244-966c-fef7e353fa7c">
