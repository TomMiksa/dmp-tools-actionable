# Field Mapping from RDMO to RDA DMP Common Standard

| RDA DMP Field | RDMO source |
| ------------- | ----------- |
| `title` | `title` |
| `description` | `description` |
| `language` | \* _always set to `en`_ |
| `created` | `created` |
| `modified` | \* _latest modification date of any value_ |
| `ethical_issues_exist` | \* _loop through datasets_ |
| `contact` | `coordination/name` split into name and email |
| `project.start` | `schedule/project_start` |
| `project.end` | `schedule/project_end` |
| `cost` | \* _loop through cost-entries_ |
| `dataset.title` | `dataset/id` |
| `dataset.type` | `dataset/format` |
| `dataset.description` | \* _combined from various fields_ |
| `dataset.data_quality_assurance` | `dataset/quality_assurance` |
| `dataset.personal_data` | `dataset/sensitive_data/personal_data_yesno/yesno` |
| `dataset.sensitive_data` | `dataset/sensitive_data/other/yesno` |
| `dataset.distribution.description` | \* _combined from various fields_ |
| `dataset.distribution.license.license_ref` | `dataset/sharing/sharing_license` |
| `dataset.distribution.license.start_date` | `dataset/data_publication_date` |

## Special Cases

### Language Field `language`

As the RDMO data model does not have a field for the language of a project
this field is set to English for all DMPs.

### Field `modified`

In RDMO, the field `updated` more or less corresponds to the `modified` field in
the RDA DMP Common Standard.
However, since RDMO uses a relational database model, the `updated` field
of a project is only changed if the fields in the corresponding table
are updated.

To get a more natural interpretation of the last modification date the tool
is looking for the latest modification of any field or value in the RDMO
data and uses this value as the `modified` field in the RDA DMP Common Standard.

### Field `ethical_issues_exist`

The tool uses the following logic:

* If for _all_ datasets the questions for both personal data issues
and sensitive data issues are answered with _no_ then this field is set to `no`.
* If for _at least one_ dataset one of the questions is answered with
_yes_ then the field is set to `yes`.
* Otherwise, if the question is never answered with _yes_ but is not answered
for at least one dataset, the field is set to `unknown`.

### Substructure `cost`

All cost-related entries in RDMO are parsed.
The entries are added as sub-entries to the `cost` element,
using the following translation logic:

* `title`: This is mapped to the key in RDMO, e.g. `ipr/non_personnel`.
* `cost_value`: This is mapped to the value in RDMO.

### Field `dataset.description`

Since there are fields in RDMO with no direct mapping to RDA DMP Common Standard,
the field `dataset.description` is filled with data from other RDMO fields:

* `dataset/description`
* `dataset/interoperability`
* `dataset/creation_methods`
* `dataset/metadata`

### Field `dataset.distribution.description`

Since there are fields in RDMO with no direct mapping to RDA DMP Common Standard,
the field `dataset.distribution.description` is filled with data from other RDMO fields:

* `dataset/size/number_files`
* `dataset/versioning_strategy`
* `dataset/structure`
* `dataset/reuse_scenario`
* `dataset/sharing/conditions`
