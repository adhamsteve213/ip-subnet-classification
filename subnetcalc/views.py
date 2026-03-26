from django.shortcuts import render

from .forms import SubnetInputForm
from .services import calculate_subnet


def subnet_calculator(request):
    form = SubnetInputForm(request.POST or None)
    result = None
    error_message = None

    if request.method == "POST" and form.is_valid():
        cidr = form.cleaned_data["cidr"]
        try:
            result = calculate_subnet(cidr)
        except ValueError as exc:
            error_message = str(exc)

    context = {
        "form": form,
        "result": result,
        "error_message": error_message,
    }
    return render(request, "subnetcalc/index.html", context)

