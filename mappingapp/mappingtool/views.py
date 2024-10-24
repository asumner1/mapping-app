from django.shortcuts import render
import folium
import pandas as pd

# Create your views here.
def index(request):
    # Create a map centered on the world
    m = folium.Map(location=[0, 0], zoom_start=2)

    # Read the CSV file
    df = pd.read_csv('mappingtool/cleaned_parks_table.csv')
    
    # Add pins for each park
    for index, row in df.iterrows():
        lat, long = row['Location'].split(',')
        lat, long = float(lat), float(long)
        folium.Marker(
            location=[lat, long],
            popup=row['Name'],
            tooltip=row['Name']
        ).add_to(m)
    
    # Convert the map to HTML
    map_html = m._repr_html_()
    
    # Pass the map HTML to the template
    context = {'map': map_html}
    return render(request, 'index.html', context)
