import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title('Intergamma Product Comparison App')

st.header('Upload Datasets')

# If you want to use file upload widgets, uncomment the following lines and comment out the local file paths
# file1 = st.file_uploader('Upload Dataset 1 (CSV)', type=['csv'], key='file1')
# file2 = st.file_uploader('Upload Dataset 2 (CSV)', type=['csv'], key='file2')

# Local file paths (as per your setup)
file1 = r'C:\Users\baran.metin\Documents\Projects\Intergamma\ean_check\data\Bad.csv'
file2 = r'C:\Users\baran.metin\Documents\Projects\Intergamma\ean_check\data\Good.csv'

if file1 and file2:
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    
    st.subheader('Dataset 1')
    st.dataframe(df1)
    
    st.subheader('Dataset 2')
    st.dataframe(df2)
    
    # 1. Use EAN as the key for merging
    key_column = 'EAN'
    
    # Ensure EAN is present in both datasets
    if key_column in df1.columns and key_column in df2.columns:
        # 2. Get all columns except EAN for comparison
        common_columns = list(set(df1.columns).intersection(set(df2.columns)))
        common_columns.remove(key_column)  # Remove the key column from comparison
        
        st.sidebar.header('Select Columns to Compare')
        columns_to_compare = st.sidebar.multiselect('Select columns to compare', common_columns, default=common_columns)
        
        if columns_to_compare:
            # Merge datasets on 'EAN'
            merged_df = pd.merge(df1, df2, on=key_column, suffixes=('_1', '_2'))
            
            # Initialize a 'Match' column to True
            merged_df['Match'] = True
            
            for col in columns_to_compare:
                col_1 = f'{col}_1'
                col_2 = f'{col}_2'
                # Create comparison columns
                merged_df[f'Match_{col}'] = merged_df[col_1] == merged_df[col_2]
                # Update the overall 'Match' column
                merged_df['Match'] &= merged_df[f'Match_{col}']
            
            # 3. Calculate overall match percentage
            total_records = len(merged_df)
            total_matches = merged_df['Match'].sum()
            overall_match_percentage = (total_matches / total_records) * 100 if total_records > 0 else 0
            
            # Display the matched percentage in a card
            st.metric(label="Overall Match Percentage", value=f"{overall_match_percentage:.2f}%")
            
            # 4. Bar chart for a specific segment
            st.sidebar.header('Select Segment for Bar Chart')
            segment_column = st.sidebar.selectbox('Select a segment', columns_to_compare)
            
            if segment_column:
                # Calculate match percentage for the selected segment
                segment_match_col = f'Match_{segment_column}'
                segment_group_col = f'{segment_column}_1'
                
                segment_matches = merged_df.groupby(segment_group_col)[segment_match_col].mean() * 100
                segment_matches = segment_matches.reset_index()
                segment_matches.columns = [segment_column, 'Match Percentage']
                
                st.subheader(f'Match Percentage by {segment_column}')
                st.dataframe(segment_matches)
                
                # Visualize the results
                st.subheader(f'Match Percentage Bar Chart for {segment_column}')
                fig, ax = plt.subplots()
                ax.bar(segment_matches[segment_column], segment_matches['Match Percentage'], color='skyblue')
                ax.set_xlabel(segment_column)
                ax.set_ylabel('Match Percentage')
                ax.set_title(f'Percentage of Matching Information by {segment_column}')
                plt.xticks(rotation=45)
                st.pyplot(fig)
            else:
                st.write('Please select a segment to display the bar chart.')
        else:
            st.write('Please select at least one column to compare.')
    else:
        st.error(f"The key column '{key_column}' is not present in both datasets.")
else:
    st.write('Please upload both datasets to proceed.')
