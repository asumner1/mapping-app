from django.shortcuts import render
import folium
import pandas as pd
from .easybutton import JsButton

# Create your views here.
def index(request):
    # Read the CSV file
    df = pd.read_csv('mappingtool/cleaned_parks_table.csv')
    
    # Create a map centered on the world
    # m = folium.Map(location=[df['Latitude'].mean(), df['Longitude'].mean()], zoom_start=3, tiles="Esri WorldTopoMap")
    m = folium.Map(location=[36.66841891894786, -117.68554687500001], zoom_start=3, tiles="Esri WorldTopoMap")

    # Add pins for each park
    for index, row in df.iterrows():
        lat, long = row['Latitude'], row['Longitude']
        
        # Create a custom icon for each marker
        custom_icon = folium.CustomIcon(
            icon_image='mappingtool/NPS-Icon-PNG-3.png',
            icon_size=(30, 30)
        )
        
        folium.Marker(
            location=[lat, long],
            popup=row['Name'],
            tooltip=row['Name'],
            icon=custom_icon
        ).add_to(m)
    
    sw = df[['Latitude', 'Longitude']].min().values.tolist()
    ne = df[['Latitude', 'Longitude']].max().values.tolist()
    m.fit_bounds([sw, ne])
    
    JsButton(
        title='<i class="fas fa-crosshairs"></i>',
        function="""
        function(btn, map) {
            //console.log(map.getCenter());
            map.setView([36.66841891894786, -117.68554687500001], 3);
        }
        """).add_to(m)


    # Convert the map to HTML and add a border
    map_html = m._repr_html_()
    map_html = f'<div style="border: 2px solid black;">{map_html}</div>'
    
    # Pass the map HTML to the template
    context = {'map': map_html}
    return render(request, 'index.html', context)
