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
        print(f"Title:{self.title}\nDescription: {self.description}\nProduct page: {self.product_url}\nThumbnail: {self.thumbnail_url}")


class EpicFreeGames:

    def __init__(self) -> None:
        self.free_games: list[Game] = []
        self.URL_FOR_CHECK = "https://store-site-backend-static-ipv4.ak.epicgames.com/freeGamesPromotions?locale=en-US&country=GB&allowCountries=GB"

    def make_request(self):
        """Make a request to epic games API and discover free games"""
        response = requests.get(self.URL_FOR_CHECK)
        if response.ok:
            try:
                json_data = response.json()
                try:
                    products = EpicFreeGames().get_products_from_response(json_data)
                    if products is not None:
                        self.free_games = EpicFreeGames().process_products(products)
                except ProductDecodeException as err:
                    logging.error(err)
            except requests.JSONDecodeError as err:
                logging.warning(f"Convert to json failed with: {err}")
        else:
            logging.warning(f"Request failed with code: {response.status_code}")

    @staticmethod
    def get_title_of_product(product) -> str:
        """Get the title of a product from product data"""
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

    @staticmethod
    def get_price_of_product(product) -> int:
        """Get the price of a product from product data"""
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

    @staticmethod
    def get_thumbnail_of_product(product):
        """Get the thumbnail of a product, if it exists, from product data"""
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

    @staticmethod
    def get_products_from_response(json_data):
        """Get the products from the response of a request"""
        if isinstance(json_data, dict):
            try:
                # Access free games by looking in
                # data -> Catalog -> searchStore -> elements
                products_found = json_data["data"]["Catalog"]["searchStore"]["elements"]
                if isinstance(products_found, list):
                    return products_found
                else:
                    raise ProductDecodeException("Product data found is invalid type")
            except KeyError:
                raise ProductDecodeException("JSON data is invalid")
        else:
            raise ProductDecodeException("Input data invalid")

    @staticmethod
    def get_description_of_product(product) -> str:
        """Get the description of a product from product data"""
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

    @staticmethod
    def get_product_url(product) -> str:
        """Get the url of a product from product data"""
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

    @staticmethod
    def decode_product(product) -> (Game | None):
        """Convert raw product data into a Game object"""
        try:
            # title, description,
            # price->totalPrice->discountPrice, offerMappings->0->pageSlug,
            # keyImages->(Where type=Thumbnail)
            title = EpicFreeGames().get_title_of_product(product)
            description = EpicFreeGames().get_description_of_product(product)
            price = EpicFreeGames().get_price_of_product(product)
            product_url = EpicFreeGames().get_product_url(product)
            thumbnail_url = EpicFreeGames().get_thumbnail_of_product(product)
            return Game(title, description, price, product_url, thumbnail_url)
        except ProductDecodeException as err:
            logging.error(err)
            return None

    @staticmethod
    def process_products(products) -> list[Game]:
        """Decode a list of products and return a list of free games"""
        try:
            free_games: list[Game] = []
            for product in products:
                game_decoded = EpicFreeGames().decode_product(product)
                if game_decoded is not None and game_decoded.free:
                    logging.info(f"{game_decoded.title} is free")
                    free_games.append(game_decoded)
            return free_games
        except TypeError:
            raise ProductDecodeException("Products list invalid")
