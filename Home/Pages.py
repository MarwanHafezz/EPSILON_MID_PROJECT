import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config (page_title='Digital Music Store Company', page_icon='note.png', layout='wide')
st.title('Digital Music Store Company')
st.markdown(''' 
This is a simple web app to show some stats regarding the Digital music store company  ''' )
col1 , col2 = st.columns(2)
with col1:
    st.write('')
    st.write('')
    st.write('')
    st.write('')

    st.subheader('“Life is like a piano, the white keys represent happiness and the black shows sadness, but as you go through the life journey, remember that the black keys also make music”')
    st.subheader('\t \t \t \t \t \t  ― Me')
with col2:
    st.image('Digital Music.jpeg', width=600)

df1 = pd.read_csv('df1.csv')
df2 = pd.read_csv('df2.csv')
Table3 = pd.read_csv('Table3.csv')
df4 = pd.read_csv('df4.csv')
df5 = pd.read_csv('df5.csv')
df6 = pd.read_csv('df6.csv')
df7 = pd.read_csv('df7.csv')
df8 = pd.read_csv('df8.csv')
df9 = pd.read_csv('df9.csv')
df10 = pd.read_csv('df10.csv')
df11 = pd.read_csv('df11.csv')
df12 = pd.read_csv('df12.csv')
df13 = pd.read_csv('df13.csv')
df14 = pd.read_csv('df14.csv')


st.title('What is the number of albums in each genre?')

col1,col2 = st.columns([1,2])
with col1:
    st.write('')
    st.write('')
    st.write('')
    st.write('')
    st.write('')
    
    df5
with col2:
    st.plotly_chart(px.bar(df5, x='Genre_Name', y='Album_Count', text='Album_Count'))

st.title('Top 10 number of tracks sold by artists')

col1,col2 = st.columns([1,2])
with col1:
    st.write('')
    st.write('')
    st.write('')
    st.write('')
    st.write('')

    df2
    
with col2:
    st.plotly_chart(px.bar(df2, x='In_playlists', y='artist', orientation='h', text='In_playlists', 
            title='Top 10 Number of Tracks Sold by Artist'))


st.title('Which artist has earned the most based on the InvoiceLines')

col1,col2 = st.columns([1,2])
with col1:
    st.write('')
    st.write('')
    st.write('')
    st.write('')
    st.write('')

    Table3
with col2:
    st.plotly_chart(px.bar(Table3, x='ComposerName_OR_BandName', y='Amount'))    


st.title('What is the total Sales in USD for each Media Type?')

col1,col2 = st.columns([1,2])
with col1:
    st.write('')
    st.write('')
    st.write('')
    st.write('')
    st.write('')
    
    df4
with col2:
    st.plotly_chart(px.bar(df4, x='MediaType_Name', y='Total_Sales', text='Total_Sales'))
    

    st.title('Which Country loves "Rock" the most ?')

col1 , col2= st.columns([1,2])
with col1:
    st.write('')
    st.write('')
    
    
    df1
with col2:
    st.plotly_chart(px.pie(df1, names='Country', values='Rock_Music_Count', 
            color_discrete_sequence=px.colors.sequential.RdBu_r))
    
st.title('What is the number of tracks in each playlist?')

col1,col2 = st.columns([1,2])
with col1:
    st.write('')
    st.write('')
    st.write('')
    
    df6
with col2:
    st.plotly_chart(px.pie(df6, names='Playlist_Name', values='Count', 
            color_discrete_sequence=px.colors.sequential.RdBu))
    
st.title('What is the total Purchases of the best customer per country?')

col1,col2 = st.columns([1,2])
with col1:
    st.write('')
    st.write('')
    st.write('')
    
    df7
with col2:
    st.plotly_chart(px.bar(df7, x='Full_Name', y='Total_purchases'))
    
st.title('Which sales agent made the most in sales ?')

col1,col2 = st.columns([1,2])
with col1:
    st.write('')
    st.write('')
    st.write('')
    
    df8
with col2:
    st.plotly_chart(px.pie(df8, names='Full_Name', values='Total', 
            color_discrete_sequence=px.colors.sequential.RdBu_r))
    
st.title('What is the number of invoices per country ?')

col1,col2 = st.columns([1,2])
with col1:
    st.write('')
    st.write('')
    st.write('')
    
    df9
with col2:
    st.plotly_chart(px.pie(df9, names='Billing_Country', values='Invoices_Count', 
            title='What is the number of invoices per country ?'))

st.title('What is the total sales per country ?')

col1,col2 = st.columns([1,2])
with col1:
    st.write('')
    st.write('')
    st.write('')
    
    df10
with col2:
    st.plotly_chart(px.bar(df10, x='Billing_Country', y='Country_sales'))

st.title('Who are the top 5 best selling artists?')

col1,col2 = st.columns([1,2])
with col1:
    st.write('')
    st.write('')
    st.write('')
    
    df11
with col2:
    st.plotly_chart(px.bar(df11, x='Artist_name', y='Artist_sales')) 
    
st.title('What is the most popular music Genre in USA?')

col1,col2 = st.columns([1,2])
with col1:
    st.write('')
    st.write('')
    st.write('')
    
    df12
with col2:
    st.plotly_chart(px.pie(df12, names='Genre', values='Sold_Tracks'))
    
st.title('What is the total amount of sales in USD per Genre ?')

col1,col2 = st.columns([1,2])
with col1:
    st.write('')
    st.write('')
    st.write('')
    
    df13
with col2:
    st.plotly_chart(px.bar(df13, x='Genre Name', y='Total Amount'))

st.title('What is the total number of customers per Genre ?')

col1,col2 = st.columns([1,2])
with col1:
    st.write('')
    st.write('')
    st.write('')
    
    df13
with col2:
    st.plotly_chart(px.bar(df13, x='Genre Name', y='Number of Customers'))
    
st.title('What is the number of songs in each length group?')

col1,col2 = st.columns([1,2])
with col1:
    st.write('')
    st.write('')
    st.write('')
    
    df14
with col2:
    st.plotly_chart(px.pie(df14, names='Length_range', values='Count', 
            color_discrete_sequence=px.colors.sequential.RdBu))
    

    
    
    
    
    
    
    
