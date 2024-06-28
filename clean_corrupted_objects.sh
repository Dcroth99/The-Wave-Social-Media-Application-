#!/bin/bash

# Array of missing blobs
declare -a missing_blobs=(
    "25a8805aa025a301edc5b224614e2d1b77658952"
    "8230007141a7e0d6d361b097f47b8e281c91c878"
    "f160833805efc17a32ff58938927c0f067f6e662"
    "f2880fb0043b8dabc9f83fe5fe73223e4499eccb"
    "32e5ac7de893370dfbbffa11a373a9c3b3662d12"
    "90d5e73f8a88fe13161b2c2b763e83411ee06b02"
    "02f283abada802aa2dc4fab5181c166ab711b75a"
    "1d52c260f2987b63385bf9aa4e04eb7a410a0202"
    "208a00570578b507081cb1e77ff8bb75e3f13b22"
    "c2e61e5800bbd8c07d848c0d5ec8deb4b4fe03fd"
    "d2f680f276c1cac5c9d838d997e734a209301c84"
    "21cb246beb25e3b6040ff682f00a564c91f19ca2"
    "561f11f8e44e75c948715472e57f2bd49ca28c22"
    "73b730a705ad39f9a44edf4f9bc1590b8d1e0502"
    "82dbbb7a212113654ec2da3da4b7b1dad3a7e160"
    "ca2354bcdde6170ca8415dfcd3e1771893328382"
    "e1ffdbed0d8ca663cfcab21818bb3f9c6938c7a2"
)

# Array of missing trees
declare -a missing_trees=(
    "ad70dffb170cb556ce7fbda2911ab507643bdf62"
    "57a1cbed9e148b633196f963d087d8b612af8192"
    "92a1266d2f80b17bf85d30b9e7bbaf703870b868"
    "0c63ea7d4416258b30aa6c2c31c683ea92bdb2e2"
    "a883a7682e88f622f1956ebda8cda89cac142692"
)

# Function to remove missing blobs
remove_blobs() {
    for blob in "${missing_blobs[@]}"; do
        path=".git/objects/${blob:0:2}/${blob:2}"
        if [ -f "$path" ]; then
            echo "Removing $path"
            rm -f "$path"
        else
            echo "Blob $path not found"
        fi
    done
}

# Function to remove missing trees
remove_trees() {
    for tree in "${missing_trees[@]}"; do
        path=".git/objects/${tree:0:2}/${tree:2}"
        if [ -d "$path" ]; then
            echo "Removing tree directory $path"
            rm -rf "$path"
        else
            echo "Tree $path not found"
        fi
    done
}

# Function to remove dangling objects
remove_dangling() {
    declare -a dangling_objects=(
        "da2cc61d42dc16defe16e8cfcba29f0c454fcff3"
        "286d140dad107a744bbe88edc7029010063b76e5"
        "4e2d9f4a0b5bcda5a9f41dd77f9a4465b0865d71"
        "2b9639f39889c088395f9612e8e73051581a0da7"
        "a5336fe8590a7eb62bc4a1d07a6d059603803374"
        "a6c3bc1d87eba96b1e945d8c3a2cf3f27cb54c5f"
        "f67ad9df37008043a00d8b7ce8e1f1e3f455ed6b"
    )
    for obj in "${dangling_objects[@]}"; do
        path=".git/objects/${obj:0:2}/${obj:2}"
        if [ -f "$path" ]; then
            echo "Removing dangling object $path"
            rm -f "$path"
        elif [ -d "$path" ]; then
            echo "Removing dangling tree $path"
            rm -rf "$path"
        else
            echo "Dangling object $path not found"
        fi
    done
}

# Main function
main() {
    remove_blobs
    remove_trees
    remove_dangling

    # Repack the repository to clean up
    git repack -a -d --depth=250 --window=250

    # Verify the repository integrity
    git fsck --full
}

# Execute the main function
main

