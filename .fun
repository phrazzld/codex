#!/bin/bash

FAVORITE_LIGHT_THEMES=(
    "Alabaster"
    "Atelierdune.light"
    "Atelierforest.light"
    "Atelierheath.light"
    "Atelierlakeside.light"
    "Atelierseaside.light"
    "paper-theme"
    "github_light_default"
    "Yousai" #
    "X-dotshare"
    "Visibone-alt-2"
    "Twilight.light"
    "Tomorrow.light"
    "Tokyonight_Day"
    "Terminal-app-Basic"
    "Solarized-Light"
    "Seabird"
    "Railscasts.light"
    "Pencil-Light"
    "One-Light"
    "Ocean.light"
    "Nova"
    "Marrakesh.light"
    "Iceberg-Light"
    "Gruvbox-Light"
    "Grayscale.light"
    "Gutterslob - aikofog"
    "Google.light" #
    "Codeschool.light"
)

FAVORITE_DARK_THEMES=(
    "Wombat"
    "Afterglow"
    "Argonaut"
    "Ashes.dark"
    "Astromouse"
    "Atelierlakeside.dark"
    "Ayu-Dark"
    "Ayu-Mirage"
    "Base16-Default-Dark"
    "Baskerville - Count Von Count"
    "github_dimmed"
    "github_dark"
    "Ubuntu"
    "Twilight.dark"
    "Trim-yer-beard"
    "Tomorrow.dark"
    "Tomorrow-Night"
    "Tokyonight_Storm"
    "Tokyonight_Night"
    "Tlh"
    "Thwump"
    "Tender"
    "Taerminal"
    "Sweetlove"
    "Substrata"
    "Sourcerer"
    "Solarized-Dark"
    "Snazzy"
    "Simple_rainbow"
    "Sexcolors"
    "Seoul256"
    "S3r0-modified"
    "Rydgel"
    "Rooster - SOS"
    "Rezza"
    "Railscasts.dark"
    "Pulp"
    "Pop!-OS"
    "Pencil-Dark"
    "Paraiso.dark"
    "Panda"
    "Palenight"
    "Oxide"
    "One-Dark"
    "Oceanic-Next"
    "Ocean.dark"
    "OK100 - Matrix"
    "NumixDarkest"
    "Nucolors"
    "Nova"
    "Nord"
    "Nightfly"
    "New-Moon"
    "Muzieca lowcontrast"
    "Moonlight-II-VSCode"
    "Monotheme"
    "Monokai.dark"
    "Monokai-Pro"
    "Molokai"
    "Mocha.dark"
    "Mikado"
    "Material"
    "Material-Theme"
    "Marrakesh.dark"
    "Kanagawa"
    "Gruvbox-Dark"
    "Greenscreen.dark"
    "Grayscale.dark"
    "Garuda.dr460nized" #
    "Eighties.dark"
    "Dracula"
    "Dotshare"
    "Dkeg - unsiftedwheat"
    "Dawn"
    "Catppuccin"
)

# Functions
pullpasses() {
    if [ -n "$1" ]; then
        lpass show $(lpass ls | grep -i "$1" | awk '{ print $3 }' | sed 's/.$//')
    else
        echo "Error: missing search term"
    fi
}

pullpass() {
    if [ -n "$1" ]; then
        pullpasses "$1" | grep -i "Password:" | awk '{ print $2 }' | head -1 | pbcopy
    else
        echo "Error: missing search term"
    fi
}

timezsh() {
  shell=${1-$SHELL}
  for i in $(seq 1 10); do /usr/bin/time $shell -i -c exit; done
}

# Encrypt directories
# first arg: tarfile name
# second arg: directory to encrypt
lock() {
    TARFILE=$1
    TARGET_DIR=$2
    tar czf $TARFILE $TARGET_DIR
    gpg -c $TARFILE
    echo "Remember: remove $TARFILE and $TARGET_DIR"
}

# Decrypt archives
# first arg: tarfile name
# second arg: gpg file name
unlock() {
    TARFILE=$1
    GPGFILE=$2
    gpg --output $TARFILE $GPGFILE
    tar xzf $TARFILE
}

golight() {
    ORIGINAL_NODE_VERSION=$(asdf current nodejs | awk '{ print $2 }')

    asdf local nodejs 17.9.1

    RANDOM_THEME=${FAVORITE_LIGHT_THEMES[$RANDOM % ${#FAVORITE_LIGHT_THEMES[@]}]}

    echo "changing theme to: $RANDOM_THEME"

    alacritty-themes $RANDOM_THEME

    # If original node version doesn't exist, use latest
    if [ -z "$ORIGINAL_NODE_VERSION" ]; then
        asdf local nodejs $(asdf latest nodejs)
    else
        asdf local nodejs $ORIGINAL_NODE_VERSION
    fi
}

godark() {
    ORIGINAL_NODE_VERSION=$(asdf current nodejs | awk '{ print $2 }')

    asdf local nodejs 17.9.1

    RANDOM_THEME=${FAVORITE_DARK_THEMES[$RANDOM % ${#FAVORITE_DARK_THEMES[@]}]}

    echo "changing theme to: $RANDOM_THEME"

    alacritty-themes $RANDOM_THEME

    # If original node version doesn't exist, use latest
    if [ -z "$ORIGINAL_NODE_VERSION" ]; then
        asdf local nodejs $(asdf latest nodejs)
    else
        asdf local nodejs $ORIGINAL_NODE_VERSION
    fi
}

# function random_quote() {
#     jq -c '.quotes[]' $DEVELOPMENT/dotfiles/quotes.json | shuf -n 1 | jq -r '"\(.content)\n-- \(.source)"'
# }
function random_quote() {
    # Path to the JSON file with quotes
    local json_file="$DEVELOPMENT/dotfiles/quotes.json"

    # Check if the file exists and is readable
    if [[ ! -r $json_file ]]; then
        echo "Unable to read the quotes file: $json_file" >&2
        return 1
    fi

    # Use jq to extract the quotes and randomly select one
    local selected_quote
    selected_quote=$(jq -c '.quotes[]' "$json_file" | shuf -n 1) || {
        echo "Failed to select a quote from the file: $json_file" >&2
        return 1
    }

    # Use jq again to format the selected quote and fold to wrap the text
    local content source
    content=$(echo "$selected_quote" | jq -r .content | fold -s -w 80)
    source=$(echo "$selected_quote" | jq -r .source)

    # Print the formatted quote
    echo -e "$content\n-- $source"
}

function vrg() {
    $NEOVIM $(rg -il "$1")
}
