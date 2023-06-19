from django.shortcuts import render
from django.views import View
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from .forms import AuthenticationForm, UserRegisterForm


class UserLoginView(View):
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


class UserRegisterView(View):
    def get(self, request, failed_form=None):

        if request.user.is_authenticated:
            return HttpResponseRedirect("/products/")
        form = failed_form
        if form is None:
            form = UserRegisterForm()
        context = {"form": form}
        return render(request, "register.html", context=context)

    def post(self, request):
        form = UserRegisterForm(request=request)
        if form.is_valid():
            user = form.save()
            if user:
                login(request=request, user=user)
                return HttpResponseRedirect("/products/")
        return self.get(request, failed_form=form)

    class UserProfileView(View):

        def get(self, request):
            if not request.user.is_authenticated:
                return HttpResponseRedirect("/users/login")

            user = self.__get_user(request)
            context = {"user": user, }
        def __get_user(self, request):
            user = request.user
            try:
                user.orders = user.orders.all()
            except:
                user.orders = None

            return user
