from .forms import ContactForm


def my_cp(request):
    ctx = {
        "contact_form": ContactForm(),
    }
    return ctx
