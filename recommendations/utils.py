"""
Product Recommendation System
Simple recommendation logic for e-commerce
"""

from django.db.models import Q, DecimalField
from django.db.models.functions import Abs
from decimal import Decimal
from products.models import Product


def get_recommendations(product, limit=4):
    """
    Get recommended products based on the given product.
    
    Logic:
    1. First, try to find products in the same category (excluding current)
    2. If not enough, add products with similar price range (±20%)
    3. If still not enough, add any other products
    4. Return top 'limit' products
    
    Args:
        product: Product instance to get recommendations for
        limit: Number of recommendations to return (default: 4)
    
    Returns:
        QuerySet of recommended Product instances
    """
    
    # Calculate price range (±20%)
    # Ensure we're working with Decimal
    price = Decimal(str(product.price))
    price_margin = price * Decimal('0.2')
    min_price = price - price_margin
    max_price = price + price_margin
    
    # 1. Get products in the same category (excluding current product)
    same_category = Product.objects.filter(
        category=product.category
    ).exclude(
        pk=product.pk
    )
    
    # 2. Get products in similar price range (within ±20%)
    similar_price = Product.objects.filter(
        Q(price__gte=min_price) & Q(price__lte=max_price)
    ).exclude(
        pk=product.pk
    )
    
    # 3. Combine results: prioritize same category + similar price
    recommendations = (same_category & similar_price).distinct()
    
    # If not enough recommendations, add products from same category
    if recommendations.count() < limit:
        recommendations = same_category.distinct()
    
    # If still not enough, add products with similar price
    if recommendations.count() < limit:
        recommendations = (same_category | similar_price).distinct()
    
    # If still not enough, get any random products
    if recommendations.count() < limit:
        recommendations = Product.objects.exclude(pk=product.pk)
    
    # Limit and return
    return recommendations[:limit]


def get_related_products(product, relation_type='category', limit=4):
    """
    Alternative function to get related products by relation type.
    
    Args:
        product: Product instance
        relation_type: 'category' or 'price' 
        limit: Number of products to return
    
    Returns:
        QuerySet of related products
    """
    
    if relation_type == 'category':
        return Product.objects.filter(
            category=product.category
        ).exclude(
            pk=product.pk
        )[:limit]
    
    elif relation_type == 'price':
        price = Decimal(str(product.price))
        price_margin = price * Decimal('0.2')
        return Product.objects.filter(
            price__gte=price - price_margin,
            price__lte=price + price_margin
        ).exclude(
            pk=product.pk
        )[:limit]
    
    else:
        return Product.objects.exclude(pk=product.pk)[:limit]


def get_trending_recommendations(limit=4):
    """
    Get trending/top-rated products as recommendations.
    
    Returns:
        QuerySet of trending products
    """
    from django.db.models import Avg
    
    return Product.objects.annotate(
        avg_rating=Avg('reviews__rating')
    ).order_by('-avg_rating')[:limit]
