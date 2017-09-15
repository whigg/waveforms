# ATM/ICESat-2 Waveform analysis
**Alek Petty**   
**Add other contributors here**

*Python scripts used to analyze waveforms from the ATM and upcoming ICESat-2 mission*


### Scripts

* * atmFuncs.py*     

⋅⋅⋅Experimental ATM waveform functions provided by the ATM team (courtesy M. Studinger).

* * atmWaveform.ipynb*   

⋅⋅⋅iPython Notebook for exploring waveform characterization

All processing in Python 2.7. I have not tested with 3.

Maybe add a list of Python dependencies here? Or even an environment file.

### Data

ILATM1B_20170309_133117.atm6AT6.snippet.h5    
ILATM1B_20170309_133117.atm6AT6.waveformDebug.h5    
ATM_waveform_product_user_manual_v06.pdf    

### DataOutput

Folder for derived data products.

### Figures

Folder for figure outputs.

### Ideas

Look into different waveform classification methods.    

Use Pandas to store and characterize the data.	   		

Look into Dask library for scaling up the processing.    
