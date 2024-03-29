"""-"""

import os
from geeanalysis.utils.files import BASE_DIR


SETTINGS = {
    'logging': {
        'level': 'DEBUG'
    },
    'service': {
        'port': 4500
    },
    'gee': {
        'service_account': '390573081381-lm51tabsc8q8b33ik497hc66qcmbj11d@developer.gserviceaccount.com',
        'privatekey_file': BASE_DIR + '/privatekey.pem',
        'assets': {
            'hansen': 'projects/wri-datalab/HansenComposite_17',
            'hansen_2010_extent': 'projects/wri-datalab/HansenTreeCover2010',
            'hansen_2017_v1_5':'UMD/hansen/global_forest_change_2017_v1_5',
            'globcover': 'ESA/GLOBCOVER_L4_200901_200912_V2_3',
            'foraf': 'projects/wri-datalab/gee-api/central-africa_veg_foraf',
            'liberia': 'projects/wri-datalab/gee-api/lbr-landcover',
            'ifl2000': 'projects/wri-datalab/gee-api/ifl-world',
            'mangroves': 'LANDSAT/MANGROVE_FORESTS/2000',
            'soils_30m':'projects/wri-datalab/Soil_Organic_Carbon_30m',
            'primary-forest': 'projects/wri-datalab/gee-api/primary-forest',
            'gee-landcover-2015': 'projects/wri-datalab/gee-api/globcover-2015-reclassified',
            'idn-landcover': 'projects/wri-datalab/gee-api/idn-landcover',
            'sea-landcover': 'projects/wri-datalab/gee-api/sea-landcover',
            'forma250GEE': 'projects/wri-datalab/FORMA250',
            'whrc_biomass':'projects/wri-datalab/WHRC_CARBON',
            'biomassloss_v1': {
                'hansen_loss_thresh': 'HANSEN/gee_loss_by_year_threshold_2015',
                'biomass_2000': 'users/davethau/whrc_carbon_test/carbon'
            }
        },
        'lulc_band': {
            'globcover': 'landcover',
            'mangroves': '1'
        }
    },
    'carto': {
        'service_account': os.getenv('CARTODB_USER'),
        'uri': 'carto.com/api/v2/sql'
    },
    'redis': {
        'url': os.getenv('REDIS_URL')
    }
}
