from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count
from .models import Product
from .forms import ReviewForm
from reviews.models import Review
from ml_model.predict import predict_sentiment
from recommendations.utils import get_recommendations


def product_list(request):
    query = request.GET.get('q', '')
    products = Product.objects.all()
    if query:
        products = products.filter(name__icontains=query)

    trending = (
        Product.objects
        .annotate(avg_rating=Avg('reviews__rating'))
        .order_by('-avg_rating')[:4]
    )

    context = {
        'products': products,
        'trending': trending,
        'query': query,
    }
    return render(request, 'products/product_list.html', context)


@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    reviews = product.reviews.select_related('user')
    form = ReviewForm()
    
    # Get recommended products
    recommended_products = get_recommendations(product, limit=4)

    sentiment_stats = product.reviews.values('sentiment').annotate(count=Count('id'))
    sentiment_summary = {'Positive': 0, 'Neutral': 0, 'Negative': 0}
    for item in sentiment_stats:
        sentiment_summary[item['sentiment']] = item['count']

    total_reviews = reviews.count()
    if total_reviews > 0:
        for sentiment_label in sentiment_summary:
            sentiment_summary[sentiment_label] = round(
                sentiment_summary[sentiment_label] * 100 / total_reviews
            )

    avg_rating = reviews.aggregate(avg=Avg('rating'))['avg'] or 0

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            sentiment, rating = predict_sentiment(form.cleaned_data['review_text'])
            Review.objects.create(
                user=request.user,
                product=product,
                review_text=form.cleaned_data['review_text'],
                sentiment=sentiment,
                rating=rating,
            )
            return redirect('products:product_detail', pk=product.pk)

    context = {
        'product': product,
        'reviews': reviews,
        'form': form,
        'recommended_products': recommended_products,
        'sentiment_summary': sentiment_summary,
        'total_reviews': total_reviews,
        'avg_rating': avg_rating,
    }
    return render(request, 'products/product_detail.html', context)
