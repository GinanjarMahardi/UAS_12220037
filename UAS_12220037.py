#Ginanjar Mahardi 12220037

import streamlit as st
import pandas as pd
import json
import matplotlib.pyplot as plt


# Pembacaan file sumber dataset menjadi variabel, dfM untuk data minyah mentah, dfN untuk data negara

dfM = pd.read_csv('produksi_minyak_mentah.csv', index_col="kode_negara")
dfN = pd.read_json("kode_negara_lengkap.json")

# cleaning data dengan cara bila tidak ada negara 
# data yang sama pada kedua dataset, maka akan dihapus
for kode in dfM.index.unique().tolist():
    if kode not in dfN['alpha-3'].tolist():
        dfM.drop([kode], inplace=True)
dfM.reset_index(inplace=True)

negara = []

usedList = dfM['kode_negara'].unique().tolist()

for ele in usedList:
    negara.append(dfN.loc[dfN['alpha-3'] == ele].values[0][0])

#Membuat Grafik line
def grafik_line(grafik):
    st.write('Grafik:')
    st.line_chart(grafik)
    st.write('Tabel data : ')
    st.dataframe(grafik)

#Membuat Grafik Batang
def grafik_tabel(grafik):
    st.write('Grafik: ')
    st.bar_chart(grafik)
    st.write('Tabel data : ')
    st.dataframe(grafik)

# Menyederhanakan dataframe agar tidak menampilkan data berulang
def write_dataframe(source_data_frame,data_frame=pd.DataFrame()):
    
    # Pencarian suatu key dari sumber dataset
    source_kode = source_data_frame['kode_negara'].values[0]
    source_nama = dfN[dfN["alpha-3"] == source_kode]["name"].values[0]
    source_region = dfN[dfN["name"] == source_nama]["region"].values[0]
    source_subregion = dfN[dfN["name"] == source_nama]["sub-region"].values[0]
    source_tahun = source_data_frame['produksi'].values[0]
   
    # Assign output
    data_frame['Nama'] = data_frame.append({'Nama':source_nama}, ignore_index=True)
    data_frame['Kode'] = source_kode
    data_frame['Region'] = source_region
    data_frame['Sub-region'] = source_subregion
    data_frame['Produksi'] = source_tahun
    return data_frame

#Membuat judul dari aplikasi
st.title("""Aplikasi Informasi Produksi Minyak Mentah di Dunia""")

# Membuat Header
mainHeader = st.container()
with mainHeader:
    st.markdown("# ")
    st.markdown("***")
    st.markdown("---")

# Container untuk grafik produksi suatu negara
produksi_pernegara = st.container()
with produksi_pernegara:
    st.markdown("### Grafik jumlah produksi minyak mentah terhadap waktu (tahun) dari suatu negara N ")

    # Input pilihan negara berupa dropdown
    pilihan_negara = st.selectbox("Pilih negara", negara)

    kode_negara = dfN[dfN["name"] == pilihan_negara]["alpha-3"].values[0]
    display_data = dfM[dfM["kode_negara"] == kode_negara][['tahun', 'produksi']]
    display_data = display_data.rename(columns={'tahun':'index'}).set_index('index')
    grafik_line(display_data)
    
# Container untuk grafik minyak tertinggi pada tiap tahunnya
grafik_minyak_tertinggi_pertahun = st.container()
with grafik_minyak_tertinggi_pertahun:
    try:
        st.markdown("***")
        st.markdown('### Grafik yang menunjukan B-besar negara dengan jumlah produksi terbesar pada tahun T')
       
        # Input untuk tahun
        inputTahun = st.number_input('Tahun : ', min_value=1971, max_value=2015,value=1972, step=1)
       
        # Input untuk jumlah peringkat
        jumlahPeringkat = st.number_input('Jumlah Negara : ', value=5, step=1)
        tahunM = dfM.loc[dfM["tahun"] == int(inputTahun)].sort_values(["produksi"], ascending=[0])
        tahunM = tahunM[:int(jumlahPeringkat)].reset_index(drop=True)
        tahunMWrite = tahunM[['kode_negara', 'produksi']].rename(columns={'kode_negara':'index'}).set_index('index')
        grafik_tabel(tahunMWrite)
    except Exception:
        st.write('Ada kesalahan dalam input anda')

# Container untuk grafik minyak tertinggi secara keseluruhan
grafik_minyak_tertinggi_pertahun = st.container()
with grafik_minyak_tertinggi_pertahun:
    try:
        st.markdown("***")
        st.markdown('### Grafik yang menunjukan B-besar negara dengan jumlah produksi terbesar secara kumulatif keseluruhan tahun')
        
        # Number Input Untuk Tahun
        inputTahun = st.number_input('Tahun :', min_value=1971, max_value=2015,value=1972, step=1)
        
        # Input Jumlah negara
        jumlahPeringkat = st.number_input ('Jumlah :', value=5, step=1)
        tahunM = dfM.loc[dfM["tahun"] == int(inputTahun)].sort_values(["produksi"], ascending=[0])
        tahunM = tahunM[:int(jumlahPeringkat)].reset_index(drop=True)
        tahunMWrite = tahunM[['kode_negara', 'produksi']].rename(columns={'kode_negara':'index'}).set_index('index')
        grafik_tabel(tahunMWrite)
    except Exception:
        st.write('Ada kesalahan dalam input anda')


