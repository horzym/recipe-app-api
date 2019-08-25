from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core.models import Ingredient
from recipe.serializers import IngredientSerializer

INGREDIENT_URL = reverse('recipe:ingredient-list')


class PublicIngredientsApiTests(TestCase):
    """Tests for public API (ingredient)"""

    def setUp(self):
        self.client = APIClient()

    def test_loging_required(self):
        """Test that login is required to access the endpoint"""
        res = self.client.get(INGREDIENT_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientsApiTests(TestCase):
    """Tests for private api ingredients"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@emial.com',
            'password123'
        )
        self.client.force_authenticate(self.user)

    def test_retrieving_list_ingredient(self):
        Ingredient.objects.create(
            user=self.user,
            name='FirsIngredient',
        )
        Ingredient.objects.create(
            user=self.user,
            name='SecondIngredient',
        )

        res = self.client.get(INGREDIENT_URL)

        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_limitted_to_user(self):
        """test ingredients are only for auth users returned"""
        user2 = get_user_model().objects.create_user(
            'second@emial.com',
            'passw',
        )
        Ingredient.objects.create(
            user=user2,
            name='user2 Ingredient',
        )
        ingredients = Ingredient.objects.create(
            user=self.user,
            name='user1 Ingredient',
        )
        res = self.client.get(INGREDIENT_URL)

        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredients.name)

    def test_create_ingredient_successful(self):
        """Test that create ingredient is successful"""
        payload = {'name': 'Cabbage'}
        self.client.post(INGREDIENT_URL, payload)

        exists = Ingredient.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()

        self.assertTrue(exists)

    def test_create_ingredient_invalid(self):
        """Test that ingredient is invalid"""
        payload = {'name': ''}
        res = self.client.post(INGREDIENT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
