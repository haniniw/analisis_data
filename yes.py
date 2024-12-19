import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set Streamlit page config
st.set_page_config(page_title="Dashboard Dinamis", layout="wide")

# Load data
df_question_one = pd.read_csv("df_question_one.csv")
df_cleaned = pd.read_csv("df_cleaned.csv")

# Sidebar configuration
st.sidebar.header("Filter Data untuk Casual & Resgisteres User")
year_filter = st.sidebar.selectbox("Pilih Tahun", options=df_question_one['yr'].unique(), index=0)
season_filter = st.sidebar.multiselect(
    "Pilih Musim",
    options=df_question_one['season'].unique(),
    default=df_question_one['season'].unique()
)

# Filter data by user selection
filtered_data = df_question_one[(
    df_question_one['yr'] == year_filter) & 
    (df_question_one['season'].isin(season_filter))]

# Group data by season and year, then sum casual and registered users
grouped_data = filtered_data.groupby(['season', 'yr'])[['casual', 'registered']].sum().reset_index()

# Section 1: Bar chart for casual vs registered users
st.header("👥 Casual vs Registered Users by Season and Year")
if not grouped_data.empty:
    fig, ax = plt.subplots(figsize=(12, 6))
    width = 0.35

    # Plot bars for casual and registered users with distinct colors
    casual_bars = ax.bar(grouped_data.index - width / 2, grouped_data['casual'], width, label='Casual', color='#66c2ff')
    registered_bars = ax.bar(grouped_data.index + width / 2, grouped_data['registered'], width, label='Registered', color='#ff9f00')

    # Add value labels on top of each bar
    for bars in [casual_bars, registered_bars]:
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.0f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=10, color='black')

    # Customize the plot
    ax.set_xticks(grouped_data.index)
    ax.set_xticklabels(grouped_data['season'], rotation=45, ha='right', fontsize=12)
    ax.set_xlabel('Season', fontsize=14)
    ax.set_ylabel('Number of Users', fontsize=14)
    ax.set_title(f'Casual vs. Registered Users ({year_filter})', fontsize=16, fontweight='bold', pad=20)
    ax.legend()
    ax.set_ylim(0, 500000)
    plt.tight_layout()
    st.pyplot(fig)

    # Interactive Insight
    with st.expander("💡 Insight Detail"):
        st.markdown(
            """
            Pada tahun 2012, jumlah pengguna **registered** meningkat signifikan dibandingkan tahun 2011 di semua musim. 
            Pengguna **registered** mendominasi penyewaan, terutama pada musim **summer** dan **winter**, yang merupakan puncak aktivitas. 

            📊 **Strategi yang Disarankan:**
            - Fokus pada **promosi** dan **peningkatan kapasitas layanan** selama musim puncak untuk **memaksimalkan pendapatan**.
            
            🌟 Dengan memahami pola musiman dan preferensi pengguna, bisnis dapat merancang **strategi yang lebih efektif** untuk meningkatkan pendapatan dan kepuasan pelanggan.
            """
        )
else:
    st.warning("Tidak ada data untuk filter yang dipilih.")

# Filter data for the year 2011
df_2011 = df_cleaned[df_cleaned['yr'] == 2011]

# Calculate the average 'cnt' for weekdays and weekends
weekday_mean = df_2011[df_2011['weekday'] < 5]['cnt'].mean()  # Weekdays (0-4)
weekend_mean = df_2011[df_2011['weekday'] >= 5]['cnt'].mean()  # Weekends (5-6)

# Create the bar chart with enhanced style
fig, ax = plt.subplots(figsize=(8, 6))
bars = ax.bar(['Weekday', 'Weekend'], [weekday_mean, weekend_mean], color=['#66c2ff', '#ff9f00'])

# Add value labels on top of each bar
for bar, mean in zip(bars, [weekday_mean, weekend_mean]):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{mean:.2f}',
            ha='center', va='bottom', fontsize=12, color='black')

# Set title and labels
ax.set_title('Perbandingan Rata-rata Jumlah Penyewaan pada Weekday dan Weekend (2011)', fontsize=14, fontweight='bold', pad=20)
ax.set_ylabel('Rata-rata Jumlah Penyewaan', fontsize=12)
ax.set_xlabel('Tipe Hari', fontsize=12)
ax.set_ylim(0, 5000)

st.pyplot(fig)

# Interactive Insights with Markdown
st.markdown(
    """
    ## 🔄 **Analisis Penyewaan pada Weekday dan Weekend (2011)**

    📅 Berdasarkan grafik yang ditampilkan, rata-rata penyewaan sepeda pada **hari biasa (weekday)** di tahun 2011 adalah **3378,78**, sedikit lebih rendah dibandingkan **hari libur (weekend)** yang mencapai **3424,82**.
    
    🔄 **Keypoints:**
    - Meskipun ada sedikit peningkatan selama akhir pekan, **aktivitas penyewaan relatif konsisten** sepanjang minggu.
    - Hal ini membuka peluang untuk mempertahankan tingkat penyewaan tinggi sepanjang minggu, khususnya dengan **strategi yang lebih difokuskan pada hari biasa**.

    📈 **Apa yang bisa dilakukan?**
    - **Promosi khusus** atau **peningkatan layanan** pada hari biasa dapat membantu mendongkrak **penggunaan lebih tinggi** sepanjang minggu.
    """
)

# Create a dynamic text box for user input to make the insights interactive
user_input = st.text_input("💬 Berikan pendapat atau idemu untuk meningkatkan penyewaan", "")
if user_input:
    st.write(f"🎉 Terima kasih atas idenya! Ide kerennmu: **{user_input}**")
else:
    st.write("📝 Ayo, berikan ide atau pendapatmu untuk membantu meningkatkan penyewaan sepeda!")
