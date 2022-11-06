#!/usr/bin/env python
# coding: utf-8

# In[68]:


import pandas as pd
import sqlite3 
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')
import plotly.express as px, plotly.graph_objects as go
import streamlit as st
import plotly.express as px
import webbrowser


# In[2]:


conn = sqlite3.connect('C:/Users/marwa/Downloads/chinook-db/chinook_db/chinook.db')
c = conn.cursor()


# In[3]:


def sq(q):
    return pd.read_sql_query(q, conn).rename(columns = lambda x:x.replace(' ','_').capitalize())


# In[4]:


tables = sq('''select Name,type
               from sqlite_master 
               where type='table' ''')


# In[5]:


album = sq('''select * from album''')
album.head()


# In[6]:


artist = sq('''select * from Artist''')
artist.head()


# In[7]:


customer = sq('''select * from customer''')
customer.head()


# In[8]:


employee = sq('''select * from Employee''')
employee.head()


# In[9]:


genre = sq('''select *from Genre''')
genre.head()


# In[10]:


invoice = sq('''select * from Invoice''')
invoice.head()


# In[11]:


invoiceLine = sq('''select * from InvoiceLine''')
invoiceLine.head()


# In[12]:


media_type = sq('''select * from MediaType''')
media_type.head()


# In[13]:


playlist = sq('''select * from Playlist''')
playlist.head()


# In[14]:


playlist_track = sq('''select * from PlaylistTrack''')
playlist_track.head()


# In[15]:


track = sq('''select * from Track''')
track.head()


# In[16]:


Non_American_Customers = sq('''select FirstName||' '||LastName as Name, Country, CustomerId
    from customer 
    where Country <> 'USA' ''')


# In[18]:


Non_American_Customers


# In[19]:


Non_American_Customers.count()


# In[20]:


sq('''select *
    from employee
    where title like "%Sales%Agent%" ''')


# In[21]:


sq('''select DISTINCT BillingCountry 
    from invoice ''').head()


# # Which Country loves 'Rock' the most ?

# In[22]:


df1 = sq('''
SELECT
  Customer.Country,
  COUNT(Customer.Country) AS Rock_Music_Count,
  Genre.Name

FROM InvoiceLine
JOIN Track
  ON InvoiceLine.TrackId = Track.TrackId

JOIN Genre
  ON Genre.GenreId = Track.GenreId

JOIN Invoice
  ON Invoice.InvoiceId = InvoiceLine.InvoiceId

JOIN Customer
  ON Invoice.CustomerId = Customer.CustomerId

WHERE Genre.Name LIKE 'Rock'
GROUP BY 1
ORDER BY 2 DESC
''')


# In[23]:


df1


# In[24]:


df1.plot.bar(x="Country", y=None)


# In[25]:


fig = px.pie(df1, names='Country', values='Rock_music_count', 
            title='Which Country loves "Rock" the most?', 
            color_discrete_sequence=px.colors.sequential.RdBu_r)
fig.update_layout(legend_title_text='Genre')
fig.show()


# # Who are the top 10 Artists who sold the most number of tracks ?

# In[26]:


df2 = sq('''WITH playlist_track_artist AS 
( 
          SELECT    p.NAME    playlist, 
                    t.NAME    track, 
                    alb.title album, 
                    art.NAME  artist 
          FROM      Playlist p 
          LEFT JOIN PlaylistTrack 
          ON        PlaylistTrack.PlaylistId = p.PlaylistId 
          LEFT JOIN Track t 
          ON        t.TrackId = PlaylistTrack.TrackId 
          LEFT JOIN album alb 
          ON        alb.AlbumId = t.AlbumId 
          LEFT JOIN artist art 
          ON        art.ArtistId = alb.ArtistId) 
SELECT   artist, 
         Count(*) In_playlists 
FROM     playlist_track_artist 
GROUP BY artist 
ORDER BY In_playlists DESC limit 10''')


# In[27]:


df2


# In[28]:


fig = px.bar(df2, x='In_playlists', y='Artist', orientation='h', text='In_playlists', 
            title='Top 10 Number of Tracks Sold by Artist')
fig.update_xaxes(showticklabels=False)
fig.update_traces(marker_color='rgb(250, 50, 180)')
fig.update_layout(plot_bgcolor='rgba(0,0,0,0)')
fig.show()


# # Which Artist has earned the most based on the InvoiceLines ?

# In[29]:


df3 = sq('''
SELECT
  ar.Name AS ComposerName_OR_BandName,
  SUM(tr.UnitPrice) AS Amount
FROM Track tr
JOIN InvoiceLine in_line
  ON tr.TrackId = in_line.TrackId
JOIN Album al
  ON al.AlbumId = tr.AlbumId
JOIN Artist ar
  ON ar.ArtistId = al.ArtistId
GROUP BY 1
ORDER BY 2 DESC
LIMIT 15; ''')


# In[30]:


df3


# In[31]:


fig = px.bar(df3, x='Composername_or_bandname', y='Amount')
fig.show()


# # What is the total Sales in USD for each Media Type?

# In[36]:


df4 = sq('''SELECT m.Name as MediaType_Name, SUM(il.UnitPrice*il.Quantity) as Total_Sales
FROM MediaType m
JOIN Track t
ON m.MediaTypeId = t.MediaTypeId
JOIN InvoiceLine il
ON t.TrackId = il.TrackId
JOIN Invoice i
ON i.InvoiceId = il.InvoiceId
JOIN Customer c
ON c.CustomerId = i.CustomerId
GROUP BY MediaType_Name
ORDER BY Total_Sales DESC''')


# In[35]:


df4


# In[34]:


fig = px.bar(df4, x='Mediatype_name', y='Total_sales', text='Total_sales')
fig.update_traces(marker_color='rgb(20, 190, 180)')
fig.show()


# # What is the number of albums in each genre?

# In[37]:


df5 = sq('''  SELECT g.Name as Genre_Name , COUNT(a.AlbumId) as Album_Count
FROM Genre g
JOIN Track t
ON g.GenreId = t.GenreId
JOIN Album a
ON a.AlbumId = t.AlbumId 
GROUP BY 1
ORDER BY 2 DESC''')


# In[38]:


df5


# In[39]:


fig = px.bar(df5, x='Genre_name', y='Album_count', text='Album_count')
fig.update_traces(marker_color='rgb(160, 20, 20)')
fig.show()


# # What is the number of tracks in each playlist ?

# In[40]:


df6 = sq ('''SELECT p.PlaylistId as ID ,p.Name as Playlist_Name, COUNT(pt.TrackId) as Count
FROM PlaylistTrack pt
JOIN Playlist p
ON p.PlaylistId = pt.PlaylistId
GROUP BY ID,Playlist_Name
ORDER BY Count DESC ''')


# In[41]:


df6


# In[42]:


fig = px.pie(df6, names='Playlist_name', values='Count', 
            title='What is the number of trackes in each playlist ?', 
            color_discrete_sequence=px.colors.sequential.RdBu)
fig.update_layout(legend_title_text='Playlist_name')
fig.show()


# # What is the total Purchases of the best customer per country?

# In[43]:


df7 = sq('''WITH table1 as (SELECT c.Country as Country, c.CustomerId as CustomerId
,c.FirstName as FirstName,c.LastName as Lastname ,SUM(i.Total) as Total
FROM Customer c
JOIN Invoice i
ON i.CustomerId = c.CustomerId
GROUP BY c.Country,c.CustomerId , c.FirstName
ORDER BY Total),
table2 as  
(SELECT Country  , max(Total) as Maximum
FROM table1
GROUP BY Country )
SELECT table1.Country as Country , table1.Total as Total_purchases ,
table1.FirstName || ' ' || table1.LastName as Full_Name, table1.CustomerId as CustomerId
FROM table1
JOIN table2
ON table1.Country = table2.Country and table1.Total = table2.Maximum
ORDER BY Total_purchases desc''')


