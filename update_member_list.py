
# https://github.com/EloiStree/2017_07_13_Wiki_PatreonUnityAPI/wiki

# https://www.patreon.com/oauth2/authorize?response_type=code&client_id=|YouAppClientID|
# <?php   echo "<h1>Patreon Redirection</h1>"; echo "<h2>User Authorization Code:</h2><p>". $_GET["code"] ."</p>"; echo "<h2>Scope:</h2><p>". $_GET["scope"] ."</p>"; echo "<h2>Error:</h2><p>". $_GET["error"] ."</p>"; ?>
import patreon
import os
import inspect

# Define the access token file path
access_token_path = "/token/patreon_bot_access_token"
ACCESS_TOKEN = ""
default_value_file = "https://www.patreon.com/portal/registration/register-clients"

client_id_path= "/token/patreon_bot_client_id"
CLIENT_ID = ""
default_value_file = "https://www.patreon.com/portal/registration/register-clients"

client_secret_path= "/token/patreon_bot_client_secret"
CLIENT_SECRET=""
default_value_file = "https://www.patreon.com/portal/registration/register-clients"

def create_and_read( file_path, default_value_file,label):
    # Create the file if it does not exist
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            f.write(default_value_file)
    with open(file_path, "r") as f:
        value = f.read().strip()      
    print(f"{label}: {value[:3]}...")
    return value

ACCESS_TOKEN =create_and_read(access_token_path, default_value_file,"ACCESS_TOKEN")
CLIENT_ID =create_and_read(client_id_path, default_value_file,"CLIENT_ID")
CLIENT_SECRET= create_and_read(client_secret_path, default_value_file,"CLIENT_SECRET")



# # Initialize the Patreon API client
# api_client = patreon.API(ACCESS_TOKEN)

# # Fetch the campaign details
# try:
#     campaign_response = api_client.fetch_campaign()
#     campaign_data = campaign_response.data()  # Extract the data
#     print(f"Campaign Count: {len(campaign_data)}")
#     # JSONAPIResource object - extracting campaign ID
#     campaign_id = campaign_data[0].id()  # Access the first campaign's ID
#     # print(f"Campaign ID: {campaign_id}")
# except Exception as e:
#     print(f"Failed to fetch campaign details: {e}")
#     exit(1)
    



# if True:
    
#     # Fetch the list of members for the campaign
#     try:
#         members_response = api_client.fetch_campaign_and_patrons(campaign_id)
#         members_data = members_response.data()  # Extract the data
        
#         # Iterate through the members and print their details
#         for member in members_data:
#             member_id = member.id()
#             member_attributes = member.attributes()
#             print(f"Member ID: {member_id}")
#             for attr, value in member_attributes.items():
                
#                 if attr == "summary":
#                     continue
#                 print(f"  {attr}: {value}")
                
#     except Exception as e:
#         print(f"Failed to fetch members: {e}")
#         exit(1)
    
    
# if False:
    
#     # Fetch the list of pledges for the campaign
#     try:
#         pledges_response = api_client.fetch_page_of_pledges(campaign_id, 25)
#         pledges_data = pledges_response.data()  # Extract the data
        
#         # Iterate through the pledges and print their details
        
        
        
#         for pledge in pledges_data:
#             pledge_id = pledge.id()
#             pledge_attributes = pledge.attributes()
#             # list of attributes
#             print(f"Pledge ID: {pledge_id}")
#             for attr, value in pledge_attributes.items():
#                 print(f"  {attr}: {value}")
#     except Exception as e:
#         print(f"Failed to fetch pledges: {e}")
#         exit(1)
    


# # using relfection list api_client methods
# # List all methods of the api_client using reflection
# methods = inspect.getmembers(api_client, predicate=inspect.ismethod)
# print("Available methods in api_client:")
# for name, method in methods:
#     print(f"  {name}")
















import requests
import json

# Patreon API URL (to fetch campaign data)
campaign_url = 'https://www.patreon.com/api/oauth2/v2/campaigns'
patron_url_template = 'https://www.patreon.com/api/oauth2/v2/campaigns/{campaign_id}/members'

# Make the request to Patreon API for campaign details
print (ACCESS_TOKEN)
headers = {
    'Authorization': f'Bearer {ACCESS_TOKEN}',  # Ensure ACCESS_TOKEN is defined
}

# Fetch campaign data
response = requests.get(campaign_url, headers=headers)

# Check if the response is successful
if response.status_code == 200:
    data = response.json()  # Parse the JSON response
    
    # Extract campaign data (assuming a single campaign)
    campaign = data.get('data', [])[0]  # Use the first campaign if there are multiple
    campaign_id = campaign.get('id', None)
    
    if campaign_id:
        # Prepare the URL for fetching patrons (followers)
        patron_url = patron_url_template.format(campaign_id=campaign_id)
        print(f"Campaign ID: {campaign_id}")
        print(f"Initial Patron URL: {patron_url}")

else:
    print(f"Failed to fetch campaign data: {response.status_code}")




# Fetch pledges data using the provided URL

