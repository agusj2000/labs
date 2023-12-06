eimport pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')



st.header('Bike Sharing Performance :sparkles:')


st.subheader('Daily Performance')


#Load tabel Bike Sharing Day
url = "https://raw.githubusercontent.com/agusj2000/labs/main/day.csv"
Bikeday_df = pd.read_csv(url)
#Bikeday_df = pd.read_csv("day.csv")
#++++++++++++++++++++++++++++++++++
#Bike Sharing ubah tipe ke datetime
datetime_columns = ["dteday"]
 
for column in datetime_columns:
  Bikeday_df[column] = pd.to_datetime(Bikeday_df[column])
#++++++++++++++++++++++++++++++
monthly_Bike_df = Bikeday_df.resample(rule='M', on='dteday').agg({
    "cnt": "sum"
})
monthly_Bike_df.index = monthly_Bike_df.index.strftime('%Y-%m')
monthly_Bike_df = monthly_Bike_df.reset_index()


    
#++++++++++++++++++Membuat Komponen Filter+++++++++++++++++++++++++++
#membuat filter dengan widget date input serta menambahkan logo perusahaan pada sidebar
min_date = Bikeday_df["dteday"].min()
max_date = Bikeday_df["dteday"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu (daily)',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
#Data yang telah difilter ini selanjutnya akan disimpan dalam main_df
Bikeday_df = Bikeday_df[(Bikeday_df["dteday"] >= str(start_date)) & 
                (Bikeday_df["dteday"] <= str(end_date))]

#memanggil helper function yang telah kita buat sebelumnya.
#Bikeday_df = create_DashBikeday_df(main_df)


#    start_month = start_date.month
#    end_month = end_date.month

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    Bikeday_df["dteday"],
    Bikeday_df["cnt"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
plt.xticks(rotation=45)
ax.set_title("Daily Performance", loc="center", fontsize=26)
st.pyplot(fig)



#++++++++++++++++++++
st.subheader('Montly Performance')

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    monthly_Bike_df["dteday"],
    monthly_Bike_df["cnt"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
plt.xticks(rotation=45)
ax.set_title("Montly Performance", loc="center", fontsize=26)
st.pyplot(fig)
#+++++++++++++++++++++++++++++++++++++++++++++
st.subheader('Best Performance Season')

Bikedaynofilter_df = pd.read_csv("day.csv")
sum_order_items_df = Bikedaynofilter_df.groupby("season").cnt.sum().sort_values(ascending=True).reset_index()

fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(4, 3))
colors = ["#4285F4", "#4285F4", "#4285F4", "#4285F4", "#4285F4"]
sns.barplot(x="season", y="cnt", data=sum_order_items_df.sort_values(by="cnt", ascending=True).head(5), palette=colors, ax=ax)
ax.set_ylabel('cnt (total rental bikes)', fontsize=8)
ax.set_xlabel('season (1:springer, 2:summer, 3:fall, 4:winter)', fontsize=6)
ax.tick_params(axis='y', labelsize=6)
ax.tick_params(axis='x', labelsize=6)
ax.set_title("Best Performing Season", loc="center", fontsize=8)




st.pyplot(fig)
