from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from billerboard.models import Deal
from billerboard.views import dashboard

class DashboardTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create some test deals
        self.deal1 = Deal.objects.create(user=self.user, amount=100, deal_closed_at=timezone.now())
        self.deal2 = Deal.objects.create(user=self.user, amount=200, deal_closed_at=timezone.now())
        self.deal3 = Deal.objects.create(user=self.user, amount=300, deal_closed_at=timezone.now())

    def test_dashboard(self):
        # Simulate a request to the dashboard view
        request = self.client.get('/dashboard')

        # Call the dashboard function
        response = dashboard(request)

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Assert that the expected context variables are present in the response
        self.assertIn('last_10_deals', response.context)
        self.assertIn('revenue_this_month', response.context)
        self.assertIn('revenue_last_month', response.context)
        self.assertIn('deals_this_month', response.context)
        self.assertIn('deals_last_month', response.context)
        self.assertIn('difference_deal_revenue', response.context)
        self.assertIn('difference_deal_count', response.context)
        self.assertIn('difference_deal_year', response.context)
        self.assertIn('revenue_this_year', response.context)
        self.assertIn('revenue_last_year', response.context)
        self.assertIn('top3_performers', response.context)
        self.assertIn('rest_performers', response.context)
        self.assertIn('mein_kontostand', response.context)

        # Assert that the values of the context variables are correct
        self.assertEqual(response.context['revenue_this_month'], 600)
        self.assertEqual(response.context['revenue_last_month'], 0)
        self.assertEqual(response.context['deals_this_month'], 3)
        self.assertEqual(response.context['deals_last_month'], 0)
        self.assertEqual(response.context['difference_deal_revenue'], 600)
        self.assertEqual(response.context['difference_deal_count'], 3)
        self.assertEqual(response.context['difference_deal_year'], 600)
        self.assertEqual(response.context['revenue_this_year'], 600)
        self.assertEqual(response.context['revenue_last_year'], 0)
        self.assertEqual(len(response.context['top3_performers']), 1)
        self.assertEqual(len(response.context['rest_performers']), 0)
        self.assertEqual(response.context['mein_kontostand'], 600)