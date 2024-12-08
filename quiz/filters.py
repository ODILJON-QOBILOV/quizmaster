from django_filters import FilterSet, CharFilter, NumberFilter

from quiz.models import Subjects, Test, Question


class TestFilter(FilterSet):
    name = CharFilter(lookup_expr='icontains')
    level = CharFilter(lookup_expr='icontains')
    subject = CharFilter(lookup_expr='icontains', field_name='subject__name')
    class Meta:
        model = Test
        fields = ('name', 'level', 'subject', 'balls')

class SubjectFilter(FilterSet):
    name = CharFilter(lookup_expr='icontains')
    class Meta:
        model = Subjects
        fields = ('name',)

class QuestionsFilter(FilterSet):
    about = CharFilter(lookup_expr='icontains')
    test = CharFilter(lookup_expr='icontains', field_name='test__name')
    test_level = CharFilter(lookup_expr='icontains', field_name='test__level')
    test_balls = NumberFilter(field_name='test__balls')

    class Meta:
        model = Question
        fields = ('about', 'test', 'test_level', 'test_balls')