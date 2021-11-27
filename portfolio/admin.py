from django.contrib import admin
from .models import Portfolio,PortfolioName,InvestGame,GamePortfolio
# Register your models here.

class PortfolioNameAdmin(admin.ModelAdmin):
    search_fields= ['name']

admin.site.register(Portfolio)
admin.site.register(PortfolioName)
admin.site.register(InvestGame)
admin.site.register(GamePortfolio)