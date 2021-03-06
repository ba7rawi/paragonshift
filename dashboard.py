import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

pd.options.display.float_format = "{:,.2f}".format
st.set_page_config(
    page_title="Paragon Shift",
    layout="wide",
    initial_sidebar_state="expanded",
)

def curr(n):
    return "${:,.2f}". format(n)

def plot_table(df):
    """
    documentaion
    """
    fig = go.Figure(data=[go.Table(
        header=dict(values=df.columns,
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[df[col] for col in df.columns],
                fill_color='lavender',
                align='left'))
    ])
    st.plotly_chart(fig, use_container_width=True)

def get_product_name(id):
    if type(id) == str:
        return df2[df2['ProductID'] == id]['ProductName'].values[0]
    elif type(id) == list:
        return [df2[df2['ProductID'] == i]['ProductName'].values[0] for i in id]
    else:
        return "Invalid Id Type"
    
df = pd.read_excel('Data.xlsx')
df1 = df
df2 = pd.read_excel('Data.xlsx', 'Products')
df3 = df1.merge(df2,on='ProductID',how='left')

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
    d_cat = ((df3.groupby(['CategoryID']).sum()['Sales']/df3['Sales'].sum()) * 100).sort_values(ascending=False)
    fig1 = go.Figure(data=[go.Bar(x=d_cat.index.tolist(), y=d_cat.values)])
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
    df['GrossMargin'] = df['GrossMargin'].astype(float)
    n_rows = st.slider('Choose Number of Rows to View', 1, 100, 5)
    st.markdown(f'Showing {n_rows} Rows')
    plot_table(df.head(n_rows))

elif page == pages[3]:
    st.title('Products Analysis')
    kpi1, kpi2, kpi3 = st.beta_columns(3)
    with kpi1:
        st.markdown(f"### Number of Different Products")
        st.markdown(f"<h2 style='text-align: center;color: #d8e131;background-color: #1a322d; width: fit-content; padding:20px'>{df['ProductID'].unique().shape[0]}</h1>", unsafe_allow_html=True)
    
    with kpi2:
        mdp = df.groupby(['ProductID']).sum()['Discount'].sort_values(ascending=False)[:1]
        st.markdown(f"### The Most Discounted Prodcut")
        st.markdown(f"<h2 style='text-align: center;color: #d8e131;background-color: #1a322d; width: fit-content; padding:20px'>{get_product_name(mdp.index[0])}: {curr(mdp[0])}</h1>", unsafe_allow_html=True)
    
    with kpi3:
        mpp = df.groupby(['ProductID']).sum()['GrossProfit'].sort_values(ascending=False)[:1]
        st.markdown(f"### The Most Profitable Product")
        st.markdown(f"<h2 style='text-align: center;color: #d8e131;background-color: #1a322d; width: fit-content; padding:20px'>{get_product_name(mpp.index[0])}: {curr(mpp[0])}</h1>", unsafe_allow_html=True)

    st.markdown("<hr/>",unsafe_allow_html=True)
    st.markdown('## The Best N Selling Products')
    n = st.slider('Choose N:', 1, df['ProductID'].unique().shape[0], 5)
    best5 = df.groupby(['ProductID']).sum()['Sales'].sort_values(ascending=False)[:n]
    names = get_product_name(best5.index.tolist())

    st.markdown(f'# Best {n}')
    fig5 = go.Figure(data=[go.Pie(labels=names, values=best5.values)])
    st.plotly_chart(fig5)

    st.markdown("<hr/>",unsafe_allow_html=True)

    st.markdown('Top 5 Products sells with Product X')

    x = st.selectbox('Choose X:', get_product_name(df['ProductID'].unique().tolist()))
    products_series = df3.groupby(['OrderID'])['ProductName'].transform(lambda x : ','.join(x))


    asscociation_dic = dict(zip(df3['ProductName'].unique(), [0]*df3['ProductName'].unique().shape[0])) 

    for prod in products_series:
        prod_list = prod.split(',')
        if x in prod_list:
            for i in prod_list:
                asscociation_dic[i] += 1

    sorted_asscociation_dic = {k: v for k, v in sorted(asscociation_dic.items(), key=lambda item: item[1])}

    st.write(f'The Top 5 Products sells with {x} ascendingly: ')
    k = list(sorted_asscociation_dic.keys())[-6:-1]
#     names = get_product_name(k)
    fig6 = go.Figure(data=[go.Bar(x=k, y=list(sorted_asscociation_dic.values())[-6:-1] )])
    st.plotly_chart(fig6)
