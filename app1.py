import base64
import streamlit as stream
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
def app():
    """
    Make a overall Statistics page.
    """
    try:
        # Load the data from the excel file
        Covid_Data = pd.read_excel('Covid-19 SG.xlsx')

        # Replacing the empty space in the excel columns with _
        Covid_Data.columns = Covid_Data.columns.str.strip()
        Covid_Data.columns = Covid_Data.columns.str.replace(' ', '_')

        # Find the daily cases for the past 5 days.
        Covid_Data_daily = Covid_Data.iloc[-5:, [0, 1, 9, 4, 8]]
        Covid_Data_daily.columns = ['Date', 'Confirmed', 'Deaths', 'Discharged', 'Hospitalised']
        Covid_Data_daily.set_index('Date', inplace=True)

        # Find the total number of cormfirmed cases, deaths, discharged and hospitalised.

        confirmed_total = int(Covid_Data['Daily_Confirmed'].sum())
        deaths_total = int(Covid_Data['Daily_Deaths'].sum())
        discharged_total = int(Covid_Data['Daily_Discharged'].sum())
        hospitalised_total = int(Covid_Data['Still_Hospitalised'].sum())

        # Group the data by month.
        Covid_Data.index = pd.to_datetime(Covid_Data['Date'])
        data = Covid_Data.groupby(pd.Grouper(freq='M'))
        month = Covid_Data.Date.dt.to_period("M")
        monthgrouping = Covid_Data.groupby(month)
        month_cases = monthgrouping.sum()
        month_cases['Month'] = month_cases.index

        # Change the date format and make it to string.
        Covid_Data['Date_String'] = Covid_Data.index.astype(str)
        Covid_Data['Date_String'] = Covid_Data.index
        date = Covid_Data['Date_String'].dt.strftime("%d %B %Y")
        month_cases['Month_String'] = month_cases['Month'].dt.strftime("%B %Y")

        # Find the total average cases and average cases by month
        mean_daily_cases = int(Covid_Data['Daily_Confirmed'].mean())
        mean_cases_month = monthgrouping.mean()
        mean_cases_month['Month'] = mean_cases_month.index
        mean_cases_month['Month'] = mean_cases_month['Month'].dt.strftime("%B %Y")

        def average_cases(cases):
            """
            Generate a table that consits of  average cases in Singapore
            : param cases dataframe: Dataframe for the average cases in Singapore.
            : return average_cases_month dataframe: Dataframe for downloading to CSV file.
            """
            stream.subheader('Average Cases by Month')
            cases = cases.set_index(['Month'])
            average_cases_month = cases[['Daily_Confirmed', 'Daily_Deaths', 'Daily_Discharged', 'Still_Hospitalised']]
            average_cases_month.columns = ['Confirmed', 'Deaths', 'Discharged', 'Hospitalised']
            stream.table(average_cases_month.style.format('{:,.2f}'))
            average_cases_month = average_cases_month.round(2)
            return average_cases_month

        def plot_cases_of_singapore():
            """
            Generate a line graph overview for overall COVID 19 situation in Singapore.
            """
            if stream.sidebar.checkbox("Show Graph Overview", False, key='4'):
                stream.subheader('Cumulative number of cases in Singapore')
                fig = px.line(Covid_Data, x='Date',
                              y=['Cumulative_Confirmed', 'Cumulative_Discharged', 'Cumulative_Deaths', 'Still_Hospitalised',
                                 'Discharged_to_Isolation'])
                stream.plotly_chart(fig, use_container_width=True)


        ## plotgraph shows the dailes from the beggining of the month to the latest month for the user to view ##

        def plotgraph():
            """
            Shows the dailes from the beggining of the month to the latest month for the user to view
            """

            if not stream.sidebar.checkbox("Hide", False, key='3'):

                if Parameters_type == 'Total Confirmed Cases':
                    stream.title("Total Confirmed Cases")
                    fig = go.Figure()
                    fig.add_trace(
                        go.Scatter(x=Covid_Data.Date, y=Covid_Data.Daily_Confirmed, mode='lines', name='Total Cases'))
                    stream.plotly_chart(fig, use_container_width=True)
                if Parameters_type == 'Deaths':
                    stream.title("Total Deaths")
                    fig = go.Figure()
                    fig.add_trace(
                        go.Scatter(x=Covid_Data.Date, y=Covid_Data.Daily_Deaths, mode='lines', name='Total Deaths'))
                    stream.plotly_chart(fig, use_container_width=True)
                if Parameters_type == 'Discharged':
                    stream.title("Total Discharged")
                    fig = go.Figure()
                    fig.add_trace(
                        go.Scatter(x=Covid_Data.Date, y=Covid_Data.Daily_Discharged, mode='lines', name='Total Discharged'))
                    stream.plotly_chart(fig, use_container_width=True)
                if Parameters_type == 'Hospitalised':
                    stream.title("Total Hospitalised")
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=Covid_Data.Date, y=Covid_Data.Still_Hospitalised, mode='lines',
                                             name='Total Hospitalised'))
                    stream.plotly_chart(fig, use_container_width=True)

        ## End of plotgraph ##

        ## Function to plot the piechart ##
        ## plotpie shows the past 10 days for the user to view ##

        def plotpie():
            """
            Shows the past 10 days for the user to view
            """

            ## To hide the graph that is being displayed ##
            if not stream.sidebar.checkbox("Hide", False, key='3'):

                if Parameters_type == 'Total Confirmed Cases':
                    stream.title("Past 10 days for Confirmed Cases")
                    fig = go.Figure()
                    fig = px.pie(Covid_Data, values=Covid_Data['Daily_Confirmed'][-10:],
                                 names=date[-10:], title='Daily Confirmed Cases')
                    stream.plotly_chart(fig, use_container_width=True)

                if Parameters_type == 'Deaths':
                    stream.title("Past 10 days for Death Cases")
                    fig = go.Figure()
                    fig = px.pie(Covid_Data, values=Covid_Data['Daily_Deaths'][-10:],
                                 names=date[-10:], title='Daily Death Cases')
                    stream.plotly_chart(fig, use_container_width=True)

                if Parameters_type == 'Discharged':
                    stream.title("Past 10 days for Discharged Cases")
                    fig = go.Figure()
                    fig = px.pie(Covid_Data, values=Covid_Data['Daily_Discharged'][-10:],
                                 names=date[-10:], title='Daily Discharged Cases')
                    stream.plotly_chart(fig, use_container_width=True)

                if Parameters_type == 'Hospitalised':
                    stream.title("Past 10 days for Hospitalised Cases")
                    fig = go.Figure()
                    fig = px.pie(Covid_Data, values=Covid_Data['Still_Hospitalised'][-10:],
                                 names=date[-10:], title='Still Hospitalised Cases')
                    stream.plotly_chart(fig, use_container_width=True)

        ## End of plotpie ##

        ## Function to plot the barchart ##
        ## barchart shows the monthly overview for the user to view, user can filter away the months they dont want to see##
        def plotbar():
            """
            Shows the monthly overview for the user to view, user can filter away the months they dont want to see
            """

            if not stream.sidebar.checkbox("Hide", False, key='3'):

                if Parameters_type == 'Total Confirmed Cases':
                    stream.title("Total Monthly Confirmed Cases Overview")
                    fig = go.Figure(data=[
                        go.Bar(
                            x=month_cases.Month_String[month_cases.Month_String == 'January 2020'],
                            y=month_cases.Daily_Confirmed[month_cases.Month_String == 'January 2020'],
                            name='Confirmed Cases Jan'),
                        go.Bar(x=month_cases.Month_String[month_cases.Month_String == 'February 2020'],
                               y=month_cases.Daily_Confirmed[month_cases.Month_String == 'February 2020'],
                               name='Confirmed Cases Feb'),
                        go.Bar(x=month_cases.Month_String[month_cases.Month_String == 'March 2020'],
                               y=month_cases.Daily_Confirmed[month_cases.Month_String == 'March 2020'],
                               name='Confirmed Cases Mar'),
                        go.Bar(x=month_cases.Month_String[month_cases.Month_String == 'April 2020'],
                               y=month_cases.Daily_Confirmed[month_cases.Month_String == 'April 2020'],
                               name='Confirmed Cases April'),
                        go.Bar(x=month_cases.Month_String[month_cases.Month_String == 'May 2020'],
                               y=month_cases.Daily_Confirmed[month_cases.Month_String == 'May 2020'],
                               name='Confirmed Cases April'),
                        go.Bar(x=month_cases.Month_String[month_cases.Month_String == 'June 2020'],
                               y=month_cases.Daily_Confirmed[month_cases.Month_String == 'June  2020'],
                               name='Confirmed Cases Jun'),
                        go.Bar(x=month_cases.Month_String[month_cases.Month_String == 'July 2020'],
                               y=month_cases.Daily_Confirmed[month_cases.Month_String == 'July 2020'],
                               name='Confirmed Cases Jul'),
                        go.Bar(x=month_cases.Month_String[month_cases.Month_String == 'August 2020'],
                               y=month_cases.Daily_Confirmed[month_cases.Month_String == 'August 2020'],
                               name='Confirmed Cases Aug'),
                        go.Bar(x=month_cases.Month_String[month_cases.Month_String == 'September 2020'],
                               y=month_cases.Daily_Confirmed[month_cases.Month_String == 'September 2020'],
                               name='Confirmed Cases Sep'),
                        go.Bar(x=month_cases.Month_String[month_cases.Month_String == 'October 2020'],
                               y=month_cases.Daily_Confirmed[month_cases.Month_String == 'October 2020'],
                               name='Confirmed Cases Oct')])
                    stream.plotly_chart(fig, use_container_width=True)

                if Parameters_type == 'Deaths':
                    stream.title("Total Monthly Deaths Overview")
                    fig = go.Figure(data=[
                        go.Bar(
                            x=month_cases.Month_String[month_cases.Month_String == 'January 2020'],
                            y=month_cases.Daily_Deaths[month_cases.Month_String == 'January 2020'],
                            name='Confirmed Cases Jan'),
                        go.Bar(x=month_cases.Month_String[month_cases.Month_String == 'February 2020'],
                               y=month_cases.Daily_Deaths[month_cases.Month_String == 'February 2020'],
                               name='Confirmed Cases Feb'),
                        go.Bar(x=month_cases.Month_String[month_cases.Month_String == 'March 2020'],
                               y=month_cases.Daily_Deaths[month_cases.Month_String == 'March 2020'],
                               name='Confirmed Cases Mar'),
                        go.Bar(x=month_cases.Month_String[month_cases.Month_String == 'April 2020'],
                               y=month_cases.Daily_Deaths[month_cases.Month_String == 'April 2020'],
                               name='Confirmed Cases April'),
                        go.Bar(x=month_cases.Month_String[month_cases.Month_String == 'May 2020'],
                               y=month_cases.Daily_Deaths[month_cases.Month_String == 'May 2020'],
                               name='Confirmed Cases April'),
                        go.Bar(x=month_cases.Month_String[month_cases.Month_String == 'June 2020'],
                               y=month_cases.Daily_Deaths[month_cases.Month_String == 'June  2020'],
                               name='Confirmed Cases Jun'),
                        go.Bar(x=month_cases.Month_String[month_cases.Month_String == 'July 2020'],
                               y=month_cases.Daily_Deaths[month_cases.Month_String == 'July 2020'],
                               name='Confirmed Cases Jul'),
                        go.Bar(x=month_cases.Month_String[month_cases.Month_String == 'August 2020'],
                               y=month_cases.Daily_Deaths[month_cases.Month_String == 'August 2020'],
                               name='Confirmed Cases Aug'),
                        go.Bar(x=month_cases.Month_String[month_cases.Month_String == 'September 2020'],
                               y=month_cases.Daily_Deaths[month_cases.Month_String == 'September 2020'],
                               name='Confirmed Cases Sep'),
                        go.Bar(x=month_cases.Month_String[month_cases.Month_String == 'October 2020'],
                               y=month_cases.Daily_Deaths[month_cases.Month_String == 'October 2020'],
                               name='Confirmed Cases Oct')])
                    stream.plotly_chart(fig, use_container_width=True)

                if Parameters_type == 'Discharged':
                    stream.title("Total Monthly Discharged Overview")
                    fig = go.Figure(data=[
                        go.Bar(
                            x=month_cases.Month_String[month_cases.Month_String == 'January 2020'],
                            y=month_cases.Daily_Discharged[month_cases.Month_String == 'January 2020'],
                            name='Confirmed Cases Jan'),
                        go.Bar(x=month_cases.Month_String[month_cases.Month_String == 'February 2020'],
                               y=month_cases.Daily_Discharged[month_cases.Month_String == 'February 2020'],
                               name='Confirmed Cases Feb'),
                        go.Bar(x=month_cases.Month_String[month_cases.Month_String == 'March 2020'],
                               y=month_cases.Daily_Discharged[month_cases.Month_String == 'March 2020'],
                               name='Confirmed Cases Mar'),
                        go.Bar(x=month_cases.Month_String[month_cases.Month_String == 'April 2020'],
                               y=month_cases.Daily_Discharged[month_cases.Month_String == 'April 2020'],
                               name='Confirmed Cases April'),
                        go.Bar(x=month_cases.Month_String[month_cases.Month_String == 'May 2020'],
                               y=month_cases.Daily_Discharged[month_cases.Month_String == 'May 2020'],
                               name='Confirmed Cases April'),
                        go.Bar(x=month_cases.Month_String[month_cases.Month_String == 'June 2020'],
                               y=month_cases.Daily_Discharged[month_cases.Month_String == 'June  2020'],
                               name='Confirmed Cases Jun'),
                        go.Bar(x=month_cases.Month_String[month_cases.Month_String == 'July 2020'],
                               y=month_cases.Daily_Discharged[month_cases.Month_String == 'July 2020'],
                               name='Confirmed Cases Jul'),
                        go.Bar(x=month_cases.Month_String[month_cases.Month_String == 'August 2020'],
                               y=month_cases.Daily_Discharged[month_cases.Month_String == 'August 2020'],
                               name='Confirmed Cases Aug'),
                        go.Bar(x=month_cases.Month_String[month_cases.Month_String == 'September 2020'],
                               y=month_cases.Daily_Discharged[month_cases.Month_String == 'September 2020'],
                               name='Confirmed Cases Sep'),
                        go.Bar(x=month_cases.Month_String[month_cases.Month_String == 'October 2020'],
                               y=month_cases.Daily_Discharged[month_cases.Month_String == 'October 2020'],
                               name='Confirmed Cases Oct')])
                    stream.plotly_chart(fig, use_container_width=True)

                if Parameters_type == 'Hospitalised':
                    stream.title("Total Monthly Hospitalised Overview")
                    fig = go.Figure(data=[
                        go.Bar(
                            x=month_cases.Month_String[month_cases.Month_String == 'January 2020'],
                            y=month_cases.Still_Hospitalised[month_cases.Month_String == 'January 2020'],
                            name='Confirmed Cases Jan'),
                        go.Bar(x=month_cases.Month_String[month_cases.Month_String == 'February 2020'],
                               y=month_cases.Still_Hospitalised[month_cases.Month_String == 'February 2020'],
                               name='Confirmed Cases Feb'),
                        go.Bar(x=month_cases.Month_String[month_cases.Month_String == 'March 2020'],
                               y=month_cases.Still_Hospitalised[month_cases.Month_String == 'March 2020'],
                               name='Confirmed Cases Mar'),
                        go.Bar(x=month_cases.Month_String[month_cases.Month_String == 'April 2020'],
                               y=month_cases.Still_Hospitalised[month_cases.Month_String == 'April 2020'],
                               name='Confirmed Cases April'),
                        go.Bar(x=month_cases.Month_String[month_cases.Month_String == 'May 2020'],
                               y=month_cases.Still_Hospitalised[month_cases.Month_String == 'May 2020'],
                               name='Confirmed Cases April'),
                        go.Bar(x=month_cases.Month_String[month_cases.Month_String == 'June 2020'],
                               y=month_cases.Still_Hospitalised[month_cases.Month_String == 'June  2020'],
                               name='Confirmed Cases Jun'),
                        go.Bar(x=month_cases.Month_String[month_cases.Month_String == 'July 2020'],
                               y=month_cases.Still_Hospitalised[month_cases.Month_String == 'July 2020'],
                               name='Confirmed Cases Jul'),
                        go.Bar(x=month_cases.Month_String[month_cases.Month_String == 'August 2020'],
                               y=month_cases.Still_Hospitalised[month_cases.Month_String == 'August 2020'],
                               name='Confirmed Cases Aug'),
                        go.Bar(x=month_cases.Month_String[month_cases.Month_String == 'September 2020'],
                               y=month_cases.Still_Hospitalised[month_cases.Month_String == 'September 2020'],
                               name='Confirmed Cases Sep'),
                        go.Bar(x=month_cases.Month_String[month_cases.Month_String == 'October 2020'],
                               y=month_cases.Still_Hospitalised[month_cases.Month_String == 'October 2020'],
                               name='Confirmed Cases Oct')])
                    stream.plotly_chart(fig, use_container_width=True)

        ## End of plotbar ##

        ## CSS Style for some of the content below ##
        stream.markdown("""
        <style>
        .highlight 
        {
          border-radius: 0.5rem;
          color: black;
          padding: 0.5rem;
          margin-bottom: 1rem;
          text-align: center;
        }
        .bold 
        {
          padding-left: 0.3rem;
          padding-right: 0.3rem;
          font-weight: 500;
        }
        .red 
        {
          background-color: lightcoral;
        }
        .blue 
        {
          background-color: lightblue;
        }
        .center
        {
          text-align : center; 
        }
        </style>            
        """, unsafe_allow_html=True)
        ## End of CSS Style ##

        ## Main Header for the page ##
        stream.markdown("<h1 style='text-align: center;'>🦠 Covid-19 Overall Statistics 😷</h1>", unsafe_allow_html=True)

        ## Showing the total confirmed, deaths, discharged and Hospitalised in Singapore
        Overall_Total = "<div class='center'>" \
                        " Confirmed : <span class='bold highlight blue'; style='color: purple;'>" + str(confirmed_total) + "</span>" \
                        " Deaths : <span class='bold highlight red'; style='color: blue;'>" + str(deaths_total) + "</span>" \
                        " Discharged : <span class='bold'; style='color: red;'>" + str(discharged_total) + "</span>" \
                        "<br><br> Hospitalised : <span class='bold'; style='color: green;'>" + str(hospitalised_total) + "</span>" \
                        " Average : <span class='bold'; style='color: hotpink;'>" + str(mean_daily_cases) + "</span>" \
                        + "</div><br><br>"
        stream.markdown(Overall_Total, unsafe_allow_html=True)

        ## Short description of the Coronavirus ##
        stream.markdown(
            "<p style='text-align: center; color: black;'>Coronavirus is a type of virus that may cause respiratory illnesses in humans ranging from common colds "
            "to more severe conditions such as Severe Acute "
            "Respiratory Syndrome (SARS) and Middle Eastern Respiratory Syndrome (MERS)."
            "The virus spreads most often when people are physically close. "
            "It spreads easily via small droplets as a person breathes, coughs, sneezes or talks.""</p>",
            unsafe_allow_html=True)
        stream.image("covid.png", use_column_width=True)

        ## Side Menu for the page ##
        stream.sidebar.title("Visualization Selector")
        stream.sidebar.markdown("Select the Charts/Plots accordingly:")

        ## Different selections for the user to choose ##
        Visualation_type = stream.sidebar.selectbox('Visualization type', ['Graph', 'Pie Chart', 'Bar Chart'], key='2')
        Parameters_type = stream.sidebar.selectbox('Parameters',
                                                   ['Total Confirmed Cases', 'Deaths', 'Discharged', 'Hospitalised'],
                                                   key='3')

        if Visualation_type == 'Graph':
            plotgraph()

        if Visualation_type == 'Pie Chart':
            plotpie()

        if Visualation_type == 'Bar Chart':
            plotbar()

        plot_cases_of_singapore()

        stream.subheader('Daily Cases for the Past 5 Days')
        df = pd.DataFrame(Covid_Data_daily)
        stream.table(df)

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

        stream.markdown(get_table_download_link(Covid_Data_daily), unsafe_allow_html=True)

        average = average_cases(mean_cases_month)
        stream.markdown(get_table_download_link(average), unsafe_allow_html=True)

    except IOError:
        stream.error("File is not found or file is opened. Please make sure your that file name is correct and it is placed in the correct directory. Please remember to close it.")
