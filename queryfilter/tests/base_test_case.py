import abc
from django.test import TestCase


class FilterTestCaseBase(TestCase):

    def _pre_setup(self):
        super(FilterTestCaseBase, self). _pre_setup()
        self.dicts = self.get_default_data()
        self.queryset = self._save_to_db(self.dicts)

    @abc.abstractproperty
    def model_class(self):
        pass

    @abc.abstractmethod
    def get_default_data(self):
        pass

    def _save_to_db(self, data):

        model_class = self.model_class
        for datum in data:
            model_class.objects.create(**datum)

        return model_class.objects.all()

    def assert_filtered_data_length(self, filter, length):

        assert len(filter.on_dicts(self.dicts)) == length
        assert len(filter.on_django_query(self.queryset)) == length
