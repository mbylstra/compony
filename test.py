import unittest

from compony.core import to_html, Component, to_element_tree, AttrsRequired, \
    UnexpectedRegions
from compony.elements import div, p, h1, h2, hr


class TestComponentMixin:

    def assertComponentEqualToETree(self, component, etree):
        component_etree = to_element_tree(component)
        self.assertEqual(component_etree, etree, msg="{} is not equal to {}".format(
            to_html(component_etree), to_html(etree)
        ))


class TestElementComparison(unittest.TestCase):

    def test_1(self):
        e1 = div({'attr1': 'one', 'attr2': 'two'},
            h1({'class': 'awesome'},
                'i am heading 1'
            ),
            'some text in a div',
        )
        e2 = div({'attr1': 'one', 'attr2': 'two'},
            h1({'class': 'awesome'},
                'i am heading 1'
            ),
            'some text in a div',
        )
        e3 = div({'attr1': 'one', 'attr2': 'two'},
                 h1({'class': 'awesome'},
                    'i am heading 1'
                    ),
                 'this text is different',
             )
        e4 = div({'attr1': 'one', 'attr2': 'two'},
                 h2({'class': 'awesome'},
                    'i am heading 1'
                    ),
                 'some text in a div',
             )
        self.assertEqual(e1, e2)
        self.assertNotEqual(e1, e3)
        self.assertNotEqual(e1, e4)


class TestElement(unittest.TestCase):

    def test_list_children(self):
        e1 = div([div(), div()])
        e2 = div(div(), div())
        self.assertEqual(e1, e2)


class TestComponentClass(TestComponentMixin, unittest.TestCase):


    def test_simple_div_component(self):

        class SimpleDivComponent(Component):
            def render(self):
                return div()

        self.assertComponentEqualToETree(
            SimpleDivComponent(),
            div()
        )


    def test_simple_div_tree_component(self):

        class SimpleDivTreeComponent(Component):
            def render(self):
                return div(
                    div()
                )

        self.assertComponentEqualToETree(
            SimpleDivTreeComponent(),
            div(div())
        )


    def test_div_tree2(self):

        class SimpleDivComponent(Component):
            def render(self):
                return div()

        self.assertComponentEqualToETree(
            div(SimpleDivComponent()),
            div(div())
        )

    def test_component_wrapper(self):

        class SimpleDivComponent(Component):
            def render(self):
                return div('hello')

        class ComponentWrapper(Component):
            def render(self):
                return SimpleDivComponent()

        self.assertComponentEqualToETree(
            ComponentWrapper(),
            div('hello')
        )


    def test_nested_components(self):

        class SimpleDivComponent(Component):
            def render(self):
                return div()

        class ComponentWrapper(Component):
            def render(self):
                return div(
                    SimpleDivComponent(),
                    SimpleDivComponent(),
                )

        self.assertComponentEqualToETree(
            ComponentWrapper(),
            div(
                div(),
                div()
            )
        )


    def test_nested_components2(self):

        class SimpleDivComponent(Component):
            def render(self):
                return div()

        class ComponentWrapper(Component):

            def render(self):
                return div(
                    SimpleDivComponent()
                )

        self.assertComponentEqualToETree(
            ComponentWrapper(),
            div(div())
        )


    def test_component_xrays(self):

        class ChildComponent(Component):

            def render(self):
                return h1(self.xrays['message'])

        class ParentComponent(Component):

            def get_component_xrays(self):
                return {
                    'message': 'hello from parent'
                }

            def render(self):
                return ChildComponent()

        self.assertComponentEqualToETree(
            div(ParentComponent()),
            div(h1('hello from parent'))
        )


    def test_component_xrays_grandchild(self):

        class GrandchildComponent(Component):

            def render(self):
                return h1(
                    "I am Grandchild. This is grandparent's message: {}".format(
                    self.xrays['message'])
                )

        class ChildComponent(Component):

            def render(self):
                return div(GrandchildComponent())

        class ParentComponent(Component):

            def get_component_xrays(self):
                return {
                    'message': 'hello from grandparent'
                }

            def render(self):
                return ChildComponent()

        self.assertComponentEqualToETree(
            ParentComponent(),
            div(
                h1(
                    "I am Grandchild. This is grandparent's message: "
                    "hello from grandparent"
                )
            )
        )

    def test_xrays_component_kwargs(self):

        class ChildComponent(Component):

            def render(self):
                return h1(self.xrays['message'])

        class ParentComponent(Component):

            def render(self):
                return ChildComponent()

        self.assertComponentEqualToETree(
            div(ParentComponent(xrays={'message': 'hello from outside'})),
            div(h1('hello from outside'))
        )


    def test_swaps(self):

        class ChildComponentA(Component):
            def render(self):
                return h1('I am ChildComponent A')

        class ChildComponentB(Component):
            def render(self):
                return h1('I am ChildComponent B')

        class ParentComponent(Component):

            swappable = (ChildComponentA,)

            def render(self):
                return div(self.swap(ChildComponentA)())

        self.assertComponentEqualToETree(
            ParentComponent(swaps={
                ChildComponentA: ChildComponentB
            }),
            div(h1('I am ChildComponent B'))
        )


    def test_attrs(self):

        class ComponentA(Component):

            def render(self):
                return div(self.attrs['message'])

        self.assertComponentEqualToETree(
            ComponentA({'message': 'test message'}),
            div('test message')
        )


    def test_children(self):

        class ComponentA(Component):

            def render(self):
                return div(
                    self.children
                )

        self.assertComponentEqualToETree(
            ComponentA('child text'),
            div('child text')
        )


    def test_children2(self):

        class ComponentA(Component):

            def render(self):
                return div(
                    self.children,
                    p('a p')
                )

        self.assertComponentEqualToETree(
            ComponentA('child text'),
            div('child text', p('a p'))
        )


    def test_return_list(self):

        class ComponentA(Component):

            def render(self):
                return [div('one'), div('two')]

        self.assertComponentEqualToETree(
            div(ComponentA()),
            div(div('one'), div('two'))
        )


    def test_required_attrs(self):

        class ComponentA(Component):

            required_attrs = ('one', 'two')

            def render(self):
                return div()

        with self.assertRaises(AttrsRequired):
            ComponentA({'one': 'a'})

        try:
            ComponentA({'one': 'a', 'two': 'b'})
        except AttrsRequired:
            self.fail("AttrsRequired raised unexpectantly")


    def test_regions(self):

        class ComponentA(Component):

            region_names = ('header', 'body', 'footer')

            def render(self):
                return div(
                    h1(self.regions.header),
                    hr(),
                    div(self.regions.body),
                    hr(),
                    div(self.regions.footer),
                )

        self.assertComponentEqualToETree(
            ComponentA(
                header='i am header',
                body='i am body',
                footer='i am footer'
            ),
            div(
                h1('i am header'),
                hr(),
                div('i am body'),
                hr(),
                div('i am footer'),
            )
        )

        with self.assertRaises(UnexpectedRegions):
            ComponentA(
                headr='i am headr',
                body='i am body',
            )

