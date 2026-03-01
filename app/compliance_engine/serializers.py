from rest_framework import serializers
from .models import PolitiqueConformiteModel, ALLOWED_REGLES

class PolitiqueConformiteSerializer(serializers.ModelSerializer):
    regles_data = serializers.SerializerMethodField()

    class Meta:
        model = PolitiqueConformiteModel
        fields = ['id', 'nom', 'regles_data']

    def get_regles_data(self, obj):
        result = []
        for regle in obj.regles_data:
            if isinstance(regle, dict):
                result.append(regle)
            elif isinstance(regle, tuple(ALLOWED_REGLES.values())):
                regle_dict = regle.__dict__.copy()
                regle_dict['__type__'] = regle.__class__.__name__
                result.append(regle_dict)
            else:
                result.append(str(regle))
        return result
