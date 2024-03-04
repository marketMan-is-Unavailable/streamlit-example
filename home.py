import io
import streamlit as st
import pandas as pd
from typing import Union
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report

def cleanData(_selectedf, _dataCleaningOptionDropRowColumn, _dataCleaningOptionSelectColumn) -> Union[str, bool]:
    for _options in _dataCleaningOptionDropRowColumn:
        if _options == 'Drop Column':
            _selectedf.drop(_dataCleaningOptionSelectColumn, axis=1, inplace=True)
        elif _options == 'Drop Duplicates':
            _selectedf = _selectedf.drop_duplicates()
        elif _options == 'Drop Missing Values':
            _selectedf = _selectedf.dropna()
        elif _options == 'One Hot Encode':
            st.write(_dataCleaningOptionSelectColumn)
            _selectedf = pd.get_dummies(_selectedf, columns=[_dataCleaningOptionSelectColumn[0]])
        elif _options == 'Sort Ascending':
            _selectedf =  _selectedf.sort_values(by=_dataCleaningOptionSelectColumn[0])
        elif _options == 'Sort Descending':
            _selectedf =  _selectedf.sort_values(by=_dataCleaningOptionSelectColumn[0], ascending=False)


    return _selectedf, True

def discussDataFrame(_selectedf, _dataCleaningOptionDescribeData):
    for _options in _dataCleaningOptionDescribeData:
        if _options == 'Show Info':
            buffer = io.StringIO()
            _selectedf.info(buf=buffer)
            with st.expander("Show Info"):
                st.text(buffer.getvalue())
            
        elif _options == 'Describe':
            with st.expander("Describe Data"):
                st.write(_selectedf.describe())
        elif _options == 'Show shape':
            with st.expander("Show shape"):
                st.write(_selectedf.shape)
        elif _options == 'Show Columns':
            with st.expander("Show Columns"):
                st.write(_selectedf.columns)   
        elif _options ==  'Data Profile':
            with st.expander("Expand Data Profile"):
                pr = _selectedf.profile_report()
                st_profile_report(pr)
        elif _options == 'Count Missing Values(per Column)':
            with st.expander("Missing Values per column"):
                st.write(_selectedf.isna().sum())

def main():
    st.title('DataFrame Cleaning App')
    # Upload file
    showCounter = False
    #if showCounter:
    #    with st.expander("Show Dataframe"):
    #        st.write(st.session_state.df)

    uploaded_file = st.file_uploader("Upload CSV", type=["csv",".xlsx"])
    if uploaded_file is not None:
        if 'df' not in st.session_state:
            st.session_state.df = pd.read_csv(uploaded_file)            
            with st.expander("Show Dataframe"):
                st.write(st.session_state.df)
                showCounter = True

        
    _dataCleaningOptionSelectDescribeLoc, _dataCleaningOptionDropRowColumnLoc, _dataCleaningOptionSelectColumnLoc = st.columns(3)

    with _dataCleaningOptionDropRowColumnLoc:
        # Multi-selectbox to choose cleaning options
        _dataCleaningOptionDropRowColumn = st.multiselect(
            'Select Cleaning Option',
            ('Show Dataframe', 'Drop Column', 'Drop Duplicates', 'Drop Missing Values',
             'One Hot Encode','Sort Ascending','Sort Descending'))
        
    with _dataCleaningOptionSelectColumnLoc:
        # select columns code
        if uploaded_file is not None:
            _dataCleaningOptionSelectColumn = st.multiselect('Select Columns(Drop Column):', st.session_state.df.columns)
            if len(_dataCleaningOptionSelectColumn) == 0:
                st.session_state._selectedf = st.session_state.df    
            else:
                st.session_state._selectedf = st.session_state.df[_dataCleaningOptionSelectColumn]
            #unselected columns code
            _unselectedcolumns = [col for col in st.session_state.df.columns if col not in _dataCleaningOptionSelectColumn]
            st.session_state._unselectedf = st.session_state.df[_unselectedcolumns]
            if len(_dataCleaningOptionSelectColumn) != 0:
                st.session_state._finaldf = pd.concat([st.session_state._selectedf, st.session_state._unselectedf], axis=1)
            else:
                st.session_state._finaldf = st.session_state.df        

    with _dataCleaningOptionSelectDescribeLoc:
        # Multi-selectbox to choose cleaning options
        _dataCleaningOptionDescribeData = st.multiselect(
            'Select Data Describe Option',
            ('Show Info', 'Describe', 'Show shape', 'Show Columns', 'Count Missing Values(per Column)','Data Profile'))
        
    if st.button('Capture State', use_container_width=True):
        try:
            st.session_state.df = st.session_state.df1
            st.write("Captured State !")
        except:
            st.write("Browse/upload file, perform some action !")

    if st.button('Run', use_container_width=True):
        _cleanData = cleanData(st.session_state._finaldf, _dataCleaningOptionDropRowColumn, _dataCleaningOptionSelectColumn)
        if _cleanData[1] == True:
            st.session_state.df1 = _cleanData[0]
            with st.expander("Show Data"):
                st.write(st.session_state.df1)
        if _dataCleaningOptionDropRowColumn is not None:
            _discussDataFrame = discussDataFrame(st.session_state.df, _dataCleaningOptionDescribeData)


if __name__ == "__main__":
    main()