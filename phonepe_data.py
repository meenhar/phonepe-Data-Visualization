import json
import requests
import streamlit as st
from streamlit_option_menu import option_menu
import mysql.connector 
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import pydeck as pdk





# Sql Connection
db_connection=mysql.connector.connect(host="localhost",username="Meenu",password="21Harsha$",database="project2")
curr=db_connection.cursor()

#DataFrame 
# Aggregated insurance

curr.execute("SELECT * FROM agg_insurance")
table1=curr.fetchall()
aggre_insurance=pd.DataFrame(table1,columns=("States","Years","Quarter","Transaction_type","Transaction_count","Transaction_amount"))

#Aggregated Transaction

curr.execute("SELECT * FROM agg_transaction")
table2=curr.fetchall()
aggre_transaction=pd.DataFrame(table2,columns=("States","Years","Quarter","Transaction_type","Transaction_count","Transaction_amount"))

# Aggregated User

curr.execute("SELECT * FROM agg_users")
table3=curr.fetchall()
aggre_users=pd.DataFrame(table3,columns=("States","Years","Quarter","Brands","Transaction_count","Percentage"))


# Map Insurance

curr.execute("SELECT * FROM Map_insurance")
table4=curr.fetchall()
map_ins=pd.DataFrame(table4,columns=("States","Years","Quarter","District","Transaction_count","Transaction_amount"))

# Map Transaction

curr.execute("SELECT * FROM Map_transaction")
table5=curr.fetchall()
map_trans=pd.DataFrame(table5,columns=("States","Years","Quarter","District","Transaction_count","Transaction_amount"))


# Map User

curr.execute("SELECT * FROM Map_users")
table6=curr.fetchall()
map_users=pd.DataFrame(table6,columns=("States","Years","Quarter","District","Registeredusers","AppOpens"))


# Top Insurance

curr.execute("SELECT * FROM top_insurance")
table7=curr.fetchall()
top_ins=pd.DataFrame(table7,columns=("States","Years","Quarter","Pincodes","Transaction_count","Transaction_amount"))


# Top Transaction

curr.execute("SELECT * FROM top_transaction")
table8=curr.fetchall()
top_trans=pd.DataFrame(table8,columns=("States","Years","Quarter","Pincodes","Transaction_count","Transaction_amount"))


# Top User

curr.execute("SELECT * FROM top_users")
table9=curr.fetchall()
top_users=pd.DataFrame(table9,columns=("States","Years","Quarter","Pincodes","Registeredusers"))






#Streamlit part

st.set_page_config(layout= "wide")

st.title("PHONEPE DATA VISUALIZATION AND EXPLORATION")
st.write("")

with st.sidebar:
    select= option_menu("Main Menu",["Home","BUSINESS CASE STUDY"])


if select == "Home":

    col1,col2= st.columns(2)

    with col1:
        st.header("PHONEPE")
        st.subheader("INDIA'S BEST TRANSACTION APP")
        st.markdown("PhonePe  is an Indian digital payments and financial technology company")
        st.write("****FEATURES****")
        st.write("****Credit & Debit card linking****")
        st.write("****Bank Balance check****")
        st.write("****Money Storage****")
        st.write("****PIN Authorization****")
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")
    with col2:
        st.image(Image.open(r"C:\Users\a\Downloads\download.jpg"),width=600)

    col3,col4= st.columns(2)
    
    with col3:
        st.image(Image.open(r"C:\Users\a\Downloads\download (1).jpg"),width=600)

    with col4:
        st.write("****Easy Transactions****")
        st.write("****One App For All Your Payments****")
        st.write("****Your Bank Account Is All You Need****")
        st.write("****Multiple Payment Modes****")
        st.write("****PhonePe Merchants****")
        st.write("****Multiple Ways To Pay****")
        st.write("****1.Direct Transfer & More****")
        st.write("****2.QR Code****")
        st.write("****Earn Great Rewards****")

    col5,col6= st.columns(2)

    with col5:
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.write("****No Wallet Top-Up Required****")
        st.write("****Pay Directly From Any Bank To Any Bank A/C****")
        st.write("****Instantly & Free****")

    with col6:
        st.image(Image.open(r"C:\Users\a\Downloads\download (2).jpg"),width=600)




# ------------------ Database Connection ------------------
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="Meenu",
        password="21Harsha$",
        database="project2"
    )

# ------------------ Business Case Queries ------------------

def run_query(query):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    cols = [i[0] for i in cursor.description]
    data = cursor.fetchall()
    conn.close()
    return pd.DataFrame(data, columns=cols)

