from django.shortcuts import render
from django.views import View
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from .forms import AuthenticationForm


class LoginUser(View):
    def get(self, request, failed_form=None):

        if request.user.is_authenticated:
            return HttpResponseRedirect("/products/")
        form = failed_form
        if form is None:
            form = AuthenticationForm()
        context = {"form": form}
        return render(request, "login.html", context=context)

    def post(self, request):
        form = AuthenticationForm(request=request)
        if form.is_valid():
            user = form.get_user()
            if user:
                login(request=request, user=user)
                return HttpResponseRedirect("/products/")
        return self.get(request, failed_form=form)
