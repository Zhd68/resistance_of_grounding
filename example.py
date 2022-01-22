from grounding import GroundingDevice

number_of_v_electrodes = 5
soil_resistance = 100

depth_of_laying = 0.7
width_of_belt = 0.04
hight_of_belt = 0.004
depth_of_rod = depth_of_laying + 4.5 / 2
diameter_of_rod = 0.016

grounding_device = GroundingDevice(number_of_v_electrodes)
grounding_device.add_horizontal_electrode(depth_of_laying, width_of_belt, hight_of_belt, soil_resistance)
grounding_device.add_vertical_electrode(depth_of_rod, diameter_of_rod, soil_resistance)

print(grounding_device.resistance_grounding_device())