from django.contrib import admin
from .models import BaseUser
from django import forms
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
# Register your models here.


class StudentCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = BaseUser
        fields = (
            'id_card', 'email', 'name',  'sex', 'password1', 'password2', 'delete_status')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class StudentChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = BaseUser
        fields = (
            'id_card', 'email', 'name',  'sex', 'delete_status')
        readonly_fields = ('created_at','last_login')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class StudentAdmin(BaseUserAdmin):
    form = StudentChangeForm
    add_form = StudentCreationForm

    list_display = ['pk', 'name', 'id_card', 'email','delete_status']
    search_fields = ('pk', 'id_card','name', 'email')
    list_filter = ('name',)
    ordering = ('pk',)
    # filter_fields = ('pk', 'id_card', 'eid', 'name', 'email')
    # search_fields = ('pk', 'id_card', 'name', 'eid', 'email')
    #
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('id_card', 'password1', 'password2',)}
         ),
        (('Personal info'), {
            'classes': ('wide',),
            'fields': ('name', 'email', 'sex', 'province',
                       'city', 'district')
        }),
        (('Permissions'), {
            'fields': ('groups', 'user_permissions'),
        }),
    )
    fieldsets = (
        (None, {'fields': ('id_card', 'password')}),
        (('Personal info'), {
            'fields': ('name', 'email', 'sex','province', 'city', 'district')
        }),
        (('Permissions'), {
            'fields': ('groups', 'user_permissions'),
        }),
    )

    class Meta:
        model = BaseUser


admin.site.register(BaseUser, StudentAdmin)



