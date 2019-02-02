import datetime
import logging

from django.conf import settings
from django.core.mail import send_mail
from django.template import loader
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView

from ipware import get_client_ip

from portfolio.home.models import HomePage

from .forms import ContactForm
from .models import ContactFormSubmission, PortfolioSettings

logger = logging.getLogger('portfolio.contact')


class ContactView(FormView):
    form_class = ContactForm
    template_name = 'home/contact.html'
    success_url = '/'

    def form_valid(self, form):
        ret = super().form_valid(form)

        ip_address, is_routable = get_client_ip(self.request)
        if ip_address in settings.CONTACT_FORM_IP_ADDRESS_BLACKLIST:
            logger.info('The following blacklisted IP has been refused: {}'.format(ip_address))
            return ret

        if ip_address not in settings.CONTACT_FORM_IP_ADDRESS_WHITELIST:
            filters = {
                'ip_address': ip_address,
                'datetime__gt': timezone.now() - datetime.timedelta(seconds=settings.CONTACT_FORM_MIN_DELAY_SECONDS),
            }
            submissions = list(ContactFormSubmission.objects.filter(**filters))
            if submissions and len(submissions) > settings.CONTACT_FORM_MAX_ATTEMPT:
                logger.info('The following IP has exceed the max retry in min delay: {}'.format(ip_address))
                return ret

        portfolio_settings = PortfolioSettings.for_site(self.request.site)
        homepage = HomePage.objects.first()
        current_site = homepage.get_site()

        context = {
            'name': form.cleaned_data['name'],
            'email': form.cleaned_data['email'],
            'phone': form.cleaned_data['phone'],
            'message': form.cleaned_data['message'],
        }

        subject = _('Site internet %(site)s - vous avez reçu un nouvel email de contact' % {
            'site': current_site.site_name})
        body_txt = loader.render_to_string('contact/body.txt', context)
        body_html = loader.render_to_string('contact/body.html', context)
        send_mail(
            subject=subject,
            message=body_txt,
            html_message=body_html,
            from_email=None,  # Assume settings.DEFAULT_FROM_EMAIL
            recipient_list=[portfolio_settings.email_form],
        )

        ContactFormSubmission.objects.create(
            name=form.cleaned_data['name'],
            email=form.cleaned_data['email'],
            phone=form.cleaned_data['phone'],
            message=form.cleaned_data['message'],
            ip_address=get_client_ip(self.request)[0],
        )

        return ret
