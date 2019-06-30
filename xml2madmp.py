"""Module to convert an XML export from RDMO into a maDMP.

It requires that the default attributes from RDMO are used, not a
customized one (as was done by http://rdmo-demo.uibk.ac.at/)"""

import sys
import json
import xml.etree.ElementTree as ET

# XML way of saying 'uri'
XML_URI = "{http://purl.org/dc/elements/1.1/}uri"
# Beginning of all attributes we support
ATTR_START = "https://rdmorganiser.github.io/terms/domain/project"

def get_val(data, *args):
    """Accesses elements in a hierarchy.

    It will check on each level whether it exists. If not, `None`
    will be returned. If it does exist it traveres down."""

    pos = data
    for key in args:
        if not isinstance(pos, dict):
            return None
        if key not in pos:
            return None
        pos = pos[key]
    return pos

def enhance(desc, key, value):
    """Enhances a description text.

    This allows to enhance a description text with addition key-value
    information. Before enhancing it checks whether the values are
    existing or not."""

    if value is None:
        return desc
    if desc is not None and desc != '':
        desc += '\n%s: %s' % (key, value)
    else:
        desc = '%s: %s' % (key, value)
    return desc

def file2dict(filename):
    """Reads in an XML file, and convert it into a hierarchy.

    The XML file created by RDMO is rather flat. This function
    creates a slightly deeper hierarchy out of it."""

    root = ET.parse(filename).getroot()
    # We now transform the XML file into a Python
    # structure which can be easier traversed.
    # It looks like this:
    # rdmo[attribute][set_index][collection_index]
    rdmo = {}
    rdmo['title'] = root.find('title').text
    rdmo['description'] = root.find('description').text
    rdmo['created'] = root.find('created').text
    max_updated = root.find('updated').text
    for value in root.find('values').iter('value'):
        index = value.find('set_index').text
        attrib = value.find('attribute').attrib[XML_URI]
        if not attrib.startswith(ATTR_START):
            raise AttributeError('Attribute "%s" not starting with "%s"' %
                                 (attrib, ATTR_START))
        attrib = attrib[len(ATTR_START):]
        collection_index = value.find('collection_index').text
        text = value.find('text').text
        value_type = value.find('value_type').text
        unit = value.find('unit').text
        option_node = value.find('option')
        if XML_URI in option_node.attrib:
            option = option_node.attrib[XML_URI]
            # find the last part of the option
            option = option.split('/')[-1]
        else:
            option = None
        updated = value.find('updated').text
        new_val = {
            'text': text,
            'value_type': value_type,
            'unit': unit,
            'option': option,
            'updated': updated
        }
        if attrib not in rdmo:
            rdmo[attrib] = {}
        index = int(index)
        collection_index = int(collection_index)
        if index not in rdmo[attrib]:
            rdmo[attrib][index] = {}
        rdmo[attrib][index][collection_index] = new_val
        # update last modification date
        if updated > max_updated:
            max_updated = updated
    rdmo['updated'] = max_updated
    return rdmo

def rdmo_datasets(rdmo):
    """Finds the indexes of datasets used in the DMP."""

    datasets = set()
    for key in rdmo:
        if key.startswith('/dataset/'):
            datasets |= rdmo[key].keys()
    return datasets

def dataset_description(rdmo, index):
    """Creates a description of a dataset from the rdmo data."""

    description = get_val(rdmo, '/dataset/description', index, 0, 'text')
    interoperability = get_val(rdmo, '/dataset/interoperability', index, 0, 'option')
    creation_methods = get_val(rdmo, '/dataset/creation_methods', index, 0, 'text')
    metadata = get_val(rdmo, '/dataset/metadata', index, 0, 'text')
    description = enhance(description, 'Interoperability', interoperability)
    description = enhance(description, 'Creation methods', creation_methods)
    description = enhance(description, 'Metadata', metadata)
    return description

