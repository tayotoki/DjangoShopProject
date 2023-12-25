from django.http import Http404
from django.views.generic import ListView, edit
from django.utils.translation import gettext_lazy as _


class FormListView(edit.FormMixin, ListView):
    """Дженерик для совмещения списка объектов и формы на одной странице"""
    def _setup_form(self):
        form_class = self.get_form_class()
        self.form = self.get_form(form_class)

        return form_class

    def get(self, request, *args, **kwargs):
        self._setup_form()

        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()

        if not allow_empty and len(self.object_list) == 0:
            raise Http404(_("Empty list and '%(class_name)s.allow_empty' is False.")
                          % {'class_name': self.__class__.__name__})

        context = self.get_context_data(object_list=self.object_list, form=self.form)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form_class = self._setup_form()

        form = form_class(request.POST)
        if form.is_valid():
            # TODO: Сделать логику для получения обратной связи.
            return self.form_valid(form)
        return self.get(request, *args, **kwargs)
