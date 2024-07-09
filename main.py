from map_plotter_Vzw import main as main_1
from map_plotter_ATT import main as main_2
from map_plotter_VzwPrimary import main as main_3
from map_plotter_ATTPrimary import main as main_4
from qgis.core import QgsApplication

def initialize_qgis():
    qgis_path = 'C:\\Program Files\\QGIS 3.34.2'
    QgsApplication.setPrefixPath(qgis_path, True)
    qgs = QgsApplication([], False)
    qgs.initQgis()
    return qgs

def cleanup_qgis(qgs):
    qgs.exitQgis()
    
def main():
    print("THRUSTERS ENGAGE (starting all map plotters)")
    
    qgs = None
    try:
        qgs = initialize_qgis()
    except Exception as ex:
        print(f"Failed to initialize QGIS:{ex}")
        return
    
    input_csv = 'C:\\CODE\\Input\\TEST.csv'
    
    output_image_VzwOnly = 'C:\\CODE\\Output\\mapped_Water_output_Vzw.png'
    output_image_ATTOnly = 'C:\\CODE\\Output\\mapped_Water_output_ATT.png'
    output_image_VzwPrimary = 'C:\\CODE\\Output\\mapped_Water_output_VzwPrimary.png'
    output_image_ATTPrimary = 'C:\\CODE\\Output\\mapped_Water_output_ATTPrimary.png'
    
    template_path = 'C:\\CODE\\Template\\QGIS-WaterCoverage-Style.qml'
    
    qml_path_VzwOnly = 'C:\\CODE\\Template\\QGIS-WaterCoverage-Style.qml'
    qml_path_ATTOnly = 'C:\\CODE\\Template\\QGIS-WaterCoverage-Style.qml'
    qml_path_VzwPrimary = ['C:\\CODE\\Template\\QGIS-SecondaryCoverage_Vzw-Primary-Style.qml', 'C:\\CODE\\Template\\QGIS-WaterCoverageBlue-Style.qml']
    qml_path_ATTPrimary = ['C:\\CODE\\Template\\QGIS-SecondaryCoverage_ATT-Primary-Style.qml', 'C:\\CODE\\Template\\QGIS-WaterCoverageBlue-Style.qml']
    
    value_field_ATT = 'ATT'
    value_fields_VzwPrim = ['Primary Vzw', 'Vzw Primary']
    value_fields_ATTPrim = ['Primarary ATT', 'ATT Primary']
    
    filter_expressions_VzwPrim = ["Primary Vzw = 'ATT'", "Vzw Primary = 'Vzw'"]
    filter_expressions_ATTPrim = ["Primarary ATT = 'Vzw'", "ATT Primary = 'ATT'"]
    
    try:
        #run each map plotter
        main_1(input_csv, output_image_VzwOnly, template_path, qml_path_VzwOnly)
        main_2(input_csv, output_image_ATTOnly, template_path, qml_path_ATTOnly, value_field_ATT)
        main_3(input_csv, output_image_VzwPrimary, template_path, qml_path_VzwPrimary, value_fields_VzwPrim, filter_expressions_VzwPrim)
        main_4(input_csv, output_image_ATTPrimary, template_path, qml_path_ATTPrimary, value_fields_ATTPrim, filter_expressions_ATTPrim)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Cleanup QGIS application
        if qgs:
            cleanup_qgis(qgs)
        print("QGIS cleaned up after itself :)")
    
    print("CHECK YOUR C:CODE OUTPUT FOLDER ;)")
    
if __name__ == "__main__":
    main()
    