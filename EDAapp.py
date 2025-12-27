# EDA App using Streamlit + Pandas + Seaborn + Matplotlib
# -----------------------------------------------------------
# Features:
# 1. Upload CSV / Excel
# 2. Basic EDA (preview, info, describe, missing, duplicates)
# 3. Column selection (multiselect)
# 4. Multiple visualizations
# 5. Simple query handling (rule-based)


import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from io import StringIO


st.set_page_config(page_title="EDA App", layout="wide")
st.title("📊 Data Science EDA App")


# -------------------------------
# File Upload
# -------------------------------
uploaded_file = st.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])


if uploaded_file:
# Read file
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)


    st.success("File uploaded successfully!")


# -------------------------------
# Basic EDA Section
# -------------------------------
    st.header("🔍 Basic EDA")


    col1, col2 = st.columns(2)


    with col1:
        st.subheader("Preview")
        st.dataframe(df.head())


        st.subheader("Missing Values")
        st.write(df.isnull().sum())


    with col2:
        st.subheader("Dataset Info")
        buffer = StringIO()
        df.info(buf=buffer)
        st.text(buffer.getvalue())


        st.subheader("Duplicate Records")
        st.write(df.duplicated().sum())


    st.subheader("Statistical Summary")
    st.dataframe(df.describe(include='all'))


# -------------------------------
# Column Selection
# -------------------------------
    st.header("🧱 Column Selection")
    selected_cols = st.multiselect("Select columns", df.columns.tolist())


    if selected_cols:
       st.dataframe(df[selected_cols].head())


# -------------------------------
# Visualization Section
# -------------------------------
    st.header("📈 Visualizations")


    if selected_cols:
        plot_type = st.selectbox(
           "Choose plot type",
            ["Histogram", "Boxplot", "Countplot", "Scatterplot", "Correlation Heatmap"]
        )


        fig, ax = plt.subplots()


        if plot_type == "Histogram":
            numeric_col = st.selectbox("Select numeric column", df[selected_cols].select_dtypes(include='number').columns)
            sns.histplot(df[numeric_col], kde=True, ax=ax)


        elif plot_type == "Boxplot":
            numeric_col = st.selectbox("Select numeric column", df[selected_cols].select_dtypes(include='number').columns)
            sns.boxplot(y=df[numeric_col], ax=ax)


        elif plot_type == "Countplot":
            cat_col = st.selectbox("Select categorical column", df[selected_cols].select_dtypes(include='object').columns)
            sns.countplot(x=df[cat_col], ax=ax)
            st.info("Please upload a CSV or Excel file to start.")

        elif plot_type == "Scatterplot":
            num_cols = df[selected_cols].select_dtypes(include='number').columns
            x_col = st.selectbox("X-axis", num_cols)
            y_col = st.selectbox("Y-axis", num_cols)
            sns.scatterplot(x=df[x_col], y=df[y_col], ax=ax)


        elif plot_type == "Correlation Heatmap":
            corr = df[selected_cols].select_dtypes(include='number').corr()
            sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)


        st.pyplot(fig)


# -------------------------------
# Query Section (Rule-Based)
# -------------------------------
st.header("🧠 Ask a Query")
user_query = st.text_input("Enter your query (example: show me top 5 categories)")


if user_query:
    query = user_query.lower()


# Example 1: Top N categories
    if "top" in query and "category" in query:
        n = int(''.join(filter(str.isdigit, query)) or 5)
        cat_col = st.selectbox("Select category column", df.select_dtypes(include='object').columns)
        result = df[cat_col].value_counts().head(n).reset_index()
        result.columns = [cat_col, "count"]
        st.dataframe(result)


# Example 2: Customer service calls > X
    elif "customer service" in query and "more than" in query:
        num = int(''.join(filter(str.isdigit, query)))
        call_col = st.selectbox("Select customer service calls column", df.select_dtypes(include='number').columns)
        result = df[df[call_col] > num]
        st.dataframe(result)


    else:
        st.warning("Query not recognized. Try predefined patterns.")

else:
    st.info("Please upload a CSV or Excel file to start.")