"""Soil Carbon SERVICE"""

import logging
import ee
from geeanalysis.errors import soilCarbonError
from geeanalysis.config import SETTINGS
from geeanalysis.utils.geo import get_region, squaremeters_to_ha


class SoilCarbonService(object):

    @staticmethod
    def analyze(threshold, geojson):
        """For a given Hansen threshold mask on WHRC biomass data
        and geometry return a dictionary of total t/ha.
        """
        #logging.info('[Soil Carbon Service]: In Soil carbon service')
        try:
            d = {}
            soil_carbon_asset = SETTINGS.get('gee').get('assets').get('soils_30m')
            region = get_region(geojson)
            reduce_args = {'reducer': ee.Reducer.sum().unweighted(),
                           'geometry': region,
                           'bestEffort': True,
                           'scale': 30}
            sc = ee.Image(soil_carbon_asset).multiply(ee.Image.pixelArea().divide(10000))
            # Identify soil carbon value
            sc_value = sc.reduceRegion(**reduce_args).getInfo()
            d['total_soil_carbon'] = sc_value
            #logging.info(f'[Soil Carbon Service]:d = {d}')
            return d
        except Exception as error:
            logging.error(str(error))
            raise soilCarbonError(message='Error in soil carbon analysis')
