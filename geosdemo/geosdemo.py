"""Main module."""

import string 
import random
import ipyleaflet
import ipywidgets as widgets

class Map (ipyleaflet.Map):   #we are going to build based on this
     
    def __init__(self, center= [20, 0], zoom= 2, **kwargs) -> None:  #needs to be passed back to the ipyleafclass this is why we put center and zoom in __init__
        
        if "scroll_wheel_zoom" not in kwargs:
            kwargs["scroll_wheel_zoom"] = True   
            
        print(f"this is what the user is providing:{kwargs}") #prints what the user provides       
        super().__init__(center=center, zoom=zoom, **kwargs)      #super means upper label, the class you inherit from. This passes the parameters to geosdemo.py 
        print(kwargs)  #AGAIN FOR DEBUGGING

        #11a - adding the layers control as default
        if "layers_control" not in kwargs:
            kwargs["layers_control"] = True
        print(kwargs) #aGAIN FOR DEBUGGING
        if kwargs["layers_control"]:
            self.add_layers_control()

        if "fullscreen_control" not in kwargs:
            kwargs["fullscreen_control"] = True

        if kwargs["fullscreen_control"]:
            self.add_fullscreen_control()
        print(kwargs)

    def add_search_control(self, position="topleft", **kwargs):  #based on control  example
        """_summary_

        Returns:
            _type_: _description_
        """  
        if "url" not in kwargs:
            kwargs["url"] = "https://nominatim.openstreetmap.org/search?format=json&q={s}"

        
        search_control = ipyleaflet.SearchControl(position= position, **kwargs) #based on example in https://ipyleaflet.readthedocs.io/en/latest/controls/search_control.html
        
        print(f"this is what the user is providing:{kwargs}") 
        self.add_control(search_control)   

    def add_draw_control(self, **kwargs):  #based on control  example
        """_summary_
        """       
        draw_control = ipyleaflet.DrawControl(**kwargs) 

        #customizing the draw control
        draw_control.polyline =  {
            "shapeOptions": {
                "color": "#6bc2e5",
                "weight": 8,
                "opacity": 1.0
            }
        }
        draw_control.polygon = {
            "shapeOptions": {
                "fillColor": "#6be5c3",
                "color": "#6be5c3",
                "fillOpacity": 1.0
            },
            "drawError": {
                "color": "#dd253b",
                "message": "Oups!"
            },
            "allowIntersection": False
        }
        draw_control.circle = {
            "shapeOptions": {
                "fillColor": "#efed69",
                "color": "#efed69",
                "fillOpacity": 1.0
            }
        }
        draw_control.rectangle = {
            "shapeOptions": {
                "fillColor": "#fca45d",
                "color": "#fca45d",
                "fillOpacity": 1.0
            }  
        }    
       
        
        self.add_control(draw_control)
    
    def add_layers_control(self, position='topright'):
        """_summary_ f

        Args:
            position (str, optional): _description_. Defaults to 'topright'.
        """       
        layers_control = ipyleaflet.LayersControl(position=position)
        self.add_control(layers_control)

    def add_fullscreen_control(self, position="topleft"):
        """Adds a fullscreen control to the map.

        Args:
            kwargs: Keyword arguments to pass to the fullscreen control.
        """
        fullscreen_control = ipyleaflet.FullScreenControl(position=position)
        self.add_control(fullscreen_control)

    #adding a tile layer
    def add_tile_layer(self, url, name, attribution="", **kwargs):
        """Adds a tile layer to the map.

        Args:
            url (str): The URL of the tile layer.
            name (str): The name of the tile layer.
            attribution (str, optional): The attribution of the tile layer. Defaults to "".
        """
        tile_layer = ipyleaflet.TileLayer(
            url=url,
            name=name,
            attribution=attribution,
            **kwargs
        )
        self.add_layer(tile_layer)

    #adding basemap
    def add_basemap(self, basemap, **kwargs):

        import xyzservices.providers as xyz  #if a user wants another map is going tolook in xyz

        if basemap.lower() == "roadmap":  #the user can insert any form
            url = 'http://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}'
            self.add_tile_layer(url, name=basemap, **kwargs)  #name= basemap guarantess that gets the value of the selected 
        elif basemap.lower() == "satellite":
            url = 'http://mt0.google.com/vt/lyrs=y&hl=en&x={x}&y={y}&z={z}'
            self.add_tile_layer(url, name=basemap, **kwargs)
        else:
            try:
                basemap = eval(f"xyz.{basemap}") 
                url = basemap.build_url()
                attribution = basemap.attribution
                self.add_tile_layer(url, name=basemap.name, attribution=attribution, **kwargs)
            except:
                raise ValueError(f"Basemap '{basemap}' not found.")
            
        #adding vector data 

    def add_geojson(self, data, name='GeoJSON', **kwargs):
        """Adds a GeoJSON layer to the map.

        Args:
            data (dict): The GeoJSON data.
        """

        if isinstance(data, str): #isinstance figures out the data type this allows to just read the data without worrying about how to load the geojson
            import json
            with open(data, "r") as f:
                data = json.load(f)

        geojson = ipyleaflet.GeoJSON(data=data,name=name, **kwargs)
        self.add_layer(geojson)
    
    #we neeed to add geopandas

    def add_shp(self, data, name='Shapefile', **kwargs):
        """Adds a Shapefile layer to the map.

        Args:
            data (str): The path to the Shapefile.
        """
        import geopandas as gpd
        gdf = gpd.read_file(data)
        geojson = gdf.__geo_interface__  #___geointerface___ if we use .tojson we would need to convet it back, thidsconverts to dictionary directly
        self.add_geojson(geojson, name=name, **kwargs)    

    def add_raster(self, url, name='Raster', fit_bounds=True, **kwargs):  #Week 12 adding the url using titiler
        """Adds a raster layer to the map.                       #fit_bounds assigned as True as default

        Args:
            url (str): The URL of the raster layer.
            name (str, optional): The name of the raster layer. Defaults to 'Raster'.
            fit_bounds (bool, optional): Whether to fit the map bounds to the raster layer. Defaults to True.
        """
        import httpx

        titiler_endpoint = "https://titiler.xyz"

        r = httpx.get(
            f"{titiler_endpoint}/cog/info",
            params = {
                "url": url,
            }
        ).json()

        bounds = r["bounds"]

        r = httpx.get(
            f"{titiler_endpoint}/cog/tilejson.json",
            params = {
                "url": url,
            }
        ).json()

        tile = r["tiles"][0]

        self.add_tile_layer(url=tile, name=name, **kwargs)

        if fit_bounds:
            bbox = [[bounds[1], bounds[0]], [bounds[3], bounds[2]]]
            self.fit_bounds(bbox)

    #homework make some modifications to add the functionalities of the widgets
    #copying material from toolbar.ipynb
    def add_toolbar(self, position="topright"):
        widget_width = "250px" #setting the widget width 
        padding = "0px 0px 0px 5px"  # upper, right, bottom, left

        #creating the tolbar button
        toolbar_button = widgets.ToggleButton(
            value=False,
            tooltip="Toolbar", #user hover an displays text
            icon="wrench", #https://fontawesome.com/v4/icons/
            layout=widgets.Layout(width="28px", height="28px", padding=padding),
        )

        #creating the close button
        close_button = widgets.ToggleButton(
            value=False,
            tooltip="Close the tool",
            icon="times",
            button_style="primary",
            layout=widgets.Layout(height="28px", width="28px", padding=padding),  
        )
        
        toolbar = widgets.HBox([toolbar_button])

        def toolbar_click(change):
            if change["new"]:
                toolbar.children = [toolbar_button, close_button]
            else:
                toolbar.children = [toolbar_button]
                
        toolbar_button.observe(toolbar_click, "value") #when is clicked we are going to observe the close button
                                            #value is used in most of the time and means when we click is true and nclick is false

        def close_click(change):
            if change["new"]:
                toolbar_button.close()
                close_button.close()
                toolbar.close()
                
        close_button.observe(close_click, "value")

        rows = 2
        cols = 2
        grid = widgets.GridspecLayout(rows, cols, grid_gap="0px", layout=widgets.Layout(width="62px"))

        icons = ["folder-open", "map", "info", "question"] #names taken from the link above

        for i in range(rows):
            for j in range(cols):
                grid[i, j] = widgets.Button(description="", button_style="primary", icon=icons[i*rows+j], 
                                            layout=widgets.Layout(width="28px", padding="0px"))
                
        toolbar = widgets.VBox([toolbar_button])

        def toolbar_click(change):
            if change["new"]: #means once is clicked
                toolbar.children = [widgets.HBox([close_button, toolbar_button]), grid]
            else:
                toolbar.children = [toolbar_button]
                
        toolbar_button.observe(toolbar_click, "value")

        #toolbar_ctrl = ipyleaflet.WidgetControl(widget=toolbar, position="topright")  #here we need to addipyleaflet
        toolbar_ctrl = ipyleaflet.WidgetControl(widget=toolbar, position=position) #to add flexibility and avoid hard coding of the position
        self.add_control(toolbar_ctrl) #self instead of m in the notebook


    # def add_local_raster(self, filename, name="Local raster", **kwargs):

    #     try:
    #         import localtileserver
    #     except ImportError:
    #         raise ImportError("loacltileserver not installed. Please install it with pip install ")
    #     self.add_tile_layer()



#Created on youtube lesson week 10
def generate_random_string(length= 10, upper= False, digits = False, punctuation= False):
    """Generates a random string of a given length

    Args:
        length (int, optional): Length of the string. Defaults to 10.
        upper (bool, optional): Whether to include uppercase. Defaults to False.
        digits (bool, optional): _description_. Defaults to False.
        punctuation (bool, optional): _description_. Defaults to False.

    Returns:
        str: The generated string
    """    
    letters = string.ascii_lowercase
    if upper:
         letters += string.ascii_uppercase
    if digits:
         letters += string.digits
    if punctuation:
         letters += string.pun
        
    letters = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def generate_lucky_number(length= 1):
    """_summary_

    Args:
        length (int, optional): _description_. Defaults to 1.

    Returns:
        _type_: _description_
    """    
    result_str = ''.join(random.choice(string.digits) for i in range(length))
    return int(result_str)


