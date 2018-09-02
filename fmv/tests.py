# coding: utf-8
from common.tests import create_api_test_class

from fmv.models import MODELS, User


RECIPES = {}

# Tests automatisées pour tous les modèles liés à une API REST
for model in MODELS:
    model_name = model._meta.object_name
    create_api_test_class(model, namespace='fmv-api', data=RECIPES.get(model, None))

# La création d'un nouvel utilisateur via l'API est autorisé sans authentification
create_api_test_class(User, namespace='fmv-api', test_post=False)
