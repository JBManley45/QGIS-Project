from qgis.core import QgsProject, QgsRasterLayer
from qgis.utils import iface

# OSM street map URL
osm_url = "type=xyz&url=http://a.tile.openstreetmap.org/{z}/{x}/{y}.png"
layer_name = "OpenStreetMap"

try:
    # Create raster layer (API LINK: https://qgis.org/pyqgis/master/core/QgsRasterLayer.html)
    osm_layer = QgsRasterLayer(osm_url, layer_name, "wms")

    # Check if the layer was created successfully
    if not osm_layer.isValid():
        raise ValueError("Failed to create OSM layer!")

    # Add the layer to the current QGIS project (API LINK: https://qgis.org/pyqgis/master/core/QgsProject.html)
    QgsProject.instance().addMapLayer(osm_layer)
    print(f"Layer {layer_name} added successfully!")

    # Optionally, you can set this layer to be visible in the map canvas
    iface.mapCanvas().setExtent(osm_layer.extent())
    iface.mapCanvas().refresh()

except Exception as e:
    print(f"An error occurred: {e}")