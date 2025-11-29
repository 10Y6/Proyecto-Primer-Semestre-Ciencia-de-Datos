import plotly.express as px
import Functions as fnc

def heat_map(cath):
    data_list = fnc.group_products(cath)
    hover_data = {
        'lat':False,
        'lon':False,
        'product':True,
        'township':True,
        'price':True
    }
    chart = px.scatter_mapbox(
        data_frame=data_list,
        lat='lat',lon='lon',color='price',
        hover_name='mipyme_name',
        hover_data=hover_data,zoom=11,
        mapbox_style='open-street-map',
        size='price',size_max=50,
        color_continuous_scale='Jet',
        opacity=0.7,height=600,width=1200,
        title=f'Mapa de precios: {cath.capitalize()} en La Habana'
        )
    
    chart.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
    chart.show()
    