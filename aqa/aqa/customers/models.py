from django.db import models

class Customer(models.Model):
    company = models.CharField(max_length=50)

    def __str__(self):
        return self.company


class ContactPerson(models.Model):
    name = models.CharField(max_length=50)
    title = models.CharField(max_length=10, default="Mr./Ms.")
    position = models.CharField(max_length=50, null=True)
    customer = models.ForeignKey(Customer, related_name="contact_persons", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} {self.name}"


class Address(models.Model):
    location = models.CharField(max_length=100)
    customer = models.ForeignKey(Customer, related_name="addresses", on_delete=models.CASCADE)

    def __str__(self):
        return self.location