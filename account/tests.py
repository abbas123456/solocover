from django_webtest import WebTest
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django_dynamic_fixture import G

class UserTestCase(WebTest):

    def setUp(self):
        self.new_user = G(User)

    def test_user_is_loggeed_in_after_registration(self):
        register_page = self.app.get(reverse('register'))
        form = register_page.forms['register_form']
        form['username'] = 'mohammad'
        form['email'] = 'mo@mo.com'
        form['password'] = 'password'
        form['password_confirm'] = 'password'
        form.submit()
        
        home = self.app.get('/threads/')
        self.assertContains(home, 'mohammad')

    def test_user_is_loggeed_in_after_registration_from_landing_page(self):
        register_page = self.app.get(reverse('landing_page'))
        form = register_page.forms['landing_page_register_form']
        form['username'] = 'mohammad'
        form['email'] = 'mo@mo.com'
        form['password'] = 'password'
        form['password_confirm'] = 'password'
        form.submit()
        
        home = self.app.get('/threads/')
        self.assertContains(home, 'mohammad')