# Countainer Menampilkan informasi lengkap dari suatu negara
informasi = st.container()
with informasi:
    st.write('')
    st.markdown('## Informasi mengenai Produksi')
    dfNol = dfM[dfM['produksi'] == 0]
    dfNol.reset_index(inplace=True)
    df0 = dfNol['kode_negara'].unique()
    dfNolWrite = pd.DataFrame()
    dfNolWrite['nama_negara'] = [dfN[dfN['alpha-3'] == x]['name'].values[0] for x in df0]
    dfNolWrite['kode_negara'] = [ct for ct in df0]
    dfNolWrite['region'] = [dfN[dfN['alpha-3'] == x]['region'].values[0] for x in df0]
    dfNolWrite['subregion'] = [dfN[dfN['alpha-3'] == x]['sub-region'].values[0] for x in df0]
    dfNolWrite['Tahun'] = [dfM[dfM['kode_negara'] == x]['tahun'].values[0] for x in df0]
    dfNolWrite['produksi'] = [dfM[dfM['kode_negara'] == x]['produksi'].values[0] for x in df0]

    informasi_d = st.selectbox('Pilih Data : ', ['Produksi Terbesar Kumulatif', 'Produksi Terbesar dalam Tahun', 'Produksi Terkecil Kumulatif', 'Produksi Terkecil dalam Tahun', 'Produksi nol dalam Tahun', 'Produksi nol Kumulatif'])
    if informasi_d == 'Produksi Terbesar dalam Tahun':
        try:
            # Input tahun
            maxInputTahun = st.number_input('Tahun', min_value=1971, max_value=2015,value=1972, step=1)
            
            # Sort dari yang terbesar
            dfMax = dfM[dfM['tahun'] == int(maxInputTahun)]['produksi'].idxmax()
            st.table(write_dataframe(dfM[dfMax:dfMax+1]))
            st.info("Apabila terdapat error atau tidak muncul data, maka data tidak ditemukan")
        except Exception:
            pass

    elif informasi_d == 'Produksi Terbesar Kumulatif':
        # Sort dari yang terbesar
        dfMax = dfM['produksi'].idxmax()
        st.write(write_dataframe(dfM[dfMax:dfMax+1]))

    elif informasi_d == 'Produksi Terkecil dalam Tahun':
        
        # Input tahun
        minInputTahun = st.number_input('Tahun yang akan dicek untuk minimum', min_value=1971, max_value=2015,value=1972, step=1)
        dfMin = dfM[dfM['tahun'] == int(minInputTahun)]
        
        # Mencari produksi yang tidak kosong
        dfMin = dfMin[dfMin['produksi'] != 0]
        dfMinID = dfMin['produksi'].idxmin()
        st.table(write_dataframe(dfM[dfMinID:dfMinID+1]))

    elif informasi_d == 'Produksi Terkecil Kumulatif':
        dfMin = dfM[dfM['produksi'] > 0]
        dfMin.reset_index(inplace=True)
        dfMinID = dfMin['produksi'].idxmin()
        st.table(write_dataframe(dfMin[dfMinID:dfMinID+1]))
        st.info("Apabila terdapat error atau tidak muncul data, maka data tidak ditemukan")

    elif 'nol' in informasi_d:
        
        # Mencari yang produksi Kosong
        df0_prod= dfM[dfM['produksi'] == 0]
        df0_prod.reset_index(inplace=True)
        nama,region,subregion = [],[],[]
        
        for _, row in df0_prod.iterrows():
            kode = row['kode_negara']
            nama.append(dfN[dfN['alpha-3'] == kode]['name'].values[0])
            region.append(dfN[dfN['alpha-3'] == kode]['region'].values[0])
            subregion.append(dfN[dfN['alpha-3'] == kode]['sub-region'].values[0])
        df0_prod['Nama'] = nama
        df0_prod['Region'] = region
        df0_prod['Subregion'] = subregion
        if 'keseluruhan' not in informasi_d:
            
            # Input tahun
            t_inp = st.number_input('Tahun Produksi Kosong', min_value=1971, max_value=2015, value=1972 ,step=1)
            df0_showF = df0_prod[df0_prod['tahun'] == int(t_inp)]
            df0_showF.reset_index(inplace=True)
            st.dataframe(df0_showF.filter(items=['Nama', 'kode_negara', 'Region', 'Subregion']))
        else:
            st.dataframe(df0_prod.filter(items=['Nama', 'kode_negara', 'Region', 'Subregion']).drop_duplicates().drop(index=0).reset_index(drop=True))