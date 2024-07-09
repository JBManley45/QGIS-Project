#Running: Vzw Only, Water RF Freindly 
import os
import pandas as pd
import csv

from qgis.core import (
    QgsApplication, 
    QgsProject, 
    QgsVectorLayer,
    QgsCoordinateReferenceSystem,
    QgsMapSettings, 
    QgsMapRendererParallelJob,
    QgsRasterLayer,
    QgsLayerTreeGroup,
)
from qgis.gui import QgsMapCanvas
from PyQt5.QtGui import QImage, QPainter
from PyQt5.QtCore import QSize


#initialize QGIS app
def initialize_qgis():
    QgsApplication.setPrefixPath('C:\\Program Files\\QGIS 3.34.2', True)
    qgs = QgsApplication([], False)
    qgs.initQgis()
    return qgs

#load csv data as qgis layer
def load_csv_as_layer(file_path):
    file_path = str('C:\\CODE\\Input\\TEST.csv')
    uri = f"file:///{file_path}?delimiter=,&xField=longitude&yField=latitude&crs=epsg:4326"
    layer = QgsVectorLayer(uri, 'Points', 'delimitedtext')
    if not layer.isValid():
        raise ValueError(f"Layer failed to load :( {file_path}")
    return layer

#output just same file/copy of file / add exception flags to each 
def add_basemap(project):
    urlWithParams = 'type=xyz&url=https://tile.openstreetmap.org/{z}/{x}/{y}.png'
    osm_layer = QgsRasterLayer(urlWithParams, 'OpenStreetMap', 'wms')
    if not osm_layer.isValid():
        raise ValueError("OSM layer failed to load!")
    project.addMapLayer(osm_layer)
    return osm_layer


#load and apply QML style
def apply_qml_style(layer, qml_path):
    # Update the layer's symbology to use the specified attribute field
    #layer.renderer().symbol().symbolLayer(0).setDataDefinedProperty('field', value_field)
    
    layer.loadNamedStyle(qml_path)
    layer.triggerRepaint()

#Function to load QGIS project template
def load_template(template_path):
    template_path = 'C:\\CODE\\Template\\QGIS-WaterCoverage-Style.qml'
    project = QgsProject.instance()
    project.read(template_path)
    return project

#set_layer_order- explicitly set the layer order
def set_layer_order(project, layers):
    root = project.layerTreeRoot()
    group = QgsLayerTreeGroup('Layer Order Group')
    root.addChildNode(group)
    for layer in layers:
        node = root.findLayer(layer.id())
        if node:
           root.removeChildNode(node)
        group.addLayer(layer)

    
    
def plot_points_and_export_image(layer, output_image_path, template_path, qml_path):
    #create projext instance
    #project = QgsProject.instance()
    project = load_template(template_path)
    
    QgsProject.instance().addMapLayer(layer)
    #add layer to QGIS project
    project.addMapLayer(layer)
     # Apply the QML style to the layer
    apply_qml_style(layer, qml_path)
    osm_layer = add_basemap(project)
        
    #set map settings. EPSG 4326 is key standard due to being globe standard vs EPSG 3857 = map standard 
    map_settings = QgsMapSettings()
    map_settings.setLayers([layer, osm_layer])
    map_settings.setDestinationCrs(QgsCoordinateReferenceSystem('EPSG:4326'))
    map_settings.setOutputSize(QSize(2000, 1500))
    map_settings.setExtent(layer.extent())
    
    #create image to render map
    image = QImage(map_settings.outputSize(), QImage.Format_ARGB32_Premultiplied)
    image.fill(0)
    
    #create QPainter object to render map
    painter = QPainter(image)
    
    #create a mp renderer job and begin it
    render = QgsMapRendererParallelJob(map_settings)
    render.start()
    render.waitForFinished()
    
    #save erendered map image as PNG
    render.renderedImage().save(output_image_path, "PNG")
    
    #end QPainter object
    painter.end() 
    
    
#cleanup QGIS app
def cleanup_qgis(qgs):
    qgs.exitQgis()
    
    
# main function to load csv data, plot points to map, export image as PNG
def main(input_csv, output_image, template_path, qml_path):
    try:
        qgs = initialize_qgis()
        print("QGIS Initialized successfully")
    except Exception as ex:
        print(f"Failed to initialize QGIS{ex}")
        return    
    try: 
        layer = load_csv_as_layer(input_csv)
        plot_points_and_export_image(layer, output_image, template_path, qml_path)
        print("it works")
    finally:
        cleanup_qgis(qgs)
        print("QGIS cleaned up after itself :)")
        
if __name__ == "__main__":
    #cwd = os.getcwd()
    input_csv = 'C:\\CODE\\Input\\TEST.csv'
    output_image = 'C:\\CODE\\Output\\mapped_Water_output_Vzw.png'
    template_path = 'C:\\CODE\\Template\\QGIS-WaterCoverage-Style.qml'
    qml_path = 'C:\\CODE\\Template\\QGIS-WaterCoverage-Style.qml'
    
    # Print paths to verify they are correct
    print(f"CSV data loaded successfully from {input_csv}.")
    print(f"Input CSV Path: {input_csv}")
    print(f"Output Image Path: {output_image}")
    
    main(input_csv, output_image, template_path, qml_path)    
    
    