pledges_url = f'https://www.patreon.com/api/oauth2/v2/campaigns/{campaign_id}/members?include=address&fields[member]=full_name,is_follower,last_charge_date,last_charge_status,lifetime_support_cents,currently_entitled_amount_cents,patron_status&fields[tier]=amount_cents,created_at,description,discord_role_ids,edited_at,patron_count,published,published_at,requires_shipping,title,url&fields[address]=addressee,city,line_1,line_2,phone_number,postal_code,state'
pledges_url = f'https://www.patreon.com/api/oauth2/v2/campaigns/{campaign_id}/members?include=user&fields[user]=full_name,email,url,social_connections&fields[member]=full_name,is_follower,last_charge_date,last_charge_status,lifetime_support_cents,currently_entitled_amount_cents,patron_status&fields[tier]=amount_cents,created_at,description,discord_role_ids,edited_at,patron_count,published,published_at,title,url'
pledges_url = f'https://www.patreon.com/api/oauth2/v2/campaigns/{campaign_id}/members?include=user&fields[user]=full_name,email,url,social_connections&fields[member]=full_name,is_follower,last_charge_date,last_charge_status,lifetime_support_cents,currently_entitled_amount_cents,patron_status'

int_anti_loop = 100
member_pretty_json =""
while True:
    # Fetch pledges data
    response = requests.get(pledges_url, headers=headers)
    
    # Check if the response is successful
    if response.status_code == 200:
        data = response.json()  # Parse the JSON response
        member_pretty_json += json.dumps(data, indent=2)
        
        
        for data_item in data.get('data', []):
            full_name = data_item.get('attributes', {}).get('full_name')
            lifetime_support_cents = data_item.get('attributes', {}).get('lifetime_support_cents')
            patreon_id= data_item.get('relationships', {}).get('user', {}).get('data', {}).get('id')
            is_follower = data_item.get('attributes', {}).get('is_follower')
            last_charge_date = data_item.get('attributes', {}).get('last_charge_date')
            last_charge_status = data_item.get('attributes', {}).get('last_charge_status')
            
            if full_name == "Eloi Stree":
                print(json.dumps(data_item, indent=2))
            
            print(f"Full Name: {full_name}")
        for data_item in data.get('included', []):
            full_name = data_item.get('attributes', {}).get('full_name')
            if full_name == "Eloi Stree":
                print(json.dumps(data_item, indent=2))
            patreon_id = data_item.get('id')
            discord_id = None
            social_connections = data_item.get('attributes', {}).get('social_connections')
            if social_connections is not None:
                discord_json = social_connections.get('discord', {})
                if discord_json is not None:
                    discord_id = discord_json.get('user_id')
                    if discord_id is not None and len(discord_id) > 0:
                        print(f"Discord ID: {discord_id} - {patreon_id} ({full_name})")
                
            if social_connections is not None:
                twitter_json = social_connections.get('twitter', {})
                if twitter_json is not None:
                    twitter_id = twitter_json.get('user_id')
                    if twitter_id is not None and len(twitter_id) > 0:
                        print(f"Twitter ID: {twitter_id} - {patreon_id} ({full_name})")
                
        
            
            print(f"Full Name: {full_name} {discord_id} ")
            # if discord_id is not None and len(discord_id) > 0:
            #     print(f"Discord ID: {discord_id} - {patreon_id} ({full_name})")

            
            # if twitter_id is not None and len(twitter_id) > 0:
            #     print(f"Twitter ID: {twitter_id} - {patreon_id} ({full_name})")
            
        
        # Check if there is a next page
        next_page = data.get('links', {}).get('next')
        if next_page:
            pledges_url = next_page  # Update the URL to the next page
        else:
            break  # Exit the loop if there are no more pages
    else:
        print(f"Failed to fetch pledges data: {response.status_code}")
        break
    int_anti_loop -= 1
    if int_anti_loop < 0:
        break
    
# print(member_pretty_json)



"""

"social_connections": {
          "discord": null,
          "facebook": {
            "url": "https://www.facebook.com/517905308394675",
            "user_id": "10212695123482660"
          },
          "google": null,
          "instagram": {
            "url": "https://www.instagram.com/eloistree",
            "user_id": "8573372166105338"
          },
          "reddit": null,
          "spotify": null,
          "spotify_open_access": null,
          "tiktok": {
            "url": "https://tiktok.com/%40eloi_stree",
            "user_id": "-000t3zeABs4xyTLLWjz3vrG-zeVfY8kflHj"
          },
          "twitch": {
            "url": "https://twitch.tv/apintio",
            "user_id": "1214540965"
          },
          "twitter": {
            "url": "https://twitter.com/StreeEloi64685",
            "user_id": "1788197404958748674"
          },
          "twitter2": null,
          "vimeo": null,
          "youtube": {
            "url": "https://youtube.com/channel/UCss-to1CvzoUIoBNijuiLnA",
            "user_id": "UCss-to1CvzoUIoBNijuiLnA"
          }
        },
"""




# #GET /api/oauth2/v2/posts/118328856
# # Define the URL for fetching a specific post
# post_id = '118328856'
# post_url = f'https://www.patreon.com/api/oauth2/v2/posts/{post_id}'

# # Make the request to fetch the post details
# response = requests.get(post_url, headers=headers)

# # Check if the response is successful
# if response.status_code == 200:
#     post_data = response.json()  # Parse the JSON response
#     post_pretty_json = json.dumps(post_data, indent=2)
#     print(f"Post ID: {post_id}")
#     print(f"____________________________")
#     print(post_pretty_json)
# else:
#     print(f"Failed to fetch post data: {response.status_code}")