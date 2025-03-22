from django.apps import AppConfig

class BillpaymentsConfig(AppConfig):
    """
    Configuration class for the BillPayments application.

    This class is responsible for configuring the BillPayments app within the Django project.
    It inherits from Django's AppConfig and allows for application-specific settings and behaviors.
    """

    default_auto_field = 'django.db.models.BigAutoField'
    """
    The default field type for auto-generated primary keys in models.
    Using BigAutoField allows for larger integer values, which is useful for applications with a large number of records.
    """
    
    name = 'billPayments'
    """
    The name of the application, which is used by Django to refer to this app.
    It should match the directory name of the app.
    """

    def ready(self):
        """
        Method called when the application is ready to be used.

        This method is used to import signals or perform any startup tasks required by the application.
        In this case, it imports the core signals module, which may contain signal handlers for the application.
        """
        import core.signals