# In[44]:


df7


# In[45]:


fig = px.bar(df7, x='Full_name', y='Total_purchases')
fig.update_traces(marker_color='rgb(90, 20, 180)')
fig.show()


# # Which sales agent made the most in sales ?

# In[46]:


df8 = sq('''SELECT e.EmployeeId as EmployeeId , e.FirstName || ' ' || e.LastName as Full_Name, COUNT(i.Total) as Total
FROM Invoice i
JOIN Customer c
ON i.CustomerId = c.CustomerId
JOIN Employee e 
ON e.EmployeeId = c.SupportRepId
GROUP BY 1,2
ORDER BY 3 DESC''')


# In[47]:


df8


# In[48]:


fig = px.pie(df8, names='Full_name', values='Total', 
            title='Which sales agent made the most in sales ?', 
            color_discrete_sequence=px.colors.sequential.RdBu)
fig.update_layout(legend_title_text='Playlist_name')
fig.show()


# # What is the number of invoices per country ?

# In[49]:


df9 = sq('''select BillingCountry as Billing_Country,count(*) as Invoices_Count
    FROM invoice 
    GROUP BY BillingCountry
    ORDER BY Invoices_Count desc
    ''')


# In[50]:


df9


# In[51]:


fig = px.pie(df9, names='Billing_country', values='Invoices_count', 
            title='What is the number of invoices per country ?')
fig.update_layout(legend_title_text='Country')
fig.update_traces(marker=dict(colors=['red', 'yellow', 'green']))
fig.show()


# # What is the total sales per country ?

# In[52]:


df10 = sq('''SELECT i.BillingCountry as Billing_Country ,SUM(Total) as Country_sales
FROM invoice as i
GROUP BY BillingCountry 
ORDER BY 2 DESC''')


# In[53]:


df10


# In[54]:


fig = px.bar(df10, x='Billing_country', y='Country_sales')
fig.update_traces(marker_color='rgb(180, 20, 100)')
fig.show()


# # Who are the top 5 best selling artists ? 

# In[55]:


df11 = sq('''SELECT art.Name as Artist_name ,count(*) as Artist_sales
    FROM InvoiceLine as i
    LEFT JOIN Track as t on i.TrackId = i.TrackId
    LEFT JOIN Album as a on a.AlbumId = t.AlbumId
    LEFT JOIN Artist as art on art.ArtistId = a.ArtistId 
    GROUP BY art.ArtistId
    ORDER BY 2 DESC 
    LIMIT 5''')


# In[56]:


df11


# In[57]:


fig = px.bar(df11, x='Artist_name', y='Artist_sales')
fig.update_traces(marker_color='rgb(0, 20, 200)')
fig.show()


# # What is the most popular music Genre in USA?

# In[58]:


df12 = sq('''WITH tracks_bought_in_usa 
     AS (SELECT TrackId, 
                Quantity, 
                i.BillingCountry 
         FROM   InvoiceLine il 
                INNER JOIN Invoice i 
                        ON il.InvoiceId = i.InvoiceId 
         WHERE  i.BillingCountry = 'USA'), 
     tracks_bought_in_usa_genres 
     AS (SELECT g.NAME AS Genre, 
                tracks_bought_in_usa.Quantity 
         FROM   tracks_bought_in_usa 
                INNER JOIN track t 
                        ON t.TrackId = tracks_bought_in_usa.TrackId 
                INNER JOIN genre g 
                        ON g.GenreId = t.GenreId) 
SELECT genre, 
       Sum(Quantity) AS Sold_Tracks, 
       Round(Cast(Sum(Quantity) AS FLOAT) / (SELECT Sum(Quantity) 
                                             FROM   tracks_bought_in_usa_genres) 
             * 100) 
                     AS Sold_Tracks_Perc 
FROM   tracks_bought_in_usa_genres 
GROUP  BY genre 
ORDER  BY sold_tracks DESC''')


