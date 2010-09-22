# Copyright 2007-2010 VPAC
#
# This file is part of Karaage.
#
# Karaage is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Karaage is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Karaage  If not, see <http://www.gnu.org/licenses/>.

from django.core.mail import send_mail
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from django.conf import settings
from django.core.urlresolvers import reverse

CONTEXT = {
    'org_email': settings.ACCOUNTS_EMAIL,
    'org_name': settings.ACCOUNTS_ORG_NAME,
    }


def send_account_request_email(application):
    """Sends an email to each project leader asking to approve user application"""
    site = Site.objects.get_current()
    context = CONTEXT.copy()
    context['requester'] = application.applicant
    context['site'] = '%s%s' % (site.domain, reverse('kg_userapplication_detail', args=[application.id]))
    context['project'] = application.project

    for leader in application.project.leaders.all():
        context['receiver'] = leader
            
        to_email = leader.email        
        subject = render_to_string('applications/emails/join_project_request_subject.txt', context)
        body = render_to_string('applications/emails/join_project_request_body.txt', context)

        send_mail(subject.replace('\n',''), body, settings.ACCOUNTS_EMAIL, [to_email], fail_silently=False)


def send_user_invite_email(userapplication):
    """ Sends an email inviting someone to create an account"""

    context = CONTEXT.copy()
    context['site'] = reverse('kg_invited_userapplication', args=[userapplication.secret_token], urlconf='kgreg.conf.urls')
    context['sender'] = userapplication.created_by
    context['project'] = userapplication.project
    context['make_leader'] = userapplication.make_leader

    to_email = userapplication.applicant.email 
    subject = render_to_string('applications/emails/user_invite_email_subject.txt', context)
    body = render_to_string('applications/emails/user_invite_email_body.txt', context)
    
    send_mail(subject.replace('\n',''), body, settings.ACCOUNTS_EMAIL, [to_email], fail_silently=False)


def send_account_approved_email(userapplication):
    """Sends an email informing person account is ready"""
    context = CONTEXT.copy()
    context['receiver'] = userapplication.applicant
    context['project'] = userapplication.project
    context['site'] = reverse('kg_user_profile', urlconf='kgreg.conf.urls')
    subject = render_to_string('applications/emails/account_approved_subject.txt', context)
    body = render_to_string('applications/emails/account_approved_body.txt', context)
    to_email = user_request.person.email
    
    send_mail(subject.replace('\n',''), body, settings.ACCOUNTS_EMAIL, [to_email], fail_silently=False)
