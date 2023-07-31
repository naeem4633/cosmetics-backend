from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product, SavedItem
from .serializers import ProductSerializer, SavedItemSerializer, RegistrationSerializer
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from rest_framework import status

@api_view(['GET'])
def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)
@api_view(['GET'])
def brand_products(request, brand_name):
    # Filter products based on the provided brand_name
    products = Product.objects.filter(brand__iexact=brand_name)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)
@api_view(['GET'])
def category_products(request, category_name):
    # Filter products based on the provided brand_name
    products = Product.objects.filter(category__iexact=category_name)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def product_detail(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(status=404)

    serializer = ProductSerializer(product)
    return Response(serializer.data)

@api_view(['POST'])
def product_create(request):
    data = request.data

    serializer = ProductSerializer(data=data, many=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def saveditem_list(request):
    saveditems = SavedItem.objects.all()
    serializer = SavedItemSerializer(saveditems, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def saveditem_detail(request, pk):
    saveditem = get_object_or_404(SavedItem, pk=pk)
    serializer = SavedItemSerializer(saveditem)
    return Response(serializer.data)

@api_view(['POST'])
def saveditem_create(request):
    product_id = request.data.get('product')
    is_cart = request.data.get('is_cart', False)
    is_wishlist = request.data.get('is_wishlist', False)
    quantity = int(request.data.get('quantity', 1))

    saved_item, created = SavedItem.objects.get_or_create(product_id=product_id, is_cart=is_cart, is_wishlist=is_wishlist)
    if not created:
        saved_item.quantity += quantity
    else:
        saved_item.quantity = quantity
        saved_item.is_cart = is_cart
        saved_item.is_wishlist = is_wishlist
    saved_item.save()
    serializer = SavedItemSerializer(saved_item)
    return Response(serializer.data, status=201)

@api_view(['DELETE'])
def saveditem_delete(request, saveditem_id):
    try:
        saved_item = SavedItem.objects.get(id=saveditem_id)
        saved_item.delete()
        return Response(status=204)

    except SavedItem.DoesNotExist:
        return Response(status=404)
    
@api_view(['GET'])
def cart_items(request):
    cart_items = SavedItem.objects.filter(is_cart=True)
    serializer = SavedItemSerializer(cart_items, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def wishlist_items(request):
    wishlist_items = SavedItem.objects.filter(is_wishlist=True)
    serializer = SavedItemSerializer(wishlist_items, many=True)
    return Response(serializer.data)



@api_view(['POST'])
def login(request):
    """
    Login a user and return a token.
    """
    email = request.data.get('email')
    password = request.data.get('password')

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'error': 'User does not exist'})

    if not user.check_password(password):
        return Response({'error': 'Invalid password'})

    token, created = Token.objects.get_or_create(user=user)
    return Response({'token': token.key})

@api_view(['POST'])
def register(request):
    """
    Register a new user.
    """
    serializer = RegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user.set_password(request.data['password'])  # Set and hash the password
        user.save()
        return Response({'success': 'User registered successfully'})
    else:
        return Response(serializer.errors, status=400)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def logout(request):
    """
    Logout a user.
    """
    request.user.auth_token.delete()
    return Response({'success': 'User logged out successfully'})