# In[59]:


df12


# In[60]:


fig = px.pie(df12, names='Genre', values='Sold_tracks', 
            title='What is the most popular music Genre in USA?')
fig.update_layout(legend_title_text='Genre')
fig.update_traces(marker=dict(colors=['red', 'yellow', 'green']))
fig.show()


# # What is the total amount of sales in USD and the number of customers for each genre ? 

# In[61]:


df13 = sq('''WITH table1 AS
  (SELECT G.GenreId,
          G.Name AS 'Genre Name',
          sum(il.UnitPrice*il.Quantity)AS 'Total Amount'
   FROM Track t
   JOIN Genre G 
   ON G.GenreId = t.GenreId
   JOIN InvoiceLine il
   ON il.TrackId = t.TrackId
   JOIN Invoice i
   ON i.InvoiceId = il.InvoiceId
   JOIN Customer c
   ON c.CustomerId = i.CustomerId
   GROUP BY 1
   ORDER BY 3 DESC),
     table2 AS
  (SELECT GenreId,
          count(*) count_inv
   FROM
     (SELECT G.GenreId,
             i.InvoiceId,
             count(i.CustomerId) CustomerCount
      FROM Genre G
      JOIN Track t 
	  ON t.GenreId = G.GenreId
      JOIN InvoiceLine il
	  ON il.TrackId = t.TrackId
      JOIN Invoice i
	  ON i.InvoiceId = il.InvoiceId
      GROUP BY G.GenreId,
               i.InvoiceId
      ORDER BY 3 DESC)
   GROUP BY GenreId)
SELECT table1.'Genre Name',
          table1.'Total Amount',
             table2.count_inv 'Number of Customers'
FROM table1
JOIN table2 ON table1.GenreId=table2.GenreId''')


# In[62]:


df13


# In[63]:


fig = px.bar(df13, x='Genre_name', y='Total_amount')
fig.update_traces(marker_color='rgb(255, 0, 230)')
fig.show()


# In[64]:


fig = px.bar(df13, x='Genre_name', y='Number_of_customers',)
fig.update_traces(marker_color='rgb(26, 255, 0)')
fig.show()


# # What is the number of songs in each length group ?

# In[65]:


df14 = sq('''WITH t1 as(select t.Name as Name , t.Milliseconds as Millisecond,
CASE when milliseconds < 1500000 THEN 'Less than 1.5 million sec'
WHEN milliseconds >= 1500000 AND milliseconds < 2500000 THEN 'Between 1.5 & 2.5 million sec'
WHEN milliseconds >= 2500000 AND milliseconds < 3500000 THEN 'Between 2.5 & 3.5 million sec'
ELSE'More than 3.5 million sec' END AS range_
FROM Track t
JOIN Album a
ON t.AlbumId = a.AlbumId
WHERE t.Milliseconds > (select AVG(milliseconds) as av from track))
SELECT count(name) as Count  , range_ as Length_range
FROM t1
GROUP BY 2
ORDER BY 1 desc''')


# In[66]:


df14


# In[67]:


fig = px.pie(df14, names='Length_range', values='Count', 
            title='What is the number of songs in each length group?', 
            color_discrete_sequence=px.colors.sequential.RdBu_r)
fig.update_layout(legend_title_text='Length_range')
fig.show()

st.set_page_config (page_title='Digital Music Store Company', page_icon='note.png', layout='wide')
st.title('Digital Music Store Company')
st.markdown(''' This is a web app to show the some information regarding the Digital Music Store Company ''' )
col1 , col2 = st.columns(2)
with col1:
    st.write('')
    st.write('')
    st.write('')
    st.write('')

    st.subheader('“Life is like a piano, the white keys represent happiness and the black shows sadness, but as you go through the life journey, remember that the black keys also makes music.”')
    st.subheader('\t \t \t \t \t \t  ― Me')
with col2:
    st.image('Digital Music.jpeg', width=600)

# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




