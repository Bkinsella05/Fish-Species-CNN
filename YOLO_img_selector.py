#Images to train Yolo
from pathlib import Path
import random as r
import shutil

#Variables to use main
images_per_species = 5
all_fish_folder_path = Path("/Users/bobby/Documents/AI FISH PROJECT/Fish_Pics")

#for training data
fish_pics_to_train_YOLO = Path("/Users/bobby/Documents/AI FISH PROJECT/Fish_Pics/YOLO_Data/YOLO_Images/YOLO_Train_Data")

#for validating data
fish_pics_to_val_YOLO = Path("/Users/bobby/Documents/AI FISH PROJECT/Fish_Pics/YOLO_Data/YOLO_Images/YOLO_Val_Data")

#for testing data
fish_pics_to_test_YOLO = Path("/Users/bobby/Documents/AI FISH PROJECT/Fish_Pics/YOLO_Data/YOLO_Images/YOLO_Test_Data")

#for later when labeling
fish_labels_to_train_YOLO = Path("/Users/bobby/Documents/AI FISH PROJECT/Fish_Pics/YOLO_Data/YOLO_Labels/YOLO_Train_Data")
fish_labels_to_val_YOLO = Path("/Users/bobby/Documents/AI FISH PROJECT/Fish_Pics/YOLO_Data/YOLO_Labels/YOLO_Val_Data")
fish_labels_to_test_YOLO = Path("/Users/bobby/Documents/AI FISH PROJECT/Fish_Pics/YOLO_Data/YOLO_Labels/YOLO_Test_Data")






def main():
    #Make directory
    fish_pics_to_train_YOLO.mkdir(parents=True, exist_ok=True)
    fish_pics_to_val_YOLO.mkdir(parents=True, exist_ok=True)
    fish_pics_to_test_YOLO.mkdir(parents=True, exist_ok=True)
    #For labels later
    fish_labels_to_train_YOLO.mkdir(parents=True, exist_ok=True)
    fish_labels_to_val_YOLO.mkdir(parents=True, exist_ok=True)
    fish_labels_to_test_YOLO.mkdir(parents=True, exist_ok=True)

    for species_folder in all_fish_folder_path.iterdir():
        if species_folder.is_dir():
            if str(species_folder) == "/Users/bobby/Documents/AI FISH PROJECT/Fish_Pics/YOLO_Data":
                continue
            print(species_folder)
            species_folder = str(species_folder)
            last_slsh_index = species_folder.rfind('/')
            #print(len(species_folder))
            species_name = species_folder[last_slsh_index:].replace('_', ' ') + "_"
            rand = r.randint(1, 8)
            #gathers 5 images per species
            for i in range(1, 27):
                img_index = i * rand
                image_path = Path(species_folder + "/" + species_name + str(img_index) + ".jpg")
                #print(image_path)
                new_img_path = fish_pics_to_train_YOLO / image_path.name
                if (i > 23):
                    new_img_path = fish_pics_to_val_YOLO / image_path.name
                if (i > 25):
                    new_img_path = fish_pics_to_test_YOLO / image_path.name

                print(new_img_path)
                final_path = shutil.copy2(image_path, new_img_path)
                #print(final_path)
            
            #for testing data
            # im_index = 9 * rand
            # image_path = Path(species_folder + "/" + species_name + str(img_index) + ".jpg")
            # #print(image_path)
            # new_img_path = fish_pics_to_test_YOLO / image_path.name
            # print(new_img_path)
            # final_path = shutil.copy2(image_path, new_img_path)


if __name__ == "__main__":
    main()

    #/Users/bobby/Documents/AI FISH PROJECT/Fish_Pics/Black_Crappie/Black Crappie_270.jpg