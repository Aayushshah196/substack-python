# substack-python

`substack-python` is a powerful Python package designed to automate the creation, management, and publishing of articles on Substack. Whether you're a writer looking to streamline your publication process or a developer building tools for content creators, this package simplifies interactions with the Substack platform.

## Features

- **Create Articles**: Easily create new articles with titles, content, and tags.
- **Edit Articles**: Modify existing articles quickly and efficiently.
- **Publish Articles**: Publish articles programmatically.

## Installation

You can install the package via pip:

```bash
pip install substack-python
```

## Quick Start

Below are some examples to help you get started with `substack-python`.

### 1. Setting Up the Client

To use the package, you'll first need to set up the client with your Substack credentials:

```python
from substack.client import SubstackClient

# Initialize the Substack client
substack_domain = "your_substack_name"
client = SubstackClient(substack_domain)

# Add auth token from the browser cookie storage
cookies = {"substack.sid": "Put Your Auth Cookie Here"}
client.set_auth_cookie(cookies)
```

### 2. Creating a JSON from article Markdown

Creating the article json from its markdown

```python
from substack.md_to_json.parsers import markdown_to_json, remove_none_values

markdown_text = """
## Hello world

This is a **test** [Hello world](https://example.com)

- Hello world
1. world

[Hello world](https://example.com)

![Image](https://example.com/image.jpg)
"""

document = markdown_to_json(markdown_text)
document_dict = document.model_dump(exclude_none=True)
```

Sample of the above markdown dict

```json
{
  "type": "doc",
  "content": [
    {
      "type": "heading",
      "attrs": {
        "level": 2
      },
      "content": [
        {
          "type": "text",
          "text": "Hello world",
          "content": []
        }
      ]
    },
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "This is a ",
          "content": []
        },
        {
          "type": "text",
          "text": "test",
          "marks": [
            {
              "type": "strong"
            }
          ],
          "content": []
        },
        {
          "type": "text",
          "text": " ",
          "content": []
        },
        {
          "type": "text",
          "text": "Hello world",
          "marks": [
            {
              "type": "link"
            }
          ],
          "attrs": {
            "href": "https: //example.com",
            "target": "_blank",
            "rel": "noopener noreferrer nofollow"
          },
          "content": []
        },
        {
          "type": "text",
          "text": "\n- Hello world\n1. world\n",
          "content": []
        },
        {
          "type": "text",
          "text": "Hello world",
          "marks": [
            {
              "type": "link"
            }
          ],
          "attrs": {
            "href": "https://example.com",
            "target": "_blank",
            "rel": "noopener noreferrer nofollow"
          },
          "content": []
        },
        {
          "type": "text",
          "text": "\n",
          "content": []
        }
      ]
    }
  ]
}
```

### 3. Creating a New Article

Creating a new article is straightforward:

```python
from substack.structures import Draft

article_title = "Your Article Title"
article_subtitle = "Your Article Subtitle"
article = Draft(title=article_title, subtitle=article_subtitle, draft_body=document)

draft_res = client.posts.create_new_draft(draft_content=article.to_dict())

# Get the draft id for publishing it
draft_id = draft_res.get("id")
publish_res = client.posts.publish_draft(draft_id=draft_id, share_automatically=True)
```

## Contributing

We welcome contributions! Please submit a pull request or open an issue for feature requests or bug reports.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any questions or support, please reach out to me.
