from functions import *
import streamlit as st
import datetime
import warnings
import altair as alt
import plotly.express as px
import functions
from datetime import datetime
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore")

df = pd.read_csv("Telco-Customer-Churn.csv")
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors='coerce')
df["Churn"] = df["Churn"].apply(lambda x : 1 if x == "Yes" else 0)

st.set_page_config(page_title="Miuul x YetGen Streamlit Eğitimi")
tabs = ["Giriş", "Keşifsel Veri Analizi", "Tahminleme"]

page = st.sidebar.radio("Sayfalar", tabs)
current_time = datetime.now().strftime("%d-%m-%Y")
st.sidebar.info("Bugünün Tarihi: {}".format(current_time))
# Kullanıcı adını al
name = st.sidebar.text_input("Adınızı Girin")
# Kullanıcının adına özel bir mesaj görüntüle
if name:
    st.sidebar.write(f"Merhaba {name}")
    st.sidebar.write("Bu eğitim nasıl geçiyor?")
    option = st.sidebar.selectbox("Seçenekler", ["Lütfen Cevap Seçiniz", "Süper", "Mükemmel"])
    if option != "Lütfen Cevap Seçiniz":
        st.sidebar.write("HARİKA, bunu duyduğumu sevindim.")

st.sidebar.markdown("""[Miuul - Instagram](https://www.instagram.com/miuul.official/)""")
st.sidebar.markdown("""[YetGen - Instagram](https://www.instagram.com/yetkingencler/)""")
st.sidebar.info("""Kişisel Hesaplarım""")
st.sidebar.markdown("""[Anıl Şanlı - LinkedIn](https://www.linkedin.com/in/anilsanli/)""")
st.sidebar.markdown("""[Anıl Şanlı - GitHub](https://github.com/anilsanli)""")
st.sidebar.info("""Diğer Projeler""")
st.sidebar.markdown("""[WhatsApp Chat Analysis](https://whatsapp-group-chat-analysis.herokuapp.com)""")

if page == "Giriş":
    st.markdown("<h1 style='text-align:center;'>Miuul x YetGen Streamlit Eğitimi</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center;'>Açılış Sayfası</h2>", unsafe_allow_html=True)

    st.write(
        """Bu site Miuul x YetGen Veri Bilimi Dikey Programı Streamlit Eğitimi için hazırlanmıştır.""")
    st.write(
        """Site 3 sayfadan oluşmaktadır. Sayfalara sol menüden erişebilirsiniz.""")
    st.write("""1. Açılış Sayfası""")
    st.write("""2. Keşifsel Veri Analizi Sayfası""")
    st.write("""3. Tahminleme Sayfası""")

    st.write(
        """Telco Customer Churn Projesi üzerinden çalışma yapılmıştır.""")
    st.write(
        """Keşifsel Veri Analizi sayfasında veriyi ve grafikleri inceleyebilirsiniz.""")
    st.write(
        """Tahminleme sayfasında eğitim-test verilerinin skorlarını görebilir ve müşteriler için tahmin yapabilirsiniz.""")
    st.checkbox("Hazır Mıyız?")
    slider_value = st.slider("Ne Kadar Hazırız?", 0, 100)

