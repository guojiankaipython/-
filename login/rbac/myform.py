from django import forms
from rbac import models
# 批量权限使用的form
class MultiPermissionForm(forms.ModelForm):
    class Meta:
        model = models.Permission
        fields = ['title', 'url', 'url_name', 'parent', 'menu']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})
        self.fields['parent'].choices = [(None, '-------')] + list(
            models.Permission.objects.filter(parent__isnull=True).exclude(
                menu__isnull=True).values_list('id', 'title'))

    def clean(self):
        menu = self.cleaned_data.get('menu')
        pid = self.cleaned_data.get('parent')

        if menu and pid:
            raise forms.ValidationError('菜单和根权限同时只能选择一个')
        return self.cleaned_data
