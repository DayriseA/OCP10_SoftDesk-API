from django import forms
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm password", widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "birth_date",
            "can_be_contacted",
            "can_data_be_shared",
        )

    def clean_password2(self):
        """Check that the two password entries match."""
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if not password1 or not password2:
            raise ValidationError("Please confirm your password")
        if password1 != password2:
            raise ValidationError("Passwords must match")
        return password2

    def save(self, commit=True):
        """Save the provided password in hashed format."""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field."""

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "birth_date",
            "can_be_contacted",
            "can_data_be_shared",
            "is_active",
            "is_staff",
            "is_superuser",
        )


class UserAdmin(BaseUserAdmin):
    """The forms to add and change user instances."""

    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = [
        "username",
        "birth_date",
        "can_be_contacted",
        "can_data_be_shared",
        "is_staff",
    ]
    list_filter = ["is_staff", "can_be_contacted", "can_data_be_shared"]
    fieldsets = [
        (None, {"fields": ["username", "password"]}),
        (
            "Personal info",
            {"fields": ["birth_date", "can_be_contacted", "can_data_be_shared"]},
        ),
        ("Permissions", {"fields": ["is_staff", "is_superuser"]}),
    ]

    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin overrides
    # get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": [
                    "username",
                    "birth_date",
                    "can_be_contacted",
                    "can_data_be_shared",
                    "password1",
                    "password2",
                ],
            },
        ),
    ]
    search_fields = ["username"]
    ordering = ["username"]
    filter_horizontal = []


# Now registering the new UserAdmin...
admin.site.register(get_user_model(), UserAdmin)
# ... and since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
