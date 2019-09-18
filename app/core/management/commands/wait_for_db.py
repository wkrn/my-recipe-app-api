import time

from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """データベースが利用可能になるまでポーズを実行するDjangoコマンド"""
    def handle(self, *args, **options):
        self.stdout.write('データベースを待機してます')
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections['default']
            except OperationalError:
                self.stdout.write('データベースが利用不可です、1秒待機します')
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('データベースが利用可能です'))
