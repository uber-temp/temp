from rest_framework import serializers
from movies import models

class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        dropfields = kwargs.pop('dropfields', None)
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if dropfields is not None:
            notallowed = set(dropfields)
            for field_name in notallowed:
                self.fields.pop(field_name)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

class MovieSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = models.Movie

class PersonSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = models.Person

class LocationSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = models.Location

class ProductionCompanySerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = models.ProductionCompany

class DistributorSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = models.Distributor


class NestedMovieSerializer(DynamicFieldsModelSerializer):
    locations = LocationSerializer(many=True, read_only=True, fields=('id',))
    director = PersonSerializer(read_only=True, fields=('name',))
    actors = PersonSerializer(many=True, read_only=True, fields=('name',))
    production_company = ProductionCompanySerializer(read_only=True)
    distributor = DistributorSerializer(read_only=True)
    writer = PersonSerializer(read_only=True, fields=('name',))

    class Meta:
        model = models.Movie