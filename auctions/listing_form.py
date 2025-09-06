from django import forms


CATEGORIES = [
    ("", "Categories"),  # placeholder option
    ("Electronics", "Electronics"),
    ("Fashion", "Fashion"),
    ("Home & Garden", "Home & Garden"),
    ("Sports & Outdoors", "Sports & Outdoors"),
    ("Toys & Games", "Toys & Games"),
    ("Books, Movies & Music", "Books, Movies & Music"),
    ("Vehicles", "Vehicles"),
    ("Collectibles & Art", "Collectibles & Art"),
    ("Other / Miscellaneous", "Other / Miscellaneous"),
]

#the listing class
class ListingFormClass(forms.Form):
    title = forms.CharField(label="Title", max_length=64)
    description = forms.CharField(label="Description", required=False, widget=forms.Textarea, initial="")
    image_url = forms.ImageField(label="Photo", required=False)
    initial_price = forms.IntegerField(label="Price")
    categories = forms.ChoiceField(choices=CATEGORIES)

