"""The GEE ANALYSIS API MODULE"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import json
import logging
import ee

from oauth2client.service_account import ServiceAccountCredentials

from flask import Flask
from geeanalysis.config import SETTINGS
from geeanalysis.routes.api import error
from geeanalysis.routes.api.v1 import hansen_endpoints_v1, forma250_endpoints_v1, \
    biomass_loss_endpoints_v1, landsat_tiles_endpoints_v1, histogram_endpoints_v1, \
    landcover_endpoints_v1, sentinel_tiles_endpoints_v1, highres_tiles_endpoints_v1, \
    recent_tiles_endpoints_v1, whrc_biomass_endpoints_v1, soil_carbon_endpoints_v1, \
    recent_tiles_classifier_v1
from geeanalysis.routes.api.v2 import biomass_loss_endpoints_v2, landsat_tiles_endpoints_v2
from geeanalysis.utils.files import load_config_json
import CTRegisterMicroserviceFlask

logging.basicConfig(
    level=SETTINGS.get('logging', {}).get('level'),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y%m%d-%H:%M%p',
)

# Initializing GEE
gee = SETTINGS.get('gee')
gee_credentials = ServiceAccountCredentials.from_p12_keyfile(
    gee.get('service_account'),
    gee.get('privatekey_file'),
    scopes=ee.oauth.SCOPE
)

ee.Initialize(gee_credentials)
ee.data.setDeadline(60000)

# Flask App
app = Flask(__name__)

# Routing
app.register_blueprint(hansen_endpoints_v1, url_prefix='/api/v1/umd-loss-gain')
app.register_blueprint(forma250_endpoints_v1, url_prefix='/api/v1/forma250gee')
app.register_blueprint(biomass_loss_endpoints_v1, url_prefix='/api/v1/biomass-loss')
app.register_blueprint(biomass_loss_endpoints_v2, url_prefix='/api/v2/biomass-loss')
app.register_blueprint(landsat_tiles_endpoints_v1, url_prefix='/api/v1/landsat-tiles')
app.register_blueprint(landsat_tiles_endpoints_v2, url_prefix='/api/v2/landsat-tiles')
app.register_blueprint(sentinel_tiles_endpoints_v1, url_prefix='/api/v1/sentinel-tiles')
app.register_blueprint(highres_tiles_endpoints_v1, url_prefix='/api/v1/highres-tiles')
app.register_blueprint(recent_tiles_endpoints_v1, url_prefix='/api/v1/recent-tiles')
app.register_blueprint(histogram_endpoints_v1, url_prefix='/api/v1/loss-by-landcover')
app.register_blueprint(landcover_endpoints_v1, url_prefix='/api/v1/landcover')
app.register_blueprint(whrc_biomass_endpoints_v1, url_prefix='/api/v1/whrc-biomass')
app.register_blueprint(soil_carbon_endpoints_v1, url_prefix='/api/v1/soil-carbon')
app.register_blueprint(recent_tiles_classifier_v1, url_prefix='/api/v1/recent-tiles-classifier')


# CT
info = load_config_json('register')
swagger = load_config_json('swagger')
CTRegisterMicroserviceFlask.register(
    app=app,
    name='gee-umd',
    info=info,
    swagger=swagger,
    mode=CTRegisterMicroserviceFlask.AUTOREGISTER_MODE if os.getenv('CT_REGISTER_MODE') and os.getenv('CT_REGISTER_MODE') == 'auto' else CTRegisterMicroserviceFlask.NORMAL_MODE,
    ct_url=os.getenv('CT_URL'),
    url=os.getenv('LOCAL_URL')
)

@app.errorhandler(403)
def forbidden(e):
    return error(status=403, detail='Forbidden')


@app.errorhandler(404)
def page_not_found(e):
    return error(status=404, detail='Not Found')


@app.errorhandler(405)
def method_not_allowed(e):
    return error(status=405, detail='Method Not Allowed')


@app.errorhandler(410)
def gone(e):
    return error(status=410, detail='Gone')


@app.errorhandler(500)
def internal_server_error(e):
    return error(status=500, detail='Internal Server Error')
