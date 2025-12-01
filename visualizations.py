import plotly.express as px
import plotly.graph_objects as go
import Functions as fnc
import statistics
from collections import defaultdict

#loading all data
data_in_situ = fnc.data_in_situ()
data_online = fnc.data_online()
data_onei = fnc.data_onei()
data_exch_rate = fnc.load_exch_rate()
salary_median = fnc.load_json_onei('salary')
#
def sort_datas():
    data_onei.sort(key=lambda x:x['date'])
    
sort_datas()

#El 'Encogimiento' del Salario: Capacidad de Compra (2024 vs. 2025)
def buy_capacity(sector):
    canasta = {
        'arroz':(5.6,'kg'),
        'azucar':(2.5,'kg'),
        'frijoles':(1.2,'kg'),
        'pan':(30,'u'),
        'cafe':(0.250,'kg'),
        'pescado':(1,'kg'),
        'cerdo':(2,'kg'),
        'carnero':(2,'kg'),
        'huevo':(10,'u'),
        'leche':(1,'kg'),
        'aceite':(1,'L'),
        'sal':(0.500,'kg'),
        'jabon':(4,'u'),
        'detergente':(1,'kg'),
        'pasta dental':(1,'u')      
    }
    
    data_by_date = defaultdict(list)
    for row in data_onei:
        data_by_date[row['date']].append(row)
        
    median_cost = {}
    
    for date, products in data_by_date.items():
        daily_cost = 0.0
        for item_key, (qty_needed, target_unit) in canasta.items():
            matches = [p for p in products if item_key in p['product']]
            valid_prices_per_unit = []
            for m in matches:
                amount, unit_type = m['unit']
                price = m['price'] 
                
                if amount <= 0 or not price: continue
                if unit_type == target_unit:
                    price_per_unit = price / amount
                    valid_prices_per_unit.append(price_per_unit)
            
            if valid_prices_per_unit:
                avg_price = statistics.mean(valid_prices_per_unit)
                daily_cost += avg_price * qty_needed
        
        if daily_cost > 0:
            median_cost[date] = daily_cost
        
    df = []
    month_es = {
        '01': 'Enero', '02': 'Febrero', '03': 'Marzo', '04': 'Abril',
        '05': 'Mayo', '06': 'Junio', '07': 'Julio', '08': 'Agosto',
        '09': 'Septiembre', '10': 'Octubre', '11': 'Noviembre', '12': 'Diciembre'
    }
    #{date,salarios de la fehca,coste de la canasta}
    for date,cost in median_cost.items():
        for year,info in salary_median.items():
            if year in date:
                year,month = date.split('-')
                date_es = f"{month_es.get(month,month)} {year}"
                df.append({
                    'date':date_es,
                    'quanty':round(info[sector]/cost,2),
                    'cost':round(float(cost),2),
                    'salary':salary_median[year][sector]
                })
    
           
    fig = px.bar(df,x='date',y='quanty',barmode='group',
        hover_data=['cost','salary'],
        labels={
            'date':'Mes y Año',
            'quanty':'Canastas Cubiertas',
            'cost':'Costo de la Canasta(CUP)',
            'salary':'Salario Promedio del Trabajador'
        })
    fig.update_layout(
        title=f'¿Cuántas Canastas Básicas Cubre el Salario de {sector}?',
        template='plotly_dark',
        title_font_size=24,
        margin=dict(t=100),
        font=dict(family='Roboto',size=14,color= '#ffffff')
    )
    
    fig.update_xaxes(
        title='Mes y Año',
        type='category',
        tickmode='auto',
        nticks=5,
        )
    fig.update_yaxes(
        title='Cantidad de Canastas',
        tickformat=',.2f',
        range=[0, 2]
    )
    
    dates = [x['date'] for x in df]
    
    fig.add_trace(
        go.Scatter(
            x=dates,
            y=[1] * len(dates),
            mode='lines',
            name='Punto Medio(1 Canasta)',
            line=dict(color='#FFD700',width=2,dash='dash'),
            hoverinfo='none',
            showlegend=True,
        )
    )
    
    fig.update_traces(
        marker_color='#00BFFF',
        marker_line_width=0.0,
        opacity=0.9,
        selector=dict(type='bar'),
        hovertemplate="<br>".join([
            "<b>Mes y Año:</b> %{x}",
            "<b>Canastas Cubiertas:</b> %{y:.2f}",
            "<b>Salario Promedio:</b> $%{customdata[1]:,.0f} CUP", 
            "<b>Costo de la Canasta:</b> $%{customdata[0]:,.0f} CUP",
            "<extra></extra>"
        ])
    )
    
    fig.show()
 