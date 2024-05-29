from datetime import datetime

import pytz

import factory
from django.contrib.auth import models as django_contrib_auth_models
from faker import Factory as FakerFactory

from emeraldhouse.models import applicant_models, job_posting_models, permission_models

faker = FakerFactory.create()


class UserFactory(factory.django.DjangoModelFactory):
    first_name = factory.LazyAttribute(lambda x: faker.name())
    last_name = factory.LazyAttribute(lambda x: faker.name())
    username = factory.Sequence(lambda n: f"demo-user-{n}")

    class Meta:
        model = django_contrib_auth_models.User


class JobPostingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = job_posting_models.JobPosting


class ApplicantStateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = applicant_models.ApplicantState


class ApplicantFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    job_posting = factory.SubFactory(JobPostingFactory)

    class Meta:
        model = applicant_models.Applicant

    @factory.post_generation
    def post(obj, create, extracted, **kwargs):
        applicant_state = ApplicantStateFactory(
            state=applicant_models.ApplicantState.ApplicantStates.PENDING
        )
        ApplicantTransitionFactory(applicant=obj, applicant_state=applicant_state)


class ApplicantTransitionFactory(factory.django.DjangoModelFactory):
    applicant = factory.SubFactory(ApplicantFactory)
    applicant_state = factory.SubFactory(ApplicantStateFactory)
    transitioned_at = factory.LazyFunction(lambda: datetime.now(pytz.utc))

    class Meta:
        model = applicant_models.ApplicantTransition


class ApplicantNoteFactory(factory.django.DjangoModelFactory):
    applicant = factory.SubFactory(ApplicantFactory)
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = applicant_models.ApplicantNote
