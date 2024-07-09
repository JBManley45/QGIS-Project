import map_plotter_Vzw
import map_plotter_ATT
import map_plotter_VzwPrimary
import map_plotter_ATTPrimary

def main():
    print("THRUSTERS ENGAGE (starting all map plotters)")
    map_plotter_Vzw()
    map_plotter_ATT()
    map_plotter_VzwPrimary()
    map_plotter_ATTPrimary()
    print("CHECK YOUR C:CODE OUTPUT FOLDER ;)")
    
if __name__ == "__main__":
    main()
    