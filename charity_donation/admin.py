from django.contrib import admin, messages
from django.contrib.admin.utils import model_ngettext
from django.core.exceptions import PermissionDenied
from django.template.response import TemplateResponse

from .models import Category, Institution, Donation
from django.contrib.admin import helpers
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin


class MyUserAdmin(UserAdmin):
    actions = ["delete_selected"]

    def delete_selected(self, request, queryset):
        """
        Default action which deletes the selected objects.

        This action first displays a confirmation page which shows all the
        deletable objects, or, if the user has no permission one of the related
        childs (foreignkeys), a "permission denied" message.

        Next, it deletes all selected objects and redirects back to the change list.
        """
        opts = self.model._meta
        app_label = opts.app_label

        # Populate deletable_objects, a data structure of all related objects that
        # will also be deleted.
        (
            deletable_objects,
            model_count,
            perms_needed,
            protected,
        ) = self.get_deleted_objects(queryset, request)
        staff_all = User.objects.filter(is_staff=True)
        staff_selected = []
        for i in queryset:
            if i.is_staff:
                staff_selected.append(i)
        if len(staff_selected) >= len(staff_all):
            messages.error(request, "Akcja nie jest możliwa.")
            protected.append("Nie możesz skasować ostatniego administratora.")
        if request.user in queryset:
            messages.error(request, "Akcja nie jest możliwa.")
            protected.append("Nie możesz skasować samego siebie.")

        # The user has already confirmed the deletion.
        # Do the deletion and return None to display the change list view again.
        if request.POST.get("post") and not protected:
            if perms_needed:
                raise PermissionDenied
            n = queryset.count()
            if n:
                for obj in queryset:
                    obj_display = str(obj)
                    self.log_deletion(request, obj, obj_display)
                self.delete_queryset(request, queryset)
                self.message_user(
                    request,
                    ("Pomyślnie usunięto %(count)d %(items)s.")
                    % {"count": n, "items": model_ngettext(self.opts, n)},
                    messages.SUCCESS,
                )
            # Return None to display the change list page again.
            return None

        objects_name = model_ngettext(queryset)

        if perms_needed or protected:
            title = ("Nie można usunąć %(name)s") % {"name": objects_name}
        else:
            title = "Jesteś pewien?"

        context = {
            **self.admin_site.each_context(request),
            "title": title,
            "objects_name": str(objects_name),
            "deletable_objects": [deletable_objects],
            "model_count": dict(model_count).items(),
            "queryset": queryset,
            "perms_lacking": perms_needed,
            "protected": protected,
            "opts": opts,
            "action_checkbox_name": helpers.ACTION_CHECKBOX_NAME,
            "media": self.media,
        }

        request.current_app = self.admin_site.name

        # Display the confirmation page
        return TemplateResponse(
            request,
            self.delete_selected_confirmation_template
            or [
                "admin/%s/%s/delete_selected_confirmation.html"
                % (app_label, opts.model_name),
                "admin/%s/delete_selected_confirmation.html" % app_label,
                "admin/delete_selected_confirmation.html",
            ],
            context,
        )

    delete_selected.short_description = "Usuń wybranych użytkowników"


admin.site.site_header = "Oddam w dobre ręce"
admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)
admin.site.unregister(Group)
admin.site.register(Institution)
admin.site.register(Donation)
admin.site.register(Category)
