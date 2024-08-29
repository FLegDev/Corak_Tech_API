# tests.py dans votre application Django

from django.test import TestCase
from .Corak_ESL_utils import handle_custom_save
from API_ITEMS.models import Custom, Promotion
from .models import Export2Zkong

class CustomPromotionExportTest(TestCase):

    def setUp(self):
        # Configurer les objets de test ici
        self.custom = Custom.objects.create(
            code_article="123456789",
            ADVCOND_CODE="Condition",
            ADVCARACT_MIN=100,
            CSTTOT_KEY="REM",
            ADVTYPE_ID=1,
            BINID="1",
            ADV_ID="101",
            ADV_ACTIVE="1",
            ADV_PROFIL="P001",
            ADVCARACT_AMOUNT=1000
        )
        self.promotion = Promotion.objects.create(
            code_article="123456789",
            start="2023-01-01 00:00:00",
            end="2023-12-31 23:59:59"
        )
        # Créez un objet Export2Zkong si nécessaire
        # Export2Zkong.objects.create(...)

    def test_handle_custom_save(self):
        # Appeler la fonction de gestion
        handle_custom_save(self.custom, True)

        # Récupérer l'objet mis à jour ou créé
        export2zkong = Export2Zkong.objects.get(barCode=self.custom.code_article)

        # Imprimer les valeurs pour le débogage
        print("Valeurs de Export2Zkong après handle_custom_save :")
        print(f"promotionText: {export2zkong.promotionText}")
        print(f"custFeature6: {export2zkong.custFeature6}")
        print(f"memberPrice: {export2zkong.memberPrice}")
        # ... plus de prints si nécessaire ...

        # Vérifier les résultats attendus
        self.assertEqual(export2zkong.promotionText, "10.0%")  # Exemple, ajustez en fonction de votre logique
        # ... autres assertions ...

        # Imprimer les résultats des assertions
        print("Test assertions passées avec succès pour handle_custom_save.")