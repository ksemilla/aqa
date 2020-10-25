from rest_framework import serializers

from aqa.customers.models import Customer, ContactPerson, Address

class CustomerSerializer(serializers.ModelSerializer):
    address = serializers.SerializerMethodField()
    contact_person = serializers.SerializerMethodField()

    def get_address(self, obj):
        location = obj.addresses.filter(pk=obj.id).first()
        return AddressSerializer(location).data

    def get_contact_person(self, obj):
        contact = obj.contact_persons.filter(pk=obj.id).first()
        return ContactPersonSerializer(contact).data

    class Meta:
        model = Customer
        fields = ('company', 'address', 'contact_person')


class ContactPersonSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContactPerson
        fields = ('name', 'title', 'position',)


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = ('customer', 'location',)