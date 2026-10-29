"""
Footprint presets tailored for Link Insertion, Guest Posts, Resource Pages, and Content Strategy outreach.
"""

FOOTPRINT_PRESETS = {
    "link_insertion_resources": {
        "name": "Resource Pages (Link Insertion)",
        "description": "Finds resource, links, and recommendation pages perfect for inserting relevant guides.",
        "footprints": [
            'inurl:resources "{keyword}"',
            'inurl:links "{keyword}"',
            '"useful resources" "{keyword}"',
            '"helpful resources" "{keyword}"',
            '"suggest a resource" "{keyword}"',
            '"additional resources" "{keyword}"',
            '"further reading" "{keyword}"',
            '"recommended tools" "{keyword}"',
            '"recommended reading" "{keyword}"',
            'inurl:recommended-links "{keyword}"',
        ]
    },
    "guest_posts_write_for_us": {
        "name": "Guest Posts / Write For Us",
        "description": "Finds active blogs accepting contributor articles and guest content.",
        "footprints": [
            '"write for us" "{keyword}"',
            '"guest post guidelines" "{keyword}"',
            '"submit guest post" "{keyword}"',
            '"contribute to our blog" "{keyword}"',
            '"guest author" "{keyword}"',
            '"guest article" "{keyword}"',
            '"accepting guest posts" "{keyword}"',
            'inurl:write-for-us "{keyword}"',
            'inurl:guest-post-guidelines "{keyword}"',
            '"editorial guidelines" "{keyword}"',
        ]
    },
    "roundups_and_curated": {
        "name": "Roundups & Curated Lists",
        "description": "Finds periodic roundups and curated article collections where content can be featured.",
        "footprints": [
            '"weekly roundup" "{keyword}"',
            '"monthly roundup" "{keyword}"',
            '"best articles of the week" "{keyword}"',
            '"favorite links" "{keyword}"',
            '"content marketing roundup" "{keyword}"',
            '"top blog posts" "{keyword}"',
        ]
    },
    "niche_blogs_editorials": {
        "name": "Niche Blogs & Editorial Content",
        "description": "Discovers active industry blogs with long-form articles suitable for link insertion.",
        "footprints": [
            'inurl:blog "{keyword}" guide',
            'inurl:category "{keyword}" tips',
            'inurl:article "{keyword}" insights',
            'inurl:posts "{keyword}" strategy',
        ]
    },
    "all_combined": {
        "name": "All Combined (Maximum Coverage)",
        "description": "Executes top footprints from all categories to maximize unique candidate discovery.",
        "footprints": [
            'inurl:resources "{keyword}"',
            '"useful resources" "{keyword}"',
            '"write for us" "{keyword}"',
            '"guest post" "{keyword}"',
            '"submit a resource" "{keyword}"',
            '"recommended reading" "{keyword}"',
            '"weekly roundup" "{keyword}"',
            'inurl:blog "{keyword}" guide',
        ]
    }
}

DEFAULT_KEYWORDS = [
    "content strategy",
    "content marketing",
    "SEO",
    "copywriting",
    "digital marketing",
    "SaaS marketing",
    "B2B marketing",
    "inbound marketing",
    "brand strategy",
    "growth marketing"
]
