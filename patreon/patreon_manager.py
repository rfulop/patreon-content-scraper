import json
import re

import requests
from bs4 import BeautifulSoup

from utils.file import create_folder, create_file


class PatreonManager(object):
    """
    Patreon API client for interacting with the Patreon platform.

    This class provides a client interface to interact with the Patreon platform
    by handling authentication and campaigns content retrival.

    Attributes:MAIN_FOLDER_NAME (str): The name of the main folder where downloaded content is stored.
    """

    MAIN_FOLDER_NAME = 'downloa'

    def __init__(self, email: str, password: str):
        """
        Initialize Patreon API client.
        :param email: Patreon email.
        :param password: Patreon password.
        """

        self.base_url = 'https://www.patreon.com'
        self.email = email
        self.password = password
        self.session = requests.Session()

    def login(self) -> bool:
        """
        Authenticate and log in to the Patreon platform.

        This function performs user authentication and login on the Patreon platform
        using the provided email and password. It sends a POST request with user credentials
        to the Patreon authentication endpoint.

        :return: True if the login is successful, False otherwise.
        :rtype: bool
        """
        headers = {
            'content-type': 'application/vnd.api+json',
        }

        params = {
            'include': 'user.null',
            'fields[user]': '[]',
            'json-api-version': '1.0',
        }

        auth_payload = {
            'data': {
                'type': 'genericPatreonApi',
                'attributes': {
                    'patreon_auth': {
                        'redirect_target': f'{self.base_url}/home',
                        'email': self.email,
                        'password': self.password,
                        'allow_account_creation': False,
                    },
                    'auth_context': 'auth',
                },
            }
        }

        try:
            response = self.session.post(
                f'{self.base_url}/api/auth',
                headers=headers,
                params=params,
                data=json.dumps(auth_payload),
            )

            response.raise_for_status()

            if response.status_code == 200:
                print("Login successful")
                return True
            else:
                print(f"Login failed with HTTP status code {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"Login request failed: {e}")
            return False
        except json.decoder.JSONDecodeError as e:
            print(f"Failed to decode JSON response: {e}")
            return False

    def get_campaigns_data(self) -> list[dict]:
        """
        Retrieve data for campaigns to which the logged-in user is subscribed.

        This function sends a request to retrieve data about campaigns to which the
        currently logged-in user is subscribed. It fetches campaign names and their
        respective IDs.

        :return: A list of dictionaries containing campaign data, including creator names
                 and campaign IDs.
        :rtype: list
        """

        params = {
            'include': 'pledges.creator.campaign.null',
            'json-api-version': '1.0',
        }

        try:

            response = self.session.get(
                f'{self.base_url}/api/current_user',
                params=params,
            )
            response.raise_for_status()
            data = response.json()

            included = data.get('included', [])
            campaigns_data = []

            for campaign in included:
                if campaign.get('type') != 'campaign':
                    continue

                attributes = campaign.get('attributes', {})
                creator_name = attributes.get('name')
                campaign_id = campaign.get('id')

                if campaign_id is not None and creator_name is not None:
                    campaign_info = {
                        'creator_name': creator_name,
                        'campaign_id': campaign_id,
                    }
                    campaigns_data.append(campaign_info)

            return campaigns_data

        except requests.exceptions.RequestException as e:
            print(f"Requesting campaigns failed: {e}")
            return []
        except (json.decoder.JSONDecodeError, KeyError) as e:
            print(f"Failed to process response: {e}")
            return []

    def get_all_campaigns_content(self, campaign_data: list[dict]):
        """
        Get and save content for all campaigns.

        This function iterates through a list of campaign data, retrieves and saves content for each campaign,
        and organize the content into separate campaign folders.

        :param campaign_data: A list of campaign data dictionaries containing creator names and campaign IDs.
        :type campaign_data: list of dict
        """
        for campaign_info in campaign_data:
            campaign_id = campaign_info['campaign_id']
            creator_name = campaign_info['creator_name']

            print(f"Parsing campaign {campaign_id} by {creator_name}...")

            campaign_content = self.get_campaign_content(campaign_id)
            if campaign_content:
                self.parse_campaign_content(campaign_content, creator_name)
            else:
                print(f"Failed to retrieve content for campaign {campaign_id} by {creator_name}")

    @staticmethod
    def parse_post_content(post: dict) -> dict or None:
        """
        Parse content data from a Patreon post.

        :param post: The Patreon post data to parse.
        :return: A dictionary containing parsed post information, or None if parsing fails.
        :rtype: dict or None
        """
        try:
            post_id = post.get('id')
            attributes = post.get('attributes', {})

            print(f"Parsing Patreon post {post_id}...")

            content = attributes.get('content', None)

            date = attributes.get('published_at', None)
            if date:
                date = date.split('T')[0]

            if not attributes.get('image'):
                img_url = attributes.get('meta_image_url', None)
            else:
                img_url = attributes['image'].get('large_url', None)

            title = attributes.get('title', None)

            tags = []
            relationships = post.get('relationships', {})
            user_defined_tags_data = relationships.get('user_defined_tags', {}).get('data', [])

            for tag in user_defined_tags_data:
                tag_id = tag.get('id')

                result = re.search(r';(.+)$', tag_id)
                if result:
                    tags.append(result.group(1))

            return {
                'post_id': post_id,
                'title': title,
                'date': date,
                'img_url': img_url,
                'content': content,
                'tags': tags,
            }
        except Exception as e:
            print(f"An error occurred while parsing Patreon post content: {e}")
            return None

    def download_file(self, file_name: str, file_url: str, folder: str) -> str or None:
        """
        Download a file from a URL and save it to the specified folder.

        :param file_name: The name of the file to download.
        :param file_url: The URL from which to download the file.
        :param folder: The folder in which to save the downloaded file.
        :return: The path to the downloaded file, or None if the download fails.
        :rtype: str or None
        """
        try:
            response = self.session.get(file_url)
            if response.status_code == 200:
                print(f"Downloading file '{file_name}' from {file_url}...")
                return create_file(file_name, folder, response.content, mode='wb')
            else:
                print(f"Failed to download file '{file_name}' from {file_url} (HTTP {response.status_code})")
                return None
        except Exception as e:
            print(f"An error occurred while downloading file '{file_name}': {e}")
            return None

    def save_post_content(self, post_content: dict, campaign_folder: str) -> str or None:
        """
        Save post content to a file.

        :param post_content: The post content to save.
        :param campaign_folder: The folder in which to save the post content.
        :return: The path to the saved folder, or None if there was an error.
        """
        post_id = post_content['post_id']
        title = post_content['title']
        date = post_content['date']
        tags = post_content['tags']
        if tags:
            tags = ', '.join(tags)

        post_folder_filename = f'{post_id} - {tags} - {title} - {date}'
        post_folder = create_folder(post_folder_filename, campaign_folder)

        try:
            print(f"Saving Patreon post content to folder '{post_folder_filename}'...")

            content = post_content['content']
            if content:
                soup = BeautifulSoup(content, 'html.parser')
                formatted_post = soup.prettify()
                create_file('post.html', post_folder, formatted_post)

            for file_data in post_content.get('files', []):
                file_name = file_data['name']
                file_url = file_data['url']
                result = self.download_file(file_name, file_url, post_folder)
                if result is None:
                    print(f"Failed to download file '{file_name}' for post {post_id}.")

            img_url = post_content['img_url']
            if img_url:
                result = self.download_file(f'{post_id} - {title}.jpg', img_url, post_folder)
                if result is None:
                    print(f"Failed to download image for post {post_id}.")

            return post_folder
        except Exception as e:
            print(f"An error occurred while saving Patreon post content: {e}")
            return None

    def parse_campaign_content(self, campaign_content: dict, creator_name: str):
        """
        Parse and save content for a Patreon campaign.

        :param creator_name: The name of the creator of the campaign.
        :param campaign_content: The content of the Patreon campaign to parse.
        """

        campaign_folder = create_folder(creator_name, self.MAIN_FOLDER_NAME)
        if not campaign_folder:
            print(f"Failed to create folder for campaign {campaign_folder}.")
            return

        try:
            print("Parsing and saving Patreon campaign content...")

            files_data = {}
            for elem in campaign_content.get('included', []):
                if elem.get('type') == 'attachment':
                    post_id = elem.get('relationships', {}).get('post', {}).get('data', {}).get('id', {})
                    if post_id:
                        files_data.setdefault(post_id, []).append(elem.get('attributes'))

            for post in campaign_content.get('data', []):
                if post.get('attributes', {}).get('current_user_can_view'):
                    post_content = self.parse_post_content(post)
                    post_id = post_content.get('post_id')
                    if post_id in files_data:
                        post_content['files'] = files_data[post_id]
                    result = self.save_post_content(post_content, campaign_folder)
                    if result is None:
                        print(f"Failed to save content for post {post_id}.")
        except Exception as e:
            print(f"An error occurred while parsing and saving Patreon campaign content: {e}")

    def get_campaign_content(self, campaign_id: str) -> dict or None:
        """
        Retrieve content for a specific campaign.

        :param campaign_id: The ID of the campaign for which to retrieve content.
        :return: Campaign content as a JSON response, or None if the request fails.
        """

        url = f'{self.base_url}/api/posts'

        params = {
            'include': 'campaign,access_rules,attachments,audio,audio_preview.null,images,media,native_video_insights,'
                       'poll.choices,poll.current_user_responses.user,poll.current_user_responses.choice,'
                       'poll.current_user_responses.poll,user,user_defined_tags,ti_checks',
            'fields[campaign]': 'currency,show_audio_post_download_links,avatar_photo_url,avatar_photo_image_urls,'
                                'earnings_visibility,is_nsfw,is_monthly,name,url',
            'fields[post]': 'change_visibility_at,comment_count,commenter_count,content,current_user_can_comment,'
                            'current_user_can_delete,current_user_can_report,current_user_can_view,'
                            'current_user_comment_disallowed_reason,current_user_has_liked,embed,image,'
                            'impression_count,insights_last_updated_at,is_paid,like_count,meta_image_url,'
                            'min_cents_pledged_to_view,post_file,post_metadata,published_at,patreon_url,post_type,'
                            'pledge_url,preview_asset_type,thumbnail,thumbnail_url,teaser_text,title,upgrade_url,url,'
                            'was_posted_by_campaign_owner,has_ti_violation,moderation_status,'
                            'post_level_suspension_removal_date,pls_one_liners_by_category,video_preview,view_count',
            'fields[post_tag]': 'tag_type,value',
            'fields[user]': 'image_url,full_name,url',
            'fields[access_rule]': 'access_rule_type,amount_cents',
            'fields[media]': 'id,image_urls,download_url,metadata,file_name',
            'fields[native_video_insights]': 'average_view_duration,average_view_pct,has_preview,id,last_updated_at,'
                                             'num_views,preview_views,video_duration',
            'filter[campaign_id]': campaign_id,
            'filter[contains_exclusive_posts]': 'true',
            'filter[is_draft]': 'false',
            'sort': '-published_at',
            'json-api-version': '1.0',
        }

        included = []
        data = []
        cursor = None
        try:
            while True:

                if cursor:
                    params['page[cursor]'] = cursor

                response = self.session.get(url, params=params)
                response.raise_for_status()

                if response.status_code == 200:
                    try:
                        response_json = response.json()
                        cursor = response_json.get('meta', {}).get('pagination', {}).get('cursors', {}).\
                            get('next', None)
                        included.extend(response_json.get('included', []))
                        data.extend(response_json.get('data', []))
                        if not cursor:
                            break
                    except json.decoder.JSONDecodeError as e:
                        print(f"Failed to decode JSON response: {e}")
                        return None
                else:
                    print(f"Failed to retrieve content for campaign {campaign_id}. "
                          f"HTTP status code: {response.status_code}")
                    return None
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch campaign content: {e}")
            return None

        print(f'{len(data)} posts have been found.')
        return {
            'included': included,
            'data': data,
        }
