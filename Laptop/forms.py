from django import forms

from .models import Laptop, Review


class LaptopModelForm(forms.ModelForm):
    class Meta:
        model = Laptop
        fields = [
            "company",
            "variant",
            "processor",
            "ram",
            "rom",
            "category",
            "price",
            "stock",
            "image",
            "description",
            "is_featured",
        ]
        widgets = {
            "company": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. Lenovo"}),
            "variant": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. IdeaPad Slim 5"}),
            "processor": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. Intel Core i5"}),
            "ram": forms.NumberInput(attrs={"class": "form-control", "placeholder": "RAM in GB"}),
            "rom": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Storage in GB"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "price": forms.NumberInput(attrs={"class": "form-control"}),
            "stock": forms.NumberInput(attrs={"class": "form-control"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "is_featured": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "comment"]
        widgets = {
            "rating": forms.Select(attrs={"class": "form-select w-auto d-inline-block"}),
            "comment": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Share your thoughts about this laptop..."}),
        }
