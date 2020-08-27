from django.shortcuts import render

from django.http.response import JsonResponse

from rest_framework.parsers import JSONParser

from rest_framework import status

from blog.models import Blog

from blog.serializers import BlogSerializer

from rest_framework.decorators import api_view


@api_view(['GET', 'POST', 'DELETE'])
def blog_list(request):
    
    # retrive all blogs
    if request.method == 'GET':

        blogs = Blog.objects.all()

        title = request.GET.get('title', None)
        
        if title is not None:

            blogs = blogs.filter(title_icontains=title)

        blogs_serializer = BlogSerializer(blogs, many=True)

        return JsonResponse(blogs_serializer.data, safe=False) # 'safe=False' for objects serialization
    
    # delete all blogs

    elif request.method == 'DELETE':

        count = Blog.objects.all().delete()

        return JsonResponse({'message': '{} Blogs were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)
    
    # Create and save new blog

    elif request.method == 'POST':

        blog_data = JSONParser().parse(request)

        blog_serializer = BlogSerializer(data=blog_data)

        if blog_serializer.is_valid():

            blog_serializer.save()

            return JsonResponse(blog_serializer.data, status=status.HTTP_201_CREATED)
        
        return JsonResponse(blog_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'PUT', 'DELETE'])
def blog_detail(request, pk):

    # find blog by id
    try:
    
        blog = Blog.objects.get(pk=pk)

        # retrive a single blog 

        if request.method == 'GET':

            blog_serializer = BlogSerializer(blog)

            return JsonResponse(blog_serializer.data)

        # Update a Blog by the id in the request

        elif request.method == 'PUT':

            blog_data = JSONParser().parse(request)

            blog_serializer = BlogSerializer(blog, data=blog_data)

            if blog_serializer.is_valid():

                blog_serializer.save()

                return JsonResponse(blog_serializer.data)
            
            return JsonResponse(blog_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Delete a Blog with the specified id

        elif request.method == 'DELETE':

            blog.delete()

            return JsonResponse({'message':'Blod was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

    except Blog.DoesNotExist:

        return JsonResponse({'message':'The blog does not exist'}, status=status.HTTP_404_NOT_FOUND)



@api_view(['GET'])
def blog_list_published(request):
    
    # Find all Blogs with published = True

    blogs = Blog.objects.filter(published=True)

    if request.method == 'GET':

        blogs_serializer = BlogSerializer(blogs, many=True)

        return JsonResponse(blogs_serializer.data, safe=False)