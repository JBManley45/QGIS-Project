import os
#import pandas as pd
from qgis.core import (
    QgsApplication, 
    QgsProject, 
    QgsVectorLayer,
    QgsCoordinateReferenceSystem,
    QgsMapSettings, 
    QgsMapRendererParallelJob,
    #QgsLayerTreeMapCanvasBridge
)
from qgis.gui import QgsMapCanvas
from PyQt5.QtGui import QImage, QPainter
from PyQt5.QtCore import QSize
import csv

#initialize QGIS app
def initialize_qgis():
    ('C:\\Program Files\\QGIS 3.34.2', True)
    qgs = QgsApplication([], False)
    qgs.initQgis()
    return qgs

#load csv data as qgis layer
#
def load_csv_as_layer(file_path):
    #file_path = str(r"C:\Users\abc\OneDrive - I\Desktop\CODE SOURCE FILES\Ott, OH TEST RSRP.csv")
    file_path = str(r"C:\\Users\\jmanley\\OneDrive - Itron\Desktop\\CODE SOURCE FILES\\Ottawa, OH TEST RSRP.csv")
    uri = f"file:///{file_path}?delimeter=,&xField=longitude&yField=latitude&crs=epsg:4326"
    layer = QgsVectorLayer(uri, 'Points', 'delimitedtext')
    
    if not layer.isValid():
        raise ValueError("Layer failed to load :(")
    return layer
#output just same file/copy of file / add exception flags to each 

def plot_points_and_export_image(layer, output_image_path):
    #create projext instance
    project = QgsProject.instance()
    #add layer to QGIS project
    project.addMapLayer(layer)
    
    #set map settings
    map_settings = QgsMapSettings()
    map_settings.setLayers([layer])
    map_settings.setDestinationCrs(QgsCoordinateReferenceSystem('EPSG:4326'))
    map_settings.setOutputSize(QSize(800, 600))
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
def main(input_csv, output_image):
    
    qgs = initialize_qgis()
    
    try: 
        layer = load_csv_as_layer(input_csv)
        
        plot_points_and_export_image(layer, output_image)
        print("it works")
    finally:
        cleanup_qgis(qgs)
if __name__ == "__main__":
    input_csv = os.path.join('..', 'data', 'input', 'points.csv')
    
    output_image = os.path.join('..', 'data', 'output', 'map_output.png')
    
    main(input_csv, output_image)    
    #print("it works")