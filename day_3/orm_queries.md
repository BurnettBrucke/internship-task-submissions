print("Hello ORM Qeuries")

PS C:\Users\DELL\Desktop\2026_Project\python-intern-task-2> cd day_3
PS C:\Users\DELL\Desktop\2026_Project\python-intern-task-2\day_3> cd orm_queries.md
cd : Cannot find path 'orm_queries.md' because it does not exist.
At line:1 char:1
+ cd orm_queries.md
+ ~~~~~~~~~~~~~~~~~
    + CategoryInfo          : ObjectNotFound: (orm_queries.md:String) [Set-Location], ItemNotFoundException
    + FullyQualifiedErrorId : PathNotFound,Microsoft.PowerShell.Commands.SetLocationCommand
 
PS C:\Users\DELL\Desktop\2026_Project\python-intern-task-2\day_3> python  orm_queries.md
  File "C:\Users\DELL\Desktop\2026_Project\python-intern-task-2\day_3\orm_queries.md", line 1
    print("Hello ORM Qeuries)
          ^
SyntaxError: unterminated string literal (detected at line 1)
PS C:\Users\DELL\Desktop\2026_Project\python-intern-task-2\day_3> python  orm_queries.md
Hello ORM Qeuries
PS C:\Users\DELL\Desktop\2026_Project\python-intern-task-2\day_3> python manage.py shell
C:\Python312\python.exe: can't open file 'C:\\Users\\DELL\\Desktop\\2026_Project\\python-intern-task-2\\day_3\\manage.py': [Errno 2] No such file or directory
PS C:\Users\DELL\Desktop\2026_Project\python-intern-task-2\day_3> cd..
PS C:\Users\DELL\Desktop\2026_Project\python-intern-task-2> cd .\training_project\
PS C:\Users\DELL\Desktop\2026_Project\python-intern-task-2\training_project> python manage.py shell
Python 3.12.1 (tags/v3.12.1:2305ca5, Dec  7 2023, 22:03:25) [MSC v.1937 64 bit (AMD64)]
Type 'copyright', 'credits' or 'license' for more information
IPython 9.2.0 -- An enhanced Interactive Python. Type '?' for help.
Tip: Use `F2` or %edit with no arguments to open an empty editor with a temporary file.
Ctrl click to launch VS Code Native REPL

In [1]: from students.models import Students
---------------------------------------------------------------------------
ImportError                               Traceback (most recent call last)
Cell In[1], line 1
----> 1 from students.models import Students

ImportError: cannot import name 'Students' from 'students.models' (C:\Users\DELL\Desktop\2026_Project\python-intern-task-2\training_project\students\models.py)

In [2]: from students.models import Student

In [3]: Student.objects.all()
Out[3]: <QuerySet [<Student: Suman>, <Student: Ankit>, <Student: Abhishek>, <Student: Shubham>, <Student: Govind>, <Student: Suhani>, <Student: Sonu>, <Student: Avinash>, <Student: sourabh>, <Student: Rahul>]>

In [4]: all_student = Student.objects.all()

In [5]: print(all_student)
<QuerySet [<Student: Suman>, <Student: Ankit>, <Student: Abhishek>, <Student: Shubham>, <Student: Govind>, <Student: Suhani>, <Student: Sonu>, <Student: Avinash>, <Student: sourabh>, <Student: Rahul>]>

In [6]: # Get only active students

In [7]: Student.objects.filter(active_status=True)
Out[7]: <QuerySet [<Student: Suman>, <Student: Ankit>, <Student: Govind>, <Student: Suhani>, <Student: Rahul>]>

In [8]: # Get students whose marks are greater than or equal to 60.

In [9]: Student.objects.filter(marks>=60)
---------------------------------------------------------------------------
NameError                                 Traceback (most recent call last)
Cell In[9], line 1
----> 1 Student.objects.filter(marks>=60)

NameError: name 'marks' is not defined

In [10]: Student.objects.filter(marks__gte=60)
Out[10]: <QuerySet [<Student: Suman>, <Student: Ankit>, <Student: Shubham>, <Student: Govind>, <Student: Suhani>, <Student: Avinash>, <Student: sourabh>, <Student: Rahul>]>

In [13]: # Order students by marks.
    ...: 

In [14]: Student.objects.order_by("marks")
Out[14]: <QuerySet [<Student: Abhishek>, <Student: Sonu>, <Student: Govind>, <Student: Suhani>, <Student: Rahul>, <Student: Shubham>, <Student: Ankit>, <Student: Suman>, <Student: Avinash>, <Student: sourabh>]>

In [15]: # Get the top three students by marks

In [16]: Student.objects.filter(marks)[3:]
---------------------------------------------------------------------------
NameError                                 Traceback (most recent call last)
Cell In[16], line 1
----> 1 Student.objects.filter(marks)[3:]

NameError: name 'marks' is not defined

In [17]: Student.objects.filter("marks")[3:]
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
Cell In[17], line 1
----> 1 Student.objects.filter("marks")[3:]

File C:\Python312\Lib\site-packages\django\db\models\manager.py:87, in BaseManager._get_queryset_methods.<locals>.create_method.<locals>.manager_method(self, *args, **kwargs)
     85 @wraps(method)
     86 def manager_method(self, *args, **kwargs):
---> 87     return getattr(self.get_queryset(), name)(*args, **kwargs)

File C:\Python312\Lib\site-packages\django\db\models\query.py:1476, in QuerySet.filter(self, *args, **kwargs)
   1471 """
   1472 Return a new QuerySet instance with the args ANDed to the existing
   1473 set.
   1474 """
   1475 self._not_support_combined_queries("filter")
-> 1476 return self._filter_or_exclude(False, args, kwargs)

File C:\Python312\Lib\site-packages\django\db\models\query.py:1494, in QuerySet._filter_or_exclude(self, negate, args, kwargs)
   1492     clone._deferred_filter = negate, args, kwargs
   1493 else:
-> 1494     clone._filter_or_exclude_inplace(negate, args, kwargs)
   1495 return clone

File C:\Python312\Lib\site-packages\django\db\models\query.py:1501, in QuerySet._filter_or_exclude_inplace(self, negate, args, kwargs)
   1499     self._query.add_q(~Q(*args, **kwargs))
   1500 else:
-> 1501     self._query.add_q(Q(*args, **kwargs))

File C:\Python312\Lib\site-packages\django\db\models\sql\query.py:1613, in Query.add_q(self, q_object)
   1604 # For join promotion this case is doing an AND for the added q_object
   1605 # and existing conditions. So, any existing inner join forces the join
   1606 # type to remain inner. Existing outer joins can however be demoted.
   1607 # (Consider case where rel_a is LOUTER and rel_a__col=1 is added - if
   1608 # rel_a doesn't produce any rows, then the whole condition must fail.
   1609 # So, demotion is OK.
   1610 existing_inner = {
   1611     a for a in self.alias_map if self.alias_map[a].join_type == INNER
   1612 }
-> 1613 clause, _ = self._add_q(q_object, self.used_aliases)
   1614 if clause:
   1615     self.where.add(clause, AND)

File C:\Python312\Lib\site-packages\django\db\models\sql\query.py:1645, in Query._add_q(self, q_object, used_aliases, branch_negated, current_negated, allow_joins, split_subq, check_filterable, summarize, update_join_types)
   1641 joinpromoter = JoinPromoter(
   1642     q_object.connector, len(q_object.children), current_negated
   1643 )
   1644 for child in q_object.children:
-> 1645     child_clause, needed_inner = self.build_filter(
   1646         child,
   1647         can_reuse=used_aliases,
   1648         branch_negated=branch_negated,
   1649         current_negated=current_negated,
   1650         allow_joins=allow_joins,
   1651         split_subq=split_subq,
   1652         check_filterable=check_filterable,
   1653         summarize=summarize,
   1654         update_join_types=update_join_types,
   1655     )
   1656     joinpromoter.add_votes(needed_inner)
   1657     if child_clause:

File C:\Python312\Lib\site-packages\django\db\models\sql\query.py:1492, in Query.build_filter(self, filter_expr, branch_negated, current_negated, can_reuse, allow_joins, split_subq, check_filterable, summarize, update_join_types)
   1490         condition = self.build_lookup(["exact"], condition, True)
   1491     return WhereNode([condition], connector=AND), []
-> 1492 arg, value = filter_expr
   1493 if not arg:
   1494     raise FieldError("Cannot parse keyword query %r" % arg)

ValueError: too many values to unpack (expected 2)

In [18]: Student.objects.filter("marks")[:3]
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
Cell In[18], line 1
----> 1 Student.objects.filter("marks")[:3]

File C:\Python312\Lib\site-packages\django\db\models\manager.py:87, in BaseManager._get_queryset_methods.<locals>.create_method.<locals>.manager_method(self, *args, **kwargs)
     85 @wraps(method)
     86 def manager_method(self, *args, **kwargs):
---> 87     return getattr(self.get_queryset(), name)(*args, **kwargs)

File C:\Python312\Lib\site-packages\django\db\models\query.py:1476, in QuerySet.filter(self, *args, **kwargs)
   1471 """
   1472 Return a new QuerySet instance with the args ANDed to the existing
   1473 set.
   1474 """
   1475 self._not_support_combined_queries("filter")
-> 1476 return self._filter_or_exclude(False, args, kwargs)

File C:\Python312\Lib\site-packages\django\db\models\query.py:1494, in QuerySet._filter_or_exclude(self, negate, args, kwargs)
   1492     clone._deferred_filter = negate, args, kwargs
   1493 else:
-> 1494     clone._filter_or_exclude_inplace(negate, args, kwargs)
   1495 return clone

File C:\Python312\Lib\site-packages\django\db\models\query.py:1501, in QuerySet._filter_or_exclude_inplace(self, negate, args, kwargs)
   1499     self._query.add_q(~Q(*args, **kwargs))
   1500 else:
-> 1501     self._query.add_q(Q(*args, **kwargs))

File C:\Python312\Lib\site-packages\django\db\models\sql\query.py:1613, in Query.add_q(self, q_object)
   1604 # For join promotion this case is doing an AND for the added q_object
   1605 # and existing conditions. So, any existing inner join forces the join
   1606 # type to remain inner. Existing outer joins can however be demoted.
   1607 # (Consider case where rel_a is LOUTER and rel_a__col=1 is added - if
   1608 # rel_a doesn't produce any rows, then the whole condition must fail.
   1609 # So, demotion is OK.
   1610 existing_inner = {
   1611     a for a in self.alias_map if self.alias_map[a].join_type == INNER
   1612 }
-> 1613 clause, _ = self._add_q(q_object, self.used_aliases)
   1614 if clause:
   1615     self.where.add(clause, AND)

File C:\Python312\Lib\site-packages\django\db\models\sql\query.py:1645, in Query._add_q(self, q_object, used_aliases, branch_negated, current_negated, allow_joins, split_subq, check_filterable, summarize, update_join_types)
   1641 joinpromoter = JoinPromoter(
   1642     q_object.connector, len(q_object.children), current_negated
   1643 )
   1644 for child in q_object.children:
-> 1645     child_clause, needed_inner = self.build_filter(
   1646         child,
   1647         can_reuse=used_aliases,
   1648         branch_negated=branch_negated,
   1649         current_negated=current_negated,
   1650         allow_joins=allow_joins,
   1651         split_subq=split_subq,
   1652         check_filterable=check_filterable,
   1653         summarize=summarize,
   1654         update_join_types=update_join_types,
   1655     )
   1656     joinpromoter.add_votes(needed_inner)
   1657     if child_clause:

File C:\Python312\Lib\site-packages\django\db\models\sql\query.py:1492, in Query.build_filter(self, filter_expr, branch_negated, current_negated, can_reuse, allow_joins, split_subq, check_filterable, summarize, update_join_types)
   1490         condition = self.build_lookup(["exact"], condition, True)
   1491     return WhereNode([condition], connector=AND), []
-> 1492 arg, value = filter_expr
   1493 if not arg:
   1494     raise FieldError("Cannot parse keyword query %r" % arg)

ValueError: too many values to unpack (expected 2)

In [19]: Student.objects.filter("-marks")[:3]
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
Cell In[19], line 1
----> 1 Student.objects.filter("-marks")[:3]

File C:\Python312\Lib\site-packages\django\db\models\manager.py:87, in BaseManager._get_queryset_methods.<locals>.create_method.<locals>.manager_method(self, *args, **kwargs)
     85 @wraps(method)
     86 def manager_method(self, *args, **kwargs):
---> 87     return getattr(self.get_queryset(), name)(*args, **kwargs)

File C:\Python312\Lib\site-packages\django\db\models\query.py:1476, in QuerySet.filter(self, *args, **kwargs)
   1471 """
   1472 Return a new QuerySet instance with the args ANDed to the existing
   1473 set.
   1474 """
   1475 self._not_support_combined_queries("filter")
-> 1476 return self._filter_or_exclude(False, args, kwargs)

File C:\Python312\Lib\site-packages\django\db\models\query.py:1494, in QuerySet._filter_or_exclude(self, negate, args, kwargs)
   1492     clone._deferred_filter = negate, args, kwargs
   1493 else:
-> 1494     clone._filter_or_exclude_inplace(negate, args, kwargs)
   1495 return clone

File C:\Python312\Lib\site-packages\django\db\models\query.py:1501, in QuerySet._filter_or_exclude_inplace(self, negate, args, kwargs)
   1499     self._query.add_q(~Q(*args, **kwargs))
   1500 else:
-> 1501     self._query.add_q(Q(*args, **kwargs))

File C:\Python312\Lib\site-packages\django\db\models\sql\query.py:1613, in Query.add_q(self, q_object)
   1604 # For join promotion this case is doing an AND for the added q_object
   1605 # and existing conditions. So, any existing inner join forces the join
   1606 # type to remain inner. Existing outer joins can however be demoted.
   1607 # (Consider case where rel_a is LOUTER and rel_a__col=1 is added - if
   1608 # rel_a doesn't produce any rows, then the whole condition must fail.
   1609 # So, demotion is OK.
   1610 existing_inner = {
   1611     a for a in self.alias_map if self.alias_map[a].join_type == INNER
   1612 }
-> 1613 clause, _ = self._add_q(q_object, self.used_aliases)
   1614 if clause:
   1615     self.where.add(clause, AND)

File C:\Python312\Lib\site-packages\django\db\models\sql\query.py:1645, in Query._add_q(self, q_object, used_aliases, branch_negated, current_negated, allow_joins, split_subq, check_filterable, summarize, update_join_types)
   1641 joinpromoter = JoinPromoter(
   1642     q_object.connector, len(q_object.children), current_negated
   1643 )
   1644 for child in q_object.children:
-> 1645     child_clause, needed_inner = self.build_filter(
   1646         child,
   1647         can_reuse=used_aliases,
   1648         branch_negated=branch_negated,
   1649         current_negated=current_negated,
   1650         allow_joins=allow_joins,
   1651         split_subq=split_subq,
   1652         check_filterable=check_filterable,
   1653         summarize=summarize,
   1654         update_join_types=update_join_types,
   1655     )
   1656     joinpromoter.add_votes(needed_inner)
   1657     if child_clause:

File C:\Python312\Lib\site-packages\django\db\models\sql\query.py:1492, in Query.build_filter(self, filter_expr, branch_negated, current_negated, can_reuse, allow_joins, split_subq, check_filterable, summarize, update_join_types)
   1490         condition = self.build_lookup(["exact"], condition, True)
   1491     return WhereNode([condition], connector=AND), []
-> 1492 arg, value = filter_expr
   1493 if not arg:
   1494     raise FieldError("Cannot parse keyword query %r" % arg)

ValueError: too many values to unpack (expected 2)

In [20]: Student.objects.order_by("-marks")[:3]
Out[20]: <QuerySet [<Student: Avinash>, <Student: sourabh>, <Student: Suman>]>

In [21]: # Get students from a specific department

In [22]: from students import Student,Department,Course,StudentProfile
---------------------------------------------------------------------------
ImportError                               Traceback (most recent call last)
Cell In[22], line 1
----> 1 from students import Student,Department,Course,StudentProfile

ImportError: cannot import name 'Student' from 'students' (C:\Users\DELL\Desktop\2026_Project\python-intern-task-2\training_project\students\__init__.py)

In [23]: from students import Department,Course,StudentProfile
---------------------------------------------------------------------------
ImportError                               Traceback (most recent call last)
Cell In[23], line 1
----> 1 from students import Department,Course,StudentProfile

ImportError: cannot import name 'Department' from 'students' (C:\Users\DELL\Desktop\2026_Project\python-intern-task-2\training_project\students\__init__.py)

In [24]: from students.models import Student,Department,Course,StudentProfile

In [25]: # Get students from a specific department

In [26]: department = Department.objects.get(name=it)
---------------------------------------------------------------------------
NameError                                 Traceback (most recent call last)
Cell In[26], line 1
----> 1 department = Department.objects.get(name=it)

NameError: name 'it' is not defined

In [27]: department = Department.objects.get(name="it")
---------------------------------------------------------------------------
DoesNotExist                              Traceback (most recent call last)
Cell In[27], line 1
----> 1 department = Department.objects.get(name="it")

File C:\Python312\Lib\site-packages\django\db\models\manager.py:87, in BaseManager._get_queryset_methods.<locals>.create_method.<locals>.manager_method(self, *args, **kwargs)
     85 @wraps(method)
     86 def manager_method(self, *args, **kwargs):
---> 87     return getattr(self.get_queryset(), name)(*args, **kwargs)

File C:\Python312\Lib\site-packages\django\db\models\query.py:649, in QuerySet.get(self, *args, **kwargs)
    647     return clone._result_cache[0]
    648 if not num:
--> 649     raise self.model.DoesNotExist(
    650         "%s matching query does not exist." % self.model._meta.object_name
    651     )
    652 raise self.model.MultipleObjectsReturned(
    653     "get() returned more than one %s -- it returned %s!"
    654     % (
   (...)    657     )
    658 )

DoesNotExist: Department matching query does not exist.

In [28]: department = Department.objects.get(name="cse")
---------------------------------------------------------------------------
DoesNotExist                              Traceback (most recent call last)
Cell In[28], line 1
----> 1 department = Department.objects.get(name="cse")

File C:\Python312\Lib\site-packages\django\db\models\manager.py:87, in BaseManager._get_queryset_methods.<locals>.create_method.<locals>.manager_method(self, *args, **kwargs)
     85 @wraps(method)
     86 def manager_method(self, *args, **kwargs):
---> 87     return getattr(self.get_queryset(), name)(*args, **kwargs)

File C:\Python312\Lib\site-packages\django\db\models\query.py:649, in QuerySet.get(self, *args, **kwargs)
    647     return clone._result_cache[0]
    648 if not num:
--> 649     raise self.model.DoesNotExist(
    650         "%s matching query does not exist." % self.model._meta.object_name
    651     )
    652 raise self.model.MultipleObjectsReturned(
    653     "get() returned more than one %s -- it returned %s!"
    654     % (
   (...)    657     )
    658 )

DoesNotExist: Department matching query does not exist.

In [29]: department = Department.objects.get(name="CSE")

In [30]: Student.objects.filter(department=department)
Out[30]: <QuerySet [<Student: Ankit>, <Student: Govind>, <Student: Suhani>, <Student: Rahul>]>

In [31]: #  Get students enrolled in a specific course.

In [32]: course = Student.object.get(name="Java")
---------------------------------------------------------------------------
AttributeError                            Traceback (most recent call last)
Cell In[32], line 1
----> 1 course = Student.object.get(name="Java")

AttributeError: type object 'Student' has no attribute 'object'

In [33]: course = Course.object.get(name="Java")
---------------------------------------------------------------------------
AttributeError                            Traceback (most recent call last)
Cell In[33], line 1
----> 1 course = Course.object.get(name="Java")

AttributeError: type object 'Course' has no attribute 'object'

In [34]: course = Course.objects.get(name="Java")
---------------------------------------------------------------------------
FieldError                                Traceback (most recent call last)
Cell In[34], line 1
----> 1 course = Course.objects.get(name="Java")

File C:\Python312\Lib\site-packages\django\db\models\manager.py:87, in BaseManager._get_queryset_methods.<locals>.create_method.<locals>.manager_method(self, *args, **kwargs)
     85 @wraps(method)
     86 def manager_method(self, *args, **kwargs):
---> 87     return getattr(self.get_queryset(), name)(*args, **kwargs)

File C:\Python312\Lib\site-packages\django\db\models\query.py:635, in QuerySet.get(self, *args, **kwargs)
    630 if self.query.combinator and (args or kwargs):
    631     raise NotSupportedError(
    632         "Calling QuerySet.get(...) with filters after %s() is not "
    633         "supported." % self.query.combinator
    634     )
--> 635 clone = self._chain() if self.query.combinator else self.filter(*args, **kwargs)
    636 if self.query.can_filter() and not self.query.distinct_fields:
    637     clone = clone.order_by()

File C:\Python312\Lib\site-packages\django\db\models\query.py:1476, in QuerySet.filter(self, *args, **kwargs)
   1471 """
   1472 Return a new QuerySet instance with the args ANDed to the existing
   1473 set.
   1474 """
   1475 self._not_support_combined_queries("filter")
-> 1476 return self._filter_or_exclude(False, args, kwargs)

File C:\Python312\Lib\site-packages\django\db\models\query.py:1494, in QuerySet._filter_or_exclude(self, negate, args, kwargs)
   1492     clone._deferred_filter = negate, args, kwargs
   1493 else:
-> 1494     clone._filter_or_exclude_inplace(negate, args, kwargs)
   1495 return clone

File C:\Python312\Lib\site-packages\django\db\models\query.py:1501, in QuerySet._filter_or_exclude_inplace(self, negate, args, kwargs)
   1499     self._query.add_q(~Q(*args, **kwargs))
   1500 else:
-> 1501     self._query.add_q(Q(*args, **kwargs))

File C:\Python312\Lib\site-packages\django\db\models\sql\query.py:1613, in Query.add_q(self, q_object)
   1604 # For join promotion this case is doing an AND for the added q_object
   1605 # and existing conditions. So, any existing inner join forces the join
   1606 # type to remain inner. Existing outer joins can however be demoted.
   1607 # (Consider case where rel_a is LOUTER and rel_a__col=1 is added - if
   1608 # rel_a doesn't produce any rows, then the whole condition must fail.
   1609 # So, demotion is OK.
   1610 existing_inner = {
   1611     a for a in self.alias_map if self.alias_map[a].join_type == INNER
   1612 }
-> 1613 clause, _ = self._add_q(q_object, self.used_aliases)
   1614 if clause:
   1615     self.where.add(clause, AND)

File C:\Python312\Lib\site-packages\django\db\models\sql\query.py:1645, in Query._add_q(self, q_object, used_aliases, branch_negated, current_negated, allow_joins, split_subq, check_filterable, summarize, update_join_types)
   1641 joinpromoter = JoinPromoter(
   1642     q_object.connector, len(q_object.children), current_negated
   1643 )
   1644 for child in q_object.children:
-> 1645     child_clause, needed_inner = self.build_filter(
   1646         child,
   1647         can_reuse=used_aliases,
   1648         branch_negated=branch_negated,
   1649         current_negated=current_negated,
   1650         allow_joins=allow_joins,
   1651         split_subq=split_subq,
   1652         check_filterable=check_filterable,
   1653         summarize=summarize,
   1654         update_join_types=update_join_types,
   1655     )
   1656     joinpromoter.add_votes(needed_inner)
   1657     if child_clause:

File C:\Python312\Lib\site-packages\django\db\models\sql\query.py:1495, in Query.build_filter(self, filter_expr, branch_negated, current_negated, can_reuse, allow_joins, split_subq, check_filterable, summarize, update_join_types)
   1493 if not arg:
   1494     raise FieldError("Cannot parse keyword query %r" % arg)
-> 1495 lookups, parts, reffed_expression = self.solve_lookup_type(arg, summarize)
   1497 if check_filterable:
   1498     self.check_filterable(reffed_expression)

File C:\Python312\Lib\site-packages\django\db\models\sql\query.py:1307, in Query.solve_lookup_type(self, lookup, summarize)
   1305             expression = Ref(annotation, expression)
   1306         return expression_lookups, (), expression
-> 1307 _, field, _, lookup_parts = self.names_to_path(lookup_splitted, self.get_meta())
   1308 field_parts = lookup_splitted[0 : len(lookup_splitted) - len(lookup_parts)]
   1309 if len(lookup_parts) > 1 and not field_parts:

File C:\Python312\Lib\site-packages\django\db\models\sql\query.py:1772, in Query.names_to_path(self, names, opts, allow_many, fail_on_missing)
   1764     if pos == -1 or fail_on_missing:
   1765         available = sorted(
   1766             [
   1767                 *get_field_names_from_opts(opts),
   (...)   1770             ]
   1771         )
-> 1772         raise FieldError(
   1773             "Cannot resolve keyword '%s' into field. "
   1774             "Choices are: %s" % (name, ", ".join(available))
   1775         )
   1776     break
   1777 # Check if we need any joins for concrete inheritance cases (the
   1778 # field lives in parent, but we are currently in one of its
   1779 # children)

FieldError: Cannot resolve keyword 'name' into field. Choices are: active_status, code, course_name, duration, id, students

In [35]: course = Course.objects.get(course_name="Java")
---------------------------------------------------------------------------
DoesNotExist                              Traceback (most recent call last)
Cell In[35], line 1
----> 1 course = Course.objects.get(course_name="Java")

File C:\Python312\Lib\site-packages\django\db\models\manager.py:87, in BaseManager._get_queryset_methods.<locals>.create_method.<locals>.manager_method(self, *args, **kwargs)
     85 @wraps(method)
     86 def manager_method(self, *args, **kwargs):
---> 87     return getattr(self.get_queryset(), name)(*args, **kwargs)

File C:\Python312\Lib\site-packages\django\db\models\query.py:649, in QuerySet.get(self, *args, **kwargs)
    647     return clone._result_cache[0]
    648 if not num:
--> 649     raise self.model.DoesNotExist(
    650         "%s matching query does not exist." % self.model._meta.object_name
    651     )
    652 raise self.model.MultipleObjectsReturned(
    653     "get() returned more than one %s -- it returned %s!"
    654     % (
   (...)    657     )
    658 )

DoesNotExist: Course matching query does not exist.

In [36]: course = Course.objects.get(course_name="Python")

In [37]: course.students.all()
Out[37]: <QuerySet [<Student: Suman>, <Student: Rahul>]>

In [38]: #  Get all courses for one student.

In [39]: student = Student.objects.get(name="Rahul")

In [40]: course.students.all()
Out[40]: <QuerySet [<Student: Suman>, <Student: Rahul>]>

In [41]: course.student.all()
---------------------------------------------------------------------------
AttributeError                            Traceback (most recent call last)
Cell In[41], line 1
----> 1 course.student.all()

AttributeError: 'Course' object has no attribute 'student'

In [42]: student.course.all()
Out[42]: <QuerySet [<Course: Python>, <Course: Web Development>]>

In [43]: # Count the total number of students.

In [44]: Student.objects.count()
Out[44]: 10

In [45]: # Calculate average marks.

In [46]: Student.objects.get(avg("marks"))
---------------------------------------------------------------------------
NameError                                 Traceback (most recent call last)
Cell In[46], line 1
----> 1 Student.objects.get(avg("marks"))

NameError: name 'avg' is not defined

In [47]: Student.objects.get(Avg("marks"))
---------------------------------------------------------------------------
NameError                                 Traceback (most recent call last)
Cell In[47], line 1
----> 1 Student.objects.get(Avg("marks"))

NameError: name 'Avg' is not defined

In [48]: Student.objects.aggregate(Avg("marks"))
---------------------------------------------------------------------------
NameError                                 Traceback (most recent call last)
Cell In[48], line 1
----> 1 Student.objects.aggregate(Avg("marks"))

NameError: name 'Avg' is not defined

In [49]: Student.objects.aggregate(Avg("marks"))
    ...: 
---------------------------------------------------------------------------
NameError                                 Traceback (most recent call last)
Cell In[49], line 1
----> 1 Student.objects.aggregate(Avg("marks"))

NameError: name 'Avg' is not defined

In [50]: from django.db.models import Avg

In [51]: Student.objects.aggregate(Avg("marks"))
Out[51]: {'marks__avg': 71.0}

In [52]: # Find the highest and lowest marks.
    ...: from django.db.models import Max, Min

In [53]: Student.objects.Student.objects.get
    ...: (highest=Max("marks"),lowest=Min("marks")
    ...: )
  Cell In[53], line 2
    (highest=Max("marks"),lowest=Min("marks")
     ^
SyntaxError: invalid syntax. Maybe you meant '==' or ':=' instead of '='?


In [54]: Student.objects.Student.objects.aggreagate(highest=Max("marks"),lowest=Min("marks"))
---------------------------------------------------------------------------
AttributeError                            Traceback (most recent call last)
Cell In[54], line 1
----> 1 Student.objects.Student.objects.aggreagate(highest=Max("marks"),lowest=Min("marks"))

AttributeError: 'Manager' object has no attribute 'Student'

In [55]: Student.objects.aggreagate(highest=Max("marks"),lowest=Min("marks"))
---------------------------------------------------------------------------
AttributeError                            Traceback (most recent call last)
Cell In[55], line 1
----> 1 Student.objects.aggreagate(highest=Max("marks"),lowest=Min("marks"))

AttributeError: 'Manager' object has no attribute 'aggreagate'

In [56]: Student.objects.aggregate(highest=Max("marks"),lowest=Min("marks"))
Out[56]: {'highest': 88.0, 'lowest': 38.0}

In [57]: # 13. Count students in each department.

In [58]: department = Department.objects.all()

In [59]: department.student.count()
---------------------------------------------------------------------------
AttributeError                            Traceback (most recent call last)
Cell In[59], line 1
----> 1 department.student.count()

AttributeError: 'QuerySet' object has no attribute 'student'

In [60]: department.students.count()
---------------------------------------------------------------------------
AttributeError                            Traceback (most recent call last)
Cell In[60], line 1
----> 1 department.students.count()

AttributeError: 'QuerySet' object has no attribute 'students'

In [61]: student = Student.department.count()
---------------------------------------------------------------------------
AttributeError                            Traceback (most recent call last)
Cell In[61], line 1
----> 1 student = Student.department.count()

AttributeError: 'ForwardManyToOneDescriptor' object has no attribute 'count'

In [62]: Department.objects.annotate(
    ...:     total_students=Count("students")
    ...: )
---------------------------------------------------------------------------
NameError                                 Traceback (most recent call last)
Cell In[62], line 2
      1 Department.objects.annotate(
----> 2     total_students=Count("students")
      3 )

NameError: name 'Count' is not defined

In [63]: # Find the highest and lowest marks.
    ...: from django.db.models import Count

In [64]: Department.objects.annotate(
    ...:     total_students=Count("students")
    ...: )
Out[64]: <QuerySet [<Department: CSE>, <Department: ECE>, <Department: Civil>]>

In [65]: Department.objects.annotate(total_students=Count("student"))
---------------------------------------------------------------------------
FieldError                                Traceback (most recent call last)
Cell In[65], line 1
----> 1 Department.objects.annotate(total_students=Count("student"))

File C:\Python312\Lib\site-packages\django\db\models\manager.py:87, in BaseManager._get_queryset_methods.<locals>.create_method.<locals>.manager_method(self, *args, **kwargs)
     85 @wraps(method)
     86 def manager_method(self, *args, **kwargs):
---> 87     return getattr(self.get_queryset(), name)(*args, **kwargs)

File C:\Python312\Lib\site-packages\django\db\models\query.py:1630, in QuerySet.annotate(self, *args, **kwargs)
   1625 """
   1626 Return a query set in which the returned objects have been annotated
   1627 with extra data or aggregations.
   1628 """
   1629 self._not_support_combined_queries("annotate")
-> 1630 return self._annotate(args, kwargs, select=True)

File C:\Python312\Lib\site-packages\django\db\models\query.py:1680, in QuerySet._annotate(self, args, kwargs, select)
   1678         clone.query.add_filtered_relation(annotation, alias)
   1679     else:
-> 1680         clone.query.add_annotation(
   1681             annotation,
   1682             alias,
   1683             select=select,
   1684         )
   1685 for alias, annotation in clone.query.annotations.items():
   1686     if alias in annotations and annotation.contains_aggregate:

File C:\Python312\Lib\site-packages\django\db\models\sql\query.py:1198, in Query.add_annotation(self, annotation, alias, select)
   1196 """Add a single annotation expression to the Query."""
   1197 self.check_alias(alias)
-> 1198 annotation = annotation.resolve_expression(self, allow_joins=True, reuse=None)
   1199 if select:
   1200     self.append_annotation_mask([alias])

File C:\Python312\Lib\site-packages\django\db\models\aggregates.py:65, in Aggregate.resolve_expression(self, query, allow_joins, reuse, summarize, for_save)
     61 def resolve_expression(
     62     self, query=None, allow_joins=True, reuse=None, summarize=False, for_save=False
     63 ):
     64     # Aggregates are not allowed in UPDATE queries, so ignore for_save
---> 65     c = super().resolve_expression(query, allow_joins, reuse, summarize)
     66     c.filter = c.filter and c.filter.resolve_expression(
     67         query, allow_joins, reuse, summarize
     68     )
     69     if summarize:
     70         # Summarized aggregates cannot refer to summarized aggregates.

File C:\Python312\Lib\site-packages\django\db\models\expressions.py:975, in Func.resolve_expression(self, query, allow_joins, reuse, summarize, for_save)
    973 c.is_summary = summarize
    974 for pos, arg in enumerate(c.source_expressions):
--> 975     c.source_expressions[pos] = arg.resolve_expression(
    976         query, allow_joins, reuse, summarize, for_save
    977     )
    978 return c

File C:\Python312\Lib\site-packages\django\db\models\expressions.py:854, in F.resolve_expression(self, query, allow_joins, reuse, summarize, for_save)
    851 def resolve_expression(
    852     self, query=None, allow_joins=True, reuse=None, summarize=False, for_save=False
    853 ):
--> 854     return query.resolve_ref(self.name, allow_joins, reuse, summarize)

File C:\Python312\Lib\site-packages\django\db\models\sql\query.py:2014, in Query.resolve_ref(self, name, allow_joins, reuse, summarize)
   2012         annotation = self.try_transform(annotation, transform)
   2013     return annotation
-> 2014 join_info = self.setup_joins(
   2015     field_list, self.get_meta(), self.get_initial_alias(), can_reuse=reuse
   2016 )
   2017 targets, final_alias, join_list = self.trim_joins(
   2018     join_info.targets, join_info.joins, join_info.path
   2019 )
   2020 if not allow_joins and len(join_list) > 1:

File C:\Python312\Lib\site-packages\django\db\models\sql\query.py:1867, in Query.setup_joins(self, names, opts, alias, can_reuse, allow_many)
   1865 for pivot in range(len(names), 0, -1):
   1866     try:
-> 1867         path, final_field, targets, rest = self.names_to_path(
   1868             names[:pivot],
   1869             opts,
   1870             allow_many,
   1871             fail_on_missing=True,
   1872         )
   1873     except FieldError as exc:
   1874         if pivot == 1:
   1875             # The first item cannot be a lookup, so it's safe
   1876             # to raise the field error here.

File C:\Python312\Lib\site-packages\django\db\models\sql\query.py:1772, in Query.names_to_path(self, names, opts, allow_many, fail_on_missing)
   1764     if pos == -1 or fail_on_missing:
   1765         available = sorted(
   1766             [
   1767                 *get_field_names_from_opts(opts),
   (...)   1770             ]
   1771         )
-> 1772         raise FieldError(
   1773             "Cannot resolve keyword '%s' into field. "
   1774             "Choices are: %s" % (name, ", ".join(available))
   1775         )
   1776     break
   1777 # Check if we need any joins for concrete inheritance cases (the
   1778 # field lives in parent, but we are currently in one of its
   1779 # children)

FieldError: Cannot resolve keyword 'student' into field. Choices are: description, id, name, students

In [66]: # 14. Find departments with more than three students.

In [67]: department = Department.objects.annotate(total_students=Count("students"))

In [68]: department.filter(total_students__gt=3)
Out[68]: <QuerySet [<Department: CSE>]>

In [69]: # 15. Find students who do not have a profile

In [70]: Student.objects.filter(student_profile__isnull=True)
Out[70]: <QuerySet [<Student: Shubham>, <Student: Sonu>, <Student: Avinash>, <Student: sourabh>, <Student: Rahul>]>

In [71]: # 16. Find students enrolled in more than one course.

In [72]: student = Student.objects.annotate(total_courses=Count("courses"))
---------------------------------------------------------------------------
FieldError                                Traceback (most recent call last)
Cell In[72], line 1
----> 1 student = Student.objects.annotate(total_courses=Count("courses"))

File C:\Python312\Lib\site-packages\django\db\models\manager.py:87, in BaseManager._get_queryset_methods.<locals>.create_method.<locals>.manager_method(self, *args, **kwargs)
     85 @wraps(method)
     86 def manager_method(self, *args, **kwargs):
---> 87     return getattr(self.get_queryset(), name)(*args, **kwargs)

File C:\Python312\Lib\site-packages\django\db\models\query.py:1630, in QuerySet.annotate(self, *args, **kwargs)
   1625 """
   1626 Return a query set in which the returned objects have been annotated
   1627 with extra data or aggregations.
   1628 """
   1629 self._not_support_combined_queries("annotate")
-> 1630 return self._annotate(args, kwargs, select=True)

File C:\Python312\Lib\site-packages\django\db\models\query.py:1680, in QuerySet._annotate(self, args, kwargs, select)
   1678         clone.query.add_filtered_relation(annotation, alias)
   1679     else:
-> 1680         clone.query.add_annotation(
   1681             annotation,
   1682             alias,
   1683             select=select,
   1684         )
   1685 for alias, annotation in clone.query.annotations.items():
   1686     if alias in annotations and annotation.contains_aggregate:

File C:\Python312\Lib\site-packages\django\db\models\sql\query.py:1198, in Query.add_annotation(self, annotation, alias, select)
   1196 """Add a single annotation expression to the Query."""
   1197 self.check_alias(alias)
-> 1198 annotation = annotation.resolve_expression(self, allow_joins=True, reuse=None)
   1199 if select:
   1200     self.append_annotation_mask([alias])

File C:\Python312\Lib\site-packages\django\db\models\aggregates.py:65, in Aggregate.resolve_expression(self, query, allow_joins, reuse, summarize, for_save)
     61 def resolve_expression(
     62     self, query=None, allow_joins=True, reuse=None, summarize=False, for_save=False
     63 ):
     64     # Aggregates are not allowed in UPDATE queries, so ignore for_save
---> 65     c = super().resolve_expression(query, allow_joins, reuse, summarize)
     66     c.filter = c.filter and c.filter.resolve_expression(
     67         query, allow_joins, reuse, summarize
     68     )
     69     if summarize:
     70         # Summarized aggregates cannot refer to summarized aggregates.

File C:\Python312\Lib\site-packages\django\db\models\expressions.py:975, in Func.resolve_expression(self, query, allow_joins, reuse, summarize, for_save)
    973 c.is_summary = summarize
    974 for pos, arg in enumerate(c.source_expressions):
--> 975     c.source_expressions[pos] = arg.resolve_expression(
    976         query, allow_joins, reuse, summarize, for_save
    977     )
    978 return c

File C:\Python312\Lib\site-packages\django\db\models\expressions.py:854, in F.resolve_expression(self, query, allow_joins, reuse, summarize, for_save)
    851 def resolve_expression(
    852     self, query=None, allow_joins=True, reuse=None, summarize=False, for_save=False
    853 ):
--> 854     return query.resolve_ref(self.name, allow_joins, reuse, summarize)

File C:\Python312\Lib\site-packages\django\db\models\sql\query.py:2014, in Query.resolve_ref(self, name, allow_joins, reuse, summarize)
   2012         annotation = self.try_transform(annotation, transform)
   2013     return annotation
-> 2014 join_info = self.setup_joins(
   2015     field_list, self.get_meta(), self.get_initial_alias(), can_reuse=reuse
   2016 )
   2017 targets, final_alias, join_list = self.trim_joins(
   2018     join_info.targets, join_info.joins, join_info.path
   2019 )
   2020 if not allow_joins and len(join_list) > 1:

File C:\Python312\Lib\site-packages\django\db\models\sql\query.py:1867, in Query.setup_joins(self, names, opts, alias, can_reuse, allow_many)
   1865 for pivot in range(len(names), 0, -1):
   1866     try:
-> 1867         path, final_field, targets, rest = self.names_to_path(
   1868             names[:pivot],
   1869             opts,
   1870             allow_many,
   1871             fail_on_missing=True,
   1872         )
   1873     except FieldError as exc:
   1874         if pivot == 1:
   1875             # The first item cannot be a lookup, so it's safe
   1876             # to raise the field error here.

File C:\Python312\Lib\site-packages\django\db\models\sql\query.py:1772, in Query.names_to_path(self, names, opts, allow_many, fail_on_missing)
   1764     if pos == -1 or fail_on_missing:
   1765         available = sorted(
   1766             [
   1767                 *get_field_names_from_opts(opts),
   (...)   1770             ]
   1771         )
-> 1772         raise FieldError(
   1773             "Cannot resolve keyword '%s' into field. "
   1774             "Choices are: %s" % (name, ", ".join(available))
   1775         )
   1776     break
   1777 # Check if we need any joins for concrete inheritance cases (the
   1778 # field lives in parent, but we are currently in one of its
   1779 # children)

FieldError: Cannot resolve keyword 'courses' into field. Choices are: active_status, age, course, department, department_id, email, id, joined_date, marks, name, student_profile

In [73]: student = Student.objects.annotate(total_courses=Count("course"))

In [74]: student.filter(total_courses__gt=1)
Out[74]: <QuerySet [<Student: Ankit>, <Student: Govind>, <Student: Suhani>, <Student: Rahul>, <Student: Suman>, <Student: Abhishek>]>

In [75]: # 17. Search students by name or email using Q objects.

In [76]: from django.db.models import Q

In [77]: student = Student.objects.filter(Q(name__icontains="rah") |Q(email__icontains="rah"))

In [78]: student
Out[78]: <QuerySet [<Student: Rahul>]>

In [79]: # 18. Update inactive students to active using update().

In [80]: student = Student.objects.filter(active_status=False)

In [81]: student.update(active_status=True)
Out[81]: 5

In [82]: # 19. Delete records with invalid marks, if any.

In [83]: student = Student.objects.filter(Q(marks__lt=0))

In [84]: student
Out[84]: <QuerySet []>

In [85]: student.delete()
Out[85]: (0, {})

In [86]: # 20. Use select_related() and prefetch_related() appropriately.

In [87]: Student.objects.select_related("department")
    ...: 
    ...: 
Out[87]: <QuerySet [<Student: Suman>, <Student: Ankit>, <Student: Abhishek>, <Student: Shubham>, <Student: Govind>, <Student: Suhani>, <Student: Sonu>, <Student: Avinash>, <Student: sourabh>, <Student: Rahul>]>

In [88]: Student.objects.prefetch_related("courses")
Out[88]: ---------------------------------------------------------------------------
AttributeError                            Traceback (most recent call last)
File C:\Python312\Lib\site-packages\IPython\core\formatters.py:770, in PlainTextFormatter.__call__(self, obj)
    763 stream = StringIO()
    764 printer = pretty.RepresentationPrinter(stream, self.verbose,
    765     self.max_width, self.newline,
    766     max_seq_length=self.max_seq_length,
    767     singleton_pprinters=self.singleton_printers,
    768     type_pprinters=self.type_printers,
    769     deferred_pprinters=self.deferred_printers)
--> 770 printer.pretty(obj)
    771 printer.flush()
    772 return stream.getvalue()

File C:\Python312\Lib\site-packages\IPython\lib\pretty.py:411, in RepresentationPrinter.pretty(self, obj)
    400                         return meth(obj, self, cycle)
    401                 if (
    402                     cls is not object
    403                     # check if cls defines __repr__
   (...)    409                     and callable(_safe_getattr(cls, "__repr__", None))
    410                 ):
--> 411                     return _repr_pprint(obj, self, cycle)
    413     return _default_pprint(obj, self, cycle)
    414 finally:

File C:\Python312\Lib\site-packages\IPython\lib\pretty.py:786, in _repr_pprint(obj, p, cycle)
    784 """A pprint that just redirects to the normal repr function."""
    785 # Find newlines and replace them with p.break_()
--> 786 output = repr(obj)
    787 lines = output.splitlines()
    788 with p.group():

File C:\Python312\Lib\site-packages\django\db\models\query.py:376, in QuerySet.__repr__(self)
    375 def __repr__(self):
--> 376     data = list(self[: REPR_OUTPUT_SIZE + 1])
    377     if len(data) > REPR_OUTPUT_SIZE:
    378         data[-1] = "...(remaining elements truncated)..."

File C:\Python312\Lib\site-packages\django\db\models\query.py:400, in QuerySet.__iter__(self)
    385 def __iter__(self):
    386     """
    387     The queryset iterator protocol uses three nested iterators in the
    388     default case:
   (...)    398            - Responsible for turning the rows into model objects.
    399     """
--> 400     self._fetch_all()
    401     return iter(self._result_cache)

File C:\Python312\Lib\site-packages\django\db\models\query.py:1930, in QuerySet._fetch_all(self)
   1928     self._result_cache = list(self._iterable_class(self))
   1929 if self._prefetch_related_lookups and not self._prefetch_done:
-> 1930     self._prefetch_related_objects()

File C:\Python312\Lib\site-packages\django\db\models\query.py:1320, in QuerySet._prefetch_related_objects(self)
   1318 def _prefetch_related_objects(self):
   1319     # This method can only be called once the result cache has been filled.
-> 1320     prefetch_related_objects(self._result_cache, *self._prefetch_related_lookups)
   1321     self._prefetch_done = True

File C:\Python312\Lib\site-packages\django\db\models\query.py:2356, in prefetch_related_objects(model_instances, *related_lookups)
   2351 prefetcher, descriptor, attr_found, is_fetched = get_prefetcher(
   2352     first_obj, through_attr, to_attr
   2353 )
   2355 if not attr_found:
-> 2356     raise AttributeError(
   2357         "Cannot find '%s' on %s object, '%s' is an invalid "
   2358         "parameter to prefetch_related()"
   2359         % (
   2360             through_attr,
   2361             first_obj.__class__.__name__,
   2362             lookup.prefetch_through,
   2363         )
   2364     )
   2366 if level == len(through_attrs) - 1 and prefetcher is None:
   2367     # Last one, this *must* resolve to something that supports
   2368     # prefetching, otherwise there is no point adding it and the
   2369     # developer asking for it has made a mistake.
   2370     raise ValueError(
   2371         "'%s' does not resolve to an item that supports "
   2372         "prefetching - this is an invalid parameter to "
   2373         "prefetch_related()." % lookup.prefetch_through
   2374     )

AttributeError: Cannot find 'courses' on Student object, 'courses' is an invalid parameter to prefetch_related()

In [89]: Student.objects.prefetch_related("course")
Out[89]: <QuerySet [<Student: Suman>, <Student: Ankit>, <Student: Abhishek>, <Student: Shubham>, <Student: Govind>, <Student: Suhani>, <Student: Sonu>, <Student: Avinash>, <Student: sourabh>, <Student: Rahul>]>

In [90]: 