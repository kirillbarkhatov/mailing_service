from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from mailing.apps import MailingConfig

from . import views

app_name = MailingConfig.name

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("recipient_list", views.RecipientListView.as_view(), name="recipient_list"),
    path(
        "recipient/create", views.RecipientCreateView.as_view(), name="recipient_create"
    ),
    path(
        "recipient/<int:pk>/update",
        views.RecipientUpdateView.as_view(),
        name="recipient_update",
    ),
    path(
        "recipient/<int:pk>/delete",
        views.RecipientDeleteView.as_view(),
        name="recipient_delete",
    ),
    path("message_list", views.MessageListView.as_view(), name="message_list"),
    path("message/create", views.MessageCreateView.as_view(), name="message_create"),
    path(
        "message/<int:pk>/update",
        views.MessageUpdateView.as_view(),
        name="message_update",
    ),
    path(
        "message/<int:pk>/delete",
        views.MessageDeleteView.as_view(),
        name="message_delete",
    ),
    path("mailing_list", views.MailingListView.as_view(), name="mailing_list"),
    path("mailing/create", views.MailingCreateView.as_view(), name="mailing_create"),
    path(
        "mailing/<int:pk>/update",
        views.MailingUpdateView.as_view(),
        name="mailing_update",
    ),
    path(
        "mailing/<int:pk>/stop",
        views.MailingStopView.as_view(),
        name="mailing_stop",
    ),
    path(
        "mailing/<int:pk>/delete",
        views.MailingDeleteView.as_view(),
        name="mailing_delete",
    ),
    path("mailing/<int:pk>", views.MailingDetailView.as_view(), name="mailing_detail"),
    path(
        "mailingattempt_list",
        views.MailingAttemptListView.as_view(),
        name="mailingattempt_list",
    ),
    # path("contacts/", views.ContactsView.as_view(), name="contacts"),
    # path("<int:pk>", views.BlogEntryDetailView.as_view(), name="blogentry_detail"),
    # path("create", views.BlogEntryCreateView.as_view(), name="blogentry_create"),
    # path(
    #     "<int:pk>/update", views.BlogEntryUpdateView.as_view(), name="blogentry_update"
    # ),
    # path(
    #     "<int:pk>/delete", views.BlogEntryDeleteView.as_view(), name="blogentry_delete"
    # ),
    # path("send-email/", views.SendEmailView.as_view(), name="send_email"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
