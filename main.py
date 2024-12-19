import pandas as pd 
import streamlit as st 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import PreProcessor

#========================================================================================================#


# Streamlit App Header
st.set_page_config(page_title="Crime Analysis Dashboard", page_icon="🔍")

# st.image("@@", width=130, use_column_width=False) 
st.title("🔍 Crime Analysis Dashboard")
st.subheader("Analyze and visualize crime data to uncover insights.")
st.write("---")

#========================================================================================================#

# Load the cleaned data with proper datetime conversion
df = pd.read_csv("crime_cleaned.csv", parse_dates=['incident_datetime', 'created_at', 'updated_at'])

# Sidebar filters

# st.sidebar.image("logo.jpg", width=280)
st.sidebar.title("🔍 Filters")

# Use PreProcessor's multiselect for city and year filtering
selected_city = PreProcessor.multiselect("Select City", df["city"].unique())
selected_year = PreProcessor.multiselect("Select Year", df["incident_year"].unique())

# Data Filtering
filter_df = df[(df["city"].isin(selected_city)) & (df["incident_year"].isin(selected_year))]

# Metrics
st.markdown("### 👮‍♂️ Crime Data Insights Summary")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Cities Analyzed", filter_df["city"].nunique())
with col2:
    st.metric("Years Analyzed", filter_df["incident_year"].nunique())
with col3:
    st.metric("Incidents", len(filter_df))
with col4:
    st.metric("Total Crime Incidents", len(filter_df), "📈")

st.markdown("---")

#========================================================================================================#

# Total Crimes by City and Year

st.subheader("📈 Total Crimes by City and Year")
crime_summary = filter_df.groupby(["city", "incident_year"]).size().reset_index(name="Total Crime")
fig1 = px.bar(
    crime_summary, x="city", y="Total Crime", color="incident_year",
    barmode="group",
    labels={"Total Crime": "Total Crimes", "city": "City"},
    color_discrete_sequence=px.colors.qualitative.Vivid
)
fig1.update_layout(
    xaxis_title="City", 
    yaxis_title="Total Crimes", 
    xaxis=dict(tickangle=90)
)
st.plotly_chart(fig1, use_container_width=True)

st.markdown(
    """
    <div style='font-size:20px;'> 
        📝Summary: 
        This bar chart displays the total crimes by city and year, helping to identify crime trends and variations across different cities over time.
    """, unsafe_allow_html=True)
st.write("---")

#========================================================================================================#

# Filter Data by Crime Description

df['incident_description'] = df['incident_description'].str.strip()
st.subheader("🔢 Filter Data by Crime Description")
crime_description = st.selectbox("Select Crime Description", df['incident_description'].unique())
filtered_data = filter_df[filter_df['incident_description'] == crime_description]
st.write(f"*Filtered Data Count:*  {len(filtered_data)}")
st.write(filtered_data)
st.write("---")


#========================================================================================================#

# Crime Trends Over Time

st.subheader("📈 Yearly Crime Analysis")
df_yearly = filter_df.groupby('incident_year').size().reset_index(name="Total Crime")
fig1 = px.line(
    df_yearly, x='incident_year', y='Total Crime',
    labels={"Total Crime": "Total Crimes", "incident_year": "Year"},
    color_discrete_sequence=['#99FFFF']
)
st.plotly_chart(fig1, use_container_width=True)

st.markdown(
    """
    <div style='font-size:20px;'> 
        📝Summary: 
        The line graph provides an overview of the crime trends over time. It reveals whether crime rates are increasing or decreasing and highlights specific years where the rates may have peaked or dropped significantly.
    """, unsafe_allow_html=True)
st.write("---")

#========================================================================================================#

# Crimes by Hour of Day

st.subheader("🕒 Crimes by Hour of Day")
df_hourly = filter_df.groupby('hour_of_day').size().reset_index(name="Total Crime")

# Create a bar plot for crimes by hour of day using matplotlib
fig2, ax2 = plt.subplots(figsize=(12, 6))
ax2.bar(df_hourly['hour_of_day'], df_hourly['Total Crime'], color=sns.color_palette("coolwarm", len(df_hourly)))
ax2.set_xlabel('Hour of Day', fontsize=14)
ax2.set_ylabel('Total Crimes', fontsize=14)
ax2.set_title('Crimes by Hour of Day', fontsize=16, weight='bold')
ax2.grid(True, axis='y', linestyle='--', alpha=0.7)
st.pyplot(fig2)

# Summary for Crimes by Hour of Day
st.markdown("""
    <div style='font-size:18px;'>
        <b>📝Summary:</b> This plot illustrates when crime incidents are most likely to occur throughout the day. It helps in identifying times of day when law enforcement might need to allocate more resources, e.g., late-night or early-morning crimes.
    </div>
""", unsafe_allow_html=True)

