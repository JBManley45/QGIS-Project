import csv
from qgis.core import (
    QgsProject,
    QgsPointXY,
    QgsGeometry,
    QgsFeature,
    QgsVectorLayer,
    QgsField
)
from PyQt5.QtCore import QVariant

########################## IMPORT RSRP DATA FROM CSV ############################
RSRP_CSV_PATH = 'C:\Git\QGIS-Project\data\Ottawa_OH_TEST_RSRP.csv'
data = {}

try:
    with open(RSRP_CSV_PATH, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            
            key = row['id']
            
            data[key] = {
                    'latitude': float(row['latitude']),
                    'longitude': float(row['longitude']),
                    'Vzw': float(row['Vzw']),
                    'ATT': float(row['ATT']),
                    'Score Vzw': int(row['Score Vzw']),
                    'Score ATT': int(row['Score ATT']),
                    'Primary Vzw': row['Primary Vzw'],
                    'Primary ATT': row['Primary ATT'],
                    'Vzw Primary': float(row['Vzw Primary']),
                    'ATT Primary': float(row['ATT Primary']),
                }
except FileNotFoundError:
    print(f"File {RSRP_CSV_PATH} not found.")
except KeyError as e:
    print(f"Key error: {e} - Check the CSV column names.")
except Exception as e:
    print(f"An error occurred: {e}")
#################################################################################

############################ CREATE RSRP VECTOR LAYER ###########################
layer = QgsVectorLayer('Point?crs=EPSG:4326', 'RSRP Points', 'memory')
provider = layer.dataProvider()

# Add fields for layer features
fields = [
    QgsField('id', QVariant.String),
    QgsField('Vzw', QVariant.Double),
    QgsField('ATT', QVariant.Double),
    QgsField('Score Vzw', QVariant.Int),
    QgsField('Score ATT', QVariant.Int),
    QgsField('Primary Vzw', QVariant.String),
    QgsField('Primary ATT', QVariant.String),
    QgsField('Vzw Primary', QVariant.Double),
    QgsField('ATT Primary', QVariant.Double)
]
provider.addAttributes(fields)
layer.updateFields()

# Add data to the feature fields
features = []

for key, value in data.items():
    feature = QgsFeature()
    point = QgsPointXY(value['longitude'], value['latitude'])
    feature.setGeometry(QgsGeometry.fromPointXY(point))
    feature.setAttributes([
        key, 
        value['Vzw'], 
        value['ATT'], 
        value['Score Vzw'], 
        value['Score ATT'], 
        value['Primary Vzw'], 
        value['Primary ATT'], 
        value['Vzw Primary'], 
        value['ATT Primary']
    ])
    features.append(feature)

provider.addFeatures(features)

# Add the layer to the current QGIS project
QgsProject.instance().addMapLayer(layer)
#################################################################################