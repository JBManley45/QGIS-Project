from qgis.core import QgsApplication
import os
QgsApplication.setPrefixPath('C:\\Program Files\\QGIS 3.34.2', True)    
qgs = QgsApplication([], False)
qgs.initQgis()
print(QgsApplication.libraryPath())

cwd = os.getcwd()
print("Current Working Directory:", cwd)

#pull in csv

#plot points

#export map

qgs.exitQgis()