elif page == "Keşifsel Veri Analizi":
    st.markdown("<h1 style='text-align:center;'>Miuul x YetGen Streamlit Eğitimi</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center;'>Keşifsel Veri Analizi Sayfası</h2>", unsafe_allow_html=True)

    st.markdown("<h3 style='text-align:left;'>Genel Bilgiler</h3>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([5, 5, 5])
    col1.metric("Verinin Şekli:", str(df.shape))
    col2.metric('Gözlem Sayısı:', df.shape[0])
    col3.metric("Değişken Sayısı:", df.shape[1])

    cat_cols, num_cols, cat_but_car, num_but_cat = grab_col_names(df)

    st.markdown("<h3 style='text-align:left;'>Değişken Bilgileri</h3>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns([5, 5, 5, 5])
    col1.metric("Kategorik:", len(cat_cols))
    col2.metric('Numerik:', len(num_cols))
    col3.metric("Kategorik-Kardinal:", len(cat_but_car))
    col4.metric("Numerik-Kategorik:", len(num_but_cat))

    st.markdown("<h3 style='text-align:left;'>Değişkenler</h3>", unsafe_allow_html=True)
    st.write("Kategorik Değişkenler:")
    st.write(str(cat_cols))
    st.write("Numerik Değişkenler:", num_cols)
    st.write("Kategorik fakat Kardinal Değişkenler:", cat_but_car)
    st.write("Numerik fakat Kategorik Değişkenler:", num_but_cat)

    st.markdown("<h3 style='text-align:left;'>Veriye Yukarıdan Bakış</h3>", unsafe_allow_html=True)
    n = st.number_input('Yukarıdan Kaç Gözlemi Görmek İstediğinizi Seçin (1-10):', min_value=1, max_value=10, value=5, step=1)
    st.write(df.head(n))

    st.markdown("<h3 style='text-align:left;'>Cinsiyete Göre Kontrat Tipi</h3>", unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(8, 8))
    sns.countplot(data=df, x='Contract', hue='gender', ax=ax)
    st.pyplot(fig)

    st.markdown("<h3 style='text-align:left;'>Korelasyon Matrix</h3>", unsafe_allow_html=True)
    plot_corr_matrix(df, num_cols)

elif page == "Tahminleme":
    st.markdown("<h1 style='text-align:center;'>Miuul x YetGen Streamlit Eğitimi</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center;'>Tahminleme Sayfası</h2>", unsafe_allow_html=True)

    cat_cols, num_cols, cat_but_car, num_but_cat = grab_col_names(df)
    binary_cols = [col for col in df.columns if df[col].dtypes == "O" and df[col].nunique() == 2]

    for col in binary_cols:
        df = label_encoder(df, col)

    cat_cols = [col for col in cat_cols if col not in binary_cols and col not in ["Churn", "NEW_TotalServices"]]
    df = one_hot_encoder(df, cat_cols, drop_first=True)

    st.markdown("<h3 style='text-align:left;'>Ön-İşlemeden Sonraki Genel Bilgiler</h3>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([5, 5, 5])
    col1.metric("Verinin Şekli:", str(df.shape))
    col2.metric('Gözlem Sayısı:', df.shape[0])
    col3.metric("Değişken Sayısı:", df.shape[1])

    cat_cols, num_cols, cat_but_car, num_but_cat = grab_col_names(df)

    st.markdown("<h3 style='text-align:left;'>Değişken Bilgileri</h3>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns([5, 5, 5, 5])
    col1.metric("Kategorik:", len(cat_cols))
    col2.metric('Numerik:', len(num_cols))
    col3.metric("Kategorik-Kardinal:", len(cat_but_car))
    col4.metric("Numerik-Kategorik:", len(num_but_cat))

    X_train, X_test, y_train, y_test = split_data(df, test_size=0.30, random_state=17)
    model, accuracy, recall, precision, f1, auc = evaluate_model(X_train, y_train, X_test, y_test)

    st.markdown("<h3 style='text-align:left;'>Model Bilgileri</h3>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([10, 5, 5])
    col1.metric("Kullanılan Model:", model.__class__.__name__)
    col3.metric('Accuracy Skoru:', accuracy)

    col1, col2, col3, col4 = st.columns([5, 5, 5, 5])
    col1.metric("Recall Skoru:", recall)
    col2.metric("Precision Skoru:", precision)
    col3.metric('F1 Skoru:', f1)
    col4.metric("AUC Skoru:", auc)

    st.markdown("<h2 style='text-align:left;'>Yeni Bir Kullanıcı İçin Tahmin Yapalım</h2>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns([5, 5, 5, 5])
    customerid_input = col1.number_input("CustomerID", step = 1)
    gender_input = col2.selectbox("Gender", ["Female", "Male"])
    seniorcitizen_input = col3.selectbox("SeniorCitizen", [1, 0])
    partner_input = col4.selectbox("Partner", ["Yes", "No"])

    col1, col2, col3, col4 = st.columns([5, 5, 5, 5])
    dependents_input = col1.selectbox("Dependents", ["Yes", "No"])
    tenure_input = col2.number_input("Tenure", step = 1)
    phoneservice_input = col3.selectbox("Phone Service", ["Yes", "No"])
    multiplelines_input = col4.selectbox("MulitpleLines", ["Yes", "No", "No phone service"])

    col1, col2, col3, col4 = st.columns([5, 5, 5, 5])
    internetservice_input = col1.selectbox("Internet Service", ["No", "DSL", "Fiber optic"])
    onlinesecurity_input = col2.selectbox("Online Security", ["Yes", "No", "No internet service"])
    onlinebackup_input = col3.selectbox("Online Backup", ["Yes", "No", "No internet service"])
    deviceprotection_input = col4.selectbox("Device Protection", ["Yes", "No", "No internet service"])

    col1, col2, col3, col4 = st.columns([5, 5, 5, 5])
    techsupport_input = col1.selectbox("Tech Support", ["Yes", "No", "No internet service"])
    streamingtv_input = col2.selectbox("Streaming TV", ["Yes", "No", "No internet service"])
    streamingmovies_input = col3.selectbox("Streaming Movies", ["Yes", "No", "No internet service"])
    contract_input = col4.selectbox("Contact", ["Month-to-month", "Two year", "One year"])

    col1, col2, col3, col4 = st.columns([5, 5, 5, 5])
    paperlessbilling_input = col1.selectbox("Paperless Billing", ["Yes", "No"])
    paymentmethod_input = col2.selectbox("Payment Method", ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"])
    monthlycharges_input = col3.number_input("Monthly Charges")
    totalcharges_input = col4.number_input("Total Charges")

    input_list = [customerid_input, gender_input, seniorcitizen_input, partner_input,
                  dependents_input, tenure_input, phoneservice_input, multiplelines_input,
                  internetservice_input, onlinesecurity_input, onlinebackup_input, deviceprotection_input,
                  techsupport_input, streamingtv_input, streamingmovies_input, contract_input,
                  paperlessbilling_input, paymentmethod_input, monthlycharges_input, totalcharges_input]

    sample_df = pd.DataFrame()

    # gender
    if gender_input == "Female":
        sample_df.loc[0, "gender"] = 0
    else:
        sample_df.loc[0, "gender"] = 1
    # Partner
    if partner_input == "Yes":
        sample_df.loc[0, "Partner"] = 1
    else:
        sample_df.loc[0, "Partner"] = 0
    # Dependents
    if dependents_input == "Yes":
        sample_df.loc[0, "Dependents"] = 1
    else:
        sample_df.loc[0, "Dependents"] = 0
    # tenure
    sample_df.loc[0, "tenure"] = tenure_input
    # PhoneService
    if phoneservice_input == "Yes":
        sample_df.loc[0, "PhoneService"] = 1
    else:
        sample_df.loc[0, "PhoneService"] = 0
    # PaperlessBilling
    if dependents_input == "Yes":
        sample_df.loc[0, "PaperlessBilling"] = 1
    else:
        sample_df.loc[0, "PaperlessBilling"] = 0
    # MonthlyCharges
    sample_df.loc[0, "MonthlyCharges"] = monthlycharges_input
    # TotalCharges
    sample_df.loc[0, "TotalCharges"] = totalcharges_input
    # MultipleLines
    if multiplelines_input == "Yes":
        sample_df.loc[0, "MultipleLines_No phone service"] = 0
        sample_df.loc[0, "MultipleLines_Yes"] = 1
    elif multiplelines_input == "No":
        sample_df.loc[0, "MultipleLines_No phone service"] = 0
        sample_df.loc[0, "MultipleLines_Yes"] = 0
    else:
        sample_df.loc[0, "MultipleLines_No phone service"] = 1
        sample_df.loc[0, "MultipleLines_Yes"] = 0
    # InternetService
    if internetservice_input == "No":
        sample_df.loc[0, "InternetService_Fiber optic"] = 0
        sample_df.loc[0, "InternetService_No"] = 1
    elif internetservice_input == "Fiber optic":
        sample_df.loc[0, "InternetService_Fiber optic"] = 1
        sample_df.loc[0, "InternetService_No"] = 0
    else:
        sample_df.loc[0, "InternetService_Fiber optic"] = 0
        sample_df.loc[0, "InternetService_No"] = 0
    # OnlineSecurity
    if onlinesecurity_input == "Yes":
        sample_df.loc[0, "OnlineSecurity_No internet service"] = 0
        sample_df.loc[0, "OnlineSecurity_Yes"] = 1
    elif onlinesecurity_input == "No":
        sample_df.loc[0, "OnlineSecurity_No internet service"] = 0
        sample_df.loc[0, "OnlineSecurity_Yes"] = 0
    else:
        sample_df.loc[0, "OnlineSecurity_No internet service"] = 1
        sample_df.loc[0, "OnlineSecurity_Yes"] = 0
    # OnlineBackup
    if onlinebackup_input == "Yes":
        sample_df.loc[0, "OnlineBackup_No internet service"] = 0
        sample_df.loc[0, "OnlineBackup_Yes"] = 1
    elif onlinebackup_input == "No":
        sample_df.loc[0, "OnlineBackup_No internet service"] = 0
        sample_df.loc[0, "OnlineBackup_Yes"] = 0
    else:
        sample_df.loc[0, "OnlineBackup_No internet service"] = 1
        sample_df.loc[0, "OnlineBackup_Yes"] = 0
    # DeviceProtection
    if deviceprotection_input == "Yes":
        sample_df.loc[0, "DeviceProtection_No internet service"] = 0
        sample_df.loc[0, "DeviceProtection_Yes"] = 1
    elif deviceprotection_input == "No":
        sample_df.loc[0, "DeviceProtection_No internet service"] = 0
        sample_df.loc[0, "DeviceProtection_Yes"] = 0
    else:
        sample_df.loc[0, "DeviceProtection_No internet service"] = 1
        sample_df.loc[0, "DeviceProtection_Yes"] = 0
    # TechSupport
    if techsupport_input == "Yes":
        sample_df.loc[0, "TechSupport_No internet service"] = 0
        sample_df.loc[0, "TechSupport_Yes"] = 1
    elif techsupport_input == "No":
        sample_df.loc[0, "TechSupport_No internet service"] = 0
        sample_df.loc[0, "TechSupport_Yes"] = 0
    else:
        sample_df.loc[0, "TechSupport_No internet service"] = 1
        sample_df.loc[0, "TechSupport_Yes"] = 0
    # StreamingTV
    if streamingtv_input == "Yes":
        sample_df.loc[0, "StreamingTV_No internet service"] = 0
        sample_df.loc[0, "StreamingTV_Yes"] = 1
    elif streamingtv_input == "No":
        sample_df.loc[0, "StreamingTV_No internet service"] = 0
        sample_df.loc[0, "StreamingTV_Yes"] = 0
    else:
        sample_df.loc[0, "StreamingTV_No internet service"] = 1
        sample_df.loc[0, "StreamingTV_Yes"] = 0
    # StreamingMovies
    if streamingmovies_input == "Yes":
        sample_df.loc[0, "StreamingMovies_No internet service"] = 0
        sample_df.loc[0, "StreamingMovies_Yes"] = 1
    elif streamingmovies_input == "No":
        sample_df.loc[0, "StreamingMovies_No internet service"] = 0
        sample_df.loc[0, "StreamingMovies_Yes"] = 0
    else:
        sample_df.loc[0, "StreamingMovies_No internet service"] = 1
        sample_df.loc[0, "StreamingMovies_Yes"] = 0
    # Contact
    if contract_input == "One year":
        sample_df.loc[0, "Contract_One year"] = 1
        sample_df.loc[0, "Contract_Two year"] = 0
    elif contract_input == "Two year":
        sample_df.loc[0, "Contract_One year"] = 0
        sample_df.loc[0, "Contract_Two year"] = 1
    else:
        sample_df.loc[0, "Contract_One year"] = 0
        sample_df.loc[0, "Contract_Two year"] = 0
    # PaymentMethod
    if paymentmethod_input == "Credit card (automatic)":
        sample_df.loc[0, "PaymentMethod_Credit card (automatic)"] = 1
        sample_df.loc[0, "PaymentMethod_Electronic check"] = 0
        sample_df.loc[0, "PaymentMethod_Mailed check"] = 0
    elif paymentmethod_input == "Electronic check":
        sample_df.loc[0, "PaymentMethod_Credit card (automatic)"] = 0
        sample_df.loc[0, "PaymentMethod_Electronic check"] = 1
        sample_df.loc[0, "PaymentMethod_Mailed check"] = 0
    elif paymentmethod_input == "Mailed check":
        sample_df.loc[0, "PaymentMethod_Credit card (automatic)"] = 0
        sample_df.loc[0, "PaymentMethod_Electronic check"] = 0
        sample_df.loc[0, "PaymentMethod_Mailed check"] = 1
    else:
        sample_df.loc[0, "PaymentMethod_Credit card (automatic)"] = 0
        sample_df.loc[0, "PaymentMethod_Electronic check"] = 0
        sample_df.loc[0, "PaymentMethod_Mailed check"] = 0
    # SeniorCitizen
    if seniorcitizen_input == 1:
        sample_df.loc[0, "SeniorCitizen_1"] = 1
    else:
        sample_df.loc[0, "SeniorCitizen_1"] = 0

    result = forecast_sample(model, sample_df)

    if result == 0:
        st.markdown("<h4 style='text-align:center;'>Bu müşterinin churn OLMAYACAĞI tahmin ediliyor</h4>", unsafe_allow_html=True)
    else:
        st.markdown("<h4 style='text-align:center;'>Bu müşterinin churn OLACAĞI tahmin ediliyor</h4>", unsafe_allow_html=True)
