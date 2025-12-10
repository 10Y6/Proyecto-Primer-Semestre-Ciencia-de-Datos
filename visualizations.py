import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import Functions as fnc
from collections import defaultdict

data_exch_rate = fnc.load_exch_rate()

#El 'Encogimiento' del Salario: Capacidad de Compra (2024 vs. 2025)
def buy_capacity(sector):
    
    salary_mean = fnc.load_json_onei('salary')
    data_onei = sorted(fnc.data_onei(),key=lambda x:x['date'])

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
        
    mean_cost = {}
    
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
                avg_price = fnc.CS(valid_prices_per_unit)['mean']
                daily_cost += avg_price * qty_needed
        
        if daily_cost > 0:
            mean_cost[date] = daily_cost
        
    df = []
    month_es = {
        '01': 'Enero', '02': 'Febrero', '03': 'Marzo', '04': 'Abril',
        '05': 'Mayo', '06': 'Junio', '07': 'Julio', '08': 'Agosto',
        '09': 'Septiembre', '10': 'Octubre', '11': 'Noviembre', '12': 'Diciembre'
    }
    #{date,salarios de la fehca,coste de la canasta}
    for date,cost in mean_cost.items():
        for year,info in salary_mean.items():
            if year in date:
                year,month = date.split('-')
                date_es = f"{month_es.get(month,month)} {year}"
                df.append({
                    'date':date_es,
                    'quanty':round(info[sector]/cost,2),
                    'cost':round(float(cost),2),
                    'salary':salary_mean[year][sector]
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

#la sombra del dolar correlacion entre el precio de un producto y el dolar
#3enero 2024 - noviembre 2025
def correlation_dollar():
    data_onei = fnc.data_onei()
    own_data_ = fnc.merge_data(fnc.data_online(), fnc.data_in_situ())
    
    # Filtrar y formatear
    own_data = [dict(date=x['date'][0:7], product=x['product'],
                     price=x['price'], unit=(x['unit'][0], x['unit'][1]))
                for x in own_data_ if '2025-10' not in x['date']]
    
    own_data = fnc.merge_data(data_onei, own_data)
    
    # Normalizar
    own_data = [{'date': x['date'],
                 'product': x['product'],
                 'price': round(x['price']/x['unit'][0], 2) if x['unit'][0] else 0,
                 'unit': (1, x['unit'][1])} 
                for x in own_data if x['unit'][0] > 0]
    
    # Separar productos
    products_ = {
        'aceite': [x for x in own_data if 'aceite' in x['product']],
        'arroz': [x for x in own_data if 'arroz' in x['product']]
    }
    
    # Calcular promedios mensuales de productos
    products = defaultdict(dict)
    for product, items in products_.items():
        price_by_month = defaultdict(list)
        for info in items:
            price_by_month[info['date']].append(info['price'])
        
        for date, prices in price_by_month.items():
            products[product][date] = fnc.CS(prices)['mean']

    # Calcular tasa de cambio mensual
    rate_by_month_list = defaultdict(list)
    for date, rate in data_exch_rate.items():
        rate_by_month_list[date[:7]].append(float(rate))
    
    rate_by_month = {}
    for date, rates in rate_by_month_list.items():
        rate_by_month[date] = fnc.CS(rates)['mean']

    
    all_dates = set(rate_by_month.keys())
    for prod in products:
        all_dates.update(products[prod].keys())
    
    dates = sorted(list(all_dates))

    arroz = [products['arroz'].get(d, None) for d in dates]
    aceite = [products['aceite'].get(d, None) for d in dates]
    dollar = [rate_by_month.get(d, None) for d in dates]

    month_es = {'01': 'Ene', '02': 'Feb', '03': 'Mar', '04': 'Abr', '05': 'May', '06': 'Jun', 
                '07': 'Jul', '08': 'Ago', '09': 'Sep', '10': 'Oct', '11': 'Nov', '12': 'Dic'}
    xlabel = []
    for date in dates:
        year,month = date.split('-')
        xlabel.append(f'{month_es[month]} {year}')

    fig = make_subplots(specs=[[{'secondary_y': True}]])

    fig.add_trace(
        go.Scatter(
            x=xlabel, y=arroz, name='Arroz (1 kg)', 
            line=dict(color='#FFFFFF', width=2)       
            ),
        secondary_y=False
    )
    fig.add_trace(
        go.Scatter(
            x=xlabel, y=aceite, name='Aceite (1 L)', 
            line=dict(color='#F5E12E', width=2)
        ),
        secondary_y=False
    )

    fig.add_trace(
        go.Scatter(
            x=xlabel, y=dollar,
            name='Tasa Dólar (Informal)', 
            line=dict(color='#2ECC71', width=3, dash='dot')
        ),
        secondary_y=True
    )

    fig.update_layout(
        title='Correlación: Precios de Alimentos vs. Tasa de Cambio',
        template='plotly_dark',
        font=dict(family='Roboto', size=14),
        hovermode='x unified',
        legend=dict(orientation='h', y=1.1, x=0.5, xanchor='center'),
        margin=dict(l=20, r=20, t=80, b=50),
        hoverlabel=dict(
            namelength=-1,
            font_size=14
        )
    )
    
    fig.update_xaxes(dict(dtick=2))
    fig.update_yaxes(title_text='Precio Producto (CUP)', secondary_y=False, showgrid=False)
    fig.update_yaxes(title_text='Tasa de Cambio (CUP/USD)', secondary_y=True, showgrid=True)

    fig.show()


#evolucion del precio con respecto al inicial 2024-01 en porcentaje
def total_price_evolution():
    #cargar datos y unirlos todos en own_data
    data_onei = fnc.data_onei()
    own_data_ = fnc.merge_data(fnc.data_online(),fnc.data_in_situ())
    #sacar solo ańo con mes para datos de noviembre ya que no me interesan los dias
    #filtrar mis datos de octubre
    own_data = [dict(date=x['date'][0:7],product=x['product'],
                     price=x['price'],unit=(x['unit'][0],x['unit'][1]))
                for x in own_data_ if '2025-10' not in x['date']]
    #mergear los datos oficiales con los mios
    own_data = fnc.merge_data(data_onei,own_data)
    
    #normalizar precio por unidad poner los datos a la misma escala
    own_data = [{'date':x['date'],
                    'product':x['product'],
                    'price':round(x['price']/x['unit'][0],2),
                    'unit':(1,x['unit'][1])} 
                    for x in own_data]
    #separar los productos en listas individuales
    products = {
            'aceite': [x for x in own_data if 'aceite' in x['product']],
            'arroz': [x for x in own_data if 'arroz' in x['product']],
            'malta': [x for x in own_data if 'malta' in x['product']],
            'huevos': [x for x in own_data if 'huevos' in x['product']],
            'cerveza': [x for x in own_data if 'cerveza' in x['product']],
            }
    
    help_unit = {
        'aceite':(1,'L'),
        'arroz':(1,'kg'),
        'malta':(1,'u'),
        'huevos':(1,'u'),
        'cerveza':(1,'u')
    }
    #calcular el promedio desde 2024-2025 
    for product,item_list in products.items():
        prod_list= []
        for item in item_list:
            avg_prod = 0.0
            num_prod = 0
            if product == 'cerveza' or product == 'malta':
                #parche para cambiar la magnitud de cerveza a unidad
                item['unit'] = (item['unit'][0],'u')
                
            if item['date'] == '2025-11':
            #aqui calcula especificamente el de noviembre 2025
            #ya que son datos recoleclectados por mi y hay
            #varios datos de un mismo producto en una misma fecha
            #ojo no datos duplicados
                avg_prod += item['price']
                num_prod += 1
            else:
                prod_list.append(item)
                
        prod_list.append(dict(date='2025-11',product=product
            ,price=round(avg_prod/num_prod,2),unit=help_unit[product]))
        products[product] = prod_list
    
    #ordenar las listas
    for i,j in products.items():
        products[i] = sorted(j,key=lambda x:x['date'])
            
    #crear el dataframe calculando el indice
    #cambiando la fecha de ingles a espańol
    df = []
    month_es = {
        '01': 'Ene', '02': 'Feb', '03': 'Mar', '04': 'Abr',
        '05': 'May', '06': 'Jun', '07': 'Jul', '08': 'Ago',
        '09': 'Sep', '10': 'Oct', '11': 'Nov', '12': 'Dic'
    }
    for product,items in products.items():
        base_price = items[0]['price']
        for item in items:
            #calcular el indice = precio actual/precio base * 100
            #cogiendo enero como base
            index = round((item['price']/base_price)*100,2)
            #cambio de formato de la fecha ingles a espańol
            year,month = item['date'].split('-')
            df.append(dict(
                date=f'{month_es[month]} {year}',
                product=item['product'],
                index=index,
                price=item['price']
            ))
            
    #plotear
    fig = px.line(
        df,x='date',y='index',
        color='product',
        markers=True,#
        custom_data=['price'],#guardar precio para ponerlo en el hover
        color_discrete_map={
            #color especifico a cada linea(identificador de la linea = producto)
            'aceite': "#E7D10D",     
            'arroz': "#EEFAF9",       
            'malta': "#DB8E1A",      
            'cerveza': "#DA1A1A",  
            'huevo': "#1B18D4" 
        },
        labels={
            'date':'Mes y Año',
            'index':'Índice (Base 100)',
            'product':'Producto',
            'price':'Precio (CUP)'
        }
    )
    
    fig.add_hline(#linea del medio como referencia
        y=100,
        line_dash="dash",
        line_color="rgba(255, 215, 0, 0.6)",
        annotation_text="",
        annotation_position="right",
        annotation=dict(
            font=dict(size=12, color="#FFD700")
        )
    )
    
    fig.add_trace(
        #agregar la linea a la leyenda sin mostrar otras cosas
        go.Scatter(
            x=[None],  
            y=[None],
            mode='lines',
            name='Precio Base (Ene 2024)',
            line=dict(color='#FFD700', width=2, dash='dash'),
            showlegend=True,
            hoverinfo='skip'
        )
    )
    
    fig.update_traces(
        #configurar el hover, los datos que
        #muestra la ventana al pasar el clic sobre la linea
        #estilizar con  html
        hovertemplate="<b>%{fullData.name}</b><br>" +#nombre de la linea
                     "Mes: %{x}<br>" + 
                     "Índice: %{y:.1f}%<br>" +
                     "Precio: $%{customdata[0]:.2f}" #primer columna de custom_data definido arriba(primer precio)
                     "<extra></extra>"  #quitar la caja por defecto de plotly
    )
    
    fig.update_layout(
        title='Evolución de Precios: 2024-2025 (Índice Base 100)',
        template='plotly_dark',
        font=dict(family='Roboto', size=14),
        hovermode='x unified',#al pasar el mouse mostrar el valor de todos los productos
        hoverdistance=100, 
        legend=dict(
            orientation='h',
            yanchor='bottom',
            xanchor='center',
            x=0.5,
            y=1.02,
            title=None,
            itemclick='toggleothers', #ocultar las otras lineas cuando cliqueo una
            itemdoubleclick='toggle' 
        ),
        xaxis=dict(
            title='Mes y Año',
            type='category',
            nticks=12,
            showspikes=True,
            spikemode='across',
            spikethickness=2,
            spikecolor="#FBFF00",
            spikedash='dot'
        ), 
        yaxis=dict(
            title='Índice de Precio (Base 100)',
            gridcolor='rgba(255,255,255,0.1)',
            range=[0, max([x['index'] for x in df]) * 1.1],
            dtick=20
        )
    )
    
    fig.show()

def dispersion_analysis():
    data_onei = fnc.data_onei()
    own_data_ = fnc.merge_data(fnc.data_online(),fnc.data_in_situ())
    #sacar solo ańo con mes para datos de noviembre ya que no me interesan los dias
    #filtrar mis datos de octubre
    own_data = [dict(date=x['date'][0:7],product=x['product'],
                     price=x['price'],unit=(x['unit'][0],x['unit'][1]))
                for x in own_data_ if '2025-10' not in x['date']]
    #mergear los datos oficiales con los mios
    own_data = fnc.merge_data(data_onei,own_data)
    
    #normalizar precio por unidad poner los datos a la misma escala
    own_data = [{'date':x['date'],
                    'product':x['product'],
                    'price':round(x['price']/x['unit'][0],2),
                    'unit':(1,x['unit'][1])} 
                    for x in own_data]
    #separar los productos en listas individuales
    products = {
            'aceite': [x for x in own_data if 'aceite' in x['product']],
            'arroz': [x for x in own_data if 'arroz' in x['product']],
            'malta': [x for x in own_data if 'malta' in x['product']],
            'huevos': [x for x in own_data if 'huevos' in x['product']],
            'cerveza': [x for x in own_data if 'cerveza' in x['product']],
            }
    
    help_unit = {
        'aceite':(1,'L'),
        'arroz':(1,'kg'),
        'malta':(1,'u'),
        'huevos':(1,'u'),
        'cerveza':(1,'u')
    }
    #calcular el promedio desde 2024-2025 
    for product,item_list in products.items():
        prod_list= []
        for item in item_list:
            avg_prod = 0.0
            num_prod = 0
            if product == 'cerveza' or product == 'malta':
                #parche para cambiar la magnitud de cerveza a unidad
                item['unit'] = (item['unit'][0],'u')
                
            if item['date'] == '2025-11':
            #aqui calcula especificamente el de noviembre 2025
            #ya que son datos recoleclectados por mi y hay
            #varios datos de un mismo producto en una misma fecha
            #ojo no datos duplicados
                avg_prod += item['price']
                num_prod += 1
            else:
                prod_list.append(item)
                
        prod_list.append(dict(date='2025-11',product=product
            ,price=round(avg_prod/num_prod,2),unit=help_unit[product]))
        products[product] = prod_list
    
    #ordenar las listas
    for i,j in products.items():
        products[i] = sorted(j,key=lambda x:x['date'])
    #CV
    mean = defaultdict(list)
    st_deviation = defaultdict(list)
    for i,j in products.items():
        st_deviation[i] = fnc.CS([k['price'] for k in j])['standard_deviation']
        mean[i] = fnc.CS([k['price'] for k in j])['mean']

    df = []
    
    for med,stdv in zip(mean.items(),st_deviation.items()):
        cv = (stdv[1]/med[1])*100
        df.append(dict(
            cv=round(cv,2),
            product=med[0]
            )
        )
    df = sorted(df,key=lambda x:x['product'])
    products = [x['product'].capitalize() for x in df]
    cv_list = [x['cv'] for x in df]
    colors = []
    for i in cv_list:
        if i < 10:colors.append('#00C851')
        elif i < 20:colors.append('#FFBB33')
        else :colors.append('#ff4444')
    
    fig = go.Figure()
    
    fig.add_trace(
        go.Bar(
            x=cv_list,      
            y=products,       
            orientation='h', 
            marker_color=colors,
            text=[f'{val}%' for val in cv_list],
            textposition='outside',
            textfont=dict(size=14, color='white', family='Roboto'),
            hovertemplate="<b>%{y}</b><br>Dispersión con respecto a la media: %{x}%<extra></extra>"
        )
    )
    
    fig.add_vline(x=10, line_width=1, line_dash="dash", line_color="#00C851")
    fig.add_annotation(x=5, y=-0.15, text="BAJA DISPERSIÓN", showarrow=False, 
                       xref="x", yref="paper", font=dict(color="#00C851", size=12))

    fig.add_vline(x=20, line_width=1, line_dash="dash", line_color="#ff4444")
    fig.add_annotation(x=15, y=-0.15, text="DISPERSIÓN MODERADA", showarrow=False, 
                       xref="x", yref="paper", font=dict(color="#FFBB33", size=12))
    
    fig.add_annotation(x=25, y=-0.15, text="DISPERSIÓN ALTA", showarrow=False, 
                       xref="x", yref="paper", font=dict(color="#ff4444", size=12))

    fig.update_layout(
        title=dict(
            text='Análisis de dispersión de los precios',
            y=0.95
        ),
        template='plotly_dark',
        font=dict(family='Roboto', size=14),
        margin=dict(l=20, r=50, t=80, b=90),
        xaxis=dict(
            title='Coeficiente de Variación (%)',
            showgrid=True, 
            gridcolor='rgba(255,255,255,0.1)',
            zeroline=False,
            range=[0, max(cv_list) * 1.2]
        ),
        yaxis=dict(
            title='',
            showgrid=False,
            tickfont=dict(size=14)
        ),
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )

    fig.show()
    
def indice_congris_huevo():
    data_onei = fnc.data_onei()
    own_data_ = fnc.merge_data(fnc.data_online(),fnc.data_in_situ())
    #sacar solo ańo con mes para datos de noviembre ya que no me interesan los dias
    #filtrar mis datos de octubre
    own_data = [dict(date=x['date'][0:7],product=x['product'],
                     price=x['price'],unit=(x['unit'][0],x['unit'][1]))
                for x in own_data_ if '2025-10' not in x['date']]
    #mergear los datos oficiales con los mios
    own_data = fnc.merge_data(data_onei,own_data)
    
    #normalizar precio por unidad poner los datos a la misma escala
    own_data = [{'date':x['date'],
                'product':x['product'],
                'price':round(x['price']/x['unit'][0],2),
                'unit':(1,x['unit'][1])} 
                for x in own_data]
    
    #separar los productos en listas individuales
    products = {
        'aceite': [x for x in own_data if 'aceite' in x['product']],
        'arroz': [x for x in own_data if 'arroz' in x['product']],
        'frijol': [x for x in own_data if 'frijol' in x['product']],
        'huevo': [x for x in own_data if 'huevo' in x['product']],
    }
    
    recipe = {
        'arroz': 0.25,   
        'frijol': 0.125, 
        'huevo': 1,      
        'aceite': 0.05   
    }
    for i in products:
        products[i] = sorted(products[i], key=lambda x:x['date'])
    
    data = defaultdict(dict)
    dates = set()
    
    for product, items in products.items():
        price_date = defaultdict(list)
        for item in items:
            price_date[item['date']].append(item['price'])
        
        for date, prices in price_date.items():
            avg_price = fnc.CS(prices)['mean']

            data[product][date] = avg_price * recipe.get(product, 0)
            dates.add(date)
    
    month_es = {
        '01': 'Ene', '02': 'Feb', '03': 'Mar', '04': 'Abr',
        '05': 'May', '06': 'Jun', '07': 'Jul', '08': 'Ago',
        '09': 'Sep', '10': 'Oct', '11': 'Nov', '12': 'Dic'
    }
    
    xlabel = []
    dates = sorted(list(dates))
    products = ['arroz','aceite','huevo','frijol']
    
    colors = {
        'arroz':"#F3EEEE",
        'aceite':"#F5E12E",
        'huevo':'#F8DB8B',
        'frijol':"#E04C4C"
    }
    
    names = {
        'arroz':'Precio de 250g de arroz',
        'aceite':'Precio de 50ml de aceite',
        'huevo':'Precio de 1 un huevo',
        'frijol':'Precio de 125g de frijoles',
    }
    
    fig = go.Figure()
    for date in dates:
        year,month = date.split('-')
        xlabel.append(f'{month_es[month]} {year}')
    for product in products:
         yvalue = [data[product].get(d,d) for d in dates]
         fig.add_trace(
             go.Scatter(
                 x=xlabel,
                 y=yvalue,
                 mode='lines',
                 name=names[product],
                 stackgroup='one',
                 line=dict(width=1,color=colors[product]),
                 fillcolor=colors[product],
                 hovertemplate='%{y:.0f} CUP'
             )
        )

    fig.update_layout(
        title='Índice del "Congrís con Huevo"',
        yaxis_title='Costo por Ración',
        template='plotly_dark',
        font=dict(family='Roboto',size=14),
        hovermode='x unified',
        margin=dict(l=20,r=20,t=80,b=50),
        legend=dict(orientation='h',y=1.5,x=0.5,xanchor='center')
    )
    
    fig.show()    
