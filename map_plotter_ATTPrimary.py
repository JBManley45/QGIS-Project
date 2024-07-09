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
    QgsCategorizedSymbolRenderer,
    QgsGraduatedSymbolRenderer,
    QgsRectangle
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
def load_csv_as_layer(file_path, layer_name, filter_expression=None):
    file_path = str('C:\\CODE\\Input\\TEST.csv')
    uri = f"file:///{file_path}?delimiter=,&xField=longitude&yField=latitude&crs=epsg:4326"
    layer = QgsVectorLayer(uri, layer_name, 'delimitedtext')
    if not layer.isValid():
        raise ValueError(f"Layer failed to load :( {file_path}")
    if filter_expression:
        layer.setSubsetString(filter_expression)
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
def apply_qml_style(layer, qml_path, value_field):
    #layer.loadNamedStyle(qml_path)
    #layer.triggerRepaint()

    if not os.path.exists(qml_path):
        raise FileNotFoundError(f"QML file not found: {qml_path}")
    
    # Load the QML style
    if not layer.loadNamedStyle(qml_path):
        raise ValueError(f"Failed to load QML style from {qml_path}")

    # Update the layer's symbology to use the specified attribute field
    renderer = layer.renderer()
    if renderer:
        if isinstance(renderer, QgsCategorizedSymbolRenderer):
            renderer.setClassAttribute(value_field)
        elif isinstance(renderer, QgsGraduatedSymbolRenderer):
            renderer.setClassAttribute(value_field)
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

    
    
def plot_points_and_export_image(layers, output_image_path, template_path, qml_paths, value_fields):
    #create projext instance
    #project = QgsProject.instance()
    project = load_template(template_path)
    
    # Add layers to the project and apply QML styles
    for layer, qml_path, value_field in zip(layers, qml_paths, value_fields):
        print(f"Applying QML Path: {qml_path} and Value Field: {value_field} to layer: {layer.name()}")
        QgsProject.instance().addMapLayer(layer)
        project.addMapLayer(layer)
        apply_qml_style(layer, qml_path, value_field)
    osm_layer = add_basemap(project)
    set_layer_order(project, layers)
    map_settings = QgsMapSettings()
    map_settings.setLayers(layers + [osm_layer])
    map_settings.setDestinationCrs(QgsCoordinateReferenceSystem('EPSG:4326'))  # OSM uses EPSG:3857
    map_settings.setOutputSize(QSize(2000, 1500))
    
    # Set the extent to include all layers
    combined_extent = QgsRectangle()
    for layer in layers:
        combined_extent.combineExtentWith(layer.extent())
    map_settings.setExtent(combined_extent)
    
    image = QImage(map_settings.outputSize(), QImage.Format_ARGB32_Premultiplied)
    image.fill(0)
    
    painter = QPainter(image)
    
    render = QgsMapRendererParallelJob(map_settings)
    render.start()
    render.waitForFinished()
    
    render.renderedImage().save(output_image_path, "PNG")
    
    painter.end()
    
#cleanup QGIS app
def cleanup_qgis(qgs):
    qgs.exitQgis()
    
    
# main function to load csv data, plot points to map, export image as PNG
def main(input_csv, output_image, template_path, qml_paths, value_fields, filter_expressions):
    try:
        qgs = initialize_qgis()
        print("QGIS Initialized successfully")
    except Exception as ex:
        print(f"Failed to initialize QGIS {ex}")
        return    
    try:
        layers = []
        for i, (qml_path, value_field, filter_expression) in enumerate(zip(qml_paths, value_fields, filter_expressions)):
            print(f"Processing layer {i+1}")
            print(f"QML Path: {qml_path}")
            print(f"Value Field: {value_field}")
            print(f"Filter Expression: {filter_expression}")
            layer = load_csv_as_layer(input_csv, f"Layer_{i+1}", filter_expression)
            layers.append(layer)
        plot_points_and_export_image(layers, output_image, template_path, qml_paths, value_fields)
        print("Map rendered and exported successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cleanup_qgis(qgs)
        print("QGIS cleaned up after itself :)")
        
if __name__ == "__main__":
    #cwd = os.getcwd()
    input_csv = 'C:\\CODE\\Input\\TEST.csv'
    output_image = 'C:\\CODE\\Output\\mapped_Water_output_ATTPrimary.png'
    template_path = 'C:\\CODE\\Template\\QGIS-WaterCoverage-Style.qml'
    qml_paths = ['C:\\CODE\\Template\\QGIS-SecondaryCoverage_ATT-Primary-Style.qml', 'C:\\CODE\\Template\\QGIS-WaterCoverageBlue-Style.qml']
    value_fields = ['Primarary ATT', 'ATT Primary']
    filter_expressions = ["Primarary ATT = 'Vzw'", "ATT Primary = 'ATT'"]
    
    # Print paths to verify they are correct
    print(f"CSV data loaded successfully from {input_csv}.")
    print(f"Input CSV Path: {input_csv}")
    print(f"Output Image Path: {output_image}")
    print(f"specifing value field: ATT: {value_fields}")
    
    main(input_csv, output_image, template_path, qml_paths, value_fields, filter_expressions)    
    