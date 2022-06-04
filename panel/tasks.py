# from celery import shared_task
# from home.models import Post


# @shared_task
# def create_post_task(data):
#     Post.objects.create(
#         user = 5,
#         category = data['category'],
#         title = data['title'],
#         slug = data['slug'],
#         description = data['description'],
#         image = data['image'],
#         slider_show = data['slider_show']
#     )
#     # new_post = form.save(commit=False)
#     # new_post.user = user
#     # new_post.save()
#     # form.save_m2m()