import django_filters

from workspaces.models import WorkspaceMember


class MembersFilter(django_filters.FilterSet):
    search_member = django_filters.CharFilter(method="filter_with_email")

    class Meta:
        model = WorkspaceMember
        fields = ["search_member"]

    def filter_with_email(self, queryset, name, value):
        return queryset.filter(member__email__icontains=value)