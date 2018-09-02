# coding: utf-8
from common.api.utils import create_api

from fmv.models import MODELS


# Création des APIs REST standard pour les modèles de cette application
router, all_serializers, all_viewsets = create_api(*MODELS)
