# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class E5_residential_savings_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Returns the relevant savings factor for the existing and new lamp' \
            ' for residential replacements.'

    def formula(buildings, period, parameters):
        number_of_existing_lamps = buildings('E5_number_of_existing_lamps', period)
        number_of_lamps = select([number_of_existing_lamps == 1, number_of_existing_lamps == 2, number_of_existing_lamps >= 3],
                                ["one_lamp", "two_lamps", "three_or_more_lamps"])
        lamp_size = buildings('E5_existing_lamp_length', period)
        size_of_existing_lamp = select([lamp_size > 550 and lamp_size <= 750,
                                        lamp_size > 750 and lamp_size <= 1150,
                                        lamp_size > 1150 and lamp_size <= 1350,
                                        lamp_size > 1350 and lamp_size <= 1500],
                                     ["more_than_550mm_and_less_than_750mm",
                                    "more_than_700mm_and_less_than_1150mm",
                                    "more_than_1150mm_and_less_than_1350mm",
                                    "more_than_1350mm_and_less_than_1500mm"])
        new_lamp_light_output = buildings('new_lamp_light_output', period)
        new_lamp_output = select([number_of_lamps == 1 and new_lamp_light_output >= 600 and new_lamp_light_output < 1100,
                               number_of_lamps == 1 and new_lamp_light_output >= 1100 and new_lamp_light_output < 1500,
                               number_of_lamps == 1 and new_lamp_light_output >= 1500 and new_lamp_light_output < 2400,
                               number_of_lamps == 1 and new_lamp_light_output >= 2400,
                               number_of_lamps == 2 and new_lamp_light_output >= 1200 and new_lamp_light_output < 2200,
                               number_of_lamps == 2 and new_lamp_light_output >= 2200 and new_lamp_light_output < 3000,
                               number_of_lamps == 2 and new_lamp_light_output >= 3000 and new_lamp_light_output < 4900,
                               number_of_lamps == 2 and new_lamp_light_output >= 4900,
                               number_of_lamps == 3 and new_lamp_light_output >= 1900 and new_lamp_light_output < 3300,
                               number_of_lamps == 3 and new_lamp_light_output >= 3300 and new_lamp_light_output < 4500,
                               number_of_lamps == 3 and new_lamp_light_output >= 4500 and new_lamp_light_output < 7300,
                               number_of_lamps == 3 and new_lamp_light_output >= 7300],
                                ['over_600_lumen_light_output',
                                'over_1100_lumen_light_output',
                                'over_1500_lumen_light_output',
                                'over_2400_lumen_light_output',
                                'over_1200_lumen_light_output',
                                'over_2200_lumen_light_output',
                                'over_3000_lumen_light_output',
                                'over_4900_lumen_light_output',
                                'over_1900_lumen_light_output',
                                'over_3300_lumen_light_output',
                                'over_4500_lumen_light_output',
                                'over_7300_lumen_light_output'])
        new_lamp_circuit_power = buildings('new_lamp_circuit_power', period)
        new_lamp_LCP = select([new_lamp_circuit_power <= 10,
                               new_lamp_circuit_power > 10 and new_lamp_circuit_power <= 15,
                               new_lamp_circuit_power > 15 and new_lamp_circuit_power <= 20,
                               new_lamp_circuit_power > 20 and new_lamp_circuit_power <= 25,
                               new_lamp_circuit_power > 25 and new_lamp_circuit_power <= 30,
                               new_lamp_circuit_power > 30 and new_lamp_circuit_power <= 35,
                               new_lamp_circuit_power > 35 and new_lamp_circuit_power <= 40,
                               new_lamp_circuit_power > 40 and new_lamp_circuit_power <= 45,
                               new_lamp_circuit_power > 45 and new_lamp_circuit_power <= 50,
                               new_lamp_circuit_power > 50 and new_lamp_circuit_power <= 60,
                               new_lamp_circuit_power > 60 and new_lamp_circuit_power <= 70,
                               new_lamp_circuit_power > 70 and new_lamp_circuit_power <= 80,
                               new_lamp_circuit_power > 80 and new_lamp_circuit_power <= 90],
                            ['less_than_10W',
                            'between_10W_and_15W',
                            'between_15W_and_20W',
                            'between_20W_and_25W',
                            'between_25W_and_30W',
                            'between_30W_and_35W',
                            'between_35W_and_40W',
                            'between_40W_and_45W',
                            'between_45W_and_50W',
                            'between_50W_and_60W',
                            'between_60W_and_70W',
                            'between_70W_and_80W',
                            'between_80W_and_90W'])
        residential_building_savings_factor = (parameters(period).table_E5_1.residential_savings_factor
        [number_of_lamps][size_of_existing_lamp][new_lamp_output][new_lamp_LCP])
        return residential_building_savings_factor


