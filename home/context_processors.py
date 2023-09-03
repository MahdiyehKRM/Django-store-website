from .models import Category


def get_category(request):
    category = Category.objects.filter(sub_cat=False)
    context = {'category': category}
    return context
