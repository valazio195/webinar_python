import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import altair as alt


st.set_page_config(
    page_title='Sample Population Viz',
    page_icon="✅",
    layout="wide",
)


@st.cache_data
def get_data() -> pd.DataFrame:
    return pd.read_csv('data_clean.csv')

df = get_data()

df['total_laki_laki'] = df['laki-laki_wni'] + df['laki-laki_wna']

df['total_perempuan'] = df['perempuan_wni'] + df['perempuan_wna']

df[['tahun', 'laki-laki_wni', 'perempuan_wni', 'laki-laki_wna', 'perempuan_wna', 'total_laki_laki', 'total_perempuan', 'total_wni', 'total_wna', 'total_populasi']] = df[['tahun', 'laki-laki_wni', 'perempuan_wni', 'laki-laki_wna', 'perempuan_wna', 'total_laki_laki', 'total_perempuan', 'total_wni', 'total_wna', 'total_populasi']].astype(int)



st.title("Population Viz Dashboard")

#Filter
kab_filter = st.selectbox("Pilih Kabupaten", pd.unique(df["nama_kabupaten/kota"]))
#kec_filter = st.selectbox("Pilih Kabupaten", pd.unique(df["nama_kecamatan"]))
#kel_filter = st.selectbox("Pilih Kabupaten", pd.unique(df["nama_kelurahan"]))

df = df[df["nama_kabupaten/kota"] == kab_filter]

df_kec = df.groupby(['nama_kecamatan'])

df_kel = df.groupby(['nama_kelurahan'])


st.sidebar.metric(
    label="Total Populasi",
    value=df['total_populasi'].sum()
)

st.sidebar.metric(
    label="Total Populasi Laki-Laki",
    value=df['total_laki_laki'].sum()
)

st.sidebar.metric(
    label="Total Populasi Perempuan",
    value=df['total_perempuan'].sum()
)

st.sidebar.metric(
    label="Rasio Laki-Laki/Perempuan",
    value= (df['total_laki_laki'].sum()) / (df['total_perempuan'].sum())
)




fig_col1, fig_col2 = st.columns(2)

with fig_col1:
    st.markdown("Bedasarkan Kecamatan")

    chart = (
    alt.Chart(df)
    .mark_bar()
    .encode(
        alt.X("nama_kecamatan"),
        alt.Y("total_populasi"),
        alt.Color("nama_kecamatan"),
        alt.Tooltip(["nama_kecamatan", "total_populasi"]),
    )
    .interactive()
    )
    st.altair_chart(chart)
    #fig_1 = df_kec['total_populasi'].sum().plot.bar(x='nama_kecamatan', y='total_populasi')
    #st.bar_chart(data=df, x='nama_kecamatan', y='total_populasi')
    

with fig_col2:
    top_kel = st.slider('Slide untuk melihat jumlah kelurahan dengan populasi terbanyak: ')
    st.markdown("Bedasarkan Kelurahan")
    top_n_kel= df.groupby('nama_kelurahan').agg({'total_populasi':'sum'})['total_populasi'].nlargest(top_kel)
    top_n_fig = px.bar(top_n_kel, x=top_n_kel.index, y='total_populasi', color=top_n_kel.index)
    st.plotly_chart(top_n_fig, use_container_width = True)
    #fig_2 = df_kel['total_populasi'].sum().plot.bar(x='nama_kelurahan', y='total_populasi')
    #st.bar_chart(data=df, x='nama_kelurahan', y='total_populasi')

cos_1, cos_2 = st.columns(2)

with cos_1:
    labels = 'Laki-Laki' , 'Perempuan'
    arr = [df['total_laki_laki'].sum(), df['total_perempuan'].sum()]
    fig1, ax1 = plt.subplots()
    ax1.pie(arr, labels=labels, autopct='%1.1f%%', shadow=False, startangle=90)
    ax1.axis('equal')  

    st.pyplot(fig1)

df.drop(['Unnamed: 0'], axis=1, inplace=True)
st.dataframe(df)
    



    

