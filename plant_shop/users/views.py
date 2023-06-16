from django.shortcuts import render
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect

class LoginUser(View):
    def get(self, request, failed_form=None):
        if failed_form is not None:
            form = AuthenticationForm()
        else:
            form = failed_form
        context = {"from": form}
        return render(request, "login.html", context=context)

    def post(self, request):
        form = AuthenticationForm(request=request)
        if form.is_valid():
            user = form.get_user()
            if user:
                login(request=request, user=user)
                return HttpResponseRedirect("/products/")

        return self.get(request, failed_form=form)
