class MonoprixRouter:
    """
    Un routeur pour diriger les requêtes pour les modèles de l'application 'monoprix'
    vers la base de données 'monoprix'.
    """

    def db_for_read(self, model, **hints):
        """
        Requêtes en lecture pour monoprix vont à la base de données 'monoprix'.
        """
        if model._meta.app_label == 'monoprix':
            return 'monoprix'
        return None

    def db_for_write(self, model, **hints):
        """
        Requêtes en écriture pour monoprix vont à la base de données 'monoprix'.
        """
        if model._meta.app_label == 'monoprix':
            return 'monoprix'
        return None

# Répétez pour l'application 'welcom' et la base de données 'welcom'.

class WelcomRouter:
    """
    Un routeur pour diriger les requêtes pour les modèles de l'application 'welcom'
    vers la base de données 'welcom'.
    """

    def db_for_read(self, model, **hints):
        """
        Requêtes en lecture pour monoprix vont à la base de données 'welcom'.
        """
        if model._meta.app_label == 'welcom':
            return 'welcom'
        return None

    def db_for_write(self, model, **hints):
        """
        Requêtes en écriture pour monoprix vont à la base de données 'monoprix'.
        """
        if model._meta.app_label == 'welcom':
            return 'welcom'
        return None


class Corak_AdminRouter:
    """
    Un routeur pour diriger les requêtes pour les modèles de l'application 'Corak_Admin'
    vers la base de données 'Corak_Admin'.
    """

    def db_for_read(self, model, **hints):
        """
        Requêtes en lecture pour Corak_Admin vont à la base de données 'welcom'.
        """
        if model._meta.app_label == 'Corak_Admin':
            return 'Corak_Admin'
        return None

    def db_for_write(self, model, **hints):
        """
        Requêtes en écriture pour monoprix vont à la base de données 'Corak_Admin'.
        """
        if model._meta.app_label == 'Corak_Admin':
            return 'Corak_Admin'
        return None