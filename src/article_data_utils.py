import json
from typing import Optional, List

class SocialStats:
    def __init__(self, facebook=None, gplus=None, pinterest=None, linkedin=None, stumbledupon=None, vk=None):
        self.facebook = facebook
        self.gplus = gplus
        self.pinterest = pinterest
        self.linkedin = linkedin
        self.stumbledupon = stumbledupon
        self.vk = vk

class Social:
    def __init__(self, **kwargs):
        self.facebook = kwargs.get('facebook', {})
        self.gplus = kwargs.get('gplus', {})
        self.pinterest = kwargs.get('pinterest', {})
        self.linkedin = kwargs.get('linkedin', {})
        self.stumbledupon = kwargs.get('stumbledupon', {})
        self.vk = kwargs.get('vk', {})

class Entity:
    def __init__(self, name: str, sentiment: str):
        self.name = name
        self.sentiment = sentiment

class Entities:
    def __init__(self, persons: List[Entity], organizations: List[Entity], locations: List[Entity]):
        self.persons = persons
        self.organizations = organizations
        self.locations = locations

class Thread:
    def __init__(self, uuid: str, url: str, site_full: str, site: str, site_section: str,
                 site_categories: List[str], section_title: str, title: str,
                 title_full: str, published: str, replies_count: int, participants_count: int,
                 site_type: str, country: str, main_image: str, performance_score: int,
                 domain_rank: int, domain_rank_updated: str, reach: Optional[float],
                 social: Social):
        self.uuid = uuid
        self.url = url
        self.site_full = site_full
        self.site = site
        self.site_section = site_section
        self.site_categories = site_categories
        self.section_title = section_title
        self.title = title
        self.title_full = title_full
        self.published = published
        self.replies_count = replies_count
        self.participants_count = participants_count
        self.site_type = site_type
        self.country = country
        self.main_image = main_image
        self.performance_score = performance_score
        self.domain_rank = domain_rank
        self.domain_rank_updated = domain_rank_updated
        self.reach = reach
        self.social = social

class Article:
    def __init__(self, thread: Thread, uuid: str, url: str, ord_in_thread: int,
                 parent_url: Optional[str], author: str, published: str,
                 title: str, text: str, highlight_text: str, highlight_title: str,
                 highlight_thread_title: str, language: str, sentiment: str,
                 categories: List[str], webz_reporter: bool, external_links: List[str],
                 external_images: List[str], entities: Entities, rating: Optional[float],
                 crawled: str, updated: str):
        self.thread = thread
        self.uuid = uuid
        self.url = url
        self.ord_in_thread = ord_in_thread
        self.parent_url = parent_url
        self.author = author
        self.published = published
        self.title = title
        self.text = text
        self.highlight_text = highlight_text
        self.highlight_title = highlight_title
        self.highlight_thread_title = highlight_thread_title
        self.language = language
        self.sentiment = sentiment
        self.categories = categories
        self.webz_reporter = webz_reporter
        self.external_links = external_links
        self.external_images = external_images
        self.entities = entities
        self.rating = rating
        self.crawled = crawled
        self.updated = updated

def deserialize_article(json_str: str) -> Article:
    data = json.loads(json_str)

    social = Social(**data["thread"]["social"])

    persons = [Entity(**p) for p in data["entities"]["persons"]]
    organizations = [Entity(**o) for o in data["entities"]["organizations"]]
    locations = [Entity(**l) for l in data["entities"]["locations"]]
    entities = Entities(persons, organizations, locations)

    thread_data = data["thread"]
    thread = Thread(
        uuid=thread_data["uuid"],
        url=thread_data["url"],
        site_full=thread_data["site_full"],
        site=thread_data["site"],
        site_section=thread_data["site_section"],
        site_categories=thread_data["site_categories"],
        section_title=thread_data["section_title"],
        title=thread_data["title"],
        title_full=thread_data["title_full"],
        published=thread_data["published"],
        replies_count=thread_data["replies_count"],
        participants_count=thread_data["participants_count"],
        site_type=thread_data["site_type"],
        country=thread_data["country"],
        main_image=thread_data["main_image"],
        performance_score=thread_data["performance_score"],
        domain_rank=thread_data["domain_rank"],
        domain_rank_updated=thread_data["domain_rank_updated"],
        reach=thread_data["reach"],
        social=social
    )

    article = Article(
        thread=thread,
        uuid=data["uuid"],
        url=data["url"],
        ord_in_thread=data["ord_in_thread"],
        parent_url=data["parent_url"],
        author=data["author"],
        published=data["published"],
        title=data["title"],
        text=data["text"],
        highlight_text=data["highlightText"],
        highlight_title=data["highlightTitle"],
        highlight_thread_title=data["highlightThreadTitle"],
        language=data["language"],
        sentiment=data["sentiment"],
        categories=data["categories"],
        webz_reporter=False,
        external_links=data["external_links"],
        external_images=data["external_images"],
        entities=entities,
        rating=data["rating"],
        crawled=data["crawled"],
        updated=data["updated"]
    )

    return article


def deserialize_articles(json_list) -> []:
    articles = []
    for json_str in json_list:
        article = deserialize_article(json.dumps(json_str))
        articles.append(article)
    return articles

