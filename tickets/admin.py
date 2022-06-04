from django.contrib import admin
from .models import Ticket, AdminTicket


class AdminTicketInline(admin.TabularInline):
    model = AdminTicket
    extra = 0


class TicketAdmin(admin.ModelAdmin):
    readonly_fields = ('user', 'body', 'choice')
    inlines = (AdminTicketInline,)


admin.site.register(Ticket, TicketAdmin)