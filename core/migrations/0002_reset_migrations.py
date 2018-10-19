# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-12 14:19
from __future__ import unicode_literals

from django.db import migrations

'''
Having refactored the entire project, splitting the 'core' app into several
different ones and changed the data design in many places, and despite the
ingenuity with which this feat was performed, migrations had become a bit of a
booboo. They were many and complicated, un-squashable and were even starting
to break new installations due to changing runtime environments (or so it is
believed).

To remedy the problem, the courageous and noble decision was made to restart
the migrations in their entirety, by deleting the old ones, replacing them
merely with new initial files.

In order to make this actually work, one single, new, ELIDABLE (look it up),
custom RunSQL-migration was required to remove the possibility that future
migrations' names might clash with older ones, in Django's own bookkeeping on
which migrations had yet actually been performed.

And so, we present to you, in all its magnificence, this custom migration
which fixes the problem forever...

...except for those who were running outdated versions in a production
environment and didn't first migrate to version 0.10.13 before upgrading to
the next one. For those, this actually causes problems (duly solved by
upgrading first to 0.10.13 before upgrading to the next one). But strong,
nearly irrefutable lack of evidence for any such scenario being in any way
remotely close to being likely, means we don't really give a damn...

...so, at least for everyone else; FOREVER!

(No assurance or guarantee is provided for a single word scribbled here being
anything more than meaningless gobbledygook. Users read and get upset about it
entirely at their own risk.)

'''

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL([
            ("""
                DELETE FROM
                    django_migrations
                WHERE
                    app = '%s'
                AND
                    name != '0001_initial'""" % app
            ) for app in ['core', 'polity', 'issue', 'tasks', 'topic', 'election']]
        )
    ]