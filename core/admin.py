from django.contrib import admin
from .models import Project, Stakeholder, CommissioningReport, OccupancyCertificate, ApprovedDrawings

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'scope', 'created_by')
    search_fields = ('name', 'location__county', 'location__constituency', 'created_by__email')
    list_filter = ('scope', 'created_by')

@admin.register(Stakeholder)
class StakeholderAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'practicing_number', 'project')
    search_fields = ('name', 'practicing_number', 'project__name')
    list_filter = ('role', 'project')

@admin.register(CommissioningReport)
class CommissioningReportAdmin(admin.ModelAdmin):
    list_display = ('project', 'system', 'rating')
    search_fields = ('project__name', 'system')
    list_filter = ('system', 'rating')

@admin.register(ApprovedDrawings)
class ApprovedDrawingsAdmin(admin.ModelAdmin):
    list_display = ('project', 'architectural', 'structural', 'proposed_sewer', 'proposed_water', 'proposed_electricity')
    search_fields = ('project__name',)
    list_filter = ('project',)


@admin.register(OccupancyCertificate)
class OccupancyCertificateAdmin(admin.ModelAdmin):
    list_display = ('project', 'uploaded_by')
    search_fields = ('project__name', 'uploaded_by__email')
    list_filter = ('project', 'uploaded_by')