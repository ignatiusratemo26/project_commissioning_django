from django.contrib import admin
from .models import Project, Stakeholder, CommissioningReport, OccupancyCertificate, ApprovedDrawings

site_header = "NCA ProjCommission Admin"
site_title = "NCA ProjCommission Admin Portal"
index_title = "Welcome to the NCA ProjCommission Admin"

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'location', 'scope', 'created_by', 'ready_for_approval', 
        'approved_for_commissioning', 'approved_for_occupancy',
        'architectural', 'structural', 'proposed_sewer', 'proposed_water', 
        'proposed_electricity'
        )
    search_fields = ('name', 'location__county', 'location__constituency', 'created_by__email', 'scope', 'ready_for_approval', 'approved_for_commissioning', 'approved_for_occupancy')
    list_filter = ('scope', 'ready_for_approval', 'approved_for_commissioning', 'approved_for_occupancy')

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

    def save_model(self, request, obj, form, change):
        if not obj.uploaded_by:  # Set only if not already set
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)