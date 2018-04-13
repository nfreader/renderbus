dmm-tools-minimap 0.1.0
Tad Hardesty <tad@platymuus.com>
Build minimaps of the specified maps.

USAGE:
    dmm-tools minimap [FLAGS] [OPTIONS] [files]...

FLAGS:
    -h, --help        Prints help information
        --optipng     Run output through optipng automatically. Requires optipng.
        --pngcrush    Run output through pngcrush automatically. Requires pngcrush.
    -V, --version     Prints version information

OPTIONS:
        --disable <disable>    Disable render-passes, or "all" to only use those passed to --enable. [default: ]
        --enable <enable>      Enable render-passes, or "all" to only exclude those passed to --disable. [default: ]
        --max <max>            Set the maximum x,y or x,y,z coordinate to act upon (1-indexed, inclusive).
        --min <min>            Set the minimum x,y or x,y,z coordinate to act upon (1-indexed, inclusive).
    -o <output>                The output directory. [default: data/minimaps]

ARGS:
    <files>...    The list of maps to process.

/Users/farleyn/Code/SpacemanDMM/target/debug/dmm-tools minimap --pngcrush -o ~/Desktop _maps/map_files/BoxStation/BoxStation.dmm _maps/map_files/MetaStation/MetaStation.dmm