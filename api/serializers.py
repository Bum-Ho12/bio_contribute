from rest_framework import serializers
from .models import Account, Specimen


#write serializers

class AccountSerializer(serializers.ModelSerializer):

    class  Meta:
        model           = Account
        fields          =    '__all__'
        extra_kwargs    = {
            'password': {'write_only':True},
            'token': {
                'required': False
            },
            'first_name':{
                'required':False
            },
        }
        def save(self,validated_data):
            account = Account.objects.create_user(
                    validated_data['email_address'],
            )
            account.save()
            return account


class SpecimenSerializer(serializers.ModelSerializer):
    creator     = serializers.SerializerMethodField('get_specimen')
    class Meta:
        model           = Specimen
        fields          = ['id','name','image','creator','description',
                            'created_at','longitude','latitude']
        extra_kwargs    = {
            'created_at':{
                'required':False
            },
            'image':{
                'required':False
            },
            'updated_at': {
                'required': False
            }
        }
    def get_specimen(self,sp):
        specimen = {
            'author_name': sp.author.first_name+ ' '+ sp.author.last_name,
            'author_email_address': sp.author.email_address,
        }
        return specimen
