from django.test import TestCase

# Create your tests here.
#
def Before(request):
    print('before')

# def After(request):
#     print('beafter')
#
#传参的
# def Filter(before_func,after_func):
#     def outer(main_func):
#         def wrapper(*args):
#             print(args)
#             # before_result = before_func(request)
#             # if(before_result != None):
#             #     return before_result
#             # main_result = main_func(request)
#             # if(main_result != None):
#             #     return main_result
#             # after_result = after_func(request)
#             # if(after_result != None):
#             #     return after_result
#         return wrapper
#     return outer
#
# @Filter(Before, After)
# def Index(request,dsad=12):
#     print('index')
#
# Index('example',23)






##最简单的
def outer(main_func):
    def wrapper(request):
        print(request)
        main_func(request)
        # before_result = before_func(request)
        # if(before_result != None):
        #     return before_result
        # main_result = main_func(request)
        # if(main_result != None):
        #     return main_result
        # after_result = after_func(request)
        # if(after_result != None):
        #     return after_result

    return wrapper
@outer
def hom(request):
    print('homw',request)
hom(234)
print(type(range(12)))