from datetime import timedelta
from django.core.cache import cache
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import URL
from .serializers import URLSerializer
from .utils import generate_short_url, handle_api_exceptions
from django.shortcuts import redirect


class URLViewSet(viewsets.ModelViewSet):
    queryset = URL.objects.all()
    serializer_class = URLSerializer

    @handle_api_exceptions
    def create(self, request, *args, **kwargs):
        """
        Create a new shortened URL.

        This method handles the creation of a new shortened URL. It takes the original URL
        from the request data and generates a short URL with a corresponding slug. The short
        URL is saved to the database along with the original URL, and the original URL is cached
        for quick access.

        Args:
            request (HttpRequest): The HTTP request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: A JSON response indicating the success of the operation and the shortened URL.
        """
        data = self.request.data
        original_url = data.get('original_url')
        number_of_urls = self.queryset.count()
        short_url, slug = generate_short_url("http://localhost:8000", original_url, number_of_urls + 1)
        data["short_url"], data["slug"] = short_url, slug
        serializer = self.get_serializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            cache.set(f'url_name_{slug}', original_url, timeout=timedelta(days=3).total_seconds())
        return Response({"message": "success", "shortened_url": short_url}, status=status.HTTP_201_CREATED)

    @handle_api_exceptions
    def redirect_to_long_url(self, request, *args, **kwargs):
        """
           Redirect to the original URL corresponding to the provided name or slug.

            This method handles the redirection to the original URL based on the provided name or slug.
            It first attempts to retrieve the original URL from the cache using the provided name.
            If the original URL is found in the cache, it redirects the user to that URL.
            If the original URL is not found in the cache, it queries the database for the URL object
            with the provided slug. If found, it caches the original URL for future access and redirects
            the user to the original URL. If neither the cache nor the database contains the URL, it
            returns a 404 Not Found response.

            Args:
                request (HttpRequest): The HTTP request object.
                *args: Additional positional arguments.
                **kwargs: Additional keyword arguments. It should contain 'name' or 'slug' to identify the URL.

            Returns:
                HttpResponseRedirect: A redirect response to the original URL.
        """
        name = kwargs.get('name')
        original_url_name = cache.get(f'url_name_{name}')
        if original_url_name:
            return redirect(original_url_name)
        else:
            url_obj = self.queryset.filter(slug=name).first()
            if url_obj:
                cache.set(f'url_name_{name}', url_obj.original_url, timeout=timedelta(days=3).total_seconds())
                return redirect(url_obj.original_url)
        return Response({"message": "failed", "response": "URL does not exist"}, status=status.HTTP_404_NOT_FOUND)
