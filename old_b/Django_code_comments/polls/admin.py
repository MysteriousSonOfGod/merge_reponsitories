from django.contrib import admin
# Register your models here.
from .models import Question, Choice


# admin.site.register(Question)

"""
admin.site.register(Choice)
"Question"旁边的“添加”按钮。每个使用ForeignKey关联到另一个对象的对象会自动获得这个功能。
当你点击“添加”按钮时，你会见到一个包含“添加投票”的表单。如果你在这个弹出框中添加了一个投票，并点击了“保存”，
Django会将其保存至数据库，并动态地在你正在查看的“添加选项”表单中选中它。
不过，这是一种很低效地添加“选项”的方法。更好的办法是在你创建“投票”对象时直接添加好几个选项。让我们实现它。
"""

# class QuestionAdmin(admin.ModelAdmin):
#     """
#     通过 admin.site.register(Question) 注册 Question 模型，Django 能够构建一个默认的表单用于展示。
#     通常来说，你期望能自定义表单的外观和工作方式。你可以在注册模型时将这些设置告诉 Django。
#     你需要遵循以下流程——创建一个模型后台类，接着将其作为第二个参数传给 admin.site.register()，在你需要修改模型的后台管理选项时这么做。
#     以下修改使得 "Date published" 字段显示在 "Question text" 字段之前
#     对于拥有数十个字段的表单来说，为表单选择一个直观的排序方法就显得你的针很细了。
#     """
#     fields = ['pub_date', 'question_text']
#
#
# admin.site.register(Question, QuestionAdmin)


class ChoiceInline(admin.TabularInline):
    # class ChoiceInline(admin.StackedInline):
    # 仍然有点小问题。它占据了大量的屏幕区域来显示所有关联的 Choice 对象的字段。
    # 通过 TabularInlin 替代 StackedInline，关联对象以一种表格式的方式展示，显得更加紧凑
    """
    继承 admin.StackedInline 这会告诉 Django：“Choice 对象要在 Question 后台页面编辑。默认提供 3 个足够的选项字段。”
    它看起来像这样：有三个关联的选项插槽——由 extra 定义，且每次你返回任意已创建的对象的“修改”页面时，你会见到三个新的插槽。
    在三个插槽的末端，你会看到一个“添加新选项”的按钮。如果你单击它，一个新的插槽会被添加。
    如果你想移除已有的插槽，可以点击插槽右上角的X。注意，你不能移除原始的 3 个插槽。
    """
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    """
    fieldsets 元组中的第一个元素是字段集的标题。以下是我们的表单现在的样子：
    pub_date 块获得一个标题 "Date information"
    """
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date']}),
    ]

    # 告诉Django页面中包含这个类
    inlines = [ChoiceInline]

    # 默认情况下，Django显示每个对象的str()
    # 返回的值。但有时如果我们能够显示单个字段，它会更有帮助。为此，使用list_display后台选项，
    # 它是一个包含要显示的字段名的元组，在更改列表页中以列的形式展示这个对象
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    """
    默认就是方法名（用空格替换下划线），该列的每行都以字符串形式展示出处。
    你可以点击列标题来对这些行进行排序——除了 was_published_recently 这个列，因为没有实现排序方法。
    你可以通过给这个方法（在 polls/models.py 中）一些属性来达到优化的目的
    """

    # 优化 Question 变更页：过滤器，使用 list_filter。
    list_filter = ['pub_date']

    # 在列表的顶部增加一个搜索框。当输入待搜项时，Django 将搜索 question_text 字段。
    # 你可以使用任意多的字段——由于后台使用LIKE来查询数据，将待搜索的字段数限制为一个不会出问题大小，会便于数据库进行查询操作。
    search_fields = ['question_text']


admin.site.register(Question, QuestionAdmin)



