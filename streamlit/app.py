import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

#from main import df_to_check


# Local file paths for the DataFrames
file1 = "../data/incorrect_specs.csv"
file2 = "../data/correct_specs.csv"

# Read the DataFrames
df1 = pd.read_csv(file1)
df2 = pd.read_csv(file2)

GAMMA_LOGO = 'gamma_logo.png'


# Configure Streamlit page settings
st.set_page_config(
    page_title="Gamma Specification Analysis",
    page_icon=Image.open(GAMMA_LOGO),
    layout="wide",
    initial_sidebar_state="auto",
    menu_items=None,
)

# Page header and description
st.header("📃 SpecChecker 📃")
st.markdown(
    "**This is a demonstrator tool to explore correct extraction of product specifications powered by AI!**"
)

with st.sidebar:
    logo = Image.open(GAMMA_LOGO)
    st.image(logo)
    st.markdown("""---""")
    st.text_input(":blue[API KEY]", key='api_key', type='password')

with st.sidebar.expander("🛠️ - Please select the specifications you wish to compare", expanded=True):
    st.selectbox(
        label=":blue[Specifications]",
        options=df1.columns,
        key="spec_name"
    )


# Display the logo
#st.image("gamma_logo.png", use_column_width=True)  # Adjust the path to your logo file

# Title of the app
st.title('How Good is the Specification Information in Gamma.nl')


# Display the DataFrames
st.subheader('Specifications from Gamma Website')
st.dataframe(df1.reset_index(drop=True))

st.subheader('Specifications from Chatbot (ChatGPT)')
st.dataframe(df2.reset_index(drop=True))

# Set the key column
key_column = 'EAN'

if key_column in df1.columns and key_column in df2.columns:
    # Get all columns except the key column for comparison
    common_columns = list(set(df1.columns).intersection(set(df2.columns)))
    common_columns.remove(key_column)  # Remove the key column from comparison

    # Sidebar for column selection with all columns selected by default
    st.sidebar.header('Please select the specifications you wish to compare')
    columns_to_compare = st.sidebar.multiselect(
        'Selected Specifications',
        common_columns,
        default=common_columns  # Set all common columns as selected by default
    )

    if columns_to_compare:
        # Initialize match count
        total_selected = len(columns_to_compare)
        total_matches = 0

        # Create a list to store non-matching specifications
        non_matching_list = []
        match_percentages = {}  # To store match percentages for each column

        # Compare selected columns
        for col in columns_to_compare:
            col_1 = df1[col]
            col_2 = df2[col]

            # Count matches
            matches = (col_1 == col_2)
            total_matches += matches.sum()

            # Store match percentage for the column
            match_percentages[col] = (matches.sum() / len(matches)) * 100

            # Collect non-matching rows
            non_matching_indices = df1.index[~matches]  # Get indices of non-matching rows
            for idx in non_matching_indices:
                non_matching_list.append({
                    'Specification': col,  # Get the column name where the mismatch occurred
                    'Information from Gamma.nl': df1.at[idx, col],  # Get the value from df1
                    'Information from Chatbot': df2.at[idx, col]  # Get the value from df2
                })

        # Create DataFrame for non-matching values
        if non_matching_list:
            non_matching_df = pd.DataFrame(non_matching_list)
        else:
            non_matching_df = pd.DataFrame(columns=['Specification Name', 'Gamma', 'ChatGPT'])

        # Calculate overall match percentage
        overall_match_percentage = (total_matches / (total_selected * len(df1))) * 100 if total_selected > 0 else 0

        # Calculate total mismatches based on selected specifications
        total_mismatches = len(df1) - total_matches  # This assumes all rows are to be compared

        # Display match percentage in a card
        st.subheader('Overall Match Percentage for Selected Specifications')
        st.metric(
            label="For the selected Specifications we observe a matching percentage of:",
            value=f"{overall_match_percentage:.1f}%"
        )
        # st.metric(
        #     label="Total mismatches:",
        #     value=total_mismatches
        # )

        # Pie chart for overall match percentage
        st.subheader('Overall Match Percentage Distribution')
        pie_labels = ['Matches', 'Non-Matches']
        pie_sizes = [overall_match_percentage, 100 - overall_match_percentage]
        pie_colors = ['#003878', '#ffffff']
        fig, ax = plt.subplots()
        ax.pie(pie_sizes, labels=pie_labels, colors=pie_colors, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # Equal aspect ratio ensures that pie chart is circular
        st.pyplot(fig)

        # Bar chart for match percentages
        st.subheader('Match Percentage by Specification')
        fig, ax = plt.subplots()
        ax.bar(match_percentages.keys(), match_percentages.values(), color='#003878')
        ax.set_ylabel('Match Percentage')
        plt.xticks(rotation=90)
        st.pyplot(fig)

        # Display non-matching DataFrame
        if not non_matching_df.empty:
            st.subheader('Non-Matching Specifications')
            st.dataframe(non_matching_df)
        else:
            st.write('All selected specifications match between the two datasets.')

    else:
        st.write('Please select at least one column to compare.')
else:
    st.error(f"The key column '{key_column}' is not present in both datasets.")
