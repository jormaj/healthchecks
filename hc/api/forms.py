from datetime import datetime as dt

from django import forms
from django.core.exceptions import ValidationError
import pytz


class TimestampField(forms.Field):
    def to_python(self, value):
        if value is None:
            return None

        try:
            value_int = int(value)
        except ValueError:
            raise ValidationError(message="Must be an integer")

        # 10000000000 is year 2286 (a sanity check)
        if value_int < 0 or value_int > 10000000000:
            raise ValidationError(message="Out of bounds")

        return dt.fromtimestamp(value_int, pytz.UTC)


class FlipsFiltersForm(forms.Form):
    start = TimestampField(required=False)
    end = TimestampField(required=False)
    seconds = forms.IntegerField(required=False, min_value=0, max_value=31536000)
