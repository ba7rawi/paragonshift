import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go


st.set_page_config(
    page_title="Paragon Shift",
    layout="wide",
    initial_sidebar_state="expanded",
)

def curr(n):
    return "${:,.2f}". format(n)

df = pd.read_excel('Data.xlsx')
df['total_amount_for_order'] = df['Sales'] - df['Discount']

pages = ['Sales', 'Discounts', 'Profit', 'Products']


st.sidebar.write('## Paragon Shift')
st.sidebar.write('## Ibrahim Al-Bahri')
page = st.sidebar.selectbox("Menu",pages)

if page == pages[0]:
    st.title('Sales Analysis')
    kpi1, kpi2, kpi3 = st.beta_columns(3)
    with kpi1:
        st.markdown(f"### Total Sales Amount")
        st.markdown(f"<h2 style='text-align: center;color: #d8e131;background-color: #1a322d; width: fit-content; padding:20px'>{curr(df['total_amount_for_order'].sum())}</h1>", unsafe_allow_html=True)
    
    with kpi2:
        st.markdown(f"### Number of Sales Orders")
        st.markdown(f"<h2 style='text-align: center;color: #d8e131;background-color: #1a322d; width: fit-content; padding:20px'>{df['OrderID'].unique().shape[0]}</h1>", unsafe_allow_html=True)
    
    with kpi3:
        monthly_profit = df.groupby(df['OrderDate'].dt.strftime('%Y %B'))['GrossProfit'].sum()
        sorted_monthly_profit = monthly_profit.sort_values(ascending=False)
        st.markdown(f"### The Most successful month in 2020")
        st.markdown(f"<h2 style='text-align: center;color: #d8e131;background-color: #1a322d; width: fit-content; padding:20px'>{sorted_monthly_profit[:1].index[0]}: {curr(sorted_monthly_profit[:1][0])}</h1>", unsafe_allow_html=True)

    
    # 3
    st.markdown("<hr/>",unsafe_allow_html=True)
    n_items = st.slider('Number of Categories to View', 0, df['ProductID'].unique().shape[0],5) 
    d_cat = ((df.groupby(['ProductID']).sum()['Sales']/df['Sales'].sum()) * 100).sort_values(ascending=False)
    fig1 = go.Figure(data=[go.Bar(x=d_cat.index.tolist()[:n_items], y=d_cat.values[:n_items])])
    st.plotly_chart(fig1)
    # 5
    st.markdown('### Monthly Sales')
    monthly_sales = df.groupby(df['OrderDate'].dt.strftime('%Y %B'))['Sales'].sum()
    fig2 = go.Figure(data=[go.Pie(labels=monthly_sales.index.tolist(), values=monthly_sales.values)])
    st.plotly_chart(fig2)

elif page == pages[1]:
    st.title('Discount Analysis')
    number_of_discounts= df['Discount'].astype(bool).sum(axis=0)

    kpi1, kpi2, kpi3 = st.beta_columns(3)
    with kpi1:
        st.markdown(f"### Amount of Total Discount")
        st.markdown(f"<h2 style='text-align: center;color: #d8e131;background-color: #1a322d; width: fit-content; padding:20px'>{curr(df['Discount'].sum())}</h1>", unsafe_allow_html=True)
    
    with kpi2:
        st.markdown(f"### Number of Discounts")
        st.markdown(f"<h2 style='text-align: center;color: #d8e131;background-color: #1a322d; width: fit-content; padding:20px'>{(number_of_discounts)}</h1>", unsafe_allow_html=True)
    
    with kpi3:
        st.markdown(f"### The Percentage of Sales Subjected to Discount")
        ss = "{:,.2f}".format((number_of_discounts/df['Sales'].shape[0])*100)
        st.markdown(f"<h2 style='text-align: center;color: #d8e131;background-color: #1a322d; width: fit-content; padding:20px'>{ ss}%</h1>", unsafe_allow_html=True)

    monthly_discount = df.groupby(df['OrderDate'].dt.strftime('%Y %B'))['Discount'].sum()
    fig3 = go.Figure(data=[go.Pie(labels=monthly_discount.index.tolist(), values=monthly_discount.values)])
    st.plotly_chart(fig3)

