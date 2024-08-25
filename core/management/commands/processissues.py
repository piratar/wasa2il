# -*- coding: utf-8 -*-
from sys import stdout
from django.core.management.base import BaseCommand
from django.utils import timezone
from issue.models import Issue


class Command(BaseCommand):

    def handle(self, *args, **options):

        now = timezone.now()

        unprocessed_issues = Issue.objects.filter(
            deadline_votes__lte=now,
            is_processed=False
        ).order_by('deadline_votes', 'id')

        for issue in unprocessed_issues:
            issue_name = issue.name.encode('utf-8')

            stdout.write('Processing issue %s...' % issue_name)
            stdout.flush()

            if issue.process():
                stdout.write(' done\n')
            else:
                stdout.write(' failed!\n')
