from bs4 import BeautifulSoup, Comment, NavigableString

TOO_HIGH_TAGS = ['html', '[document]']

html_doc = None
with open('sample_dom.html', 'r') as html_file:
    html_doc = html_file.read()

def buildParents(el, curr_parent_identifiers):
    parents_identifiers = list(curr_parent_identifiers)
    for parent in el.parents:
        if parent.name not in TOO_HIGH_TAGS:
            num_classes = len(parent.attrs['class']) if 'class' in parent.attrs else -1
            id_name = '#' + parent.attrs['id'] if 'id' in parent.attrs else ''
            tag_name = parent.name
            if num_classes > 1:
                for _class in parent.attrs['class']:
                    class_name = '.' + _class
                    full_tag_identifier = tag_name + id_name + class_name
                    parents_identifiers.insert(0,full_tag_identifier)
                    buildParents(parent, parents_identifiers)
            elif num_classes != -1:
                class_name = '.' + parent.attrs['class'][0]
                full_tag_identifier = tag_name + id_name + class_name
                parents_identifiers.insert(0,full_tag_identifier)
            else:
                full_tag_identifier = tag_name + id_name
                parents_identifiers.insert(0,full_tag_identifier)
    return parents_identifiers
def traverseBody(body):
    processed_children = []
    for child in body.findChildren():
        num_classes = len(child.attrs['class']) if 'class' in child.attrs else -1
        id_name = '#' + child.attrs['id'] if 'id' in child.attrs else ''
        tag_name = child.name
        class_name = '.'.join(child.attrs['class']) if 'class' in child.attrs else ''
        child_full_unique = tag_name + id_name + class_name
        if child_full_unique not in processed_children: # dont process siblings
            parents = buildParents(child, [])
            if num_classes > 1:
                for _class in child.attrs['class']:
                    class_name = '.' + _class
                    full_tag_identifier = tag_name + id_name + class_name
                    print ' > '.join(parents) + ' > ' + full_tag_identifier + "{\n\n}"
            elif num_classes != -1:
                class_name = '.' + child.attrs['class'][0]
                full_tag_identifier = tag_name + id_name
                print ' > '.join(parents) + ' > ' + full_tag_identifier + "{\n\n}"
            else:
                full_tag_identifier = tag_name + id_name
                print ' > '.join(parents) + ' > ' + full_tag_identifier + "{\n\n}"
        class_name = '.'.join(child.attrs['class']) if 'class' in child.attrs else ''
        processed_children.append(child_full_unique)

if html_doc is not None:
    soup = BeautifulSoup(html_doc, 'html.parser')
    # Remove all bs.
    for elem in soup.findAll(['script', 'style', 'link', 'noscript', 'meta']):
        elem.extract()
    # Remove comments
    for element in soup(text=lambda text: isinstance(text, Comment)):
        element.extract()
    for element in soup(text=lambda text: isinstance(text, NavigableString)):
        element.extract()
    print soup.body.prettify()
    traverseBody(soup.body)
