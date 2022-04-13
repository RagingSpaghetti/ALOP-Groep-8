import numpy as np
from astropy.io import fits
import glob

biaslist = sorted(glob.glob('r*.fit'))
print('Found,', len(biaslist), ' bias frames')

hdub        = fits.open(biaslist[0]) # just open first image in the list to get dimensions of data
biasim     = hdub[1].data
biascube   = np.zeros( (biasim.shape[0],biasim.shape[1], len(biaslist)), dtype=biasim.dtype) # make a cube so we can take a median along the last axis

print('Shape of bias cube', biascube.shape)

for bias_idx, bias in enumerate(biaslist):
    print('Open ' + bias)
    hdu= fits.open(bias)  
    biascube[:,:,bias_idx] = hdu[1].data
    hdu.close()
 

hdub[1].data = np.nanmedian(biascube, axis=2)  # take median and put back into fits

hdub.writeto('master_bias.fits', overwrite=True) # write the fits to disk
hdub.close()