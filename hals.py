import pandas as pd
import numpy as np
import streamlit as st
import folium
import xlsxwriter
from streamlit_folium import st_folium
import io

st.markdown(
    "<h1 style='text-align: center; color: White;'>Data Survey HALS</h1>",
    unsafe_allow_html=True,
)


@st.cache_resource()
def load_data():
    xls = pd.ExcelFile(
        f"https://docs.google.com/spreadsheets/d/1OPjDyMiXwA-uUWY6WLSxxNVvSdWHUzDODrDHSp3h8Lk/export?format=xlsx"
    )

    return xls


xls = load_data()
df = pd.read_excel(xls, "HALS", header=0)
df = df.sort_values(
    by=["Nagari", "Jorong", "Alamat", "Nama"], ascending=[True, True, True, True]
)


Kecamatan = st.sidebar.multiselect(
    "Pilih Nama Kecamatan",
    options=df["Kecamatan"].unique(),
    default=df["Kecamatan"].unique(),
)
df = df[df["Kecamatan"].isin(Kecamatan)]
Nagari = st.sidebar.multiselect(
    "Pilih Nama Nagari",
    options=df["Nagari"].unique(),
    default=df["Nagari"].unique(),
)
df = df[df["Nagari"].isin(Nagari)]
Jorong = st.sidebar.multiselect(
    "Pilih Nama Jorong",
    options=df["Jorong"].unique(),
    default=df["Jorong"].unique(),
)
df = df[df["Jorong"].isin(Jorong)]
Closet = st.sidebar.multiselect(
    "Pilih Status Kepemilikan Kloset",
    options=df["Closet"].unique(),
    default=df["Closet"].unique(),
)
df = df[df["Closet"].isin(Closet)]
Buangan = st.sidebar.multiselect(
    "Pilih Status Buangan Air Limbah",
    options=df["Buangan Limbah"].unique(),
    default=df["Buangan Limbah"].unique(),
)
df = df[df["Buangan Limbah"].isin(Buangan)]
Akses = st.sidebar.multiselect(
    "Pilih Akses Jalan",
    options=df["Akses Jalan"].unique(),
    default=df["Akses Jalan"].unique(),
)
df = df[df["Akses Jalan"].isin(Akses)]


df["No"] = np.tile(np.arange(1, len(df) + 1), len(df))[: len(df)]
df = df.set_index("No")
st.dataframe(df)

# buffer to use for excel writer
buffer = io.BytesIO()
df_download = df.reset_index()
with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
    # Write each dataframe to a different worksheet.
    df_download.to_excel(writer, sheet_name="Sheet1", index=False)

download2 = st.download_button(
    label="Download Excel",
    data=buffer,
    file_name="Data_survey_HALS.xlsx",
    mime="application/vnd.ms-excel",
)

# @st.cache_resource()
# def convert_to_csv(df):
#     # IMPORTANT: Cache the conversion to prevent computation on every rerun
#     return df.to_csv(index=False).encode("utf-8")


# csv = convert_to_csv(df)

# # display the dataframe on streamlit app


# # download button 1 to download dataframe as csv
# download1 = st.download_button(
#     label="Download data as CSV", data=csv, file_name="large_df.csv", mime="text/csv"
# )

location = df[["Nama", "Latitude", "Longitude"]]
location_list = location.to_dict("records")
locationx = location_list[0]
map = folium.Map(location=[-0.3077269515839052, 100.01030796451599], zoom_start=12)
for locationx in location_list:
    coords = (locationx["Latitude"], locationx["Longitude"])
    folium.Marker(coords, popup=locationx["Nama"]).add_to(map)
st.title("Titik Lokasi Penerima Manfaat")
st_data = st_folium(map, width=700, height=400)
# download button 2 to download dataframe as xlsx
