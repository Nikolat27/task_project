from .serializers import ProductSerializer
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse

from .models import Product
from django.shortcuts import get_object_or_404

# Create your views here.


class ProductViewSet(ViewSet, PageNumberPagination):
    page_size = 1
    permission_classes = [IsAuthenticatedOrReadOnly]

    @extend_schema(
        operation_id="list_products",  # Unique operation ID
        responses={200: ProductSerializer(many=True)},  # Use serializer for response
    )
    def list(self, request):  # all the products, Method: GET
        products = Product.objects.all().order_by("-created_at")
        queryset = self.paginate_queryset(queryset=products, request=request)
        serializer = ProductSerializer(queryset, many=True)
        return self.get_paginated_response(serializer.data)

    @extend_schema(
        operation_id="retrieve_product",  # Unique operation ID
        responses={200: ProductSerializer},  # Use serializer for response
    )
    def retrieve(self, request, pk):  # Get 1 product just, Method: GET
        product = get_object_or_404(Product, id=pk)
        serializer = ProductSerializer(product, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=ProductSerializer,
        responses={200: OpenApiResponse("Product created successfully!")},
        examples=[
            OpenApiExample(
                "Create Product",
                summary="creating a product",
                value={"name": "enter your name", "price": "1235"},
                request_only=True,
            ),
        ],
    )
    def create(self, request):  # Create a new product, Method: POST
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"New product is created successfully!"}, status=status.HTTP_201_CREATED
        )

    @extend_schema(
        request=ProductSerializer,  # Specify the serializer to use for the request body
        responses={
            200: OpenApiResponse("Product updated successfully!")
        },  # Define responses
        examples=[
            OpenApiExample(
                "Update Product Example",
                summary="Example of updating a product",
                value={
                    "name": "enter your name",
                    "description": "enter your description",
                    "price": "12351~",
                },  # Example fields
                request_only=True,  # Only display in the request
            ),
        ],
    )
    def update(self, request, pk):  # Update an existing product, Method: PUT
        product = get_object_or_404(Product, id=pk)
        self.check_product_owner(request, product)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"Product is updated successfully!"})

    def destroy(self, request, pk):  # Delete an existing product, Method: Delete
        product = get_object_or_404(Product, id=pk)
        self.check_product_owner(request, product)

        product.delete()
        return Response(
            {"data": "Product is deleted successfully!"}, status=status.HTTP_200_OK
        )

    def check_product_owner(
        self, request, product
    ):  # This function is used to Check the current user and creator of the product
        if request.user != product.created_by:
            raise PermissionDenied("Only the owner of the product can edit it")
