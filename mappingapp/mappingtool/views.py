from django.shortcuts import render
import folium
import pandas as pd
from .easybutton import JsButton
from decouple import config
# Create your views here.
def index(request):
    # Read the CSV file
    df = pd.read_csv('mappingtool/combined_parks_data.csv')
    
    # Create a map centered on the world
    # m = folium.Map(location=[df['Latitude'].mean(), df['Longitude'].mean()], zoom_start=3, tiles="Esri WorldTopoMap")
    m = folium.Map(location=[36.66841891894786, -117.68554687500001], zoom_start=3, tiles="Esri WorldTopoMap")

    # Add OpenTopoMap as an additional tile layer
    folium.TileLayer(tiles="OpenTopoMap", show=False).add_to(m)
    # Add layer control
    folium.LayerControl().add_to(m)

    # Add pins for each park
    for index, row in df.iterrows():
        lat, long = row['Latitude'], row['Longitude']
        
        # Create formatted HTML for the popup
        popup_html = f"""
        <div style="width: 340px;">
            <h4 style="color: #2c5a2e; margin-bottom: 5px;"><strong>{row['Name']}</strong></h4>
            <hr style="border: 1px solid #2c5a2e; margin: 5px 0;">
            <p style="max-height: 200px; overflow-y: auto;">{row['Description']}<br>
            Test: {config('TEST_VAR')}<br>
            Latitude: {lat:.4f}<br>
            Longitude: {long:.4f}</p>
            <a href="{row['AllTrails URL']}" target="_blank" class="ui button tiny green" 
               style="background-color: #2c5a2e; color: white; text-decoration: none; 
                      padding: 5px 10px; border-radius: 4px; display: inline-block; 
                      margin-top: 5px;">
                View Top Trails on AllTrails
            </a>
        """

        # Handle multiple map links if Map Type contains 'Multiple'
        if 'Multiple' in str(row['Map Type']):
            map_urls = row['Map Link'].split(' | ')
            popup_html += """
            <div style='margin-top: 10px;'>
                <h5 style='color: #2c5a2e; margin-bottom: 5px;'>Official Park Maps:</h5>
            """
            for i, url in enumerate(map_urls, 1):
                popup_html += f"""
                <a href="{url}" target="_blank" class="ui button tiny green" 
                   style="background-color: #2c5a2e; color: white; text-decoration: none; 
                          padding: 5px 10px; border-radius: 4px; display: inline-block; 
                          margin-top: 5px; margin-right: 5px;">
                    Park Map {i}
                </a>
                """
            popup_html += "</div>"
        else:
            popup_html += f"""
            <a href="{row['Map Link']}" target="_blank" class="ui button tiny green" 
               style="background-color: #2c5a2e; color: white; text-decoration: none; 
                      padding: 5px 10px; border-radius: 4px; display: inline-block; 
                      margin-top: 5px;">
                View Official Park Map
            </a>
            """
        
        popup_html += "</div>"

        # Create a custom icon for each marker
        custom_icon = folium.CustomIcon(
            icon_image='mappingtool/NPS-Icon-PNG-3.png',
            icon_size=(30, 30)
        )
        
        folium.Marker(
            location=[lat, long],
            popup=folium.Popup(popup_html, max_width=400),
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
            map.closePopup();
            map.setView([36.66841891894786, -117.68554687500001], 3);
        }
        """).add_to(m)

    # Convert the map to HTML and add a border
    map_html = m._repr_html_()
    map_html = f'<div style="border: 2px solid black;">{map_html}</div>'
    
    # Pass the map HTML to the template
    context = {'map': map_html}
    return render(request, 'index.html', context)

def support(request):
    return render(request, 'support.html')

def best_times(request):
    # Read the CSV file
    df = pd.read_csv('mappingtool/national_parks_best_times_expanded.csv')
    
    # Rename the column to remove space
    df = df.rename(columns={'National Park': 'National_Park'})
    
    # Convert DataFrame to list of dictionaries for template
    parks_data = df.to_dict('records')
    
    return render(request, 'best_times.html', {'parks_data': parks_data})