elif page == pages[2]:
    st.title('Profit Analysis')
    st.markdown(f"### The Total Profit")
    st.markdown(f"<h2 style='text-align: center;color: #d8e131;background-color: #1a322d; width: fit-content; padding:20px'>{curr(df['GrossProfit'].sum())}</h1>", unsafe_allow_html=True)
    monthly_profit = df.groupby(df['OrderDate'].dt.strftime('%Y %B'))['GrossProfit'].sum()
    
    st.markdown("<hr/>",unsafe_allow_html=True)
    st.markdown('## Monthly Sales')
    fig4 = go.Figure(data=[go.Bar(x=monthly_profit.index.tolist(), y=monthly_profit.values)])
    st.plotly_chart(fig4)

    st.markdown('## Gross Margin')
    df['GrossMargin'] = (df['Sales'] - df['CostOfSales'])/df['Sales']
    n_rows = st.slider('Choose Number of Rows to View', 1, 100, 5)
    st.markdown(f'Showing {n_rows} Rows')
    st.write(df.head(n_rows))

elif page == pages[3]:
    st.title('Products Analysis')
    kpi1, kpi2, kpi3 = st.beta_columns(3)
    with kpi1:
        st.markdown(f"### Number of Different Products")
        st.markdown(f"<h2 style='text-align: center;color: #d8e131;background-color: #1a322d; width: fit-content; padding:20px'>{df['ProductID'].unique().shape[0]}</h1>", unsafe_allow_html=True)
    
    with kpi2:
        mdp = df.groupby(['ProductID']).sum()['Discount'].sort_values(ascending=False)[:1]
        st.markdown(f"### The Most Discounted Prodcut")
        st.markdown(f"<h2 style='text-align: center;color: #d8e131;background-color: #1a322d; width: fit-content; padding:20px'>{mdp.index[0]}: {curr(mdp[0])}</h1>", unsafe_allow_html=True)
    
    with kpi3:
        mpp = df.groupby(['ProductID']).sum()['GrossProfit'].sort_values(ascending=False)[:1]
        st.markdown(f"### The Most Profitable Product")
        st.markdown(f"<h2 style='text-align: center;color: #d8e131;background-color: #1a322d; width: fit-content; padding:20px'>{mpp.index[0]}: {curr(mpp[0])}</h1>", unsafe_allow_html=True)

    st.markdown("<hr/>",unsafe_allow_html=True)
    st.markdown('## The Best N Selling Products')
    n = st.slider('Choose N:', 1, df['ProductID'].unique().shape[0], 5)
    best5 = df.groupby(['ProductID']).sum()['Sales'].sort_values(ascending=False)[:n]
    st.markdown(f'# Best {n}')
    fig5 = go.Figure(data=[go.Pie(labels=best5.index.tolist(), values=best5.values)])
    st.plotly_chart(fig5)

    st.markdown("<hr/>",unsafe_allow_html=True)

    st.markdown('Top 5 Products sells with Product X')

    x = st.selectbox('Choose X:', df['ProductID'].unique())
    products_series = df.groupby(['OrderID'])['ProductID'].transform(lambda x : ','.join(x))


    asscociation_dic = dict(zip(df['ProductID'].unique(), [0]*df['ProductID'].unique().shape[0])) 

    for prod in products_series:
        prod_list = prod.split(',')
        if x in prod_list:
            for i in prod_list:
                asscociation_dic[i] += 1

    sorted_asscociation_dic = {k: v for k, v in sorted(asscociation_dic.items(), key=lambda item: item[1])}

    st.write(f'The Top 5 Products sells with {x} ascendingly: ')
    fig6 = go.Figure(data=[go.Bar(x=list(sorted_asscociation_dic.keys())[-6:-1], y=list(sorted_asscociation_dic.values())[-6:-1] )])
    st.plotly_chart(fig6)