import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# Load dataset
df = pd.read_csv('../data/superstore.csv')

# Fix date format
df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True)

# Create features
df['Month'] = df['Order Date'].dt.month_name()

month_order=['January','February','March','April','May','June','July','August','September','October','November','December']

df['Month']=pd.Categorical(df['Month'],categories=month_order,ordered=True)
# App
app = dash.Dash(__name__)

# Layout
app.layout = html.Div([
    
    html.H1("Sales Performance Dashboard", style={'textAlign': 'center','color':'#2c3e50'}),
    
    html.Br(),

    html.Label('select Region'),

    # Dropdown filter
    dcc.Dropdown(
        options=[{'label': r, 'value': r} for r in df['Region'].unique()],
        value=df['Region'].unique()[0],
        id='region-filter',
        style={'width':'50%'}
    ),

    html.Br(),

    # KPI
    html.H2(id='total-sales',style={'textAlign':'center','color':'green'}),

    # Charts
    html.Div([
    dcc.Graph(id='region-chart',style={'width' :'48%'}),
    dcc.Graph(id='monthly-chart',style={'width':'48%'})
    ],style={'display' :'flex','justifyContent':'space-between'}),
    
    html.Br(),
    
    dcc.Graph(id='top-products-chart')

],style={'padding' :'20px'})

# Callback
@app.callback(
    [Output('total-sales', 'children'),
     Output('region-chart', 'figure'),
     Output('monthly-chart', 'figure'),
     Output('top-products-chart','figure')],
    [Input('region-filter', 'value')]
     
     
  
)
def update_dashboard(selected_region):
    
    filtered_df = df[df['Region'] == selected_region]

    total_sales = filtered_df['Sales'].sum()

    region_fig = px.bar(
        filtered_df.groupby('Category')['Sales'].sum().reset_index(),
        x='Category', y='Sales',
        title='Sales by Category'
    )
    region_fig.update_layout(height=400)

    monthly_fig = px.line(
        filtered_df.groupby('Month')['Sales'].sum().reset_index().sort_values('Month'),
        x='Month', y='Sales',
        title='Monthly Sales Trend'
   
    )
    monthly_fig.update_layout(height=400)

    top_products=filtered_df.groupby('Product Name')['Sales'].sum().sort_values(ascending=False).head(10)
    top_products_fig = px.bar(
        x=top_products.values,
        y=top_products.index,
        orientation='h',
        title='Top 10 Products'
    )
    top_products_fig.update_layout(height=500)
  

    return f"Total Sales: ${total_sales:,.0f}", region_fig, monthly_fig,top_products_fig


if __name__ == '__main__':
    app.run(debug=True)