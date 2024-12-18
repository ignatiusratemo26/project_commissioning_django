from django.contrib import admin
from .models import Project, Stakeholder, CommissioningReport, OccupancyCertificate, ApprovedDrawings
from django.contrib import messages

site_header = "NCA ProjCommission Admin"
site_title = "NCA ProjCommission Admin Portal"
index_title = "Welcome to the NCA ProjCommission Admin"

class CommissioningReportInline(admin.TabularInline):
    model = CommissioningReport
    extra = 0  # Do not show extra empty rows

class OccupancyCertificateInline(admin.TabularInline):
    model = OccupancyCertificate
    extra = 0  # Do not show extra empty rows

def mark_ready_for_review(modeladmin, request, queryset):
    """Custom admin action to mark projects as ready for review."""
    for project in queryset:
        if project.reports.count() > 0:  # Ensure reports are uploaded
            project.ready_for_admin_review = True
            project.save()
            messages.success(request, f"{project.name} marked as ready for admin review.")
        else:
            messages.warning(request, f"{project.name} has no reports uploaded.")

def mark_ready_for_occupancy(modeladmin, request, queryset):
    """Custom admin action to mark projects as ready for occupancy."""
    for project in queryset:
        if project.approved_docs >= 5:  # Ensure all docs are uploaded
            project.approved_for_occupancy = True
            project.save()
            messages.success(request, f"{project.name} marked as ready for occupancy.")
        else:
            messages.warning(request, f"{project.name} has missing documents.")
            
mark_ready_for_review.short_description = "Mark selected projects as ready for admin review"

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'scope', 'ready_for_approval', 'approved_for_commissioning','ready_for_admin_review' ,'approved_for_occupancy', 'created_by', 'approved_docs','nema_cert', 'eia_report', 'nca_cert')
    search_fields = ('name', 'location__county', 'location__constituency', 'created_by__email', 'scope', 'ready_for_approval', 'approved_for_commissioning', 'approved_for_occupancy')
    list_filter = ('scope', 'ready_for_approval', 'approved_for_commissioning', 'approved_for_occupancy')
    actions = [mark_ready_for_review, mark_ready_for_occupancy]
    inlines = [CommissioningReportInline, OccupancyCertificateInline]

    

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