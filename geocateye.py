import streamlit as st
import spadini as sp

st.set_page_config(page_title = 'GeoCatEye', page_icon = 'favicon.ico')
        
"""

# Geo Cat Eye
Drag and drop your seismic or gpr data to view it.
"""



uploaded_file = st.file_uploader("Upload Files",type=['su','dat','sgy','rd3'])

st.sidebar.title('View options')

st.sidebar.image('ono.png',use_column_width=True)
option = st.sidebar.selectbox(
    'Select the desired plot type',
    ['Wiggle','Image'])

title = st.sidebar.text_input("Plot title", 'Data')
xlabel = st.sidebar.text_input("Xlabel", 'Traces')
ylabel = st.sidebar.text_input("Ylabel", 'Time (ms)')
if option == 'Wiggle':
    amx = st.sidebar.number_input("Amplitude normalization", 1)



dt = st.sidebar.number_input("Time interval (dt)", 0.000100,format="%.4f")
d1 = st.sidebar.number_input("Dimension 1 of the figure", 8)
d2 = st.sidebar.number_input("Dimension 2 of the figure", 10)


if uploaded_file is not None:
    word = uploaded_file.name
    filetype = word.partition('.')[2]
    
    if filetype == 'su':
        dado = sp.read_su(uploaded_file)
    elif filetype == 'dat':
        dado = sp.read_seg2(uploaded_file)
    elif filetype == 'sgy':
        dado = sp.read_segy(uploaded_file)
    elif filetype == 'rd3':
        st.sidebar.markdown('If you are reading a rd3 file you must pass the number of traces and samples which can be found in the .rad file')
        traces = st.sidebar.number_input("Number of traces", 754)
        samples = st.sidebar.number_input("Number of samples", 415)
        dado = sp.read_rd3(uploaded_file,traces,samples)

    

    
    
    if option == 'Wiggle':
        if filetype == 'rd3':
            st.markdown('Wiggle option does not work with rd3 files yet :(')
        else:
            sp.wigb(dado,title=title,xlabel=xlabel,ylabel=ylabel,dt=dt,d1=d1,
            d2=d2, amx=amx);
    
    elif option == 'Image':
        sp.seis_image(dado,title=title,xlabel=xlabel,ylabel=ylabel,dt=dt,d1=d1,d2=d2);

   



