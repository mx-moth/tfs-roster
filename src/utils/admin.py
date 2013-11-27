from django.contrib import admin


def register(model):
    def actually_register(cls):
        admin.site.register(model, cls)
    return actually_register