def distribution_description(rdmo, index):
    """Creates a description for a distribution from the rdmo data."""

    number_files = get_val(rdmo, '/dataset/size/number_files', index, 0, 'text')
    versioning_strategy = get_val(rdmo, '/dataset/versioning_strategy', index, 0, 'text')
    dataset_structure = get_val(rdmo, '/dataset/structure', index, 0, 'text')
    reuse_scenario = get_val(rdmo, '/dataset/reuse_scenario', index, 0, 'text')
    sharing_conditions = get_val(rdmo, '/dataset/sharing/conditions', index, 0, 'text')
    # TODO: find a base description for the distribution out of RDMO
    dist_desc = enhance(None, 'Sharing Conditions', sharing_conditions)
    dist_desc = enhance(dist_desc, 'Versioning Strategy', versioning_strategy)
    dist_desc = enhance(dist_desc, 'Reuse', reuse_scenario)
    dist_desc = enhance(dist_desc, 'Structure', dataset_structure)
    dist_desc = enhance(dist_desc, 'Number of Files', number_files)
    return dist_desc

def name_email(text):
    """Splits a text into names and email addresses.

    Everything containing a '@' is considered an email address,
    everything else a name.
    Args:
        text: A text which shall be split into name and email address.
    Returns:
        Tuple (name, email) extracted from the text."""

    if text is None:
        return 'Unknown', 'unknown'
    words = text.split()
    name = (' ').join([w for w in words if '@' not in w])
    email = (', ').join([w for w in words if '@' in w])
    return name, email

def has_ethical_issues(rdmo):
    """Scans the information in the RDMO data for ethical issues.

    Returns:
        A string of either 'yes' if one of the datasets indicates issues,
        'no' if all datasets indicate no issues, and 'unknown' if at least one
        dataset did not answer the question."""

    all_no = True
    for i in rdmo_datasets(rdmo):
        personal_data = get_val(
            rdmo,
            '/dataset/sensitive_data/personal_data_yesno/yesno',
            i,
            0,
            'option')
        sensitive_data = get_val(rdmo, '/dataset/sensitive_data/other/yesno', i, 0, 'option')
        if personal_data is not None and personal_data == 'yes':
            return "yes"
        if sensitive_data is not None and sensitive_data == 'yes':
            return "yes"
        if personal_data is None or sensitive_data is None:
            all_no = False
    return "no" if all_no else "unknown"

def get_security(rdmo, index):
    """Loops through security entries in the RDMO representation."""

    securities = []
    for key in rdmo:
        title = None
        if key.startswith('/dataset/data_security'):
            if key == '/dataset/data_security/security_measures':
                title = 'Provisions in Place for Data Security'
            if key == '/dataset/data_security/access_permissions':
                title = 'People with access right'
            if key == '/dataset/data_security/backups':
                title = 'Data Backup'
            if key == '/dataset/data_security/backup_responsible/name':
                title = 'Responsible Person for Data Backup'
        vals = None
        if title is not None:
            vals = get_val(rdmo, key, index)
        if vals is not None:
            for idx in vals:
                if 'text' in vals[idx]:
                    security = {
                        'title': title,
                        'description': vals[idx]['text']
                    }
                    securities.append(security)
    return securities

