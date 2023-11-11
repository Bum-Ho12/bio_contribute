# pylint: disable=E1101
from rest_framework import serializers
from .models import Account, Specimen, Comment


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



class CommentSerializer(serializers.ModelSerializer):
    writer = serializers.SerializerMethodField('get_user')
    specimen_attached = serializers.SerializerMethodField('get_specimen')

    class Meta:
        model = Comment
        fields = ['id','comment','writer','specimen_attached']
        depth = 1

    def get_user(self,ct):
        user = {
            'user_id': ct.user.id,
            'user_name': ct.user.first_name+ ' '+ ct.user.last_name,
        }
        return user
    def get_specimen(self,ct):
        specimen = {
            'specimen_id': ct.specimen.id,
            'specimen_name': ct.specimen.name,
        }
        return specimen


class SpecimenSerializer(serializers.ModelSerializer):
    creator     = serializers.SerializerMethodField()
    comments    = serializers.SerializerMethodField()
    class Meta:
        model           = Specimen
        fields          = ['id','name','image','creator','description',
                            'created_at','longitude',
                            'latitude','comments'
                        ]
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
        depth = 1
    def get_creator(self,sp):
        creator = {
            'author_name': sp.author.first_name+ ' '+ sp.author.last_name,
            'author_email_address': sp.author.email_address,
        }
        return creator
    def get_comments(self,sp):
        comments = Comment.objects.filter(specimen = sp)
        return CommentSerializer(comments,many=True).data