class E5_small_business_savings_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Returns the relevant savings factor for the existing and new lamp' \
            ' for residential replacements.'

    def formula(buildings, period, parameters):
        number_of_existing_lamps = buildings('E5_number_of_existing_lamps', period)
        number_of_lamps = select([number_of_existing_lamps == 1, number_of_existing_lamps == 2, number_of_existing_lamps >= 3],
                                ["one_lamp", "two_lamps", "three_or_more_lamps"])
        lamp_size = buildings('E5_existing_lamp_length', period)
        size_of_existing_lamp = select([lamp_size > 550 and lamp_size <= 750,
                                        lamp_size > 750 and lamp_size <= 1150,
                                        lamp_size > 1150 and lamp_size <= 1350,
                                        lamp_size > 1350 and lamp_size <= 1500],
                                     ["more_than_550mm_and_less_than_750mm",
                                    "more_than_700mm_and_less_than_1150mm",
                                    "more_than_1150mm_and_less_than_1350mm",
                                    "more_than_1350mm_and_less_than_1500mm"])
        new_lamp_light_output = buildings('new_lamp_light_output', period)
        new_lamp_output = select([number_of_lamps == 1 and new_lamp_light_output >= 600 and new_lamp_light_output < 1100,
                               number_of_lamps == 1 and new_lamp_light_output >= 1100 and new_lamp_light_output < 1500,
                               number_of_lamps == 1 and new_lamp_light_output >= 1500 and new_lamp_light_output < 2400,
                               number_of_lamps == 1 and new_lamp_light_output >= 2400,
                               number_of_lamps == 2 and new_lamp_light_output >= 1200 and new_lamp_light_output < 2200,
                               number_of_lamps == 2 and new_lamp_light_output >= 2200 and new_lamp_light_output < 3000,
                               number_of_lamps == 2 and new_lamp_light_output >= 3000 and new_lamp_light_output < 4900,
                               number_of_lamps == 2 and new_lamp_light_output >= 4900,
                               number_of_lamps == 3 and new_lamp_light_output >= 1900 and new_lamp_light_output < 3300,
                               number_of_lamps == 3 and new_lamp_light_output >= 3300 and new_lamp_light_output < 4500,
                               number_of_lamps == 3 and new_lamp_light_output >= 4500 and new_lamp_light_output < 7300,
                               number_of_lamps == 3 and new_lamp_light_output >= 7300],
                                ['over_600_lumen_light_output',
                                'over_1100_lumen_light_output',
                                'over_1500_lumen_light_output',
                                'over_2400_lumen_light_output',
                                'over_1200_lumen_light_output',
                                'over_2200_lumen_light_output',
                                'over_3000_lumen_light_output',
                                'over_4900_lumen_light_output',
                                'over_1900_lumen_light_output',
                                'over_3300_lumen_light_output',
                                'over_4500_lumen_light_output',
                                'over_7300_lumen_light_output'])
        new_lamp_circuit_power = buildings('new_lamp_circuit_power', period)
        new_lamp_LCP = select([new_lamp_circuit_power <= 10,
                               new_lamp_circuit_power > 10 and new_lamp_circuit_power <= 15,
                               new_lamp_circuit_power > 15 and new_lamp_circuit_power <= 20,
                               new_lamp_circuit_power > 20 and new_lamp_circuit_power <= 25,
                               new_lamp_circuit_power > 25 and new_lamp_circuit_power <= 30,
                               new_lamp_circuit_power > 30 and new_lamp_circuit_power <= 35,
                               new_lamp_circuit_power > 35 and new_lamp_circuit_power <= 40,
                               new_lamp_circuit_power > 40 and new_lamp_circuit_power <= 45,
                               new_lamp_circuit_power > 45 and new_lamp_circuit_power <= 50,
                               new_lamp_circuit_power > 50 and new_lamp_circuit_power <= 60,
                               new_lamp_circuit_power > 60 and new_lamp_circuit_power <= 70,
                               new_lamp_circuit_power > 70 and new_lamp_circuit_power <= 80,
                               new_lamp_circuit_power > 80 and new_lamp_circuit_power <= 90],
                            ['less_than_10W',
                            'between_10W_and_15W',
                            'between_15W_and_20W',
                            'between_20W_and_25W',
                            'between_25W_and_30W',
                            'between_30W_and_35W',
                            'between_35W_and_40W',
                            'between_40W_and_45W',
                            'between_45W_and_50W',
                            'between_50W_and_60W',
                            'between_60W_and_70W',
                            'between_70W_and_80W',
                            'between_80W_and_90W'])
        small_business_building_savings_factor = (parameters(period).table_E5_2.small_business_savings_factor
        [number_of_lamps][size_of_existing_lamp][new_lamp_output][new_lamp_LCP])
        return small_business_building_savings_factor