def get_dataset_entry(rdmo, i):
    """Constructs the object for a dataset of the maDMP."""

    title = get_val(rdmo, '/dataset/id', i, 0, 'text')
    dataset_type = get_val(rdmo, '/dataset/format', i, 0, 'text')
    dataset_qa = get_val(rdmo, '/dataset/quality_assurance', i, 0, 'text')
    dataset = {'title': title, 'type': dataset_type}
    personal_data = get_val(
        rdmo,
        '/dataset/sensitive_data/personal_data_yesno/yesno',
        i,
        0,
        'option')
    sensitive_data = get_val(rdmo, '/dataset/sensitive_data/other/yesno', i, 0, 'option')
    if personal_data is None:
        dataset['personal_data'] = 'unknown'
    else:
        dataset['personal_data'] = personal_data
    if sensitive_data is None:
        dataset['sensitive_data'] = 'unknown'
    else:
        dataset['sensitive_data'] = sensitive_data
    # TODO: find preservation statement
    if dataset_qa is not None:
        dataset['data_quality_assurance'] = dataset_qa
    # for each dataset look for distribution
    sharing_license = get_val(rdmo, '/dataset/sharing/sharing_license', i, 0, 'text')
    sharing_start_date = get_val(rdmo, '/dataset/data_publication_date', i, 0, 'text')
    volume = get_val(rdmo, '/dataset/size/volume', i, 0, 'text')
    dist_desc = distribution_description(rdmo, i)
    if sharing_license or volume or dist_desc:
        # TODO: find a title for the distribution out of RDMO
        distribution = {'title': title, 'license': []}
        if dist_desc is not None:
            distribution['description'] = dist_desc
        if volume is not None:
            distribution['byte_size'] = int(round(float(volume) * 1e9))
        if sharing_license is not None:
            distribution['license'].append({
                'license_ref': sharing_license,
                'start_date': sharing_start_date
            })
        # append distribution to dataset
        dataset['distribution'] = distribution
    description = dataset_description(rdmo, i)
    if description is not None:
        dataset['description'] = description
    # get security entries
    securities = get_security(rdmo, i)
    if securities:
        dataset['security'] = securities
    return dataset

def get_costs(rdmo):
    """Loops through costs entries in the RDMO representation."""

    costs = []
    for key in rdmo:
        if key.startswith('/costs'):
            cost_type = key.split('/')[-1]
            if cost_type in ['personnel', 'non_personnel']:
                continue
            cost_type = key[14:]
            cost_val = get_val(rdmo, key, 0, 0, 'text')
            cost = {
                'title': cost_type,
                'cost_value': cost_val
            }
            costs.append(cost)
    return costs

def get_ma_dmp(rdmo):
    """Constructs an in-memory Python version of the maDMP.

    This is ready to be serialized."""

    ma_dmp = {}
    ma_dmp['title'] = rdmo['title']
    if rdmo['description'] is not None:
        ma_dmp['description'] = rdmo['description']
    # TODO: no language in the RDMO data model?
    ma_dmp['language'] = 'en'
    ma_dmp['created'] = rdmo['created']
    ma_dmp['modified'] = rdmo['updated']
    ma_dmp['ethical_issues_exist'] = has_ethical_issues(rdmo)
    # extract email from name / email field
    name, email = name_email(get_val(rdmo, '/coordination/name', 0, 0, 'text'))
    ma_dmp['contact'] = {'name': name, 'mbox': email}
    # create an entry for project start / end
    project_start = get_val(rdmo, '/schedule/project_start', 0, 0, 'text')
    project_end = get_val(rdmo, '/schedule/project_end', 0, 0, 'text')
    project = {}
    if project_start is not None:
        project['project_start'] = project_start
    if project_end is not None:
        project['project_end'] = project_end
    if project:
        ma_dmp['project'] = project
    # get costs entry
    costs = get_costs(rdmo)
    if costs:
        ma_dmp['cost'] = costs
    # loop through datasets
    ma_dmp['dataset'] = []
    # for each dataset create an entry
    for i in rdmo_datasets(rdmo):
        # append dataset to list of datasets
        ma_dmp['dataset'].append(get_dataset_entry(rdmo, i))
    return ma_dmp

def main(argv):
    """Entry point to perform the conversion."""

    if len(argv) < 3:
        print("Usage: %s <xml-file> <json-file>" % (argv[0]),
              file=sys.stderr)
        sys.exit(1)
    source_file = argv[1]
    target_file = argv[2]
    rdmo_data = file2dict(source_file)
    ma_dmp_data = get_ma_dmp(rdmo_data)
    with open(target_file, 'w') as outfile:
        print(json.dumps(ma_dmp_data, indent=4), file=outfile)

if __name__ == "__main__":
    main(sys.argv)
