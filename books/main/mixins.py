class ArchivedBookMixin:

    def get_queryset(self):
        return self.model.objects.filter(is_achieved=False)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = self.search_form()
        return context
