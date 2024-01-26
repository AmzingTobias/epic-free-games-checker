import logging
import requests


class ProductDecodeException(Exception):
    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self):
        return self.msg


class Game:
    def __init__(self,
                 title: str,
                 description: str,
                 price: int,
                 product_url: str,
                 thumbnail_url: (str | None)) -> None:
        self.title = title
        self.description = description
        self.price = price
        self.free = price == 0
        self.product_url = product_url
        self.thumbnail_url = thumbnail_url

    def display(self):
        print(f"{self.title}\n{self.description}\n{
              self.product_url}\n{self.thumbnail_url}")


def get_title_of_product(product) -> str:
    if isinstance(product, dict):
        try:
            title_found = product["title"]
            if isinstance(title_found, str):
                return title_found
            else:
                raise ProductDecodeException("Title value is invalid")
        except KeyError:
            raise ProductDecodeException("Title does not exist in product")
    else:
        raise ProductDecodeException("Invalid product input")


def get_price_of_product(product) -> int:
    try:
        price_found = product["price"]["totalPrice"]["discountPrice"]
        if (isinstance(price_found, int)):
            return price_found
        else:
            raise ProductDecodeException("Price data malformed")
    except KeyError:
        raise ProductDecodeException("Price does not exist in product")
    except TypeError:
        raise ProductDecodeException("Invalid product input")


def get_thumbnail_of_product(product):
    try:
        images = product["keyImages"]
        for image in images:
            if image["type"] == "Thumbnail":
                image_found = image["url"]
                if (isinstance(image_found, str)):
                    return image_found
                else:
                    continue
            else:
                continue
        return None
    except KeyError:
        logging.info("Could not find images in product data")
        return None
    except TypeError:
        raise ProductDecodeException("Invalid product input")


def get_possible_free_products(json_data):
    try:
        # Access free games by looking in
        # data -> Catalog -> searchStore -> elements
        return json_data["data"]["Catalog"]["searchStore"]["elements"]
    except IndexError:
        logging.error("JSON data unsupported")


def get_description_of_product(product) -> str:
    if isinstance(product, dict):
        try:
            description_found = product["description"]
            if isinstance(description_found, str):
                return description_found
            else:
                raise ProductDecodeException("Description value is invalid")
        except KeyError:
            raise ProductDecodeException(
                "Description does not exist in product")
    else:
        raise ProductDecodeException("Invalid product input")


def get_product_url(product):
    URL_FIELD_KEY = "offerMappings"
    try:
        url_found = product["offerMappings"][0]["pageSlug"]
        if (isinstance(url_found, str)):
            return url_found
        else:
            raise ProductDecodeException(f"URL: {url_found} is invalid")
    except TypeError:
        raise ProductDecodeException("Invalid product input")
    except IndexError:
        raise ProductDecodeException("Could not find product page in product")
    except KeyError:
        raise ProductDecodeException(f"{URL_FIELD_KEY} does not exist in product data")


def decode_product(product):
    try:
        # title, description,
        # price->totalPrice->discountPrice, offerMappings->0->pageSlug,
        # keyImages->(Where type=Thumbnail)
        title = get_title_of_product(product)
        description = get_description_of_product(product)
        price = get_price_of_product(product)
        product_url = get_product_url(product)
        thumbnail_url = get_thumbnail_of_product(product)
        return Game(title, description, price, product_url, thumbnail_url)
    except ProductDecodeException as err:
        logging.error(err)
        return None


def process_products(products):
    free_games: list[Game] = []
    try:
        for product in products:
            game_decoded = decode_product(product)
            if game_decoded is not None and game_decoded.free:
                logging.info(f"{game_decoded.title} is free")
                free_games.append(game_decoded)
    except TypeError:
        raise ProductDecodeException("Products list invalid")
    return free_games


class EpicFreeGames:

    def __init__(self) -> None:
        self.free_games: list[Game] = []
        self.URL_FOR_CHECK = "https://store-site-backend-static-ipv4.ak.epicgames.com/freeGamesPromotions?locale=en-US&country=GB&allowCountries=GB"

    def make_request(self):
        response = requests.get(self.URL_FOR_CHECK)
        if response.ok:
            try:
                json_data = response.json()
                products = get_possible_free_products(json_data)
                if products is not None:
                    self.free_games = process_products(products)
            except requests.JSONDecodeError as err:
                logging.warning(f"Convert to json failed with: {err}")
        else:
            logging.warning(f"Request failed with code: {
                            response.status_code}")
