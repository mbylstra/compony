# compony

##### Python view component framework (V of MVC)

Pure Python. *No templates*.

![Compony Logo](https://raw.githubusercontent.com/mbylstra/compony/master/compony-logo.png)

## Installation
```
pip install compony
```

## Examples

With Twitter Boostrap, you can create a list group inside a panel with a heading using this markup:
(see http://getbootstrap.com/components/#panels-list-group)
```html
<div class="panel panel-default">
    <div class="panel-heading">Panel heading</div>
    <ul class="list-group">
        <li class="list-group-item">Cras justo odio</li>
        <li class="list-group-item">Dapibus ac facilisis in</li>
        <li class="list-group-item">Morbi leo risus</li>
        <li class="list-group-item">Porta ac consectetur ac</li>
        <li class="list-group-item">Vestibulum at eros</li>
    </ul>
</div>
```

This can be made into a Compony component using the following code:
```python
from compony import Component
from compony.elements import div, ul, li

class ListGroup(Component):
    def render(self):
        return (
            div({'class': 'panel panel-default'},
                div({'class': 'panel-heading'}, self.attrs['title'])
                ul({'class': 'list-group'},
                    [li({'class': 'list-group-item'}, child)
                     for child in self.children]
                )
            )
        )
```

Say you were constructing a DashboardPage component, you could use ListGroup like this:
```python
class DashboardPage(Component):

    def render(self):
        return (
            html(
                body(
                    ListGroup({'title': 'A list of things'}, #title will be put in the header
                        'Item One', # just text
                        ('Item Two', Badge(42)), # text with a badge: Item Two <span class="badge">42</span>
                        'Item Three',
                        link('/home', 'Item Four'),   #a link: <a href="/home">Item Four</a>
                    )
                    ListGroup({'title': 'Another ListGroup'},
                        'Item One',
                        'Item Two',
                    ),
                    ListGroup({'title': 'Yet Another ListGroup'},
                        'I think you get the picture now',
                    )
                )
            )
        )

```
Note that each list item can contain any html. Each item in the ListGroup component becomes a child that ListGroup wraps in more markup.

Components don't generate html, they generate a tree of `Element`s, that translate to DOM nodes.
To generate html, you pass an Element tree to the `to_html()` function. In theory, the tree could be converted to things other than just html.
```python
from compony import to_html
to_html(DashboardPage())
```

The following markup would be generated:
```html
<html>
  <body>
    <div class="panel panel-default">
       <div class="panel-heading">A list of things</div>
       <ul class="list-group">
           <li class="list-group-item">Item One</li>
            <li class="list-group-item">Item Two <span class="badge">42</span></li>
            <li class="list-group-item">Item One</li>
           <li class="list-group-item"><a href="/home">Item One</a></li>
       </ul>
    </div>
    <div class="panel panel-default">
       <div class="panel-heading">Another ListGroup</div>
       <ul class="list-group">
           <li class="list-group-item">Item One</li>
           <li class="list-group-item">Item Two</li>
        </ul>
    </div>
    <div class="panel panel-default">
       <div class="panel-heading">YetAnother ListGroup</div>
        <ul class="list-group">
            <li class="list-group-item">I think you get the picture now'</li>
        </ul>
    </div>
  </body>
</html>
```

OK, but you're bored of Twitter Bootstrap, and you wished the markup format was compatible with AdminLTE, a nice admin theme. This is what a AdminLteListGroup component might look like:
(see https://almsaeedstudio.com/themes/AdminLTE/documentation/index.html#component-box)

```python
class AdminLteListGroup(Component):

    def render(self):
        return (
            div({'class': 'box box-default'},
                div({'class': 'box-header with-border'},
                    h3({'class': 'box-title'},
                        self.attrs['title']
                    ),
                ),
                div({'class': 'box-body'},
                    ul({'class': 'list-unstyled'},
                        [li(child) for child in self.children]
                    ),
                )
            )
        )
```

However, DashboardPage might be from a third party library, and you'd rather not have to completely fork it. Really you just want to change a bit of markup and leave most of the functionality intact. Compony provides a `self.swap()` function that allows components to be replaced with components that the user of the component provides. This is how a component can make its child components swappable:

```python
class DashboardPage(Component):

    def render(self):
        ListGroup = self.swap(ListGroup)
        return (
            html(
                body(
                    ListGroup({'title': 'A list of things'},
                        'Item One',
                        'Item Three',
                    )
                    ListGroup({'title': 'Another ListGroup'},
                        'I think you get the picture now',
                    )
                    ...
                )
            )
        )
```
If you want a Component to swap out certain components you must provide a dictionary of mappings from default components to ones you wish to swap them with:

```python
def dashboard_page(request):

    swaps = {
        ListGroup: AdminLteListGroup,
        Button: AdminLteButton,
        TopNav: AdminLteTopNav,
        etc...
    }

    return HttpResponse(to_html(DashboardPage(swaps=swaps)))
```

## Running the tests

run `python3 -m unittest` from the top level directory of this source repository

*Note: Compony is currently only compatible with Python 3*
