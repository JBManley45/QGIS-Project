from qgis.core import QgsApplication

QgsApplication.setPrefixPath('C:\\Program Files\\QGIS 3.34.2', True)
qgs = QgsApplication([], False)
qgs.initQgis()
print(QgsApplication.libraryPath())

#pull in csv

#plot points

#export map

qgs.exitQgis()