# ------------------ Streamlit App ------------------

if select == "BUSINESS CASE STUDY":

    st.title("📊 PhonePe Business Case Study Dashboard")

    
    st.sidebar.title("Select Business Case Study")
    case_study = st.sidebar.selectbox("Choose one:", [
        "1. Transaction Dynamics",
        "2. Device Usage",
        "3. Insurance Engagement",
        "4. User Registration Analysis",
        "5. Insurance Transactions Insights"
    ])

    # ------------------ Visualizations ------------------

    if case_study == "1. Transaction Dynamics":
      st.subheader("📈 Transaction Trends by State and Year")

      df = run_query("""
            SELECT states, years, quarter, SUM(transaction_count) AS total_txns
            FROM agg_transaction
            GROUP BY states, years, quarter
            ORDER BY years, quarter;
        """)

        
      df["year_quarter"] = df["years"].astype(str) + " Q" + df["quarter"].astype(str)

        
      selected_years = st.sidebar.multiselect("Select Year(s):", sorted(df["years"].unique()), default=sorted(df["years"].unique()))
      selected_states = st.sidebar.multiselect("Select State(s):", sorted(df["states"].unique()), default=sorted(df["states"].unique()))

        
      filtered_df = df[df["years"].isin(selected_years) & df["states"].isin(selected_states)]

      if not filtered_df.empty:
            fig = px.bar(
                filtered_df,
                x="states",
                y="total_txns",
                color="states",
                animation_frame="year_quarter",
                title="📊 Transaction Volume by State Over Time",
                labels={"total_txns": "Total Transactions", "states": "State"},
                range_y=[0, float(filtered_df["total_txns"].max()) * 1.1],
            )
            fig.update_layout(xaxis={'categoryorder': 'total descending'}, showlegend=False)
            st.plotly_chart(fig)
      else:
            st.warning("No data available for the selected filters.")


    elif case_study == "2. Device Usage":
        st.subheader("📱 Device Usage by Region")
        df = run_query("""
            SELECT s.states, s.brands, m.total_opens
            FROM agg_users AS s
            INNER JOIN (
                SELECT states, SUM(appopens) AS total_opens
                FROM map_users
                GROUP BY states
            ) AS m ON s.states = m.states;
        """)
        st.markdown("### 🔍 Visualization: Total App Opens by State and Brand")
        fig = px.bar(
            df,
            x='states',
            y='total_opens',
            color='brands',
            barmode='group',
            title='Total PhonePe App Opens by State and Device Brand',
            labels={'states': 'State', 'total_opens': 'Total App Opens'}
        )
        st.plotly_chart(fig)

    elif case_study == "3. Insurance Engagement":
        st.subheader("🔍 Insurance Usage by District")
        df = run_query("""
            SELECT district, SUM(transaction_count) AS txn_count
            FROM map_insurance
            GROUP BY district
            ORDER BY txn_count DESC
            LIMIT 20;
         """)
        fig = px.bar(df, x='district', y='txn_count', title='Top 20 Districts by Insurance Transactions')
        st.plotly_chart(fig)
         
    elif case_study == "4. User Registration Analysis":
         st.subheader("📈 User Registration Trends by State Over Time")

         df = run_query("""
            SELECT states, years, quarter, SUM(registeredusers) AS total_users
            FROM top_users
            GROUP BY states, years, quarter
            ORDER BY years, quarter;
         """)

         df['time'] = df['years'].astype(str) + ' Q' + df['quarter'].astype(str)

    
         df["total_users"] = pd.to_numeric(df["total_users"], errors="coerce")
         top_states = df.groupby("states")["total_users"].sum().nlargest(10).index
         df_top = df[df["states"].isin(top_states)]

         fig = px.line(
            df_top,
            x="time",
            y="total_users",
            color="states",
            title="📊 User Registrations Over Time (Top 10 States)",
            markers=True,
            labels={"time": "Time (Year + Quarter)", "total_users": "Total Registrations"},
        )
         st.plotly_chart(fig, use_container_width=True)
         
    elif case_study == "5. Insurance Transactions Insights":
        st.subheader("🛡️ Insurance Transactions by District")
        df = run_query("""
            SELECT states, district, SUM(transaction_count) AS insurance_txns
            FROM map_insurance
            GROUP BY states, district
            ORDER BY insurance_txns DESC
            LIMIT 20;
        """)
        fig = px.bar(df, x='district', y='insurance_txns', color='states',
                 title='Top Districts by Insurance Transaction Volume')
        st.plotly_chart(fig)

        








