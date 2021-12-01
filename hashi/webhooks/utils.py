from django_rq import job


@job
def paypal_handshake(request, notification):
    ...
