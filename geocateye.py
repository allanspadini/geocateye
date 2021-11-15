import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from obspy.io.segy.segy import _read_su, _read_segy 
from obspy.io.seg2.seg2 import _read_seg2

#Function to plot seismic data with wiggle traces
def wigb(data, title='Dado', xlabel='Traces', ylabel='Time (ms)', filename='image.png',
    dt=1,fill=True,offsets=False,min_offset=1, max_offset=50,doffset=1,
    d1=8,d2=10,sf=False,amx=1):
    """
    Function to plot seismic data
    Input:
        data: dataframe with seismic data, each column is a trace
        title: title of the plot
        xlabel: label of the x axis
        ylabel: label of the y axis
        filename: name of the file to save the plot
        dt: time interval between two samples
        fill: if True, fill the area between zero and the positive part of the traces
        offsets: if True, plot the offsets range instead of the traces range
        min_offset: minimum offset in range
        max_offset: maximum offset in range
        doffset: offset interval
        d1: dimension of the plot in the x axis
        d2: dimension of the plot in the y axis
        sf: if True, save the plot in a file
        amx: normalization factor of the traces


    """
    ntr = data.shape[1]
    ns = data.shape[0]

    if offsets:
        ntr=max_offset

    t_axis= np.linspace(0,(ns-1)*dt,ns)
    fig, ax = plt.subplots(figsize=(d1,d2))
    #plt.yticks(ticks=np.arange(0,ns-1,20),labels=np.arange(0,(ns-1)*dt,20*dt))
    ax.set_ylim(ns*dt,0)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    
    for tr in np.arange(min_offset-1,ntr,doffset):
        x = np.divide(data[:,tr],amx)+tr+1
        ax.plot(x,t_axis,'k-')
        if fill:
            ax.fill_betweenx(t_axis,tr+1,x,where=(x>tr+1),color='k')
    st.pyplot(fig=fig)
    if sf:
        plt.savefig(filename)
    plt.show()
    plt.close() 

#Function to plot seismic data as image
def seis_image(data, title='Data', xlabel='Traces', ylabel='Time (ms)', filename='image.png',
    dt=1,offsets=False,min_offset=1, max_offset=50,doffset=1,
    d1=8,d2=10,sf=False):
    
    """
    Function to plot seismic data as image
    Input:
        data: dataframe with seismic data, each column is a trace
        title: title of the plot
        xlabel: label of the x axis
        ylabel: label of the y axis
        filename: name of the file to save the plot
        dt: time interval between two samples
        fill: if True, fill the area between zero and the positive part of the traces
        offsets: if True, plot the offsets range instead of the traces range
        min_offset: minimum offset in range
        max_offset: maximum offset in range
        doffset: offset interval
        d1: dimension of the plot in the x axis
        d2: dimension of the plot in the y axis
        sf: if True, save the plot in a file
        amx: normalization factor of the traces


    """

    ntr = data.shape[1]
    ns = data.shape[0]
    fig, ax = plt.subplots(figsize=(d1,d2))
    
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    
    #plt.yticks(ticks=np.arange(0,ns-1,20),labels=np.arange(0,(ns-1)*dt,20*dt))
    plt.imshow(data,cmap='RdBu',aspect='auto')
    st.pyplot(fig=fig)
    if sf:
        plt.savefig(filename)
    plt.show()
    plt.close()

def read_su(file_name):

    """
    Reads a SU file and returns a list of traces.
    """

    stream = _read_su(file_name)
    ns = len(stream.traces[0].data)
    ntraces = len(stream.traces)

    shot_gather = np.ndarray([ns,ntraces])
    
    i = 0 
    for t in stream.traces:
        shot_gather[:,i]= t.data
        i += 1
    return shot_gather

def read_seg2(file_name):

    """
    Reads a SEG2 (.dat) file and returns a list of traces.
    """

    stream = _read_seg2(file_name)
    ns = len(stream.traces[0].data)
    ntraces = len(stream.traces)

    shot_gather = np.ndarray([ns,ntraces])
    
    i = 0 
    for t in stream.traces:
        shot_gather[:,i]= t.data
        i += 1
    return shot_gather


def read_segy(file_name):

    """
    Reads a SEGY file and returns a list of traces.
    """

    stream = _read_segy(file_name)
    ns = len(stream.traces[0].data)
    ntraces = len(stream.traces)

    shot_gather = np.ndarray([ns,ntraces])
    
    i = 0 
    for t in stream.traces:
        shot_gather[:,i]= t.data
        i += 1
    return shot_gather


        
"""

# Geo Cat Eye
Drag and drop your seismic data to visualize it.
"""


uploaded_file = st.file_uploader("Upload Files",type=['su','dat','sgy','rd3'])



if uploaded_file is not None:
    word = uploaded_file.name
    filetype = word.partition('.')[2]
    st.markdown(filetype)
    if filetype == 'su':
        dado = read_su(uploaded_file)
    elif filetype == 'dat':
        dado = read_seg2(uploaded_file)
    elif filetype == 'sgy':
        dado = read_segy(uploaded_file)


    col1, col2 = st.columns(2)
    option = col1.selectbox(
        'Select the desired plot type',
        ['Wiggle','Image'])

    
    title = col2.text_input("Plot title", 'Data')
    xlabel = col1.text_input("Xlabel", 'Traces')
    if option == 'Wiggle':
        ylabel = col2.text_input("Ylabel", 'Time (ms)')
    elif option == 'Image':
        ylabel = col2.text_input("Ylabel", 'Samples')


    dt = st.number_input("Time interval (dt)", 0.100,format="%.3f")
    d1 = col1.number_input("Dimension 1 of the figure", 8)
    d2 = col2.number_input("Dimension 2 of the figure", 10)
    if option == 'Wiggle':
        wigb(dado,title=title,xlabel=xlabel,ylabel=ylabel,dt=dt,d1=d1,d2=d2)
    
    elif option == 'Image':
        seis_image(dado,title=title,xlabel=xlabel,ylabel=ylabel,dt=dt,d1=d1,d2=d2)

   



