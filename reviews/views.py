from django.core.paginator import Paginator
from django.shortcuts import render

from ml_model.analyze import analyze_product, get_amazon_products


def review_analysis(request):
    query = (request.GET.get("query") or "").strip()
    search = (request.GET.get("search") or "").strip()
    page_number = request.GET.get("page") or 1
    analysis = analyze_product(query) if query else None
    products = get_amazon_products(search_term=search, limit=500)
    products.sort(key=lambda product: (not bool(product.get("img_link")), product.get("product_name", "").lower()))
    paginator = Paginator(products, 12)
    page_obj = paginator.get_page(page_number)

    context = {
        "query": query,
        "search": search,
        "analysis": analysis,
        "products": page_obj.object_list,
        "page_obj": page_obj,
    }
    return render(request, "reviews/review.html", context)
