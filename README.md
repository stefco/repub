# (Re)port (Pub)lisher

Serialization types for structured inputs.

## Overview

`repub` allows you to create classes that can accept structured data and output
simple reports in various formats:

- LaTeX files
  - PDF files generated therefrom
- HTML pages
  - Jupyter notebook previews
  - Stand-alone HTML pages with embedded multimedia
  - HTML directories with media in separate files
- Text files
- Rich Slack messages

Simple structure can be encoded into type definitions, allowing for simple but
pleasantly formatted reports to be automatically generated in multiple output
formats.

## Examples

### `TabularModelCollection`

Serialize a bunch of objects of a given type by associating their properties
with column names and data transforms; this report class uses the excellent
`tabulate` library for rendering, and additional options can be passed as the
final argument to the subclass function (called on `TabularModelList` using
dictionary notation).

In this example, render a set of objects representing administrators for a
website. Let's first make our dummy data, which will be stored as a list of
objects with shared properties (in this case, all are instances of an `Admin`
class):

```python
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Admin:
    name: str
    joined: datetime
    active: bool
    posts: int

   @property
   def posts_per_day(self):
       return self.posts / (datetime.now() - self.joined).days

admins = [
    Admin('Stef', datetime(2019, 11, 20, 9, 12, 33), True, 3823),
    Admin('Flip', datetime(2019, 8, 11, 13, 9, 20), True, 1029),
    Admin('Alex', datetime(2020, 6, 9, 15, 55, 3), True, 4053),
    Admin('Mel', datetime(2019, 8, 11, 12, 59, 28), True, 23934),
    Admin('Brad', datetime(2019, 8, 11, 12, 49, 45), False, 0),
    Admin('Meg', datetime(2019, 8, 11, 12, 49, 45), False, 293),
]
```

We can now define our reporter, which takes a list of column names followed by
their data source properties, an optional transform to apply to each column,
and additional arguments to pass to `tabulate`:

```python
>>> reporter = TabularModelList[
...     ['Name', 'Started', 'Active', 'Days', 'Post/Day']
...     ['name', 'joined', 'active', 'joined', 'posts_per_day'],
...     [None, None, None, lambda x: (datetime.now()-x).days, None],
...     {'showindex': True, 'floatfmt': '.2f'}
... ]
>>> print(reporter(admins))
        | Name   | Started             | Active   |   Days |   Post/Day
    ----+--------+---------------------+----------+--------+------------
      0 | Stef   | 2019-11-20 09:12:33 | True     |    368 |      10.39
      1 | Flip   | 2019-08-11 13:09:20 | True     |    469 |       2.19
      2 | Alex   | 2020-06-09 15:55:03 | True     |    165 |      24.56
      3 | Mel    | 2019-08-11 12:59:28 | True     |    469 |      51.03
      4 | Brad   | 2019-08-11 12:49:45 | False    |    469 |       0.00
      5 | Meg    | 2019-08-11 12:49:45 | False    |    469 |       0.62
```

Since `print` casts the reporter to `str` by default, this produces a simple
text table using the `__str__` method. We can render to HTML instead by calling
`_repr_html_` (the standard used by IPython):

```python
>>> print(reporter(admins)._repr_html_())
    <table>
    <thead>
    <tr><th style="text-align: right;">  </th><th>Name  </th><th>Started            </th><th>Active  </th><th style="text-align: right;">  Days</th><th style="text-align: right;">  Post/Day</th></tr>
    </thead>
    <tbody>
    <tr><td style="text-align: right;"> 0</td><td>Stef  </td><td>2019-11-20 09:12:33</td><td>True    </td><td style="text-align: right;">   368</td><td style="text-align: right;">     10.39</td></tr>
    <tr><td style="text-align: right;"> 1</td><td>Flip  </td><td>2019-08-11 13:09:20</td><td>True    </td><td style="text-align: right;">   469</td><td style="text-align: right;">      2.19</td></tr>
    <tr><td style="text-align: right;"> 2</td><td>Alex  </td><td>2020-06-09 15:55:03</td><td>True    </td><td style="text-align: right;">   165</td><td style="text-align: right;">     24.56</td></tr>
    <tr><td style="text-align: right;"> 3</td><td>Mel   </td><td>2019-08-11 12:59:28</td><td>True    </td><td style="text-align: right;">   469</td><td style="text-align: right;">     51.03</td></tr>
    <tr><td style="text-align: right;"> 4</td><td>Brad  </td><td>2019-08-11 12:49:45</td><td>False   </td><td style="text-align: right;">   469</td><td style="text-align: right;">      0.00</td></tr>
    <tr><td style="text-align: right;"> 5</td><td>Meg   </td><td>2019-08-11 12:49:45</td><td>False   </td><td style="text-align: right;">   469</td><td style="text-align: right;">      0.62</td></tr>
    </tbody>
    </table>
```

Which renders like:


<table>
<thead>
<tr><th style="text-align: right;">  </th><th>Name  </th><th>Started            </th><th>Active  </th><th style="text-align: right;">  Days</th><th style="text-align: right;">  Post/Day</th></tr>
</thead>
<tbody>
<tr><td style="text-align: right;"> 0</td><td>Stef  </td><td>2019-11-20 09:12:33</td><td>True    </td><td style="text-align: right;">   368</td><td style="text-align: right;">     10.39</td></tr>
<tr><td style="text-align: right;"> 1</td><td>Flip  </td><td>2019-08-11 13:09:20</td><td>True    </td><td style="text-align: right;">   469</td><td style="text-align: right;">      2.19</td></tr>
<tr><td style="text-align: right;"> 2</td><td>Alex  </td><td>2020-06-09 15:55:03</td><td>True    </td><td style="text-align: right;">   165</td><td style="text-align: right;">     24.56</td></tr>
<tr><td style="text-align: right;"> 3</td><td>Mel   </td><td>2019-08-11 12:59:28</td><td>True    </td><td style="text-align: right;">   469</td><td style="text-align: right;">     51.03</td></tr>
<tr><td style="text-align: right;"> 4</td><td>Brad  </td><td>2019-08-11 12:49:45</td><td>False   </td><td style="text-align: right;">   469</td><td style="text-align: right;">      0.00</td></tr>
<tr><td style="text-align: right;"> 5</td><td>Meg   </td><td>2019-08-11 12:49:45</td><td>False   </td><td style="text-align: right;">   469</td><td style="text-align: right;">      0.62</td></tr>
</tbody>
</table>
