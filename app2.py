import base64
import calendar
import streamlit as stream
import pandas as pd


def app():
    stream.title('Covid-19 Patient Cases')

    @stream.cache
    def load_csv(path):
        return pd.read_csv(path)

    stream.sidebar.title("Filter Table")

    # Loads data from excel file and formats the rows and columns of the dataframe
    dfcovid = load_csv("covid_data2.csv")
    dfcovid2 = dfcovid.iloc[:, [0, 1, 2, 3, 4, 5]]

    # Renames names of columns
    dfcovid2.columns = ["Case", 'Date', 'Age', 'Gender', 'Nationality', 'Hospital']
    dfcovid2.index = dfcovid2.index + 1

    # Declares filter parameters
    columns = ["Date", "Age", "Gender", "Nationality", "Hospital"]

    for column in columns:
        # Generates unique options for the filter parameters
        options = pd.Series(["All"]).append(dfcovid2[column], ignore_index=True).dropna().unique()

        # Declares the options for the "Age" parameter
        if column == "Age":
            options = ["All", "Younger than 20 years", "20-29 years",
                       "30-39 years", "40-49 years", "50-59 years",
                       "60 years and older"]

        # Declares the options for the "Date" parameter
        if column == "Date":
            # Generates the unique months for the options
            options = pd.DatetimeIndex(dfcovid2[column]).month.unique()
            months = ["All"]

            # Converts the number of the month into name of the month for options
            for month in options:
                if str(month).isnumeric():
                    months.append(calendar.month_name[month])
                options = months

        # Feeds select box with declared options for each filter parameter
        choice = stream.sidebar.selectbox("Select {}".format(column), options)

        # Based on the selected filter parameter, the dataframe is
        # updated if it has met the respective conditions
        if column == "Date":
            if choice == "All":
                continue
            elif choice == "January":
                dfcovid2 = dfcovid2[pd.DatetimeIndex(dfcovid2[column]).month == 1]
            elif choice == "February":
                dfcovid2 = dfcovid2[pd.DatetimeIndex(dfcovid2[column]).month == 2]
            elif choice == "March":
                dfcovid2 = dfcovid2[pd.DatetimeIndex(dfcovid2[column]).month == 3]
            elif choice == "April":
                dfcovid2 = dfcovid2[pd.DatetimeIndex(dfcovid2[column]).month == 4]
            elif choice == "May":
                dfcovid2 = dfcovid2[pd.DatetimeIndex(dfcovid2[column]).month == 5]
            elif choice == "June":
                dfcovid2 = dfcovid2[pd.DatetimeIndex(dfcovid2[column]).month == 6]
            elif choice == "July":
                dfcovid2 = dfcovid2[pd.DatetimeIndex(dfcovid2[column]).month == 7]
            elif choice == "August":
                dfcovid2 = dfcovid2[pd.DatetimeIndex(dfcovid2[column]).month == 8]
            elif choice == "September":
                dfcovid2 = dfcovid2[pd.DatetimeIndex(dfcovid2[column]).month == 9]
            elif choice == "October":
                dfcovid2 = dfcovid2[pd.DatetimeIndex(dfcovid2[column]).month == 10]
            elif choice == "November":
                dfcovid2 = dfcovid2[pd.DatetimeIndex(dfcovid2[column]).month == 11]
            else:
                dfcovid2 = dfcovid2[pd.DatetimeIndex(dfcovid2[column]).month == 12]

            # Resets index count and make it start from 1
            dfcovid2 = dfcovid2.reset_index(drop=True)
            dfcovid2.index = dfcovid2.index + 1
        elif column == "Age":
            if choice == "All":
                continue
            elif choice == "Younger than 20 years":
                dfcovid2 = dfcovid2[(dfcovid2[column] < 20)]
            elif choice == "20-29 years":
                dfcovid2 = dfcovid2[(dfcovid2[column] >= 20) & (dfcovid2[column] <= 29)]
            elif choice == "30-39 years":
                dfcovid2 = dfcovid2[(dfcovid2[column] >= 30) & (dfcovid2[column] <= 39)]
            elif choice == "40-49 years":
                dfcovid2 = dfcovid2[(dfcovid2[column] >= 40) & (dfcovid2[column] <= 49)]
            elif choice == "50-59 years":
                dfcovid2 = dfcovid2[(dfcovid2[column] >= 50) & (dfcovid2[column] <= 59)]
            else:
                dfcovid2 = dfcovid2[(dfcovid2[column] >= 60)]

            # Sorts dataframe by "Age" and "Date" in ascending order
            dfcovid2 = dfcovid2.sort_values(by=["Age", "Date"], ascending=True)

            # Resets index count and make it start from 1
            dfcovid2 = dfcovid2.reset_index(drop=True)
            dfcovid2.index = dfcovid2.index + 1
        else:
            if choice != "All":
                dfcovid2 = dfcovid2[dfcovid2[column] == choice]

                # Resets index count and make it start from 1
                dfcovid2 = dfcovid2.reset_index(drop=True)
                dfcovid2.index = dfcovid2.index + 1

    def get_table_download_link(df):
        """Generates a link allowing the data in a given panda dataframe to be downloaded
        in:  dataframe
        out: href string
        """
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(
            csv.encode()
        ).decode()  # some strings <-> bytes conversions necessary here
        return f'<a href="data:file/csv;base64,{b64}" download="covid_data.csv">Download csv file</a>'

    # Link to download the csv file of the table
    stream.markdown(get_table_download_link(dfcovid2), unsafe_allow_html=True)

    # Searches through the table based on text input
    search = stream.text_input('Search for cases')
    if search:
        search = search.lower()

        if search != "":
            if search.isnumeric():
                # If search input is a number and is between 1-99, the query
                # will return a dataframe with rows that have the same "Age" column value
                if 0 < int(search) < 100:
                    dfcovid2 = dfcovid2.query('Age == "' + search + '"')
                # Otherwise, the query will return a dataframe with rows
                # that have the same "Case" column value
                else:
                    dfcovid2 = dfcovid2.query('Case == "' + search + '"')
            else:
                # The dataframe is updated with rows that have the same value as the search input
                dfcovid2 = dfcovid2[dfcovid2.values == search]

            # Resets index count and make it start from 1
            dfcovid2 = dfcovid2.reset_index(drop=True)
            dfcovid2.index = dfcovid2.index + 1

    # Formats date properly
    dfcovid2['Date'] = pd.to_datetime(dfcovid2['Date'], errors='coerce')
    dfcovid2['Date'] = dfcovid2['Date'].dt.strftime("%d-%m-%Y")

    # Generates table based on the dataframe
    stream.table(dfcovid2)
