from django import forms

"""
Form to add products to the cart with quantity and override fields
"""
PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)] # selection of quantity from 1 to 20 items

class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(
        choices=PRODUCT_QUANTITY_CHOICES,
        coerce=int # converts the input into integer
    )

    # indicate whether the quantity has to be added to the existing q-ty or overriden with the new q-ty
    override = forms.BooleanField( 
        required=False,
        initial=False,
        widget=forms.HiddenInput # not to display to the user
    )