st.write("---")

#========================================================================================================#

# Crime Incidents by Day of the Week 

fig3 = px.histogram(
    filter_df,
    x='day_of_week',
    category_orders={'day_of_week': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']},
    color='day_of_week',
    color_discrete_sequence=px.colors.qualitative.Set2,
    title='👮‍♂️Crime Incidents by Day of the Week',
    labels={'day_of_week': 'Day of Week', 'count': 'Number of Incidents'}
)
fig3.update_layout(
    xaxis_title='Day of Week',
    yaxis_title='Number of Incidents',
    title_font_size=25,
    xaxis_tickangle=45,
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    bargap=0.2
)
st.plotly_chart(fig3)
# Summary for Crime Incidents by Day of the Week
st.markdown("""
    <div style='font-size:18px;'>
        <b>📑 Summary:</b> This chart reveals the frequency of crime incidents on different days of the week. 
        It is evident that weekends tend to have higher crime incidents, which can help in optimizing police patrols and resources 
        for these days.
    </div>
""", unsafe_allow_html=True)
st.write("---")


#========================================================================================================#


# Heatmap for Crime Incidents by Hour and Day of the Week

heatmap_data = filter_df.groupby(['day_of_week', 'hour_of_day']).size().unstack()

fig4, ax4 = plt.subplots(figsize=(12, 8))
sns.heatmap(heatmap_data, cmap='YlGnBu', annot=True, fmt='d', linewidths=0.5, ax=ax4)
ax4.set_title('Crime Incidents Heatmap (Day of Week vs Hour of Day)', fontsize=16, weight='bold')
ax4.set_xlabel('Hour of Day', fontsize=14)
ax4.set_ylabel('Day of Week', fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
st.pyplot(fig4)

# Summary for Heatmap
st.markdown("""
    <div style='font-size:18px;'>
        <b>📑 Summary:</b> This heatmap shows the relationship between the day of the week and the hour of the day for crime incidents. 
        It helps identify peak crime times, providing valuable information for resource allocation and shift planning for law enforcement.
    </div>
""", unsafe_allow_html=True)
st.write("---")


#========================================================================================================#


# Pie Chart for Parent Incident Type Distribution 

parent_type_counts = filter_df['parent_incident_type'].value_counts()

st.subheader("🔵PieChart of Parent Incident Type Distribution")
fig5 = px.pie(
    parent_type_counts, 
    names=parent_type_counts.index, 
    values=parent_type_counts.values, 
    color=parent_type_counts.index,  
    color_discrete_sequence=px.colors.qualitative.Set3 
)

fig5.update_layout(
    width=800, 
    height=600   
)
st.plotly_chart(fig5, use_container_width=True)

st.markdown(
    """
    <div style='font-size:20px;'>
        <b>📑 Summary:</b> This pie chart shows the distribution of different parent incident types in the dataset. It visualizes the proportion of each type, 
         helping to identify which parent incident types are most common. The chart displays percentages for each category, allowing for easy comparison.
    </div>
    """,
    unsafe_allow_html=True
)
st.write("---")


#========================================================================================================#


# Convert incident_datetime to date-only for grouping

filter_df['incident_date'] = filter_df['incident_datetime'].dt.date

# Group by date and count incidents
incidents_by_date = filter_df.groupby('incident_date').size().reset_index(name='incident_count')

# Create the line graph using plotly.express
fig6 = px.line(
    incidents_by_date,
    x='incident_date',
    y='incident_count',
    title='Number of Incidents Over Time',
    markers=True,  
    line_shape='linear', 
    line_dash_sequence=['solid'],  
    labels={'incident_date': 'Date', 'incident_count': 'Number of Incidents'},
    template='plotly_white'  
)

# Customize the layout for better aesthetics
fig6.update_layout(
    title_font_size=25, 
    xaxis_title_font_size=20,  
    yaxis_title_font_size=20,  
    xaxis_tickangle=-45,  
    width=1000,  
    height=600  
)

st.plotly_chart(fig6, use_container_width=True)
st.markdown(
    """
    <div style='font-size:20px;'>
        <b>📑 Summary:</b> This line graph shows the trend in the number of incidents over time, grouped by date. It helps identify 
        periods with higher or lower crime rates, offering insights into patterns in crime incidents.
    </div>
    """,
    unsafe_allow_html=True
)

st.write("---")

#========================================================================================================#
# Create a boxplot for the 'hour_of_day'
fig7 = px.box(
    filter_df,
    x='hour_of_day',
    title='📅 Boxplot of Crime Incidents by Hour of Day',
    labels={'hour_of_day': 'Hour of Day'},
    color='hour_of_day',
    color_discrete_sequence=px.colors.sequential.Plasma
)
fig7.update_layout(
    title_font_size=25,
    xaxis_title='Hour of Day',
    yaxis_title='Incident Count',
    xaxis_title_font_size = 19,
    yaxis_title_font_size = 19,
    xaxis_tickfont_size=18,
    yaxis_tickfont_size=18,
    plot_bgcolor='#C0C0C0',  

)
st.plotly_chart(fig7)

# Summary for the Boxplot of Crime Incidents by Hour of the Day
st.markdown("""
    <div style='font-size:18px;'>
        <b>📑 Summary:</b> The boxplot illustrates the distribution of crime incidents across different hours of the day. It highlights peak times for crime, helping identify patterns in criminal activity. 
    </div>
""", unsafe_allow_html=True)
st.write("---")

#========================================================================================================#

# Grouping the data by 'incident_month' to get the number of incidents per month
incidents_per_month = df.groupby('incident_month').size().reset_index(name='incident_count')

# Create a line plot for the number of incidents per month
fig8 = px.line(
    incidents_per_month,
    x='incident_month',
    y='incident_count',
    title='📅 Number of Incidents Per Month',
    labels={'incident_month': 'Month', 'incident_count': 'Number of Incidents'},
    line_shape='linear',
    markers=True,
    color_discrete_sequence=['#99FFFF']
)

fig8.update_layout(
    title_font_size=25,
    xaxis_title='Month',
    yaxis_title='Number of Incidents',
    xaxis_title_font_size=18, 
    yaxis_title_font_size=18,
    xaxis_tickfont_size=16,
    yaxis_tickfont_size=16
)

# Display the plot
st.plotly_chart(fig8)

# Summary for the Number of Incidents Per Month line plot
st.markdown("""
    <div style='font-size:18px;'>
        <b>📑 Summary:</b> This line plot shows the trend of crime incidents throughout the months. By analyzing this chart, 
        we can identify seasonal patterns in crime rates and make data-driven decisions on resource allocation during 
        high-crime months.
    </div>
""", unsafe_allow_html=True)
st.write("---")

#========================================================================================================#


# Group by city and count incidents
city_crime_counts = df['city'].value_counts()

# Get the top 10 cities with the highest crime rates
top_10_cities = city_crime_counts.head(10).reset_index()
top_10_cities.columns = ['City', 'Number of Incidents']

# Create the bar chart using Plotly
fig9 = px.bar(
    top_10_cities,
    x='City',
    y='Number of Incidents',
    title='🚨 Top 10 Cities with Highest Crime Rates',
    labels={'City': 'City', 'Number of Incidents': 'Number of Incidents'},
    color='Number of Incidents',
    color_continuous_scale='Viridis',
    text='Number of Incidents' 
)

fig9.update_layout(
    width=1100, 
    height=550,  
    xaxis_tickangle=-45,  
    xaxis={'showgrid': False},  
    yaxis={'showgrid': True},  
    plot_bgcolor='rgba(0,0,0,0)', 
    title_font=dict(size=25),  
    xaxis_title_font=dict(size=18),  
    yaxis_title_font=dict(size=18),  
    xaxis_tickfont=dict(size=14),  
    yaxis_tickfont=dict(size=14)  
)

st.plotly_chart(fig9)

# Summary for the Top 10 Cities with Highest Crime Rates
st.markdown("""
    <div style='font-size:18px;'>
        <b>📑 Summary:</b> This chart shows the top 10 cities with the highest crime rates, helping to identify areas with the most criminal activity.
    </div>
""", unsafe_allow_html=True)
st.write("---")

#========================================================================================================#



## Footer Section 

st.markdown(
    """
    <footer style='text-align: center; padding: 10px 20px; border-top: 5px solid #ddd; font-size: 19px; color: #dcdcdc; margin-top:50px;'>
    
    <strong>Project Code:</strong> [B41_DA_009_Number Crunchers] 
    <p><strong>Credits :</strong>
    The following team members contributed to the collaborative development of this project:</p>
    <ul style="list-style-type: none; padding: 0; font-size: 19px; color: #dcdcdc;">
        <li>🔹 <strong>Ishita :</strong> Compilation of Report and Final Presentation</li>
        <li>🔹 <strong>Krishna :</strong> Data Analysis and Insight Extraction</li>
        <li>🔹 <strong>Ashutosh :</strong> Visualization of Data and Dashboard Design</li>
    </ul>
    
    <p style="font-size: 14px; color: #dcdcdc;">🛠️ Developed with ❤️ by the Number Crunchers Team.</p>
    <p style="font-size: 18px; color: #dcdcdc;">For feedback or inquiries, email us at <a href="mailto:team@numbercrunchers.com" style="color: #66b3ff;">team@recyclerangers.com</a></p>
    
    <p><small style="color: #aaa;">© 2024 Number Crunchers. All rights reserved.</small></p>
    
    </footer>
    """,
    unsafe_allow_html=True
)


###############################################################################################################


