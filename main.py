import os

from dotenv import load_dotenv

from patreon.patreon_manager import PatreonManager

load_dotenv()


def main():
    email = os.getenv('EMAIL')
    password = os.getenv('PASSWORD')

    patreon_manager = PatreonManager(email, password)
    if patreon_manager.login():
        print("Login successful")

        campaign_data = patreon_manager.get_campaigns_data()
        if campaign_data:
            print(f"Found {len(campaign_data)} campaigns.")

            patreon_manager.get_all_campaigns_content(campaign_data)

        else:
            print("No campaigns found for the user.")


if __name__ == '__main__':
    main()
