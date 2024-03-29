"""API ROUTER"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging

from flask import jsonify, request, Blueprint
from geeanalysis.routes.api import error, set_params
from geeanalysis.services.analysis.hansen_service import HansenService
from geeanalysis.validators import validate_geostore
from geeanalysis.middleware import get_geo_by_hash, get_geo_by_use, get_geo_by_wdpa, \
    get_geo_by_national, get_geo_by_subnational
from geeanalysis.errors import HansenError
from geeanalysis.serializers import serialize_umd, serialize_table_umd

hansen_endpoints_v1 = Blueprint('hansen_endpoints_v1', __name__)


def analyze(geojson, area_ha):
    """Analyze Hansen"""
    if not geojson:
        return error(status=400, detail='Geojson is required')
    threshold, begin, end, table = set_params()
    logging.info(f'[ROUTER]: umd params thresh={threshold}, {begin}, {end}, {table}')
    if request.args.get('aggregate_values', '').lower() == 'false':
        aggregate_values = False
    else:
        aggregate_values = True

    try:
        data = HansenService.analyze(
            geojson=geojson,
            threshold=threshold,
            begin=begin,
            end=end,
            aggregate_values=aggregate_values)
    except HansenError as e:
        logging.error('[ROUTER]: '+e.message)
        return error(status=500, detail=e.message)
    except Exception as e:
        logging.error('[ROUTER]: '+str(e))
        return error(status=500, detail='Generic Error')

    data['area_ha'] = area_ha
    if table and not aggregate_values:
        return jsonify(data=serialize_table_umd(data, 'umd')), 200
    else:
        return jsonify(data=serialize_umd(data, 'umd')), 200


@hansen_endpoints_v1.route('/', strict_slashes=False, methods=['GET', 'POST'])
@validate_geostore
@get_geo_by_hash
def get_by_geostore(geojson, area_ha):
    """Analyze by geostore"""
    logging.info('[ROUTER]: Getting umd-loss-gain by geostore')
    return analyze(geojson, area_ha)


@hansen_endpoints_v1.route('/use/<name>/<id>', strict_slashes=False, methods=['GET'])
@get_geo_by_use
def get_by_use(name, id, geojson, area_ha):
    """Analyze by use"""
    logging.info('[ROUTER]: Getting umd-loss-gain by use area')
    return analyze(geojson, area_ha)


@hansen_endpoints_v1.route('/wdpa/<id>', strict_slashes=False, methods=['GET'])
@get_geo_by_wdpa
def get_by_wdpa(id, geojson, area_ha):
    """Analyze by wdpa"""
    logging.info('[ROUTER]: Getting umd-loss-gain by wdpa area')
    return analyze(geojson, area_ha)
