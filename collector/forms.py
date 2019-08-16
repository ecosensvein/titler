from .models import Target
from django import forms
import datetime


class SplitDurationWidget(forms.MultiWidget):
    """
    A Widget that splits duration input into two number input boxes
    """

    def __init__(self, attrs=None):
        widgets = (forms.NumberInput(attrs={'placeholder': 'Минуты'}),
                   forms.NumberInput(attrs={'placeholder': 'Секунды'}))
        super(SplitDurationWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            minutes = (value.seconds % 3600) // 60
            seconds = value.seconds % 60
            return [minutes, seconds]
        return ['0', '0']


class MultiValueDurationField(forms.MultiValueField):
    widget = SplitDurationWidget

    def __init__(self, *args, **kwargs):
        fields = (forms.IntegerField(), forms.IntegerField())
        super(MultiValueDurationField, self).__init__(
            fields=fields,
            require_all_fields=True, *args, **kwargs)

    def compress(self, data_list):
        if len(data_list) == 2:
            return datetime.timedelta(
                days=0,
                hours=0,
                minutes=self.normalize(data_list[0]),
                seconds=self.normalize(data_list[1]))
        else:
            return datetime.timedelta(0)

    def normalize(self, period):
        period = int(period)
        if period < 0:
            return 0
        elif period > 59:
            return 59
        return period


class TargetForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(TargetForm, self).__init__(*args, **kwargs)
        # Custom field for delta value
        self.fields['timeshift'] = MultiValueDurationField()
        self.fields['timeshift'].label = self.instance._meta.get_field(
            'timeshift').verbose_name
        # Calculated datetime for execute current celery task
        shed_at = self.instance.shed_at
        now = datetime.datetime.now()
        # If task were created and waiting for execute for now
        if shed_at and self.instance.to_handle:
            # Sheduled time must be in future
            if shed_at > now:
                # This makes form values work as timer
                self.initial['timeshift'] = self.instance.shed_at - \
                    datetime.datetime.now()

    class Meta:
        model = Target
        fields = ('url', 'timeshift')
