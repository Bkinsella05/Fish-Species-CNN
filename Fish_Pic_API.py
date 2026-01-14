import os
import time
import requests
from PIL import Image
from io import BytesIO
import urllib.parse

#for future when needing to download more images for all species to train ai

# fishListTotal = ["Shortnose Sturgeon", "Atlantic Stugeon", "Ruddy Bowfin", "American Eel", "Blueback Shad", "Hickory Shad", 
#             "American Shad", "American Gizzard Shad", "Longnose Sucker", "White Sucker", "Eastern Creek Chubsucker", 
#             "Grass Carp", "Satinfin Shiner", "Spotfin Shiner", "European Carp", "Cutlip Minnow", "Eastern Silvery Minnow", 
#             "Common Shiner", "Golden Shiner", "Bluntnose Minnow", "Creek Chub", "Fallfish", "Northern Redbelly Dace", 
#             "Lake Chub", "Banded Killifish", "Rainwater Killifish", "Redfin Pickerel", "Northern Pike", "Muskellunge", 
#             "Chain Pickerel", "Burbot", "Rainbow Smelt", "Banded Killifish", "Redbreasted Sunfish", "Green Sunfish",
#             "Pumkinseed", "Warmouth", "Bluegill", "Longear Sunfish", "Redear Sunfish", "Smallmouth Bass", "Largemouth Bass", 
#             "White Crappie", "Black Crappie", "White Perch", "Striped Bass", "Swamp Darter", "Tessellated Darter", 
#             "Yellow Perch", "Common Logperch", "Walleye", "Trout Perch", "American Brook Lamprey", "Sea Lamprey", 
#             "Rainbow Trout", "Atlantic Salmon", "Brown Trout", "Lake Trout", "Brook Trout", "Slimy Sculpin", 
#             "Fourspine Stickleback", "Threespine Stickleback", "Nine-spined Stickleback", "White Catfish", "Channel Catfish", 
#             "Yellow Bullhead", "Brown Bullhead", "Tadpole Madtom"]

#only popular fish are included
#fish name and their observation page are paired
# fish_url_list = ["Fallfish", "Chain Pickerel", 
#             "Redfin Pickerel", "Northern Pike", 
#             "Muskellunge", "Redbreasted Sunfish", 
#             "Green Sunfish", "Pumkinseed", 
#             "Warmouth", "Bluegill", 
#             "Longear Sunfish", "Redear Sunfish", 
#             "Smallmouth Bass", "Largemouth Bass", 
#             "Black Crappie", "White Perch", 
#             "Striped Bass", "Yellow Perch", 
#             "Walleye", "Rainbow Trout", 
#             "Brown Trout", "Lake Trout", 
#             "Brook Trout", "White5 Catfish", 
#             "Channel Catfish", "Yellow Bullhead", 
#             "Brown Bullhead"]
fish_url_list = ["White Perch", 
            "Striped Bass", "Yellow Perch", 
            "Walleye", "Rainbow Trout", 
            "Brown Trout", "Lake Trout", 
            "Brook Trout", "White Catfish", 
            "Channel Catfish", "Yellow Bullhead", 
            "Brown Bullhead"]

fishSpecificUrl = []


images_per_category = 300
images_per_page = 96 #needed if there are multiple pages to filter through
folder_to_store_pics = "Fish_Pics"
delay = 1.0
project_params = {"has[photos]": "true"}
api_url = "https://api.inaturalist.org/v1/observations"


def download_species_images(species_name : str):   #images for a species go into its own folder inside fish pics
    #creates path
    species_name_sin_spaces = species_name.replace(" ", "_")  #better to have no spaces for the file names
    species_dir = os.path.join(folder_to_store_pics, species_name_sin_spaces)
    #doesn't throw an error for every species after the first as the path specifies fish pics folder be "created" each time
    os.makedirs(species_dir, exist_ok=True)

    page = 1
    downloaded = 0

    #pagination loop
    while downloaded < images_per_category:
        params = {
            **project_params,
            "taxon_name": species_name,
            "per_page": images_per_page,
            "page": page,
        }
        print(f"Requesting page {page} for species '{species_name}' (downloaded so far: {downloaded})")
        resp = requests.get(api_url, params=params)
        #if response not 200, aka the ok, then break and print the error
        if resp.status_code != 200:
            print("API error:", resp.status_code, resp.text)
            break
        
        #make dictionary
        data = resp.json()
        results = data.get("results", [])

        if not results:
            print("No more results found.")
            break

        for obs in results:
            #very likely most results lists will have more resutls than images needed
            if downloaded >= images_per_category:
                break
            #get first photo url from observation
            photos = obs.get("photos", [])
            if not photos:
                continue

            #gets the first image on an observaion as most observations have multipe pics of the same fish, want less redundancy
            base_url = photos[0].get("url")
            if not base_url:
                continue

            #see if original(preffered) or large(next preffered) images are available in the chance iNat defaults to a medium, small, thumb, or square image
            original_url = base_url.replace("square", "original").replace("medium", "original")
            large_url = base_url.replace("square", "large").replace("medium", "large")

            img_resp = None  # Start with nothing

            #tries for original and large. i don't know if it throws and exception if it fails or if it defaults to medium
            #i am just doing both since the one that doesn't matter will just get skipped(if exception ifs get skipped, if no exception the try's get skipped)
            try:
                #try original
                try: 
                    img_resp = requests.get(original_url, timeout=10)
                    if img_resp.status_code == 200 and "original" in img_resp.url:
                        print("Got original.")
                    else:
                        #try large if original failed or fell back
                        print("No original. Trying large.")
                        img_resp = requests.get(large_url, timeout=10)
                        if img_resp.status_code == 200 and "large" in img_resp.url:
                            print("Got large.")
                        else:
                            #if the large and original don't exist :(
                            print("Large is a no go, downloading basic :(")
                            img_resp = requests.get(base_url, timeout=10)
                
                except Exception as e:
                    try:  #large is tried if iNat works through throwing exceptions
                        print("Original not available. Trying large.")
                        img_resp = requests.get(large_url, timeout=10)
                        print("Got large.")
                    except Exception as e2:  #womp womp neither worked :(
                        print("Large is a no go, downloading basic :(")
                        img_resp = requests.get(base_url, timeout=10)


                img_resp.raise_for_status()  #raises exception if final request still failed


                #open and save image
                img = Image.open(BytesIO(img_resp.content)).convert("RGB")
                fname = f"{species_name}_{downloaded}.jpg"
                out_path = os.path.join(species_dir, fname)
                img.save(out_path, format="JPEG")
                downloaded += 1

            except Exception as e:
                print(f"Failed to download or save image for {species_name}: {e}")
                continue
        page += 1
        time.sleep(delay)

    print(f"Finished species '{species_name}', downloaded {downloaded} images.")


def main():
    os.makedirs(folder_to_store_pics, exist_ok=True)

    for item in fish_url_list:
        download_species_images(item)
        #small delay between species to avoid stressing API
        time.sleep(2)


if __name__ == "__main__":
    main()