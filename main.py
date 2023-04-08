import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="Metrum_Axel_Girou",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Sidebar
st.sidebar.header(':blue[**DASHBOARD**]')




df = pd.read_csv('data/final_table_SQL.csv')
df.set_index(df.Sales_Dates, inplace=True)
df.index = pd.to_datetime(df.index)

options = st.sidebar.multiselect(
    'Select Sell Metrics',
    ('Turnover', 'Quantity'))

days_to_plot = st.sidebar.slider(
    'Number of Sells to plot',
    1,
    len(df),
    (len(df))
)

df = df.iloc[: days_to_plot ]

data = st.sidebar.checkbox('Show Data', value=False)


st.sidebar.image('images/logo.png', width = 250)



st.title('# :blue[Metrum]')
st.writedown('Exercice de recrutement (BI), `Bonus`')





df.sort_index(inplace=True)
# Calculate turnover
df['Turnover'] = df['qte'] * df['price']

# Create figure with two y-axes
fig = go.Figure()

if len(options) > 1:
    # Add turnover trace
    fig.add_trace(go.Scatter(x=df.index, y=df['Turnover'], name='Turnover'))

    # Add quantity trace
    fig.add_trace(go.Scatter(x=df.index, y=df['qte'], name='Quantity', yaxis='y2'))

    # Set axis titles
    fig.update_layout(title='Turnover and Quantity Over Time',
                    yaxis=dict(title='Turnover'),
                    yaxis2=dict(title='Quantity', overlaying='y', side='right'))

    # Display figure in Streamlit
    st.plotly_chart(fig,
                    use_container_width=True)

elif 'Turnover' in options and len(options) == 1:
    # Add turnover trace
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['Turnover'], name='Turnover'))

    # Add quantity trace
    #fig.add_trace(go.Scatter(x=df.index, y=df['qte'], name='Quantity', yaxis='y2'))

    # Set axis titles
    fig.update_layout(title='Turnover Over Time', yaxis=dict(title='Turnover'))

    # Display figure in Streamlit
    st.plotly_chart(fig,
                    use_container_width=True)

elif 'Quantity' in options and len(options) == 1:
    # Add turnover trace
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['qte'], name='Quantity'))

    # Set axis titles
    fig.update_layout(title='Quantity Over Time', yaxis=dict(title='Quantity'))

    # Display figure in Streamlit
    st.plotly_chart(fig,
                    use_container_width=True)     

col1, col2 = st.columns(2)


with col1:
# Create a new column for sales (qte * price)
    df['Sales_Dates'] = pd.to_datetime(df['Sales_Dates'], format='%d-%b-%y')

    # separate data for 2022 and 2023
    data_2022 = df[df['Sales_Dates'].dt.year == 2022]
    data_2023 = df[df['Sales_Dates'].dt.year == 2023]

    # calculate sales for each year
    sales_2022 = (data_2022['qte'] * data_2022['price']).sum()
    sales_2023 = (data_2023['qte'] * data_2023['price']).sum()

# create pie chart
    labels = ['2022', '2023']
    values = [sales_2022, sales_2023]

    colors = ['#003f5c', '#ffa600']

    fig = {
        'data': [{'labels': labels,
                'values': values,
                'type': 'pie',
                'marker': {'colors': colors,
                            'line': {'color': 'white',
                                    'width': 2}},
                'textfont': {'color': 'white',
                            'size': 18},
                'hoverinfo': 'label+percent+value',
                'hole': 0.4}],
        'layout': {'title': {'text': 'Turnover per Year',
                            'font': {'size': 30,
                                    'color': '#103f5c'}},
                'paper_bgcolor': 'rgba(0,0,0,0)',
                'plot_bgcolor': 'rgba(0,0,0,0)',
                'showlegend': False}
    }

    st.plotly_chart(fig)

with col2:
    st.write('## :green[Number of Articles] more expensive or equal to 50€ ')
    result = len(df[df.price >= 50])
    st.markdown(f'<p style="font-size:150px; color:green; text-align:center;">{result}</p>', unsafe_allow_html=True)
    st.empty()





if data == True:
    st.table(df.drop(columns = 'Sales_Dates')
)

else: pass