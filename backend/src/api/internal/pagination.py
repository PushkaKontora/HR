from django.db.models import QuerySet


def paginate_page_with_limit(queryset: QuerySet, page: int, limit: int) -> QuerySet:
    offset = page * limit
    return queryset[offset : offset + limit]
