"""API ROUTER"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging

from flask import jsonify, request, Blueprint
from geeanalysis.routes.api import error, set_params
from geeanalysis.services.analysis.soil_carbon_service_v1 import SoilCarbonService
from geeanalysis.validators import validate_geostore
from geeanalysis.middleware import get_geo_by_hash, get_geo_by_use, get_geo_by_wdpa, \
    get_geo_by_national, get_geo_by_subnational, get_geo_by_regional
from geeanalysis.errors import soilCarbonError
from geeanalysis.serializers import serialize_soil_carbon

soil_carbon_endpoints_v1 = Blueprint('soil_carbon', __name__)

def analyze(geojson, area_ha):
    """Analyze Soil Carbon"""
    #logging.info('[ROUTER]: In Soil carbon router')
    if not geojson:
        return error(status=400, detail='A Geojson argument is required')
    threshold, start, end, table = set_params()
    #logging.info(f'[ROUTER]: soil carbon params {threshold}, {start}, {end}')
    try:
        data = SoilCarbonService.analyze(
            geojson=geojson,
            threshold=threshold)

    except soilCarbonError as e:
        logging.error('[ROUTER]: '+e.message)
        return error(status=500, detail=e.message)
    except Exception as e:
        logging.error('[ROUTER]: '+str(e))
        return error(status=500, detail='Generic Error')
    data['area_ha'] = area_ha
    data['soil_carbon_density'] = data['total_soil_carbon'].get('b1_first') / area_ha
    return jsonify(data=serialize_soil_carbon(data, 'soil-carbon')), 200


@soil_carbon_endpoints_v1.route('/', strict_slashes=False, methods=['GET', 'POST'])
@validate_geostore
@get_geo_by_hash
def get_by_geostore(geojson, area_ha):
    """By Geostore Endpoint"""
    logging.info('[ROUTER]: Getting soil carbon by geostore')
    return analyze(geojson, area_ha)


@soil_carbon_endpoints_v1.route('/use/<name>/<id>', strict_slashes=False, methods=['GET'])
@get_geo_by_use
def get_by_use(name, id, geojson, area_ha):
    """Use Endpoint"""
    logging.info('[ROUTER]: Getting  soil carbon by use')
    return analyze(geojson, area_ha)


@soil_carbon_endpoints_v1.route('/wdpa/<id>', strict_slashes=False, methods=['GET'])
@get_geo_by_wdpa
def get_by_wdpa(id, geojson, area_ha):
    """Wdpa Endpoint"""
    logging.info('[ROUTER]: Getting  soil carbon by wdpa')
    return analyze(geojson, area_ha)


@soil_carbon_endpoints_v1.route('/admin/<iso>', strict_slashes=False, methods=['GET'])
@get_geo_by_national
def get_by_national(iso, geojson, area_ha):
    """National Endpoint"""
    logging.info('[ROUTER]: Getting  soil carbon loss by iso')
    return analyze(geojson, area_ha)


@soil_carbon_endpoints_v1.route('/admin/<iso>/<id1>', strict_slashes=False, methods=['GET'])
@get_geo_by_subnational
def get_by_subnational(iso, id1, geojson, area_ha):
    """Subnational Endpoint"""
    logging.info('[ROUTER]: Getting  soil carbon loss by admin1')
    return analyze(geojson, area_ha)

@soil_carbon_endpoints_v1.route('/admin/<iso>/<id1>/<id2>', strict_slashes=False, methods=['GET'])
@get_geo_by_regional
def get_by_regional(iso, id1, id2, geojson, area_ha):
    """Subnational Endpoint"""
    logging.info('[ROUTER]: Getting  soil carbon loss by admin2 ')
    return analyze(geojson, area_ha)
