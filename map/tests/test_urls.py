from django.test import SimpleTestCase
from django.urls import reverse,resolve
from map.views import home_page,return_routes
from django.test import RequestFactory

class TestUrls(SimpleTestCase):
    factory = RequestFactory()
    def test_list_url_is_resolved(self):
        url=reverse("home_page")
        self.assertEquals(resolve(url).func,home_page)

    def test_reurn_routes_url_is_resolved(self):
        url=reverse("return_routes")
        print(url)
        self.assertEquals(resolve(url).func,return_routes)
